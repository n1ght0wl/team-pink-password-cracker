import hashlib
from urllib.request import urlopen
import json
import random
import string
import time
import pwinput
from tkinter import * 
from threading import Thread
from PIL import Image, ImageTk
import sys
import os

#----- Functions -------# 


def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)


'''reads a worldlist via url and returns it as a file'''
def readwordlist(url):
    try:
        wordlistfile = urlopen(url).read()
    except Exception as e:
        print("Hey there was some error while reading the wordlist, error:", e)
        exit()
    return wordlistfile

'''hashes a cleartext password and returns the hashed result'''
def hash(wordlistpassword):
    result = hashlib.sha256(wordlistpassword.encode('utf-8')).hexdigest()
    return result


'''merge three lists without duplicates'''
def merge_lists(list1, list2, list3):
    temp_set = set(list1)
    temp_set.update(list2)
    temp_set.update(list3)
    return list(temp_set)

'''returns data (json or txt) from url as python list'''
def return_as_list(url): 
    if url == '': #if no url
        return [] #return empty list 
    else:
        password_list = readwordlist(url).decode("utf-8") #decode url to string 
        try :      
            return json.loads(password_list) #parse json
        except Exception:
            try: 
                return password_list.split('\n') #treat as txt string
            except Exception as e:
                print("Error converting data to list:", e) #other conversion error 
    
'''function to validate password'''
def validate_password(password):
    conds = {
        "an uppercase letter": lambda s: any(x.isupper() for x in s),
        "a lowercase letter": lambda s: any(x.islower() for x in s),
        "a number": lambda s: any(x.isdigit() for x in s),
        "to be at least 8 characters long": lambda s: len(s) >= 8
    }

    valid = True
    for name, cond in conds.items():
        if not cond(password):
            print("Your password needs " + name)
            valid = False

    if valid:
        print("This password is strong!")
    else:
        print("Please try and create a stronger password.")
    return valid


def get_user_password_and_start_bruteforce():
    global pw_found
    global test
    global statusbar

    '''create common password list'''
    url1 = 'https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.json'
    url2 = 'https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top12Thousand-probable-v2.txt'
    url3 = 'https://github.com/danielmiessler/SecLists/blob/master/Passwords/probable-v2-top12000.txt'

    pw_list1 = return_as_list(url1)
    pw_list2 = return_as_list(url2) 
    pw_list3 = return_as_list(url3)

    common_password_list = merge_lists(pw_list1, pw_list2, pw_list3) 

    '''get user's password'''
    #actual_password = pwinput.pwinput(prompt='Please enter your password: ')
    actual_password = user_input.get()

    '''hash user's password'''
    actual_password_hash = hash(actual_password)
    
    '''Running the Brute Force attack from common password list'''
    bruteforce(common_password_list, actual_password_hash)

    if pw_found == True:
        time.sleep(120)

    if pw_found == False:
       
        '''Continue bruteforcing if password is not in common password list'''
        test.config(text="Not a common password but we're not quite in the clear yet...")
        print("Not a common password but we're not quite in the clear yet...")
        list_of_possible_pw_characters = list(string.digits + string.ascii_lowercase + string.ascii_uppercase)
        current_pw_guess = ""

        bruteforce_phase2_start_time = time.time() # mark start of bruteforce phase 2

        while hash(current_pw_guess) != actual_password_hash:
            test.config(text="Not a common password but we're not")
            test2.config(text="quite in the clear yet...")
            
            bruteforce_attack_time_in_minutes = 1 # duration of bruteforce before timeout  
            current_pw_guess = random.choices(list_of_possible_pw_characters, k=len(actual_password))
            test2.config(text="quite in the clear yet..")
            current_pw_guess = "".join(current_pw_guess)
            current_time = time.time()
            test2.config(text="quite in the clear yet.")
            if current_time - bruteforce_phase2_start_time > bruteforce_attack_time_in_minutes * 60 : 
                
                # Update status bar
                statusbar.destroy()
                statusbar = Label(root, text="You've beat the password cracker!", width=500, bd=1, relief=SUNKEN, anchor=E)
                statusbar.pack(side="bottom")
                
                firststring = f"{bruteforce_attack_time_in_minutes} minute(s) timeout!" 
                test.config(text=firststring)
                test2.config(text="Your password appears to be secure, well done.")
                time.sleep(120)
                #print(f"{bruteforce_attack_time_in_minutes} minute(s) timeout! Your password appears to be secure, well done.")
               
        pw_found = True
        #Update status bar
        statusbar.destroy()
        statusbar = Label(root, text = "Password cracked!", width=500, bd=1, relief=SUNKEN, anchor=E)
        statusbar.pack(side='bottom')
   
        firststring = f"Hey! Your password is: {current_pw_guess}" 
        test.config(text=firststring)
        test2.config(text="Your password appears to be secure, well done.")
        print("Hey! Your password is:", current_pw_guess,
            "\n please change this. It's not common but you've been hacked now!")
        time.sleep(120)
        

#bruteforce 
'''implementation of the bruteforce technique'''
def bruteforce(list_of_passwords_to_check_against, actual_password_hash):
    global pw_found
    global statusbar

    for password in list_of_passwords_to_check_against:
        if hash(password) == actual_password_hash:
            pw_found = True
            
            # Update status bar
            statusbar.destroy()
            statusbar = Label(root, text="Password cracked!", width=500, bd=1, relief=SUNKEN, anchor=E)
            statusbar.pack(side='bottom')

            firststring = f"Hey! Your password is: {password}" 
            test.config(text=firststring)
            test2.config(text="Please change this, it's a commonly used password!")
            print("Hey! your password is:", password,
                "\n please change this, it's a commonly used password!")
            return


#----- Main -------# 



'''gui start'''

root = Tk()
root.title("imperva mini")
root.iconbitmap('titlebar_logo.ico')
#If .ico image is not working, can delete line 187 of code and use line 189-190 above instead for logo
#titlebar_logo = PhotoImage(file='titlebar_logo.png')
#root.iconphoto(False, titlebar_logo)
root.geometry("500x500")
root.resizable(width=False, height=False)


logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.pack()

#flag
pw_found = False


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
start_btn = Button(root, textvariable=start_text, command=threading, font="Helvetica", bg="#fc03db", fg="black", height=2, width=15)
start_text.set("start bruteforce")
start_btn.pack(pady=10)

#text labels 
test = Label(root, text="", font='Helvetica')
test.place(x=100, y=320)
test2 = Label(root, text="", font='Helvetica')
test2.place(x=100, y=340)

#restart button
restart_btn = Button(root, text="restart app", font="Helvetica", command=restart_app, height=2, width=15)
restart_btn.place(x=180, y=400)

#status bar
statusbar = Label(root, text = "Awaiting password", width=500, bd=1, relief=SUNKEN, anchor=E)
#status = ttk.Progressbar (root, text="Image: 1 of", bd=1, relief=SUNKEN, anchor=E)
statusbar.pack(side="bottom")

root.mainloop()











