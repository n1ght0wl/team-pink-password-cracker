# Imperva Mini
A customisable app that tests passwords against bruteforce attacks 

## Authors

- [@Amy](https://github.com/amyt-code)
- [@Androulla](https://github.com/n1ght0wl)
- [@Jess](https://github.com/jeslyw)
- [@Cate Di Donato](https://github.com/catedido)

## Customisation 
The user may set up to 3 password lists to test against. We have implemented url read-in for lists in json or txt formats, as this provides a higher flexibility of data sources that can be used

Default lists: 
- [UK NCSC PwnedPasswordsTop100k](https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.json)
- [OWASP Passfault 10k Worst](https://github.com/OWASP/passfault/blob/master/wordlists/wordlists/10k-worst-passwords.txt)
- [SecLists Top 12k](https://github.com/danielmiessler/SecLists/blob/master/Passwords/probable-v2-top12000.txt)

Phase 2: randomised bruteforce timeout can be set by user 

The default is set to a 1 minute timeout

## Running the app

install required modules
`pip3 install -r requirements.txt`

run 
`python3 main.py`

## Requirements 

python >= 3.7

pillow>=9.4.0

pwinput>=1.0.3

`pip3 install -r requirements.txt`

## Screenshots

   | Logo  |      Password Cracker |    Enter Password|    Start Bruteforce
   :-------------------------:| :-------------------------:|:-------------------------:|:-------------------------:|
![](https://github.com/n1ght0wl/team-pink-password-cracker/blob/main/logo.png?raw=true) |![](https://github.com/n1ght0wl/team-pink-password-cracker/blob/main/password_cracker_1.png?raw=true)|![](https://github.com/n1ght0wl/team-pink-password-cracker/blob/main/password_cracker_2.png?raw=true)|![](https://github.com/n1ght0wl/team-pink-password-cracker/blob/main/password_cracker_3.png?raw=true)

