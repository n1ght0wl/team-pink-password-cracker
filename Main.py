import hashlib
from urllib.request import urlopen
import json
import random
import string
import time
import pwinput

#----- Functions -------# 

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

'''implementation of the bruteforce technique'''
def bruteforce(list_of_passwords_to_check_against, actual_password_hash):
    pw_found = False
    for password in list_of_passwords_to_check_against:
        if hash(password) == actual_password_hash:
            pw_found = True
            print("Hey! your password is:", password,
                "\n please change this, it's a commonly used password!")
            exit()          
    if pw_found == False: 
        pass
        


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


#----- Main -------# 

'''input common password lists as url'''
url1 = 'https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.json'
url2 = 'https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top12Thousand-probable-v2.txt'
url3 = ''

pw_list1 = return_as_list(url1)
pw_list2 = return_as_list(url2)
pw_list3 = return_as_list(url3)

ultimate_password_list = merge_lists(pw_list1, pw_list2, pw_list3)

'''get user's password'''
actual_password = pwinput.pwinput(prompt='Please enter your password: ')

'''hash user's password'''
actual_password_hash = hash(actual_password)

'''Running the Brute Force attack from common password list'''
bruteforce(ultimate_password_list, actual_password_hash)

'''Continue bruteforcing if password is not in common password list'''
list_of_possible_pw_characters = list(string.digits + string.ascii_lowercase + string.ascii_uppercase)
current_pw_guess = ""

bruteforce_phase2_start_time = time.time() # mark start of bruteforce phase 2

while hash(current_pw_guess) != actual_password_hash:
    current_pw_guess = random.choices(list_of_possible_pw_characters, k=len(actual_password))
    current_pw_guess = "".join(current_pw_guess)
    current_time = time.time()
    if current_time - bruteforce_phase2_start_time > 60 : #timeout after 1 minute 
        print("Timeout! Your password appears to be secure, well done.")
        exit()

print("Hey! Your password is:", current_pw_guess,
      "\n please change this. It's not common but you've been hacked now!")


