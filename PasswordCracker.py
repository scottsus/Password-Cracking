# Scott Susanto
# ITP 125 Final Project: Password Cracking

# this script does 2 things:
#   1. it breaks the passwords from the example file "hashes.txt"
#   2. it takes an input file of hashed passwords from a user and attempts to convert
#       them into plaintext passwords
#       (in case you ever come across a hashed database and plan to hack it :p KIDDING)

# thank you Dr. Gregg and the awesome learning assistants for an excellent class!

import sys
import hashlib
from pydoc import plain
from itertools import product
from string import ascii_letters, digits
from timeit import default_timer as timer
from datetime import timedelta


# Input/Output function, simply reading hashes from file
def read_file(filename):
    with open(filename) as file:
        hashList = file.read().splitlines()
    return hashList

# main function to crack a list of passwords
# also measures the time taken to crack a particular password
def crack_passwords_bruteforce(hashList, num_passwords):
    print("Using brute force: \n")
    for passwordLen in range(1, num_passwords):
        start = timer()
        crack_password(hashList, passwordLen)
        end = timer()
        elapsed_time = end - start
        print("Time elapsed:", timedelta(seconds=elapsed_time))
    print('\n')

# attempts to crack a given password
# generates all possible ascii + digit strings of a given length
# if there is a match, return the original password in plaintext
def crack_password(hashList, passwordLen):
    chars = ascii_letters + digits  # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    possible_passwords = map(''.join, product(chars, repeat=passwordLen))
    for plaintext_password in possible_passwords:
        hashed_password = hashlib.md5(plaintext_password.encode('utf8')).hexdigest()
        for original_password in hashList:
            if hashed_password == original_password:
                print("Password cracked:", plaintext_password)
                return

# tries words in the english dictionary to narrow scope of attack
# this might potentially make the script faster for some passwords
def dictionary_attack(hashList, dictionary):
    print("Using dictionary attack: \n")
    done = False
    for word in dictionary:
        start = timer()
        hashed_password = hashlib.md5(word.encode('utf8')).hexdigest()
        for original_password in hashList:
            if hashed_password == original_password:
                done = True
                end = timer()
                elapsed_time = end - start
                print("Password cracked:", word)
                print("Time elapsed:", timedelta(seconds=elapsed_time))
    print('\n')

# cracks hashed passwords in a given database
# passwords must be hashed using MD5
def crack_database(input_file, num_passwords):
    hashList = read_file(input_file)
    dictionary = read_file('dictionary.txt')

    print("Cracking the", input_file, "file... \n")
    dictionary_attack(hashList, dictionary)
    crack_passwords_bruteforce(hashList, int(num_passwords))
    print("Done with cracking all passwords!")


# main function
def main():
    num_args = len(sys.argv)
    if (num_args == 1):
        crack_database('hashes.txt', 8)
    elif (num_args == 3):
        input_file = sys.argv[1]
        num_passwords = sys.argv[2]
        crack_database(input_file, num_passwords)
    else:
        print("Incorrect arguments. Please try again with the following format:")
        print("PasswordCracker.py [input_file] [num_passwords]")

if __name__ == "__main__":
    main()





