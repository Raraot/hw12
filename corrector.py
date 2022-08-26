
def corrector_birthday(birthday):
    datalist = birthday.split("-")
    try:
        if not ((1<int(datalist[0])<31) and (1<int(datalist[1])<12) and (1890<int(datalist[2])<2022)):
            print(" *** Date of birth entered incorrectly *** \nplease enter in the format dd-mm-yyyy dd - day, mm - month, yyyy - year")
        elif not ((len(datalist[0])==2) and (len(datalist[1])==2) and (len(datalist[2])==4)) :
            print(" *** Date of birth entered incorrectly *** \nplease enter in the format dd-mm-yyyy dd - day (two digits), mm - month(two digits), yyyy - year(four digits")
        else:
            return birthday
    except:
        print(" *** Date of birth entered incorrectly *** \nplease enter in the format dd-mm-yyyy dd - day, mm - month, yyyy - year")
    

def corrector_phone(phone):
    valid_characters = ["-", "+", "(", ")", "#", "№", " ", ".", ","]
    new_phone = ""
    for i in phone:
        if i in valid_characters:
            continue
        else:
            new_phone += i
    try:
        return int(new_phone)
    except:
        print("In phone must not contain letters")




