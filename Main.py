import hashlib
from urllib.request import urlopen
import json
import random
import string
from getpass import getpass 

def readwordlist(url):
    try:
        wordlistfile = urlopen(url).read()
    except Exception as e:
        print("Hey there was some error while reading the wordlist, error:", e)
        exit()
    return wordlistfile


def hash(wordlistpassword):
    result = hashlib.sha1(wordlistpassword.encode())
    return result.hexdigest()

def bruteforce(guesspasswordlist, actual_password_hash):
    for guess_password in guesspasswordlist:
        if hash(guess_password) == actual_password_hash:
            print("Hey! your password is:", guess_password,
                "\n please change this, it's a commonly used password!")
            exit()

############# append the below code ################

url = 'https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.json'

#actual_password = str(input("Please enter your password: "))
actual_password = getpass("Please enter your password: ")
actual_password_hash = hash(actual_password)

passwordlist = readwordlist(url).decode("utf-8")
guesspasswordlist = json.loads(passwordlist)

# Running the Brute Force attack from common password list
bruteforce(guesspasswordlist, actual_password_hash)

# Running the Brute Force if password is not in the top 100 list
character = string.digits + string.ascii_lowercase + string.ascii_uppercase
character_list = list(character)
guess = ""
while hash(guess) != actual_password_hash:
    guess = random.choices(character_list, k=len(actual_password))
    guess = "".join(guess)
print("Hey! Your password is:", guess,
      "\n please change this. It's not common but you've been hacked now!")

#function to validate password
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
