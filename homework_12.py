import functools
from collections import UserDict
from datetime import datetime
from corrector import *
import csv

DICT = {}
# ДЕКОРАТОРИ із ДЗ-9
def welcome(func):                                                        # декоратор оформлення привітання
    def inner(*args, **kwargs):
        print("-"*36+"\n* Welcome to Assistant Console Bot *\n"+"-"*36)
        return func(*args, **kwargs)
    return inner


def input_error(func):                                                    # декоратор обробки помилок
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print("""*** You have not entered all data!!! ***
--------------------------------------------------------------------------------------------------
for adding new phone number please input:   add name tel.      (example: add Volodymyr 345-45-45)
for change please input:                    change name tel.   (example: change Volodymyr 2345789)
for reading please input:                   phone name         (example: phone Volodymyr)
--------------------------------------------------------------------------------------------------""")
        except KeyError:
            print("*** This user was not found in the phone book! ***")
        except ValueError:
            print("*** Invalid value. Try again. ***")
    return wrapper

# КЛАСИ ДЗ-10
class FieldHandler:

    @ input_error
    def handler(self, userinput):                                                        # функція обробки команд
        if userinput.lower() == "hello":
            return "How can I help you?"
        elif userinput.lstrip()[0:3].lower() == "add":
            name = userinput.split(" ")[1]
            phone = userinput.split(" ")[2]
            adressbook.add_data(name, phone)
        elif "birthday" in userinput.lower():
            name = userinput.split(" ")[1]
            birthday = userinput.split(" ")[2]
            adressbook.add_birthday(name, birthday)
        elif userinput.lstrip()[0:4].lower() == "left":
            name = userinput.split(" ")[1]
            adressbook.days_to_birthday(name)  
        elif "change" in userinput.lower():
            name = userinput.split(" ")[1]
            phone = userinput.split(" ")[2]
            adressbook.change_data(name, phone)
        elif "phone" in userinput.lower():
            return adressbook.data[userinput.split(" ")[1]]["phones"]
        elif "show all" in userinput.lower():
            return adressbook.show_all()
        elif userinput.lstrip()[0:6].lower() == "search":
            ask_me = userinput.split(" ")[1]
            adressbook.search(ask_me)
        else:
            return "*** Unknown command, please input correct data or command! ***"


class AddressBook(UserDict, FieldHandler):
    def __init__(self):
        self.filename = "all_adressbook.csv"
        self.data = {}

    def open_csv(self):
        with open(self.filename, 'r') as fh:
            reader = csv.DictReader(fh, delimiter=',')
            for row in reader:
                self.data[row['name']]={'phones': row['phones'], 'birthday': row['birthday']}

    def save_in_csv(self):
        with open(self.filename, 'w') as fh:
            header_names = ['name', 'phones', 'birthday']
            writer = csv.DictWriter(fh, fieldnames = header_names, delimiter=',')
            writer.writeheader()
            for k, v in self.data.items():
                writer.writerow({'name': k,'phones': v['phones'],'birthday': v['birthday']})   

    def search(self, ask_me):
        result = ""
        if len(ask_me) < 3:
            result = "*** The request must consist of 3 or more characters ***"
        for key, value in self.data.items():
            if (ask_me in key) or (ask_me in value['phones']):
                result += (f'Found: {key} :\t\t{value}\n')
            for i in value['phones']:
                if ask_me in i:
                    result += (f'Found: {key} :\t\t{value}\n')
        if result:
            print(result)
        else:
            print("*** Nothing found ***")


    def show_all(self):
        if self.data == {}:
            return "*** Your phone book is empty ***"
        start = 0
        end = 10
        count = 0
        dic_list = []
        for k, v in self.data.items():
            dic_list.append(str(k)+" :    "+str(v))
        for i in dic_list:
            result = "\n".join(dic_list[start:end])
            count += 1
            print(f'\nPage {count} phone book:\n\n{result}')
            start = end
            end = end + 10
            if start < len(dic_list):
                print('\nFor the next page phone book - type "next"\nFor the exit from phone book - type "exit"')
            else:
                break
            inp = input("::")
            if inp == "exit" or start >= len(dic_list):
                break

    def change_data(self, name, phone):
        phoneclass = Phone(phone)
        if name not in self.data:
            print(f"*** {name} <<< contact is missing in your phone book ***")
        else:
            self.data[name]["phones"][0] = phoneclass.phone

    def add_data(self ,name , phone = "", birthday = None ):
        phoneclass = Phone(phone)
        if name not in self.data:
            client_cart = {"phones": [phoneclass.phone], "birthday": birthday}
            self.data[name] = client_cart
        else:
            self.data[name]["phones"].append(phoneclass.phone)
        adressbook.save_in_csv()

    def add_birthday(self, name, birthday):
        if name not in self.data:
            print(f"CLI comment:\n {name}  contact is missing in your phone book")
        else:
            corect_date = corrector_birthday(birthday)
            self.data[name]["birthday"] = corect_date
        adressbook.save_in_csv()

    def days_to_birthday(self, name):
        if name not in self.data:
            print(f"CLI comment:\n{name} - contact is missing in your phone book")
        elif self.data[name]["birthday"] == None:
            print(f"CLI comment:\nPlease enter the date of birth for contact: {name}")
        else:
            b_day = datetime.strptime(self.data[name]["birthday"], '%d-%m-%Y')
            current_datetime = datetime.now()
            birthday_in_this_year = dr_in_this_year = datetime(year=current_datetime.year, month=b_day.month, day=b_day.day)
            delta = birthday_in_this_year - current_datetime
            left = delta.days
            if left <= 0:
                left = 365 + left
            print(f"{left} days left until the birthday of the contact: {name}")

class Name(FieldHandler):
    def __init__(self, name):
        self.name = name


class Phone(FieldHandler):
    def __init__(self, phone = ""):
        self.__phone = phone

    @property
    def phone(self):
        return corrector_phone(self.__phone)

    @phone.setter
    def phone(self, phone):
        if type(phone) == str:
            self.__phone = corrector_phone(phone)


class Record(FieldHandler):
    def __init__(self ,name = "" , phone_list = [], birthday = ""):
        self.name = name
        self.phone_list = phone_list
        self.birthday = birthday

@ welcome
def main():
    while True:
        userinput = input(": ")
        if userinput.strip().lower() in [".", "good bye", "close", "exit", "stop", "palyanytsya"]:
            adressbook.save_in_csv()
            print("-"*36+"\n  Good bye!\n"+"-"*36)
            break
        else:
            print_me = fieldhandler.handler(userinput)
            if print_me != None:                                                # необхідне прінтування 
                print(print_me)
            continue

if __name__ == '__main__':
    adressbook = AddressBook()
    adressbook.open_csv()
    record = Record()
    fieldhandler = FieldHandler()
    main()



