import sqlite3
import hashlib
import os
from termcolor import colored
import random
import string

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def create_database():
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                website TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id));''')
    conn.commit()
    conn.close()

def register():
    clear_screen()
    print("Register")
    print("-" * 10)
    username = input("Username: ")
    password = input("Password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()
    input("Registration successful. Press enter to continue...")

def login():
    clear_screen()
    print("Login")
    print("-" * 10)
    username = input("Username: ")
    password = input("Password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password_hash))
    user = c.fetchone()
    conn.close()
    if user is not None:
        return user[0]
    else:
        input("Incorrect username or password. Press enter to try again...")
        return None


def generate_password():
    clear_screen()
    print("Generate Password")
    print("-" * 10)
    length = int(input("Length of password (min 8): "))
    if length < 8:
        input("Password length too short. Press enter to try again...")
        return
    uppercase = input("Include uppercase letters? (y/n): ").lower() == "y"
    lowercase = input("Include lowercase letters? (y/n): ").lower() == "y"
    digits = input("Include digits? (y/n): ").lower() == "y"
    special = input("Include special characters? (y/n): ").lower() == "y"
    chars = ""
    if uppercase:
        chars += string.ascii_uppercase
    if lowercase:
        chars += string.ascii_lowercase
    if digits:
        chars += string.digits
    if special:
        chars += string.punctuation
    if chars == "":
        input("At least one type of character must be included. Press enter to try again...")
        return
    password = ''.join(random.choice(chars) for i in range(length))
    input(f"Generated password: {password}. Press enter to continue...")
    return password

def save_password(user_id):
    clear_screen()
    print("Save Password")
    print("-" * 10)
    website = input("Website: ")
    password = input("Password (leave blank to generate): ")
    if password == "":
        password = generate_password()
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords (user_id, website, password) VALUES (?, ?, ?)", (user_id, website, password))
    conn.commit()
    conn.close()
    input("Password saved. Press enter to continue...") 

def view_passwords(user_id):
    clear_screen()
    print("View Passwords")
    print("-" * 10)
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("SELECT website, password FROM passwords WHERE user_id=?", (user_id,))
    passwords = c.fetchall()
    conn.close()
    if len(passwords) == 0:
        input("No passwords found. Press enter to continue...")
    else:
        print("Website\t\tPassword")
        print("-" * 10)
        for website, password in passwords:
            print(f"{website}\t\t{password}")
        input("Press enter to continue...")
def get_username(user_id):
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def main_menu():
    create_database()
    user_id = None
    
    while True:
        clear_screen()
        logo = colored("""            
                  

888     888                  888 888     .d8888b.                                888 d8b                   
888     888                  888 888    d88P  Y88b                               888 Y8P                   
888     888                  888 888    888    888                               888                       
Y88b   d88P 8888b.  888  888 888 888888 888        888  888  8888b.  888d888 .d88888 888  8888b.  88888b.  
 Y88b d88P     "88b 888  888 888 888    888  88888 888  888     "88b 888P"  d88" 888 888     "88b 888 "88b 
  Y88o88P  .d888888 888  888 888 888    888    888 888  888 .d888888 888    888  888 888 .d888888 888  888 
   Y888P   888  888 Y88b 888 888 Y88b.  Y88b  d88P Y88b 888 888  888 888    Y88b 888 888 888  888 888  888 
    Y8P    "Y888888  "Y88888 888  "Y888  "Y8888P88  "Y88888 "Y888888 888     "Y88888 888 "Y888888 888  888                                                      
                                            Author:Ly0kha
                                            Email:M@ly0kha.net                                                               
                                                                                                           

        """, "magenta")
        print(logo)
        print("-" * 60)
        
        if user_id is None:
            print("1.Register")
            print("2.Login")
        else:           
            username = get_username(user_id)
            print(f"Welcome, {username}!")
            print("3.Generate Password")
            print("4.Save Password")
            print("5.View Passwords")
            print("6.Logout")
        
        print("0.Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
        elif choice == "3" and user_id is not None:
            generate_password()
        elif choice == "4" and user_id is not None:
            save_password(user_id)
        elif choice == "5" and user_id is not None:
            view_passwords(user_id)
        elif choice == "6" and user_id is not None:
            user_id = None
        elif choice == "0":
            clear_screen()
            print("Exiting...")
            break
        else:
            input("Invalid choice. Press enter to try again...")
if __name__ == "__main__":
    main_menu()

