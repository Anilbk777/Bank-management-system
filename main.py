import json 
import random
import string
from pathlib import Path
import re #regular expression module for calidating email

class Bank: 
    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as f:
                # data = json.loads(f.read())
                data = json.load(f)
        else:
            print("No such file exist!")

    except Exception as err:
        print(f"An exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as f:
            # f.write(json.dumps(Bank.data))
            json.dump(cls.data, f, indent=4)
            
    @classmethod
    def __account_generator(cls):
        return  random.randint(1000000000, 9999999999)



    def create_acc(self):
        info = {
            "Name" : input("Enter your name:-"),
            "Age" :int(input("Enter your age:-")),
            "Email": input("Enter your email:-"),
            "Pin" :int(input("Enter your 4 digits Pin:-")),
            "Account_no" :Bank.__account_generator(),
            "Balance": 0
        }
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        errors = []

        if not info.get('Name').isalpha():
            errors.append("Name must be alphabetical.") 


        if info.get('Age') <18 and info.get('Age') >100 :   
            errors.append("Age must be 18 or above.")

        if len(str(info.get('Pin')))!=4 : #we can't use directly len function on integers
            errors.append("Pin must be 4 digits.")

        if not re.match(pattern, info.get('Email', ' ')):
            errors.append("Email format is invalid.")

        if errors:
            print("Sorry account cannot be created!\n")
            for err in errors:
                
                print(f"{err}")

        else:
            for i in info:
                print(f"{i} = {info[i]}")

            Bank.data.append(info)
            Bank.__update() 
            print("Account has been created successfully!")


    def deposit_money(self):
        accno = int(input("Please enter your account number:-"))
        pinno = int(input("Please enter your pin :-"))

        # print(Bank.data)
        found  = False
        for item in Bank.data:
            if item['Account_no'] == accno and item['Pin'] ==pinno:
                    print(f"Your current balance is {item['Balance']}")
                    blc = int(input("How much money you want to deposit:- "))

                    if blc >25000 or blc <100:
                        print("Amount must be below 25000 and above 0.")

                    else:
                        item['Balance'] = item['Balance'] + blc
                        print(f"Total balance = {item['Balance']}")
                        print("Balance updated successfully.")
                        found = True
                        Bank.__update()
                    
        if not found:
            print("Account not found!")

    def withdraw_money(self):
        accno = int(input("Please enter your account number:-"))
        pinno = int(input("Please enter your pin :-"))

        # print(Bank.data)
        found  = False
        for item in Bank.data:
            if item['Account_no'] == accno and item['Pin'] ==pinno:
                    print(f"Your current balance is {item['Balance']}")
                    blc = int(input("How much money you want to withdraw:- "))

                    if blc >item['Balance'] :
                        print("Insufficient amount")
                        found = True

                    elif blc > 25000 or blc < 100:
                        print("Failed to withdraw money!")
                        print("You can withdraw lesser or equal to 25000 and above 100")
                        found = True
                    else:
                        item['Balance'] = item['Balance'] - blc
                        print(f"Total remaining balance = {item['Balance']}")
                        print("Balance withdrew successfully.")
                        found = True
                        Bank.__update()
                    
        if not found:
            print("Account not found!")

    def show_details(self):
        # print(Bank.data)
        accno = int(input("Please enter your account number:-"))
        pinno = int(input("Please enter your pin :-"))

       
        found  = False
        for item in Bank.data:
            if item['Account_no'] == accno and item['Pin'] ==pinno:
                    print("Your information are\n")
                    found = True
                    for key in item:
                        print(f"{key} = {item[key]}")
                   
                    
        if not found:
            print("Account not found!")

    def update_details(self):
        accno = int(input("Please enter your account number:-"))
        pinno = int(input("Please enter your pin :-"))

       
        found  = False
        for item in Bank.data:
            if item['Account_no'] == accno and item['Pin'] ==pinno:
                found = True
                print("For updating your details\n\n")
                print("Press 1 for updating Name.")
                print("Press 2 for updating Email.")
                print("Press 3 for updating Age.")
                print("Press 4 for updating Pin.\n")
                check = int(input("Choose one option:- "))
                
                match check:
                    case 1:
                        update_name = input("Enter your new name = ")
                        item['Name'] = update_name

                        Bank.__update()
                        print("Detail updated successfully.")

                    case 2:
                        update_email = input("Enter your new Email = ")
                        item['Email'] = update_email

                        Bank.__update()
                        print("Detail updated successfully.")

                    case 3:
                        update_age = input("Enter your new age = ")
                        item['Age'] = update_age

                        Bank.__update()
                        print("Detail updated successfully.")

                    case 4:
                        update_Pin = int(input("Enter your new Pin = "))
                        item['Pin'] = update_Pin
                        Bank.__update()
                        print("Detail updated successfully.")

                    case _:
                        print("Invalid choice!")
                    
                   
                    
        if not found:
            print("Account not found!")

    def delete_acc(self):
        accno = int(input("Please enter your account number:-"))
        pinno = int(input("Please enter your pin :-"))

        userdata = [item for item in Bank.data if item['Account_no']== accno and item['Pin']==pinno]
        
        if userdata ==False:
            print("Account not found!")
        else:
            check = input("Press y if you want to delete the account or press n for cancel :-")
            if check=='n' or check =='N':
                pass
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)

                print("Account deleted successfully")
                Bank.__update()



user = Bank()

def choices(num):
    match num:
        case 1:
            user.create_acc()
        case 2:
            user.deposit_money()
        case 3:
            user.withdraw_money()
        case 4:
            user.show_details()
        case 5:
            user.update_details()
        case 6:
            user.delete_acc()
        case _:
            print("You pressed wrong number!")



print("Press 1 for creating an account.")
print("Press 2 for depositing money.")
print("Press 3 for withdrawing money.")
print("Press 4 for detail.")
print("Press 5 for updating details.")
print("Press 6 for deleting your account.")

choice = int(input("Enter your response:-"))

choices(choice)