#!/bin/env python3

from sys import argv
from pathlib import Path
import requests
import json

creds_path = str(Path.home())+ "/.local/share/pydef/credentials"

# ansi color codes
green = "\033[32m"
red = "\033[31m"
blue = "\033[34m"
cyan = "\033[36m"
endclr = "\033[0m"

def main():

    if len(argv) < 2:
        print("Usage:\n\t" +green+ "def" +endclr+ " [word]")
        exit()

    # create the folder for the credentials file if it doesn't exits
    if not Path("~/.local/share/pydef").expanduser().exists():
        Path("~/.local/share/pydef").expanduser().mkdir(parents=True)

    if argv[1] == "--credentials":
        create_credentials()
        exit()

    word = argv[1].lower()

    credentials = get_credentials()

    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/en-us/"

    global oxfordapi
    oxfordapi = requests.get(url + word, headers = credentials)

    if oxfordapi.status_code != 200:
        print(red + "error" +endclr+ ": word not found.")
        exit()

    print(green + word + endclr)
    for i in word:
        print("=" ,end='')
    print('\n')

    print_all_defs()

def get_credentials():

    try:
        creds_file = open(creds_path)
        creds = creds_file.read().splitlines()
        creds_file.close()

        return {"app_id": creds[0], "app_key": creds[1]}

    except:
        print("No credentials found.")
        print("Go to https://developer.oxforddictionaries.com/ and sign up for an API key.")
        print("Then come back and run 'def --credentials' to enter your app id and key.")
        exit()

def create_credentials():

    if Path(creds_path).exists():
        print("An api key file already exits, would you like to overrite it? [y/n] " , end='')
        answer = str(input())

        if not (answer == "y" or answer == "Y" or answer == ""):
            return

    creds_file = open(creds_path, "w")

    app_id = str(input("Enter your app_id: "))
    app_key = str(input("Enter your app_key: "))

    creds_file.write(app_id + '\n')
    creds_file.write(app_key + '\n')
    creds_file.close()

def print_all_defs():

    results = oxfordapi.json()["results"]
    count = 0

    # print all the definitions in each lexical entry
    for entry in results:
        print_defs(entry["lexicalEntries"])
        count += 1

        # add spacers in between each lexical entry
        if count != len(results):
            print(" ----------\n")

def print_defs(lexical_entry):

    senses = lexical_entry[0]["entries"][0]["senses"]

    for entry in senses:

        # print definition
        if "definitions" in entry:
            definition = entry["definitions"][0]
            print(green + "+" + endclr, definition)

        # print examples
        if "examples" in entry:
            examples = [] 
            for eg in entry["examples"]:
                examples.append(eg["text"])

            print(blue + "  eg: " + endclr, end='')
            print(*examples, sep='\n      ')

        # print synonyms
        if "synonyms" in entry:
            synonyms = []
            for syn in entry["synonyms"]:
                synonyms.append(syn["text"])

            print(cyan + "  synonyms: " + endclr, end='')
            print(*synonyms, sep=', ')

        print('')

main()
