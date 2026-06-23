from encryption import encrypt_password, decrypt_password
from database import load_data, save_data


def add_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    data = load_data()

    data[website] = {
        "username": username,
        "password": encrypt_password(password)
    }

    save_data(data)

    print("Password Saved Successfully!")


def view_password():
    website = input("Enter Website: ")

    data = load_data()

    if website in data:
        print("\nUsername:", data[website]["username"])

        print(
            "Password:",
            decrypt_password(data[website]["password"])
        )
    else:
        print("No Record Found")


def view_all():
    data = load_data()

    if not data:
        print("No Passwords Stored")
        return

    for website, details in data.items():
        print("\nWebsite:", website)
        print("Username:", details["username"])
        print(
            "Password:",
            decrypt_password(details["password"])
        )