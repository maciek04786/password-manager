from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- SAVE/LOAD EMAIL ---------------------------------- #
def save_email():
    email = email_entry.get()
    with open("email.json", "w") as data_file:
        json.dump(email, data_file)


def load_email():
    try:
        with open("email.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(message="You haven't saved any email address.")
    else:
        email_entry.insert(0, data)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))] + \
                    [random.choice(numbers) for _ in range(random.randint(2, 4))] + \
                    [random.choice(symbols) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    random_password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, random_password)
    pyperclip.copy(random_password)


# ---------------------------- SAVE ACCOUNT ------------------------------- #
def save_account():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                data.update(new_data)
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# --------------------------- CLEAR ENTRIES --------------------------- #
def clear_entries():
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


# --------------------------- FIND PASSWORD --------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            email_entry.delete(0, END)
            email_entry.insert(0, email)
            password_entry.delete(0, END)
            password_entry.insert(0, password)
        else:
            messagebox.showerror(title="Error", message=f"Details For {website} Not Found.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
back_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=back_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky="we", padx=5)
website_entry.focus()
email_entry = Entry(width=32)
email_entry.grid(row=2, column=1, pady=5)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="we")

# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2, columnspan=2, sticky="w")
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, columnspan=2, sticky="w")
add_button = Button(text="Add account", width=27, command=save_account)
add_button.grid(row=4, column=1, sticky="w")
clear_button = Button(text="Clear all fields", width=14, command=clear_entries)
clear_button.grid(row=4, column=2, padx=5, columnspan=2, sticky="w")
save_email_button = Button(text="Save", width=6, command=save_email)
save_email_button.grid(row=2, column=2, sticky="w")
load_email_button = Button(text="Load", width=6, command=load_email)
load_email_button.grid(row=2, column=3, sticky="w")

window.mainloop()
