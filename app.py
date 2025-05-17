# Improved version with modular design, error handling, and Streamlit integration

import json
import random
import re
from pathlib import Path
import streamlit as st

class Bank:
    database = 'data.json'
    data = []

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database) as f:
                cls.data = json.load(f)
        else:
            cls.data = []

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as f:
            json.dump(cls.data, f, indent=4)

    @classmethod
    def __account_generator(cls):
        return random.randint(1000000000, 9999999999)

    @classmethod
    def create_acc(cls, name, age, email, pin):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        errors = []

        if not name.isalpha():
            errors.append("Name must be alphabetical.")

        if age < 18 or age > 100:
            errors.append("Age must be between 18 and 100.")

        if len(str(pin)) != 4:
            errors.append("Pin must be 4 digits.")

        if not re.match(pattern, email):
            errors.append("Email format is invalid.")

        if errors:
            return False, errors

        info = {
            "Name": name,
            "Age": age,
            "Email": email,
            "Pin": pin,
            "Account_no": cls.__account_generator(),
            "Balance": 0
        }
        cls.data.append(info)
        cls.__update()
        return True, info

    @classmethod
    def find_account(cls, account_no, pin):
        for acc in cls.data:
            if acc['Account_no'] == account_no and acc['Pin'] == pin:
                return acc
        return None

    @classmethod
    def deposit(cls, account_no, pin, amount):
        acc = cls.find_account(account_no, pin)
        if acc:
            acc['Balance'] += amount
            cls.__update()
            return True, acc['Balance']
        return False, "Invalid account or PIN."

    @classmethod
    def withdraw(cls, account_no, pin, amount):
        acc = cls.find_account(account_no, pin)
        if acc:
            if acc['Balance'] >= amount:
                acc['Balance'] -= amount
                cls.__update()
                return True, acc['Balance']
            else:
                return False, "Insufficient balance."
        return False, "Invalid account or PIN."

    @classmethod
    def show_details(cls, account_no, pin):
        acc = cls.find_account(account_no, pin)
        if acc:
            return True, acc
        return False, "Invalid account or PIN."

    @classmethod
    def update_account(cls, account_no, pin, new_name=None, new_email=None):
        acc = cls.find_account(account_no, pin)
        if acc:
            if new_name:
                if not new_name.isalpha():
                    return False, "Invalid name. Must contain only letters."
                acc['Name'] = new_name
            if new_email:
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(pattern, new_email):
                    return False, "Invalid email format."
                acc['Email'] = new_email
            cls.__update()
            return True, "Account updated successfully."
        return False, "Invalid account or PIN."

    @classmethod
    def delete_account(cls, account_no, pin):
        acc = cls.find_account(account_no, pin)
        if acc:
            cls.data.remove(acc)
            cls.__update()
            return True, "Account deleted successfully."
        return False, "Invalid account or PIN."

# ---------------- STREAMLIT UI ----------------

st.title("Simple Bank Management System")
Bank.load_data()

menu = ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Account", "Delete Account"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Create Account":
    st.subheader("Create New Account")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, step=1)
    email = st.text_input("Enter your email")
    pin = st.text_input("Enter 4 digit PIN", type="password")

    if st.button("Create Account"):
        if pin.isdigit():
            success, response = Bank.create_acc(name, int(age), email, int(pin))
            if success:
                st.success("Account created successfully!")
                st.json(response)
            else:
                st.error("Failed to create account:")
                for err in response:
                    st.warning(err)
        else:
            st.error("Pin must be numeric")

elif choice == "Deposit Money":
    st.subheader("Deposit to Account")
    acc = st.number_input("Enter your Account Number", step=1)
    pin = st.text_input("Enter your PIN", type="password")
    amount = st.number_input("Enter Amount to Deposit", min_value=0.0, step=1.0)

    if st.button("Deposit"):
        if pin.isdigit():
            success, response = Bank.deposit(int(acc), int(pin), float(amount))
            if success:
                st.success(f"Deposit successful! New Balance: Rs. {response}")
            else:
                st.error(response)

elif choice == "Withdraw Money":
    st.subheader("Withdraw from Account")
    acc = st.number_input("Enter your Account Number", step=1)
    pin = st.text_input("Enter your PIN", type="password")
    amount = st.number_input("Enter Amount to Withdraw", min_value=0.0, step=1.0)

    if st.button("Withdraw"):
        if pin.isdigit():
            success, response = Bank.withdraw(int(acc), int(pin), float(amount))
            if success:
                st.success(f"Withdrawal successful! New Balance: Rs. {response}")
            else:
                st.error(response)

elif choice == "Show Details":
    st.subheader("Account Details")
    acc = st.number_input("Enter your Account Number", step=1)
    pin = st.text_input("Enter your PIN", type="password")

    if st.button("Show Details"):
        if pin.isdigit():
            success, response = Bank.show_details(int(acc), int(pin))
            if success:
                st.json(response)
            else:
                st.error(response)

elif choice == "Update Account":
    st.subheader("Update Account Information")
    acc = st.number_input("Enter your Account Number", step=1)
    pin = st.text_input("Enter your PIN", type="password")
    new_name = st.text_input("Enter new name (leave blank if no change)")
    new_email = st.text_input("Enter new email (leave blank if no change)")

    if st.button("Update"):
        if pin.isdigit():
            success, message = Bank.update_account(int(acc), int(pin), new_name if new_name else None, new_email if new_email else None)
            if success:
                st.success(message)
            else:
                st.error(message)

elif choice == "Delete Account":
    st.subheader("Delete Your Account")
    acc = st.number_input("Enter your Account Number", step=1)
    pin = st.text_input("Enter your PIN", type="password")

    if st.button("Delete Account"):
        if pin.isdigit():
            success, message = Bank.delete_account(int(acc), int(pin))
            if success:
                st.success(message)
            else:
                st.error(message)
