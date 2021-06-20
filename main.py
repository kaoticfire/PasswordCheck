#!/usr/bin/env python3
#  Copyright (c) 2021
#
#  MIT License
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
""" A program the check given passwords again those that have been found leaked, and those likely to be leaked.
If either are true, a suggested password is given in return. """
__name__ = 'Password Check v.2'
__author__ = 'Virgil Hoover'
__version__ = '2.0.1'

from array import array
from locale import setlocale, LC_ALL
from random import choice, shuffle
from string import ascii_uppercase, ascii_lowercase, digits, punctuation

# Using dictionary checking
from enchant import Dict
# Using automated typing
from pyautogui import press
# Using Chrome to access web
from selenium.webdriver import Chrome

# TODO Make into Flask Application

RED = '\033[1;31;40m'
GREEN = '\033[1;32;40m'
RESET = '\033[1;38;40m'
CYAN = '\033[1;36;40m'


def check_if_password_found(password: str):
    """ Compares a given password to a list of hacked or easily hackable passwords.
    If the password is not found add it to the list to discourage re-use.

    :param password: the password to check for issues.
    """
    password_list = []
    file = 'pass.txt'
    with open(file, 'r') as file_reader:
        password_list.append(file_reader.read())

    if (password not in password_list) and (not compare_to_dictionary(password)):
        print(RESET + 'Local Check: ' + GREEN + 'PASS' + RESET)
        print('Remote Check:', check_password_again(password), '\n' + RESET)
        answer = input('Would you like a suggested password? (y/n) ')

        if answer.lower() == 'y':
            password_generator(length=len(password) + 2)

        with open(file, 'a') as file_writer:
            file_writer.write(password)
    else:
        print(RESET + 'Local Check: ' + RED + 'FAIL\n' + RESET)
        password_generator(length=len(password))


def compare_to_dictionary(password: str) -> bool:
    """ Compares given string against English dictionary for match of valid word.
    Called from check_password function.

    :param: password: The password is then checked against the english dictionary.
    """
    dictionary_string = Dict('en_US')
    setlocale(LC_ALL, 'en_US.UTF-8')
    return dictionary_string.check(password)


def password_generator(length: int):
    """ Generates a password of n length, comprised of letters (upper and lower), numbers, and symbols.

    :param length: how many characters the password should be."""
    generated_password = ''
    temporary_list = ''
    combined_list = digits + ascii_uppercase + ascii_lowercase + punctuation
    temporary_password = choice(digits) + choice(ascii_uppercase) + choice(ascii_lowercase) + choice(punctuation)

    # Add 5 to length of temporary_password to help ensure a strong generated one.
    for _ in range(length - len(temporary_password) + 5):
        temporary_password += choice(combined_list)
        temporary_list = array('u', temporary_password)
        shuffle(temporary_list)

    for item in temporary_list:
        generated_password += item

    print('Try this one instead\n' + CYAN + generated_password + RESET)


def check_password_again(pswd: str) -> str:
    """ Check against a website with known data breach credentials database. Using a Chrome Web Driver.

    :param pswd: the password checked a second time for problems.
    """
    driver = Chrome(executable_path='/home/v/Downloads/chromedriver')
    # Open the website
    driver.get('https://cybernews.com/password-leak-check/')

    # Send Password to check
    text_box = driver.find_element_by_name('p')
    text_box.send_keys(pswd)
    press('enter')

    if 'detected 1969085 times' in driver.page_source:
        return RED + 'FAIL'
    else:
        return GREEN + 'PASS'


if __name__ == 'Password Check v.2':
    passwd = input('Enter the password you wish to check for data breaches: ')
    check_if_password_found(passwd)
