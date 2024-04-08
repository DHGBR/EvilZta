import threading
import shodan
import coloredlogs, logging
from colorama import just_fix_windows_console
from termcolor import colored

import subprocess
import datetime
from time import sleep
import os


# Create a logger object.
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

# # use Colorama to make Termcolor work on Windows too
just_fix_windows_console()
# --------------------------------------------------------
# Salva uma nova linha no arquivo de texto
def save_line(file_name, line):
    # abrindo arquivo de texto
    opened_file = open(file_name, 'a')
    # escrevendo uma nova linha
    opened_file.write(f"{line}\n")
    # fechando o arquivo de texto
    opened_file.close()
# --------------------------------------------------------
# --------------------------------------------------------
# Lista de alvos vulneraveis
targets = []

# Funçao que checa a conexao de cada alvo
def check_connection(target):
    process = subprocess.check_output(f'adb connect {target} ', shell=True)
    date = datetime.datetime.now()

    if "cannot connect" in process.decode('utf-8'):
       logger.info(f" - Dispositivo  nao vulneravel: {target}\n")
    else:
        logger.info(f" - Dispositivo Vulneravel\n")

        # Adicionando alvo a lista
        targets.append(target)

        # Salvando alvos
        print (f"[!] Debug: {date} - Dispositivo  vulneravel salvo em targets.txt: {target}\n")
        file_name = 'targets.txt'
        save_line(file_name, target)

        # Desconectando o dispositivo para testar o proximo
        check = subprocess.check_output(f'adb disconnect {target}', shell=True)
        result = check.decode('utf-8')
        logger.error(f" - {result}\n")

    # Exibe a quantidade de alvos falhos salvos . 
    logger.info(f"{len(targets)} dispositivos vulneraveis e salvos.")
    # Aguarda 4 segundos para limpar a tela e voltar ao menu.
    sleep(5)
    os.system('cls')
# --------------------------------------------------------


# --------------------------------------------------------
# Insira sua chave de API do Shodan
# Alvo teste
# 138.204.63.130
API_KEY = "15hlnqlCHZTxvko4O5mJKM51AhyOLCSZ"

def search_targets():
    date = datetime.datetime.now()
    # Cria uma instância da classe API do Shodan
    api = shodan.Shodan(API_KEY)

    try:
        # Realiza a consulta no shoda usando dork par "ADB"
        # Filtro por pais Exp:  country:"BR"
        query = '"Android Debug Bridge" "Device" port:5555 country:"BR"'
        results = api.search(query)

        # Exibe os resultados
        print('Resultados encontrados:', results['total'])
        for result in results['matches']:
            target = result['ip_str']
            print(f"[*] Debug: {date} - Testando: {target} ...\n")
            # Checa alvo por alvo 
            check_connection(target)

    except shodan.APIError as e:
       logger.info(f" Erro: {e}\n")
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


# Funçao principal
def main():
    while True:

        print(colored(f"{banner}\n", "magenta"))

        print(colored(f"{menu}\n", "green"))
        
        command = input(colored(">>", "green"))
        command = int(command)
        if command == 1:
            search_targets()
        if command == 2:
            target = input(colored("Seu Alvo:", "yellow"))
            check_connection(target)
        else:
            print ("[!]Debug: Comando invalido")

if __name__ == '__main__':
    main()

