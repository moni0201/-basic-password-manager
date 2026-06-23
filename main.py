import json
import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"


# Generate encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as file:
        file.write(key)


# Load encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()

    with open(KEY_FILE, "rb") as file:
        return file.read()


cipher = Fernet(load_key())


# Load passwords
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump({}, file)

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


# Save passwords
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Add password
def add_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted_password = cipher.encrypt(password.encode()).decode()

    data = load_data()

    data[website] = {
        "username": username,
        "password": encrypted_password
    }

    save_data(data)

    print("Password saved successfully!")


# View one password
def view_password():
    website = input("Enter website: ")

    data = load_data()

    if website in data:
        username = data[website]["username"]
        encrypted_password = data[website]["password"]

        password = cipher.decrypt(
            encrypted_password.encode()
        ).decode()

        print(f"Username: {username}")
        print(f"Password: {password}")

    else:
        print("Website not found!")


# View all passwords
def view_all():
    data = load_data()

    if not data:
        print("No passwords stored.")
        return

    for website, details in data.items():
        password = cipher.decrypt(
            details["password"].encode()
        ).decode()

        print("\n---------------------")
        print("Website :", website)
        print("Username:", details["username"])
        print("Password:", password)


# Main menu
while True:
    print("\n===== PASSWORD MANAGER =====")
    print("1. Add Password")
    print("2. View Password")
    print("3. View All Passwords")
    print("4. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        add_password()

    elif choice == "2":
        view_password()

    elif choice == "3":
        view_all()

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid option")