from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "username": username,
        "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Some fields are empty.")
    else:
        try:
            with open("passwords.json", "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError as err:
            with open("passwords.json", "w") as file:
                # Saving updated data
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("passwords.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- LOGIN SEARCH ------------------------------- #


def search():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="No website was specified.")
    else:
        try:
            with open("passwords.json", "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError as err:
            messagebox.showinfo(title="Error", message="No data file found.")
        else:
            if website in data:
                username = data[website]['username']
                password = data[website]['password']
                messagebox.showinfo(title=website, message=f"Username: {username}\n Password: {password}.")
            else:
                messagebox.showinfo(title="Oops", message=f"No details for {website} exists.")
        finally:
            website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#FFFFFF")

canvas = Canvas(width=200, height=200, bg="#FFFFFF", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)


# Labels
website_label = Label(text="Website")
website_label.config(fg="#000000", bg="#FFFFFF")#, font=(FONT_NAME, 45, "bold"))
username_label = Label(text="Email/Username")
username_label.config(fg="#000000", bg="#FFFFFF")
password_label = Label(text="Password")
password_label.config(fg="#000000", bg="#FFFFFF")


# Entries
website_entry = Entry(fg="#000000", bg="#FFFFFF", highlightbackground="#FFFFFF", width=22)
website_entry.focus()
username_entry = Entry(width=39, fg="#000000", bg="#FFFFFF", highlightbackground="#FFFFFF")
username_entry.insert(0, "example@gmail.com")
password_entry = Entry(width=22, fg="#000000", bg="#FFFFFF", highlightbackground="#FFFFFF")


# Buttons
search_button = Button(text="Search", highlightbackground="#FFFFFF", bg="#FFFFFF", width=13, command=search)
generate_password_button = Button(text="Generate Password", highlightbackground="#FFFFFF", bg="#FFFFFF",
                                  command=generate_password)
add_button = Button(text="Add", width=37, highlightbackground="#FFFFFF", bg="#FFFFFF", command=save)


# Grid Layout
canvas.grid(column=1, row=0)
website_label.grid(column=0, row=1)
website_entry.grid(column=1, row=1)
search_button.grid(column=2, row=1)
username_label.grid(column=0, row=2)
username_entry.grid(column=1, row=2, columnspan=2)
password_label.grid(column=0, row=3)
password_entry.grid(column=1, row=3)
generate_password_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()
