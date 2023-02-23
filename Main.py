import hashlib
import json
import os
import random
import ssl
import string
import sys
import threading
import time
from tkinter import *
from threading import Thread
from urllib.request import urlopen
from PIL import Image, ImageTk

#fix SSL certificate verification errors
ssl._create_default_https_context = ssl._create_stdlib_context

#----- Functions -------#

def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def readwordlist(url):
    try:
        wordlistfile = urlopen(url).read()
    except Exception as e:
        print("Hey there was some error while reading the wordlist, error:", e)
        exit()
    return wordlistfile

def hash(wordlistpassword):
    result = hashlib.sha256(wordlistpassword.encode('utf-8')).hexdigest()
    return result

def merge_lists(list1, list2, list3):
    temp_set = set(list1)
    temp_set.update(list2)
    temp_set.update(list3)
    return list(temp_set)

def return_as_list(url):
    if url == '': #if no url
        return [] #return empty list

    password_list = readwordlist(url).decode("utf-8") #decode url to string
    try :
        return json.loads(password_list) #parse json
    except Exception:
        try:
            return password_list.split('\n') #treat as txt string
        except Exception as e:
            print("Error converting data to list:", e) #other conversion error

#main bruteforce method
def get_user_password_and_start_bruteforce():
    global pw_found
    global text

    url1 = "https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.json"
    url2 = "https://github.com/OWASP/passfault/blob/master/wordlists/wordlists/10k-worst-passwords.txt"
    url3 = "https://github.com/danielmiessler/SecLists/blob/master/Passwords/probable-v2-top12000.txt"
    
    pw_list1 = return_as_list(url1)
    pw_list2 = return_as_list(url2)
    pw_list3 = return_as_list(url3)
    common_password_list = merge_lists(pw_list1, pw_list2, pw_list3)
    actual_password = user_input.get()
    actual_password_hash = hash(actual_password)
    bruteforce(common_password_list, actual_password_hash)
    if pw_found is True:
        time.sleep(120)
    if pw_found is False:
        #Continue random bruteforce using valid characters if password not in common password list
        text.config(text="Not a common password but we're not quite in the clear yet...")
        print("Not a common password but we're not quite in the clear yet...")
        list_of_valid_pw_characters = list(
            string.digits + string.ascii_lowercase + string.ascii_uppercase
        )
        list_of_valid_pw_characters.append("!_")
        current_pw_guess = ""

        bruteforce_phase2_start_time = time.time()  # mark start of phase2: random bruteforce 

        while hash(current_pw_guess) != actual_password_hash:
            text.config(text="Not a common password but we're not")
            text2.config(text="quite in the clear yet...")
            bruteforce_attack_time_in_minutes = 1  # duration of random bruteforce before timeout
            current_pw_guess = random.choices(
                list_of_valid_pw_characters, k=len(actual_password))
            text2.config(text="quite in the clear yet..")
            current_pw_guess = "".join(current_pw_guess)
            current_time = time.time()
            text2.config(text="quite in the clear yet.")
            if current_time - bruteforce_phase2_start_time > bruteforce_attack_time_in_minutes * 60:
                firststring = f"{bruteforce_attack_time_in_minutes} minute(s) timeout!"
                text.config(text=firststring)
                text2.config(text="Your password appears to be secure, well done.")
                time.sleep(120)
        pw_found = True

        firststring = f"Hey! Your password is: {current_pw_guess}"
        text.config(text=firststring)
        text2.config(text="Your password appears to be secure, well done.")
        print(
            "Hey! Your password is:",
            current_pw_guess,
            "\n please change this. It's not common but you've been hacked now!",
        )
        time.sleep(120)


#bruteforce hashed password against a password list
def bruteforce(list_of_passwords_to_check_against, actual_password_hash):
    global pw_found

    for password in list_of_passwords_to_check_against:
        if hash(password) != actual_password_hash:
            continue

        pw_found = True
        firststring = f"Hey! Your password is: {password}"
        text.config(text=firststring)
        text2.config(text="Please change this, it's a commonly used password!")
        print(
            "Hey! your password is:",
            password,
            "\n please change this, it's a commonly used password!",
        )
        return


#----- Main -------#

'''gui start'''

#window config
root = Tk()
root.title("imperva mini")
root.geometry("500x500")
root.iconbitmap("titlebar_logo.ico")
root.resizable(width=False, height=False)

#logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.pack()

#instructions
instructions = Label(root, text="please enter your password:", font="Helvetica", pady=5)
instructions.pack()

#entry box
user_input = StringVar()
entry_box = Entry(root, show="*", textvariable=user_input)
entry_box.pack()

#thread for bruteforce function
def threading():
    t1=Thread(target=get_user_password_and_start_bruteforce)
    t1.start()

#start button
start_text = StringVar()
start_btn = Button(
    root,
    textvariable=start_text,
    command=threading,
    font="Helvetica",
    bg="#fc03db",
    fg="black",
    height=2,
    width=15,
)
start_text.set("start bruteforce")
start_btn.pack(pady=10)

#output text
text = Label(root, text="", font='Helvetica')
text.pack(pady=10)
text2 = Label(root, text="", font='Helvetica')
text2.pack()

#restart button
restart_btn = Button(root, text="restart app", font="Helvetica", command=restart_app, height=2, width=15)
restart_btn.pack(side="bottom", pady=10)

root.mainloop()