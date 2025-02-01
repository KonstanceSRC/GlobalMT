import time
import sys
import os
import threading
import subprocess
import requests
import random
import string
import json
from playsound import playsound
from colorama import init
init(autoreset=True)

PINK = "\033[38;5;213m"
RESET = "\033[0m"

ascii_art = r'''
  /$$$$$$  /$$           /$$                 /$$ /$$      /$$ /$$$$$$$$
 /$$__  $$| $$          | $$                | $$| $$$    /$$$|__  $$__/
| $$  \__/| $$  /$$$$$$ | $$$$$$$   /$$$$$$ | $$| $$$$  /$$$$   | $$   
| $$ /$$$$| $$ /$$__  $$| $$__  $$ |____  $$| $$| $$ $$/$$ $$   | $$   
| $$|_  $$| $$| $$  \ $$| $$  \ $$  /$$$$$$$| $$| $$  $$$| $$   | $$   
| $$  \ $$| $$| $$  | $$| $$  | $$ /$$__  $$| $$| $$\  $ | $$   | $$   
|  $$$$$$/| $$|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$| $$ \/  | $$   | $$   
 \______/ |__/ \______/ |_______/  \_______/|__/|__/     |__/   |__/   
'''

def type_text(text, delay):
    for char in text:
        sys.stdout.write(PINK + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)

def print_ascii_art():
    print(PINK + ascii_art + RESET)

def play_audio(file):
    playsound(file)

def run_animation_and_audio():
    audio_thread = threading.Thread(target=play_audio, args=('audio.mp3',))
    audio_thread.start()
    delay = 4 / len(ascii_art)
    type_text(ascii_art, delay)
    audio_thread.join()

def handle_command(command):
    if command.lower() == "exit":
        print(PINK + "Exiting program..." + RESET)
        return False
    elif command.lower() == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif command.lower() == "help":
        print(PINK + "Available commands:\nexit - Exit the program\nclear - Clear the screen\nhelp - Show this help message\nabout - Show program info\npingip - Ping an IP address with custom settings\nippacket - Send an IP packet to an address with custom settings\nwebhook - Send or spam messages using a Discord webhook\npassgen - Generate a new password\npassview - View stored passwords\npassdel - Delete a stored password\nconfigfolder - Open the folder where passwords and config are stored" + RESET)
    elif command.lower() == "about":
        print(PINK + "This is a command-line tool with ASCII art and audio effects." + RESET)
    elif command.lower() == "date":
        print(PINK + time.strftime("%Y-%m-%d %H:%M:%S") + RESET)
    elif command.lower() == "time":
        print(PINK + time.strftime("%H:%M:%S") + RESET)
    elif command.lower() == "greet":
        print(PINK + "Hello, user!" + RESET)
    elif command.lower() == "pingip":
        ping_ip_command()
    elif command.lower() == "ippacket":
        ippacket_command()
    elif command.lower() == "webhook":
        webhook_command()
    elif command.lower() == "cls":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif command.lower() == "passgen":
        passgen_command()
    elif command.lower() == "passview":
        passview_command()
    elif command.lower() == "passdel":
        passdel_command()
    elif command.lower() == "configfolder":
        open_config_folder()
    else:
        print(PINK + f"Command '{command}' not recognized. Type 'help' for a list of commands." + RESET)
    return True

def get_hidden_folder_path():
    # Get the path to the hidden folder, now named GLOBALMT in the current working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
    hidden_folder = os.path.join(current_dir, ".GLOBALMT")  # Make it a hidden folder on Unix-like systems
    if not os.path.exists(hidden_folder):
        os.makedirs(hidden_folder)
    if os.name == 'nt':  # For Windows, make the folder hidden
        subprocess.run(['attrib', '+h', hidden_folder])
    return hidden_folder

def open_config_folder():
    hidden_folder = get_hidden_folder_path()
    if os.name == 'nt':  # Windows
        subprocess.run(['explorer', hidden_folder])
    elif os.name == 'posix':  # Linux/macOS
        if sys.platform == "darwin":  # macOS
            subprocess.run(['open', hidden_folder])
        else:  # Linux
            subprocess.run(['xdg-open', hidden_folder])
    else:
        print(PINK + "Unsupported OS." + RESET)

def prompt_password():
    hidden_folder = get_hidden_folder_path()
    config_file = os.path.join(hidden_folder, "config.json")
    
    if not os.path.exists(config_file):
        return False
    
    with open(config_file, "r") as f:
        config = json.load(f)

    stored_password = config.get("password", None)

    if stored_password:
        entered_password = input(PINK + "Enter the password to continue: " + RESET)
        return entered_password == stored_password
    return False

def set_password():
    hidden_folder = get_hidden_folder_path()
    config_file = os.path.join(hidden_folder, "config.json")

    new_password = input(PINK + "Enter a new password to set: " + RESET)
    
    with open(config_file, "w") as f:
        json.dump({"password": new_password}, f)
    print(PINK + "Password set successfully!" + RESET)

def prompt_create_password():
    hidden_folder = get_hidden_folder_path()
    config_file = os.path.join(hidden_folder, "config.json")
    
    if not os.path.exists(config_file):
        response = input(PINK + "You don't have a password set. Would you like to create one? (y/n): " + RESET).lower()
        if response == "y":
            set_password()
            return True
        return False
    return True

def ping_ip_command():
    ip = input(PINK + "Enter the IP address to ping: " + RESET)
    times = int(input(PINK + "How many times do you want to ping the IP? " + RESET))
    delay = float(input(PINK + "Enter the delay between pings (in seconds): " + RESET))

    print(PINK + f"Pinging {ip} {times} times with a {delay}s delay..." + RESET)

    for i in range(times):
        response = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode == 0:
            print(PINK + f"Ping {i + 1}: Success" + RESET)
        else:
            print(PINK + f"Ping {i + 1}: Failed" + RESET)
        time.sleep(delay)

def ippacket_command():
    ip = input(PINK + "Enter the IP address to send the packet to: " + RESET)
    times = int(input(PINK + "How many packets do you want to send? " + RESET))
    delay = float(input(PINK + "Enter the delay between sending packets (in seconds): " + RESET))

    print(PINK + f"Sending IP packets to {ip} {times} times with a {delay}s delay..." + RESET)

    for i in range(times):
        response = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode == 0:
            print(PINK + f"Packet {i + 1}: Success" + RESET)
        else:
            print(PINK + f"Packet {i + 1}: Failed" + RESET)
        time.sleep(delay)

def webhook_command():
    webhook_url = input(PINK + "Enter your Discord webhook URL: " + RESET)
    action = input(PINK + "Do you want to [spam] or [send] a message? " + RESET).lower()

    if action not in ['spam', 'send']:
        print(PINK + "Invalid action. Please enter either 'spam' or 'send'." + RESET)
        return

    message = input(PINK + "Enter the message to send: " + RESET)

    if action == 'send':
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 204:
            print(PINK + "Message sent successfully!" + RESET)
        else:
            print(PINK + "Failed to send message." + RESET)

    elif action == 'spam':
        times = int(input(PINK + "How many times do you want to spam the message? " + RESET))
        delay = float(input(PINK + "Enter the delay between spams (in seconds): " + RESET))

        for i in range(times):
            response = requests.post(webhook_url, json={"content": message})
            if response.status_code == 204:
                print(PINK + f"Spam {i + 1}: Message sent!" + RESET)
            else:
                print(PINK + f"Spam {i + 1}: Failed to send message." + RESET)
            time.sleep(delay)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def passgen_command():
    if not prompt_password() and not prompt_create_password():
        return
    
    account_name = input(PINK + "Enter the account/service name (e.g. 'Email', 'Facebook'): " + RESET)
    password = generate_password()
    print(PINK + f"Generated Password for {account_name}: {password}" + RESET)
    
    hidden_folder = get_hidden_folder_path()
    passwords_file = os.path.join(hidden_folder, "passwords.json")
    
    if os.path.exists(passwords_file):
        with open(passwords_file, "r") as f:
            passwords = json.load(f)
    else:
        passwords = {}
    
    password_id = len(passwords) + 1
    passwords[password_id] = {"account_name": account_name, "password": password}
    
    with open(passwords_file, "w") as f:
        json.dump(passwords, f, indent=4)
    
    print(PINK + f"Password saved for account '{account_name}' with ID {password_id}" + RESET)

def passview_command():
    if not prompt_password() and not prompt_create_password():
        return
    
    hidden_folder = get_hidden_folder_path()
    passwords_file = os.path.join(hidden_folder, "passwords.json")
    
    if os.path.exists(passwords_file):
        with open(passwords_file, "r") as f:
            passwords = json.load(f)
        
        print(PINK + "Stored Passwords:" + RESET)
        for pid, data in passwords.items():
            print(f"ID: {pid} - Account: {data['account_name']} - Password: {data['password']}")
    else:
        print(PINK + "No passwords stored." + RESET)

def passdel_command():
    if not prompt_password() and not prompt_create_password():
        return
    
    hidden_folder = get_hidden_folder_path()
    passwords_file = os.path.join(hidden_folder, "passwords.json")
    
    if os.path.exists(passwords_file):
        with open(passwords_file, "r") as f:
            passwords = json.load(f)
        
        print(PINK + "Stored Passwords:" + RESET)
        for pid, data in passwords.items():
            print(f"ID: {pid} - Account: {data['account_name']} - Password: {data['password']}")

        try:
            pid_to_delete = int(input(PINK + "Enter the ID of the password you want to delete: " + RESET))

            if pid_to_delete in passwords:
                del passwords[pid_to_delete]
                with open(passwords_file, "w") as f:
                    json.dump(passwords, f, indent=4)
                print(PINK + f"Password with ID {pid_to_delete} has been deleted." + RESET)
            else:
                print(PINK + "No password found with that ID." + RESET)
        except ValueError:
            print(PINK + "Invalid input. Please enter a valid ID number." + RESET)
    else:
        print(PINK + "No passwords stored." + RESET)

def main():
    run_animation_and_audio()
    while True:
        try:
            command = input(PINK + "[$] > " + RESET)
            if not handle_command(command):
                break
        except KeyboardInterrupt:
            print(PINK + "\nProgram interrupted. Exiting..." + RESET)
            break

if __name__ == "__main__":
    main()
