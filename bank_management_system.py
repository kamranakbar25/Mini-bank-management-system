import json
import random
import string
from pathlib import Path

import streamlit as st


class Bank:
    database = Path("data.json")

    @classmethod
    def load_data(cls):
        if cls.database.exists():
            try:
                with open(cls.database, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def generate_account_no(cls, data):
        while True:
            alpha = random.choices(string.ascii_uppercase, k=3)
            num = random.choices(string.digits, k=6)
            splchar = random.choices("!@#$%^&*", k=1)

            acc_no_list = alpha + num + splchar
            random.shuffle(acc_no_list)

            account_no = "".join(acc_no_list)

            exists = any(user["accountNo"] == account_no for user in data)
            if not exists:
                return account_no

    @staticmethod
    def find_user(data, account_no, pin):
        for user in data:
            if user["accountNo"] == account_no and user["pin"] == pin:
                return user
        return None


st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Bank Management System")

data = Bank.load_data()

menu = st.sidebar.radio(
    "Choose Option",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Update Details",
        "Delete Account"
    ]
)

if menu == "Create Account":
    st.subheader("Create New Account")

    with st.form("create_account_form"):
        name = st.text_input("Enter your name")
        age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
        email = st.text_input("Enter your email")
        pin = st.text_input("Enter your 4 digit PIN", type="password", max_chars=4)

        submit = st.form_submit_button("Create Account")

        if submit:
            if not name or not email or not pin:
                st.error("Please fill all fields.")

            elif age < 10:
                st.error("Sorry! Age must be at least 10 years.")

            elif not pin.isdigit() or len(pin) != 4:
                st.error("PIN must be exactly 4 digits.")

            else:
                account_no = Bank.generate_account_no(data)

                new_user = {
                    "name": name,
                    "age": age,
                    "email": email,
                    "pin": pin,
                    "accountNo": account_no,
                    "balance": 0
                }

                data.append(new_user)
                Bank.save_data(data)

                st.success("ACCOUNT CREATED SUCCESSFULLY!")
                st.info(f"Your Account Number: `{account_no}`")
                st.warning("Please note down your account number.")


elif menu == "Deposit Money":
    st.subheader("Deposit Money")

    with st.form("deposit_form"):
        account_no = st.text_input("Enter your account number")
        pin = st.text_input("Enter your PIN", type="password", max_chars=4)
        amount = st.number_input("Enter amount to deposit", min_value=1, step=1)

        submit = st.form_submit_button("Deposit")

        if submit:
            user = Bank.find_user(data, account_no, pin)

            if not user:
                st.error("Sorry! No account found.")

            elif amount > 10000:
                st.error("You can deposit only up to ₹10,000 at once.")

            else:
                user["balance"] += amount
                Bank.save_data(data)
                st.success(f"₹{amount} deposited successfully!")
                st.info(f"Current Balance: ₹{user['balance']}")


elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")

    with st.form("withdraw_form"):
        account_no = st.text_input("Enter your account number")
        pin = st.text_input("Enter your PIN", type="password", max_chars=4)
        amount = st.number_input("Enter amount to withdraw", min_value=1, step=1)

        submit = st.form_submit_button("Withdraw")

        if submit:
            user = Bank.find_user(data, account_no, pin)

            if not user:
                st.error("Sorry! No account found.")

            elif amount > 10000:
                st.error("You can withdraw only up to ₹10,000 at once.")

            elif amount > user["balance"]:
                st.error("Insufficient balance.")

            else:
                user["balance"] -= amount
                Bank.save_data(data)
                st.success(f"₹{amount} withdrawn successfully!")
                st.info(f"Current Balance: ₹{user['balance']}")

elif menu == "Account Details":
    st.subheader("Account Details")

    with st.form("details_form"):
        account_no = st.text_input("Enter your account number")
        pin = st.text_input("Enter your PIN", type="password", max_chars=4)

        submit = st.form_submit_button("Show Details")

        if submit:
            user = Bank.find_user(data, account_no, pin)

            if not user:
                st.error("Sorry! No account found.")

            else:
                st.success("Account found!")

                st.write("### Your Information")
                st.write(f"**Name:** {user['name']}")
                st.write(f"**Age:** {user['age']}")
                st.write(f"**Email:** {user['email']}")
                st.write(f"**Account Number:** `{user['accountNo']}`")
                st.write(f"**Balance:** ₹{user['balance']}")

elif menu == "Update Details":
    st.subheader("Update Details")

    st.info("You cannot change your age and account number.")

    with st.form("update_form"):
        account_no = st.text_input("Enter your account number")
        pin = st.text_input("Enter your current PIN", type="password", max_chars=4)

        new_name = st.text_input("Enter new name or leave empty")
        new_email = st.text_input("Enter new email or leave empty")
        new_pin = st.text_input("Enter new 4 digit PIN or leave empty", type="password", max_chars=4)

        submit = st.form_submit_button("Update Details")

        if submit:
            user = Bank.find_user(data, account_no, pin)

            if not user:
                st.error("Sorry! No account found.")

            else:
                if new_name:
                    user["name"] = new_name

                if new_email:
                    user["email"] = new_email

                if new_pin:
                    if new_pin.isdigit() and len(new_pin) == 4:
                        user["pin"] = new_pin
                    else:
                        st.error("New PIN must be exactly 4 digits.")
                        st.stop()

                Bank.save_data(data)
                st.success("DETAILS UPDATED SUCCESSFULLY!")

elif menu == "Delete Account":
    st.subheader("Delete Account")

    with st.form("delete_form"):
        account_no = st.text_input("Enter your account number")
        pin = st.text_input("Enter your PIN", type="password", max_chars=4)

        confirm = st.checkbox("Yes, I want to delete my account permanently.")

        submit = st.form_submit_button("Delete Account")

        if submit:
            user = Bank.find_user(data, account_no, pin)

            if not user:
                st.error("Sorry! No account found.")

            elif not confirm:
                st.warning("Please confirm before deleting your account.")

            else:
                data.remove(user)
                Bank.save_data(data)
                st.success("ACCOUNT DELETED SUCCESSFULLY.")