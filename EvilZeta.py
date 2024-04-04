import shodan
from colorama import just_fix_windows_console
from termcolor import colored

import subprocess
import datetime
import os


# use Colorama to make Termcolor work on Windows too
just_fix_windows_console()

# --------------------------------------------------------
# Funçao que checa a conexao de cada alvo
def check_connection(ip):
    process = subprocess.check_output(f'adb connect {ip} ', shell=True)
    date = datetime.datetime.now()
    if "cannot connect" in process.decode('utf-8'):
        print (f"[!] Debug: {date} - Dispositivo  nao vulneravel: {ip}\n")
    else:
        print (f"[*] Debug: {date} - Dispositivo Vulneravel\n")
        check = subprocess.check_output(f'adb disconect {ip}', shell=True)
        result = check.decode('utf-8')
        print (f"[*] Debug: {date} - {result}\n")
# --------------------------------------------------------


# --------------------------------------------------------
# Insira sua chave de API do Shodan
API_KEY = "15hlnqlCHZTxvko4O5mJKM51AhyOLCSZ"
def search_targets():
    # Cria uma instância da classe API do Shodan
    api = shodan.Shodan(API_KEY)

    try:
        # Realiza a consulta
        query = '"Android Debug Bridge" "Device" port:5555 country:"BR"'
        results = api.search(query)

        # Exibe os resultados
        print('Resultados encontrados:', results['total'])
        for result in results['matches']:
            target = result['ip_str']
            print(f"IP: {target}")

    except shodan.APIError as e:
        print('Erro: %s' % e)
# --------------------------------------------------------

# --------------------------------------------------------
banner = """
            .__.__            __          
    _______  _|__|  | _________/  |______   
    _/ __ \  \/ /  |  | \___   /\   __\__  \  
    \  ___/\   /|  |  |__/    /  |  |  / __ \_
    \___  >\_/ |__|____/_____ \ |__| (____  /
        \/                   \/           \/ 
        Code by DHG.
"""

menu = """
    1 = Buscar alvos no shodan.
    2 = Avaliar alvo específico.
       """
# --------------------------------------------------------
# Ip dos alvos 
ip = "138.204.63.130"

# Funçao principal
def main():
    while True:

        print(colored(f"{banner}\n", 'magenta'))

        print(colored(f"{menu}\n", 'green'))
        
        command = input(colored(">>", 'green'))
        command = int(command)
        if command == 1:
            search_targets()
        if command == 2:
            target = input("Seu Alvo: ")
            check_connection(target)
        else:
            print (colored("[!]Debug: Comando invalido", 'red'))

if __name__ == '__main__':
    main()

