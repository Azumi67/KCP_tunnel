
# KCP Tunnel Configuration Script
# Author: github.com/Azumi67
# This is for educational use and my own learning, please provide me with feedback if possible
# There maybe some erros , please forgive me as i have worked on it while i was studying.
# This script is designed to simplify the configuration of KCP tunnel.
#
# Tested on: Ubuntu 20, Debian 12
#
# This script comes with no warranties or guarantees. Use it at your own risk.

import urllib.request
import tarfile
import sys
import os
import time
import shutil
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import netifaces as ni
import platform
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')

if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)


def display_progress(total, current):
    width = 40
    percentage = current * 100 // total
    completed = width * current // total
    remaining = width - completed

    print('\r[' + '=' * completed + '>' + ' ' * remaining + '] %d%%' % percentage, end='')
    
def display_error(message):
    print('\u2718 Error: ' + message)
    
def display_notification(message):
    print(f"\033[93m{message}\033[0m")

def display_checkmark(message):
    print("\033[92m\u2714 \033[0m" + message)

def display_loading():
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    delay = 0.1
    duration = 5  

    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in frames:
            print('\r[' + frame + '] Loading...  ', end='')
            time.sleep(delay)
            print('\r[' + frame + ']             ', end='')
            time.sleep(delay)

    
def display_logo2():
    colorama.init()
    logo2 = colorama.Style.BRIGHT + colorama.Fore.GREEN + """
     _____       _     _      
    / ____|     (_)   | |     
   | |  __ _   _ _  __| | ___ 
   | | |_ | | | | |/ _` |/ _ \\
   | |__| | |_| | | (_| |  __/
    \_____|\__,_|_|\__,_|\___|
""" + colorama.Style.RESET_ALL
    print(logo2)
    
def display_logo():
    colorama.init()  
    logo = """ 
\033[1;96m          
                 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⠤⠒⠊⠉⠀⠀⠀⠀⠈⠁⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀\033[1;93m⠀⢀⠔⠉⠀⠀⠀⠀⢀⡠⠤⠐⠒⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⣀⡠⠤⠤⠀⠀⠂⠐\033[1;96m⠀⠠⢤⠎⢑⡭⣽⣳⠶⣖⡶⣤⣖⣬⡽⡭⣥⣄\033[1;93m⠒⠒⠀⠐⠁⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢀⠴⠊⠁⠀⠀⠀⠀⡀⠀\033[1;96m⣠⣴⡶⣿⢏⡿⣝⡳⢧⡻⣟⡻⣞⠿⣾⡽⣳⣯⣳⣞⡻⣦⡀⠀⠀\033[1;93m⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢨⠀⠀⠀⢀⠤⠂⠁\033[1;96m⢠⣾⡟⣧⠿⣝⣮⣽⢺⣝⣳⡽⣎⢷⣫⡟⡵⡿⣵⢫⡷⣾⢷⣭⢻⣦⡄\033[1;93m⠤⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⡄⠀⠀⠓⠂⠀\033[1;96m⣴⣿⢷⡿⣝⣻⣏⡷⣾⣟⡼⣣⢟⣼⣣⢟⣯⢗⣻⣽⣏⡾⡽⣟⣧⠿⡼⣿⣦\033[1;93m⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠇⠀⠀⠀⠀\033[1;96m⣼⣿⢿⣼⡻⣼⡟⣼⣧⢿⣿⣸⡧⠿⠃⢿⣜⣻⢿⣤⣛⣿⢧⣻⢻⢿⡿⢧⣛⣿⣧⠀\033[1;93m⠛⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢸⠁⠀⠀⠀⠀\033[1;96m⣼⣻⡿⣾⣳⡽⣾⣽⡷⣻⣞⢿⣫⠕⣫⣫⣸⢮⣝⡇⠱⣏⣾⣻⡽⣻⣮⣿⣻⡜⣞⡿⣷\033[1;93m⢀⠀⠀⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⣧⠀⠀⠀\033[1;96m⣼⣳⢯⣿⣗⣿⣏⣿⠆⣟⣿⣵⢛⣵⡿⣿⣏⣟⡾⣜⣻⠀⢻⡖⣷⢳⣏⡶⣻⡧⣟⡼⣻⡽⣇\033[1;93m⠁⠢⡀⠠⡀⠑⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠈⢦⠀\033[1;96m⣰⣯⣟⢯⣿⢾⣹⢾⡟⠰⣏⡾⣾⣟⡷⣿⣻⣽⣷⡶⣟⠿⡆⠀⢻⣝⣯⢷⣹⢧⣿⢧⡻⣽⣳⢽⡀\033[1;93m⠀⠈⠀⠈⠂⡼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⢵\033[1;96m⣟⣾⡟⣾⣿⣻⢽⣺⠇⠀⣿⡱⢿⡞⣵⡳⣭⣿⡜⣿⣭⣻⣷⠲⠤⢿⣾⢯⢯⣛⢿⣳⡝⣾⣿⢭⡇⠀\033[1;93m⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠤⠊⠀\033[1;96m⣼⢻⣿⢞⣯⢿⡽⣸⣹⡆⠀⢷⣏⢯⣿⣧⣛⠶⣯⢿⣽⣷⣧⣛⣦⠀⠀⠙⢿⣳⣽⣿⣣⢟⡶⣿⣫⡇⠀⠀\033[1;93m⠀⠰⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⣠⠖⠁⠀⠀⡄\033[1;96m⡿⣯⣷⣻⡽⣞⡟⣿⣿⣟⠉⠈⢯⣗⣻⣕⢯⣛⡞⣯⢮⣷⣭⡚⠓⠋⠀⠀⠀⠈⠉⣿⡽⣎⠷⡏⡷⣷⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠐⣇⠀⠀⢀⠊\033[1;96m⣼⣇⣿⡗⣿⣽⣷⡿⣿⣱⡿⣆⠀⠀⠙⠒⠛⠓⠋⠉⠉⠀⠀⠀\033[1;91m⢠⣴⣯⣶⣶⣤⡀\033[1;96m ⠀⣿⣟⡼⣛⡇⣟⣿⡆\033[1;93m⡀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⢤⠀⠃⠌\033[1;96m⣸⣿⢾⡽⣹⣾⠹⣞⡵⣳⣽⡽⣖⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;91m⣤⣖⣻⣾⣝⢿⡄\033[1;96m ⢸⣯⢳⣏⡿⣏⣾⢧\033[1;93m⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⠀⠈⠀\033[1;96m⡿⣿⣻⡽⣽⣿⢧⠌⠉\033[1;91m⠉⣴⣿⣿⣫⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣛⠿⠿⢟⢙⡄⠙\033[1;96m ⠘⣯⢳⣞⡟⣯⢾⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀\033[1;96m⡿⣿⣿⢵⣫⣿⣆⠁⠂\033[1;91m⣼⡿⢹⣿⡿⠽⠟⢢⠀⠀⠀⠀⠀⠀⠀⢹⠀⢄⢀⠀⡿⠀⠀\033[1;96m ⢰⣯⢷⣺⣏⣯⢻⡽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⢀⠠\033[1;96m⣿⣿⢾⣛⡶⣽⠈⢓⠀\033[1;91m⢻⠁⢸⠇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠑⠠⠤⠔⠂⠀⠀\033[1;96m ⢸⣿⢮⣽⠿⣜⣻⡝⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠑⠊⠁\033[1;96m⢠⡷⡇⣿⣿⢼⣹⡀⠀⠑⢄⠀\033[1;91m⠀⠃⠌⣁⠦⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀\033[1;96m⢀⣿⢾⡝⣾⡽⣺⢽⣹⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢽⣻⡟⣮⣝⡷⢦⣄⣄⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣯⢿⡺⣟⢷⡹⢾⣷⡞⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⡿⣎⢿⡽⣳⢮⣿⣹⣾⣯⡝⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⣀⣴⡟⣿⢧⣏⢷⡟⣮⠝⢿⣹⣯⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⡷⣏⣾⡳⣽⢺⣷⡹⣟⢶⡹⣾⡽⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⣾⢯⣷⡇⣿⢳⣎⢿⡞⣽⢦⣼⡽⣧⢻⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⢾⡷⣭⣿⢳⣭⢻⣷⡻⣜⣻⡵⣻⡼⣿⠾⠫\033[1;96m⣽⣟⣶⣶⣶⠒⠒⠂⠉⠀\033[1;96m⢸⣽⢺⡷⣷⣯⢗⣮⣟⢾⢧⣻⠼⡿⣿⢣⡟⣼⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣝⣾⢳⢧⣟⡳⣎⣿⣿⣱⢏⣾⣽⣳⠟\033[1;92m⠁⠀⡌⠈\033[1;96m⢹⡯⠟⠛⠀⠀⠀⠀⠀⠈\033[1;96m⣷⢻⣼⣽⣿⡾⣼⣏⣾⣻⡜⣯⣷⢿⣟⣼⡳⣞⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢿⡸⣎⠿⣾⡏⣷⣉⣷⣿⢹⣎⡿\033[1;92m⠎⡎⠀⠀⠀⡇⠀⣾⠱⡀⠀⠀⠀⠀⠀⠀⠀⠈⣹⠉⡏⠀\033[1;96m⠹⣾⣏⢹⣶⢹⣶⢿⡾⣿⢶⣿⣸⠾⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⢫⣞⡽⣯⢿⣹⡟⣶⣹⢷⣻\033[1;92m⡷⠊⠀⡜⠀⠀⠀⠀⢱⠀⣿⡀⠈⠢⢀⣀⣀⠠⠄⠒⢈⡏⡰⠀⠀⠀\033[1;96m⠀⣿⡜⣮⢟⡼⣻⡵⣻⣗⠾⣟⣯⢻⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⢣⣟⡾⣽⣯⢳⣿⡹⣖⣿⡳\033[1;92m⠋⠀⠀⡸⠀⠀⠀⠀⠀⢸⠀⢺⢂⠀⠀⠀⠀⠀⠀⠀⢠⡺⡱⠁⠀⠀⠀⠀\033[1;96m⢹⣧⣻⢮⡳⣝⡷⢧⣻⢯⢿⣻⣳⢞⡆⠀⠀⠀
⠀⠀⠀⠀⢀⡾⣽⣣⡿⣼⣏⡿⣼⣳⡯⢷⣹⣯⠇\033[1;92m⠀⠀⢠⠁⠀⠀⠀⠀⠀⠈⡆⠈⢹⡰⠤⡀⠀⠀⠀⢠⡼⢱⠁⠀⠀⠀⠀⠀⠀\033[1;96m⠹⣿⣿⣱⣻⣼⣏⢷⣯⣿⡳⣿⣎⢿⡀⠀⠀
⠀⠀⠀⠀⣾⣽⠷⣿⣵⡿⣼⡟⣭⣷⡟⣿⢯⡏⠀\033[1;92m⠀⠀⠘⠀⠀⠒⠈⢡⠀⠀⢗⢄⠀⠃⠀⠺⢁⢈⠥⠋⣀⠇⠀⠀⠀⠀⠀⠀⡀⠀\033[1;96m⠈⠙⢿⣳⢞⣽⢯⣞⣾⣯⡝⣿⡾⡇⠀⠀\033[1;92mAuthor: github.com/Azumi67  \033[1;96m  ⠀⠀

  \033[96m  ______   \033[1;94m _______  \033[1;92m __    \033[1;93m  _______     \033[1;91m    __      \033[1;96m  _____  ___  
 \033[96m  /    " \  \033[1;94m|   __ "\ \033[1;92m|" \  \033[1;93m  /"      \    \033[1;91m   /""\     \033[1;96m (\"   \|"  \ 
 \033[96m // ____  \ \033[1;94m(. |__) :)\033[1;92m||  |  \033[1;93m|:        |   \033[1;91m  /    \   \033[1;96m  |.\\   \    |
 \033[96m/  /    ) :)\033[1;94m|:  ____/ \033[1;92m|:  |  \033[1;93m|_____/   )   \033[1;91m /' /\  \   \033[1;96m |: \.   \\  |
\033[96m(: (____/ // \033[1;94m(|  /     \033[1;92m|.  | \033[1;93m //       /   \033[1;91m //  __'  \  \033[1;96m |.  \    \ |
 \033[96m\        / \033[1;94m/|__/ \   \033[1;92m/\  |\ \033[1;93m |:  __   \  \033[1;91m /   /  \\   \ \033[1;96m |    \    \|
 \033[96m \"_____ / \033[1;94m(_______) \033[1;92m(__\_|_)\033[1;93m |__|  \___) \033[1;91m(___/    \___) \033[1;96m\___|\____\)
"""
    print(logo)
def main_menu():
    try:
        while True:
            display_logo()
            border = "\033[93m+" + "="*70 + "+\033[0m"
            content = "\033[93m║            ▌║█║▌│║▌│║▌║▌█║ \033[92mMain Menu\033[93m  ▌│║▌║▌│║║▌█║▌                  ║"
            footer = " \033[92m            Join Opiran Telegram \033[34m@https://t.me/OPIranClub\033[0m "

            border_length = len(border) - 2
            centered_content = content.center(border_length)

            print(border)
            print(centered_content)
            print(border)

            print(border)
            print(footer)
            print(border)
            print("0. \033[91mSTATUS Menu\033[0m")
            print("1. \033[93mKCP Tunnel \033[92mTCP\033[93m  Single\033[0m")
            print("2. \033[96mKCP Tunnel \033[92mICMP\033[96m Single\033[0m")
            print("3. \033[93mKCP Tunnel \033[92mTCP\033[93m  [5] Configs\033[0m")
            print("4. \033[96mKCP Tunnel \033[92mICMP\033[96m [5] Configs\033[0m")
            print("5. \033[93mKCP Tunnel \033[92mTCP\033[93m  Private IP\033[0m")
            print("6. \033[92mStop | Restart Service\033[0m")
            print("7. \033[91mUninstall\033[0m")
            print("q. Exit")
            print("\033[93m╰─────────────────────────────────────────────────────────────────────╯\033[0m")

            choice = input("\033[5mEnter your choice Please: \033[0m")
            print("choice:", choice)
            if choice == '0':
                start_menu()
            elif choice == '1':
                kcp_s_menu()
            elif choice == '2':
                kcp_s2_menu()
            elif choice == '3':
                kcp_m_menu()
            elif choice == '4':
                kcp_m2_menu()
            elif choice == '5':
                kcp_p_menu()
            elif choice == '6':
                restart_azumi()
            elif choice == '7':
                remove_menu()
            elif choice == 'q':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        display_error("\033[91m\nProgram interrupted. Exiting...\033[0m")
        sys.exit()

def restart_azumi():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICES \033[0m')
    print('2. \033[93mStop SERVICES \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_servv()
            break
        elif server_type == '2':
            stop_servv()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
         
def restart_servv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Restart SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mSingle Config\033[0m')
    print('2. \033[93mMulti Config \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart1()
            break
        elif server_type == '2':
            restart2()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def restart1():
    os.system("clear")
    display_notification("\033[93mRestarting...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)

        service_name = "kcpkharej"
        subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        service_name = "kcpiran"
        subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)
		
def restart2():
    os.system("clear")
    display_notification("\033[93mRestarting \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kcpkharej{i}"
			

            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"kcpiran{i}"
            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def stop_servv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Stop SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mSingle Config\033[0m')
    print('2. \033[93mMulti Config \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            stop1()
            break
        elif server_type == '2':
            stop2()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')   

def stop1():
    os.system("clear")
    display_notification("\033[93mStopping...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)

        service_name = "kcpkharej"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        service_name = "kcpiran"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mSevice Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)

def stop2():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Stop Multi SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mService 1\033[0m')
    print('2. \033[92mService 2\033[0m')
    print('3. \033[92mService 3\033[0m')
    print('4. \033[92mService 4\033[0m')
    print('5. \033[93mService 5 \033[0m')
    print('0. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            stopp1()
            break
        elif server_type == '2':
            stopp2()
            break
        elif server_type == '2':
            stopp3()
            break
        elif server_type == '2':
            stopp4()
            break
        elif server_type == '2':
            stopp5()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')  
            
def stopp1():
    os.system("clear")
    display_notification("\033[93mStopping...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)

        service_name = "kcpkharej1"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        service_name = "kcpiran1"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)

def stopp2():
    os.system("clear")
    display_notification("\033[93mStopping...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)

        service_name = "kcpkharej2"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        service_name = "kcpiran2"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)

def stopp3():
    os.system("clear")
    display_notification("\033[93mStopping...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)

        service_name = "kcpkharej3"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        service_name = "kcpiran3"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)
        
def stopp4():
    os.system("clear")
    display_notification("\033[93mStopping...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)

        service_name = "kcpkharej4"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        service_name = "kcpiran4"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)

def stopp5():
    os.system("clear")
    display_notification("\033[93mStopping...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)

        service_name = "kcpkharej5"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        service_name = "kcpiran5"
        subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)
       

def add_cron_job():
    file_path = '/etc/private.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
def run_ping():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
 
def run_ping_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v6.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v6.service'])
    
def ping_ipip_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])


def ipip6_tunnel(remote_ip, local_ip):
    file_path = '/etc/ipip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ipip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumip mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:0db8:1234:a220::1/64 dev azumip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)


    command = f"echo 'ip link set azumip up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    subprocess.run(f"bash {file_path}", shell=True, check=True)


def ipip_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def create_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip_kharej():
    remote_ip = "fd2d:fc98:b53e:b481::2"
    local_ip = "fd2d:fc98:b53e:b481::1"   
    ipip6_tunnel(remote_ip, local_ip)


    ip_address = "2002:0db8:1234:a220::2" 
    max_pings = 3
    interval = 50
    create_ping_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_ipip_service()

    ipip_cronjob()
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")


def kharej_ipip6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring \033[92mKharej\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd2d:fc98:b53e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd2d:fc98:b53e:b481::1/64 dev azumi\n")

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="fd2d:fc98:b53e:b481::2"

max_pings=3

interval=40

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip_kharej()
    sleep(1)	


def iran_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd2d:fc98:b53e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd2d:fc98:b53e:b481::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    

def iran_ipip_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])


def ipip6_iran_tunnel(remote_ip, local_ip):
    file_path = '/etc/ipip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ipip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumip mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:0db8:1234:a220::2/64 dev azumip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)


    command = f"echo 'ip link set azumip up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    subprocess.run(f"bash {file_path}", shell=True, check=True)


def ipip_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip_iran():
    remote_ip = "fd2d:fc98:b53e:b481::1" 
    local_ip = "fd2d:fc98:b53e:b481::2"   
    ipip6_iran_tunnel(remote_ip, local_ip)


    ip_address = "2002:0db8:1234:a220::1" 
    max_pings = 3
    interval = 60
    iran_ping_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip_service()

    ipip_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

def iran_ipip6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring \033[92mIran\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd2d:fc98:b53e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd2d:fc98:b53e:b481::2/64 dev azumi\n")

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping()


    script_content1 = '''#!/bin/bash


ip_address="fd2d:fc98:b53e:b481::1"

max_pings=3

interval=38

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
def start_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mSingle Service \033[0m')
    print('2. \033[96mMulti Service \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            single_status()
            break
        elif server_type == '2':
            multi_status()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

            
def single_status():
    services = {
        'iran': 'kcpiran.service',
        'kharej': 'kcpkharej.service'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║                 \033[92mKCP Status\033[93m                 ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            status_output = os.popen(f"systemctl is-active {service_name}").read().strip()

            if status_output == "active":
                status = "\033[92m✓ Active     \033[0m"
            else:
                status = "\033[91m✘ Inactive   \033[0m"

            if service == 'iran':
                display_name = '\033[93mIRAN Server   \033[0m'
            elif service == 'kharej':
                display_name = '\033[93mKharej Service\033[0m'
            else:
                display_name = service

            print(f"           \033[93m ║\033[0m    {display_name}:   |    {status:<10}   \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error retrieving status for {service}: {e}")
            continue
          

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")
    
def multi_status():
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

    services = {
        'iran': 'kcpiran',
        'kharej': 'kcpkharej'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║                 \033[92mKCP Status\033[93m                 ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            for i in range(num_configs):
                config_service_name = f"{service_name}{i+1}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                else:
                    status = "\033[91m✘ Inactive   \033[0m"

                if service == 'iran':
                    display_name = '\033[93mIRAN Server   \033[0m'
                elif service == 'kharej':
                    display_name = '\033[93mKharej Server \033[0m'
                else:
                    display_name = service

                print(f"           \033[93m ║\033[0m    {display_name} {i+1}:   |    {status:<10} \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error retrieving status for {service}: {e}")
            continue

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")

def remove_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mUninstall Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mSingle Service \033[0m')
    print('2. \033[96mMulti Service \033[0m')
    print('3. \033[93mRemove PrivateIP + KCP \033[0m')
    print('4. \033[96mRemove Single + ICMP \033[0m')
    print('5. \033[93mRemove Multi  + ICMP \033[0m')
    print('6. \033[92mRemove LIMIT [Optional] \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_single()
            break
        elif server_type == '2':
            remove_multi()
            break
        elif server_type == '3':
            remove_ipip6()
            break
        elif server_type == '4':
            remove_icmp_single()
            break
        elif server_type == '5':
            remove_ipicmp()
            break
        elif server_type == '6':
            rmv_limit()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def reset_icmp():
    try:
        reset_ipv4 = False
        reset_ipv6 = False

        os.system("sysctl -w net.ipv4.icmp_echo_ignore_all=0")
        reset_ipv4 = True

        os.system("sudo sysctl -w net.ipv6.icmp.echo_ignore_all=0")
        reset_ipv6 = True

        if reset_ipv4 or reset_ipv6:
            display_checkmark("\033[92mICMP has been reset to default!\033[0m")
        else:
            display_notification("\033[93mICMP settings have been reset.\033[0m")
    except Exception as e:
        display_error("\033[91mAn error occurred: {}\033[0m".format(str(e)))
		
def disable_icmp_echo():
    try:
        subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        display_checkmark("\033[92mecho disabled..\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"\033[91mError occurred disabling echo:\033[0m {e.stderr.decode().strip()}")		

def install_icmp():
    display_notification("\033[93mInstalling \033[92mIcmptunnel\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_loading()


    ipv4_forward_status = subprocess.run(["sysctl", "-n", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if int(ipv4_forward_status.stdout) != 1:
        subprocess.run(["sysctl", "net.ipv4.ip_forward=1"])


    if os.path.exists("/root/icmptunnel"):
        shutil.rmtree("/root/icmptunnel")

    clone_command = 'git clone https://github.com/jamesbarlow/icmptunnel.git icmptunnel'
    clone_result = os.system(clone_command)
    if clone_result != 0:
        print("Error: Failed to clone Repo.")
        return

    if os.path.exists("/root/icmptunnel"):
        os.chdir("/root/icmptunnel")

        subprocess.run(['sudo', 'apt', 'install', '-y', 'net-tools'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'make'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libssl-dev'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'g++'], capture_output=True, text=True)

        subprocess.run(['make'], capture_output=True, text=True)

        os.chdir("..")
    else:
        display_error("\033[91micmptunnel folder not found !\033[0m")
		

def remove_icmp():
    reset_icmp()
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving icmptunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    try:
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp-iran.sh\" | crontab -", shell=True)
        subprocess.run("ip link set dev tun0 down > /dev/null", shell=True)
        subprocess.run("ip link set dev tun1 down > /dev/null", shell=True)
        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        try:
            lsof_process = subprocess.Popen(["lsof", "-t", "/root/icmptunnel/icmptunnel"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lsof_output, lsof_error = lsof_process.communicate()

            if lsof_output:
                pids = lsof_output.decode().split('\n')[:-1]
                for pid in pids:
                    subprocess.run(["kill", pid])

            subprocess.run(["rm", "-rf", "/root/icmptunnel"])
        except FileNotFoundError:
            print("Error: Directory '/root/icmptunnel' does not exist.")
        except Exception as e:
            print("Error:", e)

        subprocess.run("crontab -l | grep -v \"/bin/bash /etc/icmp.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"/bin/bash /etc/icmp-iran.sh\" | crontab -", shell=True)
        display_checkmark("\033[92mICMPtunnel Uninstallation completed!\033[0m")

        if os.path.isfile("/etc/icmp.sh"):
            os.remove("/etc/icmp.sh")
        if os.path.isfile("/etc/icmp-iran.sh"):
            os.remove("/etc/icmp-iran.sh")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)
		

def rmv_limit():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mUninstall Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_notification("\033[93mRemoving ..\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    ulimit_setting = 'ulimit -n 65535'
    bashrc_path = os.path.expanduser('~/.bashrc')

    with open(bashrc_path, 'r') as f:
        existing_bashrc = f.read()

    if ulimit_setting in existing_bashrc:
        existing_bashrc = existing_bashrc.replace(ulimit_setting, '')

        with open(bashrc_path, 'w') as f:
            f.write(existing_bashrc)

    sysctl_conf_path = '/etc/sysctl.conf'
    sysctl_params = [
        'net.core.rmem_max=26214400',
        'net.core.rmem_default=26214400',
        'net.core.wmem_max=26214400',
        'net.core.wmem_default=26214400',
        'net.core.netdev_max_backlog=2048'
    ]

    with open(sysctl_conf_path, 'r') as f:
        existing_sysctl_conf = f.read()

    params_to_remove = []
    for param in sysctl_params:
        if param in existing_sysctl_conf:
            params_to_remove.append(param)

    if params_to_remove:
        for param in params_to_remove:
            existing_sysctl_conf = existing_sysctl_conf.replace(param, '')

        with open(sysctl_conf_path, 'w') as f:
            f.write(existing_sysctl_conf)

        try:
            subprocess.run(["sudo", "sysctl", "-p"], stderr=subprocess.DEVNULL, check=True)
            display_checkmark("\033[92mLimit removal was Successful!\033[0m")
        except subprocess.CalledProcessError:
            print("\033[91mAn error occurred.\033[0m")
    else:
        display_checkmark("\033[92mNothin was found! moving on..\033[0m")
        
def remove_single():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving KCP Tunnel ..\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    try:
        if os.path.isdir("/root/kcp"):  
            shutil.rmtree("/root/kcp")  

        kcp_services = ["kcpkharej", "kcpiran"]  

        for service_name in kcp_services:
            subprocess.run(f"systemctl disable {service_name}.service > /dev/null 2>&1", shell=True)
            subprocess.run(f"systemctl stop {service_name}.service > /dev/null 2>&1", shell=True)
            subprocess.run(f"rm /etc/systemd/system/{service_name}.service > /dev/null 2>&1", shell=True)
            time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        
        rmve_cron()
        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mKcP Single Uninstallation completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())


def remove_icmp_single():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mKCP + ICMP\033[93m Single ...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        reset_icmp()
        remove_icmp()
        remove_single()

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mKCP + ICMP Uninstallation completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def remove_ipicmp():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mKCP +ICMP\033[93m Multi...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        reset_icmp()
        remove_icmp()
        remove_multi()
        rmve_cron()

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mKCP + ICMP Uninstallation completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_ipip6():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mPrivate + KCP\033[93m Multi ...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/ipip.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip.sh", shell=True)
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        sleep(1)
        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumip down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)
        remove_multi()
        rmve_cron()

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mPrivateIP + KCP Uninstallation completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_multi2():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving KCP Tunnel ..\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    try:
        if os.path.isdir("/root/kcp"):  
            shutil.rmtree("/root/kcp") 

        kcp_services = ["kcpkharej", "kcpiran"]  

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

        for service_name in kcp_services:
            for i in range(1, num_configs + 1):
                service_name_with_num = f"{service_name}{i}"
                subprocess.run(f"systemctl disable {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_with_num}.service > /dev/null 2>&1", shell=True)
                time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_multi():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving KCP Tunnel ..\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    try:
        if os.path.isdir("/root/kcp"):  
            shutil.rmtree("/root/kcp") 

        kcp_services = ["kcpkharej", "kcpiran"]  

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

        for service_name in kcp_services:
            for i in range(1, num_configs + 1):
                service_name_with_num = f"{service_name}{i}"
                subprocess.run(f"systemctl disable {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_with_num}.service > /dev/null 2>&1", shell=True)
                time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mKCP Multi Uninstallation completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    
def up_up():
    clear_c()
    ulimit_setting = 'ulimit -n 65535'
    bashrc_path = os.path.expanduser('~/.bashrc')

    with open(bashrc_path, 'r') as f:
        existing_bashrc = f.read()

    if ulimit_setting not in existing_bashrc:
        with open(bashrc_path, 'a') as f:
            f.write('\n')
            f.write(ulimit_setting)
            f.write('\n')

    sysctl_conf_path = '/etc/sysctl.conf'
    sysctl_params = [
        'net.core.rmem_max=26214400',
        'net.core.rmem_default=26214400',
        'net.core.wmem_max=26214400',
        'net.core.wmem_default=26214400',
        'net.core.netdev_max_backlog=2048'
    ]

    with open(sysctl_conf_path, 'r') as f:
        existing_sysctl_conf = f.read()

    params_to_add = []
    for param in sysctl_params:
        if param not in existing_sysctl_conf:
            params_to_add.append(param)

    if params_to_add:
        with open(sysctl_conf_path, 'a') as f:
            f.write('\n')
            f.write('\n'.join(params_to_add))
            f.write('\n')
        try:
            subprocess.run(["sudo", "sysctl", "-p"], stderr=subprocess.DEVNULL, check=True)
            display_checkmark("\033[92mLimit has been Set!\033[0m")
        except subprocess.CalledProcessError:
            print("\033[91mAn error occurred setting it up.\033[0m")
    else:
        display_checkmark("\033[92mLimit Increase was already Done.\033[0m")

def clear_c():
    script_path = '/etc/clear.sh'
    command = 'sync; echo 1 > /proc/sys/vm/drop_caches'
    script_content = f'#!/bin/sh\n{command}'

    with open(script_path, 'w') as f:
        f.write(script_content)

    cron_command = f'0 */2 * * * sh {script_path}'
    os.system(f'(crontab -l | grep -v "{script_path}") | crontab -')
    os.system(f'(crontab -l 2>/dev/null; echo "{cron_command}") | crontab -')
    
def rmve_cron():

    entries_to_remove = [
        f"0 */2 * * * sh /etc/clear.sh",
        "0 */1 * * * /etc/kcp.sh",
        "0 */2 * * * /etc/kcp.sh",
        "0 */3 * * * /etc/kcp.sh",
        "0 */4 * * * /etc/kcp.sh",
        "0 */5 * * * /etc/kcp.sh",
        "0 */6 * * * /etc/kcp.sh",
        "0 */7 * * * /etc/kcp.sh",
        "0 */8 * * * /etc/kcp.sh",
        "0 */9 * * * /etc/kcp.sh",
        "0 */10 * * * /etc/kcp.sh",
        "0 */11 * * * /etc/kcp.sh",
        "0 */12 * * * /etc/kcp.sh",
        "0 */13 * * * /etc/kcp.sh",
        "0 */14 * * * /etc/kcp.sh",
        "0 */15 * * * /etc/kcp.sh",
        "0 */16 * * * /etc/kcp.sh",
        "0 */17 * * * /etc/kcp.sh",
        "0 */18 * * * /etc/kcp.sh",
        "0 */19 * * * /etc/kcp.sh",
        "0 */20 * * * /etc/kcp.sh",
        "0 */21 * * * /etc/kcp.sh",
        "0 */22 * * * /etc/kcp.sh",
        "0 */23 * * * /etc/kcp.sh",
        "0 */24 * * * /etc/kcp.sh"
    ]

    if subprocess.call("test -f /etc/kcp.sh", shell=True) == 0:
        subprocess.call("rm /etc/kcp.sh", shell=True)

    if subprocess.call("test -f /etc/clear.sh", shell=True) == 0:
        subprocess.call("rm /etc/clear.sh", shell=True)

    existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    modified_crontab = existing_crontab

    for entry in entries_to_remove:
        if entry in modified_crontab:
            modified_crontab = modified_crontab.replace(entry, "")

    if modified_crontab != existing_crontab:
        subprocess.call(f"echo '{modified_crontab}' | crontab -", shell=True)
        display_checkmark("\033[92mCache Clear Removed!\033[0m")
    else:
        print("\033[91m\nCron doesn't exist..\033[0m")

def delete_cron():
    entries_to_delete = [
        "0 */1 * * * /etc/kcp.sh",
        "0 */2 * * * /etc/kcp.sh",
        "0 */3 * * * /etc/kcp.sh",
        "0 */4 * * * /etc/kcp.sh",
        "0 */5 * * * /etc/kcp.sh",
        "0 */6 * * * /etc/kcp.sh",
        "0 */7 * * * /etc/kcp.sh",
        "0 */8 * * * /etc/kcp.sh",
        "0 */9 * * * /etc/kcp.sh",
        "0 */10 * * * /etc/kcp.sh",
        "0 */11 * * * /etc/kcp.sh",
        "0 */12 * * * /etc/kcp.sh",
        "0 */13 * * * /etc/kcp.sh",
        "0 */14 * * * /etc/kcp.sh",
        "0 */15 * * * /etc/kcp.sh",
        "0 */16 * * * /etc/kcp.sh",
        "0 */17 * * * /etc/kcp.sh",
        "0 */18 * * * /etc/kcp.sh",
        "0 */19 * * * /etc/kcp.sh",
        "0 */20 * * * /etc/kcp.sh",
        "0 */21 * * * /etc/kcp.sh",
        "0 */22 * * * /etc/kcp.sh",
        "0 */23 * * * /etc/kcp.sh",
        "0 */24 * * * /etc/kcp.sh"
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        display_error("\033[91mNothing Found, moving on..!\033[0m")
        
def res_kcp_im():
    delete_cron()
    if subprocess.call("test -f /etc/kcp.sh", shell=True) == 0:
        subprocess.call("rm /etc/kcp.sh", shell=True)

    with open("/etc/kcp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("systemctl restart kcpiran1\n")
        f.write("systemctl restart kcpiran2\n")
        f.write("systemctl restart kcpiran3\n")
        f.write("systemctl restart kcpiran4\n")
        f.write("systemctl restart kcpiran5\n")

    subprocess.call("chmod +x /etc/kcp.sh", shell=True)
    print("\033[93m╭──────────────────────────────────────╮\033[0m")
    hours = input("\033[93mEnter the \033[92mReset timer:\033[0m ")
    cron_entry = f"0 */{hours} * * * /etc/kcp.sh"
    existing_crontab = ""
    print("\033[93m╰──────────────────────────────────────╯\033[0m")
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")

    if cron_entry in existing_crontab:
        display_error("\033[91mCron already exists!\033[0m")
    else:
        new_crontab = existing_crontab.strip() + f"\n{cron_entry}\n"
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_checkmark(f"\033[92m{hours} hour reset timer added!\033[0m")

    
def res_kcp_km():
    delete_cron()
    if subprocess.call("test -f /etc/kcp.sh", shell=True) == 0:
        subprocess.call("rm /etc/kcp.sh", shell=True)

    with open("/etc/kcp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("systemctl restart kcpkharej1\n")
        f.write("systemctl restart kcpkharej2\n")
        f.write("systemctl restart kcpkharej3\n")
        f.write("systemctl restart kcpkharej4\n")
        f.write("systemctl restart kcpkharej5\n")

    subprocess.call("chmod +x /etc/kcp.sh", shell=True)
    print("\033[93m╭──────────────────────────────────────╮\033[0m")
    hours = input("\033[93mEnter the \033[92mReset timer:\033[0m ")
    cron_entry = f"0 */{hours} * * * /etc/kcp.sh"
    existing_crontab = ""
    print("\033[93m╰──────────────────────────────────────╯\033[0m")
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")

    if cron_entry in existing_crontab:
        display_error("\033[91mCron already exists!\033[0m")
    else:
        new_crontab = existing_crontab.strip() + f"\n{cron_entry}\n"
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_checkmark(f"\033[92m{hours} hour reset timer added!\033[0m")

    
def res_kcp_i():
    delete_cron()
    if subprocess.call("test -f /etc/kcp.sh", shell=True) == 0:
        subprocess.call("rm /etc/kcp.sh", shell=True)

    with open("/etc/kcp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("systemctl restart kcpiran\n")

    subprocess.call("chmod +x /etc/kcp.sh", shell=True)
    print("\033[93m╭──────────────────────────────────────╮\033[0m")
    hours = input("\033[93mEnter the \033[92mReset timer:\033[0m ")
    cron_entry = f"0 */{hours} * * * /etc/kcp.sh"
    existing_crontab = ""
    print("\033[93m╰──────────────────────────────────────╯\033[0m")
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")

    if cron_entry in existing_crontab:
        display_error("\033[91mCron already exists!\033[0m")
    else:
        new_crontab = existing_crontab.strip() + f"\n{cron_entry}\n"
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_checkmark(f"\033[92m{hours} hour reset timer added!\033[0m")

    
def res_kcp_k():
    delete_cron()
    if subprocess.call("test -f /etc/kcp.sh", shell=True) == 0:
        subprocess.call("rm /etc/kcp.sh", shell=True)

    with open("/etc/kcp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("systemctl restart kcpkharej\n")


    subprocess.call("chmod +x /etc/kcp.sh", shell=True)
    print("\033[93m╭──────────────────────────────────────╮\033[0m")
    hours = input("\033[93mEnter the \033[92mReset timer:\033[0m ")
    cron_entry = f"0 */{hours} * * * /etc/kcp.sh"
    existing_crontab = ""
    print("\033[93m╰──────────────────────────────────────╯\033[0m")
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")

    if cron_entry in existing_crontab:
        display_error("\033[91mCron already exists!\033[0m")
    else:
        new_crontab = existing_crontab.strip() + f"\n{cron_entry}\n"
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_checkmark(f"\033[92m{hours} hour reset timer added!\033[0m")

    
def kcp_s_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKCP Tunnel\033[92m TCP \033[96mSingle\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_s()
            break
        elif server_type == '2':
            iran_s()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')

def kcp_s2_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKCP Tunnel\033[92m ICMP \033[96mSingle\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            khareju_s()
            break
        elif server_type == '2':
            iranu_s()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')

def kcp_m_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKCP Tunnel\033[92m TCP \033[96mMulti\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_m()
            break
        elif server_type == '2':
            iran_m()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')   
                       

def kcp_p_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKCP Tunnel\033[92m TCP \033[96mPrivateIP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_pm()
            break
        elif server_type == '2':
            iran_pm()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')   
            
def kcp_m2_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKCP Tunnel\033[92m ICMP\033[93m Multi Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            khareju_m()
            break
        elif server_type == '2':
            iranu_m()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')   
            
download_urls = {
    'amd64': 'https://github.com/xtaci/kcptun/releases/download/v20231012/kcptun-linux-amd64-20231012.tar.gz',
    'arm64': 'https://github.com/xtaci/kcptun/releases/download/v20231012/kcptun-linux-arm64-20231012.tar.gz'
}

file_names = {
    'amd64': 'kcptun-linux-amd64-20231012.tar.gz',
    'arm64': 'kcptun-linux-arm64-20231012.tar.gz'
}

extract_dirs = {
    'amd64': 'kcp',
    'arm64': 'kcp'
}

renamed_files = {
    'server': {
        'amd64': 'server_linux_amd64',
        'arm64': 'server_linux_arm64'
    },
    'client': {
        'amd64': 'client_linux_amd64',
        'arm64': 'client_linux_arm64'
    }
}

def cpu_arch():
    machine = platform.machine()
    if machine == 'x86_64':
        return 'amd64'
    elif machine == 'aarch64':
        return 'arm64'
    else:
        error_message = f"\033[91mUnsupported CPU architecture: {machine}\033[0m"
        raise ValueError(error_message)

def downl():
    try:
        arch = cpu_arch()
        
        url = download_urls[arch]
        file_name = file_names[arch]
        display_notification(f"Downloading KCP ..")
        urllib.request.urlretrieve(url, file_name)
        subprocess.run(['wget', '--quiet', '--show-progress', '-O', file_name, url])
        extract_dir = extract_dirs[arch]
        with tarfile.open(file_name, 'r:gz') as tar:
            tar.extractall(extract_dir)

        for target, source in renamed_files.items():
            source_file = os.path.join(extract_dir, source[arch])
            target_file = os.path.join(extract_dir, target)
            os.rename(source_file, target_file)
            
        os.remove(file_name)
        
        display_checkmark("\033[92mKCPtun Downloaded!\033[0m")
    except ValueError as e:
        display_error(f"Error: {str(e)}")

def get_ipv4():
    interfaces = ni.interfaces()
    for interface in interfaces:
        if interface.startswith('eth') or interface.startswith('en'):
            try:
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    ipv4 = addresses[ni.AF_INET][0]['addr']
                    return ipv4
            except KeyError:
                pass
    return None
    
def kcpk_service(command, key, restart_time="5"):
    service_file_path = "/etc/systemd/system/kcpkharej.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCP Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n")    
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call("systemctl enable kcpkharej", shell=True)
    subprocess.call("systemctl restart kcpkharej", shell=True)

    display_checkmark(f"\033[92mKHAREJ service created successfully\033[0m")

def kharej_s():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej \033[92mTCP \033[93mSingle Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    forward()
    if not os.path.isdir("/root/kcp"):
        downl()
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    kharej_ipv6 = input("\033[93mEnter the \033[92mKharej IPv6\033[93m address:\033[0m ")
    config_port = input("\033[93mEnter \033[96mKharej \033[92mConfig port\033[93m: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443 OR 300-400): \033[0m") or "443"
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    key = "381aa2ab019f563753fefa72bf0d8253"
    
    command = f"/root/kcp/./server -t \"[{kharej_ipv6}]:{config_port}\" -l \":{tunnel_port}\" --rcvwnd 4048 --sndwnd 4048 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"
    
    kcpk_service(command, key)
    up_up()
    res_kcp_k()
    display_checkmark("\033[92mConfig Completed!\033[0m")

def kcpi_service(command, key, restart_time="5"):
    service_file_path = "/etc/systemd/system/kcpiran.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCP Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n") 
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call("systemctl enable kcpiran", shell=True)
    subprocess.call("systemctl restart kcpiran", shell=True)
    display_checkmark(f"\033[92mIRAN service created successfully\033[0m")
    
def iran_s():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN \033[92mTCP\033[93m Single Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    forward()
    if not os.path.isdir("/root/kcp"):
        downl()
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    kharej_ipv6 = input("\033[93mEnter the \033[92mKharej IPv6\033[93m address:\033[0m ")
    config_port = input("\033[93mEnter \033[96mKharej \033[92mConfig port\033[93m: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443 OR 300-400): \033[0m") or "443"
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    key = "381aa2ab019f563753fefa72bf0d8253"
    
    command = f"/root/kcp/./client -r \"[{kharej_ipv6}]:{tunnel_port}\" -l \":{config_port}\" --rcvwnd 2048 --sndwnd 1024 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304  --mode fast3 --crypt aes --quiet --log 0 --autoexpire 900 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"

    kcpi_service(command, key)
    up_up()
    res_kcp_i()
    display_checkmark("\033[92mConfig Completed!\033[0m")
    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

def kcpku_service(command, key, restart_time="5"):
    service_file_path = "/etc/systemd/system/kcpkharej.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCP Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n") 
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call("systemctl enable kcpkharej", shell=True)
    subprocess.call("systemctl restart kcpkharej", shell=True)

    display_checkmark(f"\033[92mKHAREJ service created successfully\033[0m")

def khareju_s():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej \033[92mICMP + KCP\033[93m Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    start_ic_kharej()
    if not os.path.isdir("/root/kcp"):
        downl()
    print('\033[93m══════════════════════════════════════════\033[0m')
    config_port = input("\033[93mEnter \033[96mKharej \033[92mConfig port\033[93m: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443 OR 300-400): \033[0m") or "443"
    
    key = "381aa2ab019f563753fefa72bf0d8253"
    
    command = f"/root/kcp/./server -t \"70.0.0.1:{config_port}\" -l \":{tunnel_port}\" --rcvwnd 4048 --sndwnd 4048 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"
    
    kcpku_service(command, key)
    up_up()
    res_kcp_k()
    display_checkmark("\033[92mConfig Completed!\033[0m")

def kcpiu_service(command, key, restart_time="5"):
    service_file_path = "/etc/systemd/system/kcpiran.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCP Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n") 
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call("systemctl enable kcpiran", shell=True)
    subprocess.call("systemctl restart kcpiran", shell=True)
    display_checkmark(f"\033[92mIRAN service created successfully\033[0m")
    
def iranu_s():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN \033[92mICMP + KCP\033[93m Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    
    if not os.path.isdir("/root/kcp"):
        try:
            downl()
        except Exception as e:
            print("Error downloading: ", e)
            return
    
    start_ic_iran()
    print('\033[93m══════════════════════════════════════════\033[0m')
    config_port = input("\033[93mEnter \033[96mKharej \033[92mConfig port\033[93m: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default: 443 OR 300-400): \033[0m") or "443"
    
    key = "381aa2ab019f563753fefa72bf0d8253"
    
    command = f"/root/kcp/./client -r \"70.0.0.1:{tunnel_port}\" -l \":{config_port}\" --rcvwnd 2048 --sndwnd 1024 --conn 7 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304  --mode fast3 --crypt aes --quiet --log 0 --autoexpire 900 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"

    kcpiu_service(command, key)
    up_up()
    res_kcp_i()
    display_checkmark("\033[92mConfig Completed!\033[0m")
    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        

def service_k_multi(command, service_file_name, restart_time="5"):
    service_file_path = f"/etc/systemd/system/{service_file_name}.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCPi Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n") 
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call(f"systemctl enable {service_file_name}", shell=True)
    subprocess.call(f"systemctl restart {service_file_name}", shell=True)

    display_checkmark(f"\033[92mService file '{service_file_path}' created successfully\033[0m")

def kharej_m():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej \033[92mTCP\033[93m Multi Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    forward()
    if not os.path.isdir("/root/kcp"):
        downl()
    print('\033[93m══════════════════════════════════════════\033[0m')
    num_configs = int(input('\033[93mEnter the \033[96mnumber \033[93mof \033[92mconfigs\033[93m you want (\033[91mmax 5\033[93m): \033[0m'))
    num_configs = min(num_configs, 5)
    print('\033[93m══════════════════════════════════════════\033[0m')
    
    key_base = "381aa2ab019f563753fefa72bf0d82"
    
    for i in range(num_configs):
        print("\033[93m──────────────────────\033[0m")
        print(f"\033[96m       Config {i+1}\033[0m")
        print("\033[93m──────────────────────\033[0m")
        kharej_ipv6 = input('\033[93mEnter \033[92mKharej IPv6\033[93m address: \033[0m')
        config_port = input('\033[93mEnter \033[92mKharej Config port\033[93m: \033[0m')
        tunnel_port = input('\033[93mEnter \033[92mTunnel Port\033[93m for this config \033[96m[Single or Port Range]\033[93m: \033[0m')
        key = key_base + str(i)
        
        command = f"/root/kcp/./server -t \"[{kharej_ipv6}]:{config_port}\" -l \":{tunnel_port}\" --rcvwnd 4048 --sndwnd 4048 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"
        
        service_file_name = f"kcpkharej{i+1}"
        service_k_multi(command, service_file_name)
        print("\033[93m──────────────────────────\033[0m")
        print(f"\033[92mConfig {i+1} created successfully.\033[0m")
        print("\033[93m──────────────────────────\033[0m")
        print()
    up_up()
    res_kcp_km()
    display_checkmark("\033[92mConfigs Completed!\033[0m")
   
def service_i_multi(command, service_file_name, restart_time="5"):
    service_file_path = f"/etc/systemd/system/{service_file_name}.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCPi Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n") 
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call(f"systemctl enable {service_file_name}", shell=True)
    subprocess.call(f"systemctl restart {service_file_name}", shell=True)

    display_checkmark(f"\033[92mService file '{service_file_path}' created successfully\033[0m")

def iran_m():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN \033[92mTCP\033[93m Multi Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    forward()
    if not os.path.isdir("/root/kcp"):
        try:
            downl()
        except Exception as e:
            print("Error downloading:", e)
            return
    print('\033[93m══════════════════════════════════════════\033[0m')
    num_configs = int(input('\033[93mEnter the \033[96mnumber \033[93mof \033[92mconfigs\033[93m you want (\033[91mmax 5\033[93m): \033[0m'))
    num_configs = min(num_configs, 5)
    print('\033[93m══════════════════════════════════════════\033[0m')
    
    key_base = "381aa2ab019f563753fefa72bf0d82"

    for i in range(num_configs):
        print("\033[93m──────────────────────\033[0m")
        print(f"\033[96m       Config {i+1}\033[0m")
        print("\033[93m──────────────────────\033[0m")
        kharej_ipv6 = input('\033[93mEnter \033[92mKharej IPv6\033[93m address: \033[0m')
        config_port = input('\033[93mEnter \033[92mKharej Config port\033[93m: \033[0m')
        tunnel_port = input('\033[93mEnter \033[92mTunnel Port\033[93m for this config \033[96m[Single or Port Range]\033[93m: \033[0m')
        key = key_base + str(i)
        
        command = f"/root/kcp/./client -r \"[{kharej_ipv6}]:{tunnel_port}\" -l \":{config_port}\" --rcvwnd 2048 --sndwnd 1024 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --autoexpire 900 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"

        service_file_name = f"kcpiran{i+1}"
        service_i_multi(command, service_file_name)
        print("\033[93m──────────────────────────\033[0m")
        print(f"\033[92mConfig {i+1} created successfully.\033[0m")
        print("\033[93m──────────────────────────\033[0m")
        print()

        current_ipv4 = get_ipv4()
        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            print(f"\033[93m| Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    up_up()
    res_kcp_im()
    display_checkmark("\033[92mConfigs Completed!\033[0m")
   
def khareju_m():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej \033[92mICMP + KCP\033[93m Multi Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    start_ic_kharej()
    if not os.path.isdir("/root/kcp"):
        downl()
    print('\033[93m══════════════════════════════════════════\033[0m')
    num_configs = int(input('\033[93mEnter the \033[96mnumber \033[93mof \033[92mconfigs\033[93m you want (\033[91mmax 5\033[93m): \033[0m'))
    num_configs = min(num_configs, 5)
    print('\033[93m══════════════════════════════════════════\033[0m')
    
    key_base = "381aa2ab019f563753fefa72bf0d82"
    
    for i in range(num_configs):
        print("\033[93m──────────────────────\033[0m")
        print(f"\033[96m       Config {i+1}\033[0m")
        print("\033[93m──────────────────────\033[0m")
        config_port = input('\033[93mEnter \033[92mKharej Config port\033[93m: \033[0m')
        tunnel_port = input('\033[93mEnter \033[92mTunnel Port\033[93m for this config \033[96m[Single or Port Range]\033[93m: \033[0m')
        key = key_base + str(i)
        
        command = f"/root/kcp/./server -t \"70.0.0.1:{config_port}\" -l \":{tunnel_port}\" --rcvwnd 4048 --sndwnd 4048 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"
        
        service_file_name = f"kcpkharej{i+1}"
        service_k_multi(command, service_file_name)
        print("\033[93m──────────────────────────\033[0m")
        print(f"\033[92mConfig {i+1} created successfully.\033[0m")
        print("\033[93m──────────────────────────\033[0m")
        print()
    up_up()
    res_kcp_km()
    display_checkmark("\033[92mConfigs Completed!\033[0m")
   
def iranu_m():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN \033[92mICMP + KCP\033[93m Multi Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    if not os.path.isdir("/root/kcp"):
        try:
            downl()
        except Exception as e:
            print("Error downloading: ", e)
            return
    start_ic_iran()
    print('\033[93m══════════════════════════════════════════\033[0m')
    num_configs = int(input('\033[93mEnter the \033[96mnumber \033[93mof \033[92mconfigs\033[93m you want (\033[91mmax 5\033[93m): \033[0m'))
    num_configs = min(num_configs, 5)
    print('\033[93m══════════════════════════════════════════\033[0m')
    
    key_base = "381aa2ab019f563753fefa72bf0d82"
    
    for i in range(num_configs):
        print("\033[93m──────────────────────\033[0m")
        print(f"\033[96m       Config {i+1}\033[0m")
        print("\033[93m──────────────────────\033[0m")
        config_port = input('\033[93mEnter \033[92mKharej Config port\033[93m: \033[0m')
        tunnel_port = input('\033[93mEnter \033[92mTunnel Port\033[93m for this config \033[96m[Single or Port Range]\033[93m: \033[0m')
        key = key_base + str(i)
        
        command = f"/root/kcp/./client -r \"70.0.0.1:{tunnel_port}\" -l \":{config_port}\" --conn 7 --rcvwnd 2048 --sndwnd 1024 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --autoexpire 900 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"
       

        service_file_name = f"kcpiran{i+1}"
        service_i_multi(command, service_file_name)
        print("\033[93m──────────────────────────\033[0m")
        print(f"\033[92mConfig {i+1} created successfully.\033[0m")
        print("\033[93m──────────────────────────\033[0m")
        print()
        current_ipv4 = get_ipv4()
        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            print(f"\033[93m| Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    up_up()
    res_kcp_im()
    display_checkmark("\033[92mConfigs Completed!\033[0m")
    

def service_pk_multi(command, service_file_name, restart_time="5"):
    service_file_path = f"/etc/systemd/system/{service_file_name}.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCPi Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n") 
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call(f"systemctl enable {service_file_name}", shell=True)
    subprocess.call(f"systemctl restart {service_file_name}", shell=True)

    display_checkmark(f"\033[92mService file '{service_file_path}' created successfully\033[0m")

def kharej_pm():
    kharej_ipip6_menu()
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej \033[92mTCP + Private\033[93m Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    forward()
    if not os.path.isdir("/root/kcp"):
        downl()
    print('\033[93m══════════════════════════════════════════\033[0m')
    num_configs = int(input('\033[93mEnter the \033[96mnumber \033[93mof \033[92mconfigs\033[93m you want (\033[91mmax 5\033[93m): \033[0m'))
    num_configs = min(num_configs, 5)
    print('\033[93m══════════════════════════════════════════\033[0m')
    
    key_base = "381aa2ab019f563753fefa72bf0d82"
    
    for i in range(num_configs):
        print("\033[93m──────────────────────\033[0m")
        print(f"\033[96m       Config {i+1}\033[0m")
        print("\033[93m──────────────────────\033[0m")
        config_port = input('\033[93mEnter \033[92mKharej Config port\033[93m: \033[0m')
        tunnel_port = input('\033[93mEnter \033[92mTunnel Port\033[93m for this config \033[96m[Single or Port Range]\033[93m: \033[0m')
        key = key_base + str(i)
        
        command = f"/root/kcp/./server -t \"[2002:0db8:1234:a220::1]:{config_port}\" -l \":{tunnel_port}\" --rcvwnd 4048 --sndwnd 4048 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"
        
        service_file_name = f"kcpkharej{i+1}"
        service_pk_multi(command, service_file_name)
        print("\033[93m──────────────────────────\033[0m")
        print(f"\033[92mConfig {i+1} created successfully.\033[0m")
        print("\033[93m──────────────────────────\033[0m")
        print()
    up_up()    
    res_kcp_km()    
    display_checkmark("\033[92mConfigs Completed!\033[0m")
   
def service_pi_multi(command, service_file_name, restart_time="5"):
    service_file_path = f"/etc/systemd/system/{service_file_name}.service"
    
    with open(service_file_path, "w") as file:
        file.write("[Unit]\n")
        file.write("Description=Azumi KCPi Service\n")
        file.write("\n")
        file.write("[Service]\n")
        file.write(f"ExecStart={command}\n")
        file.write("Restart=always\n")
        file.write(f"RestartSec={restart_time}\n")
        file.write(f"LimitNOFILE=1048576\n") 
        file.write("\n")
        file.write("[Install]\n")
        file.write("WantedBy=default.target\n")
    subprocess.call("systemctl daemon-reload", shell=True)
    subprocess.call(f"systemctl enable {service_file_name}", shell=True)
    subprocess.call(f"systemctl restart {service_file_name}", shell=True)

    display_checkmark(f"\033[92mService file '{service_file_path}' created successfully\033[0m")

def iran_pm():
    iran_ipip6_menu()
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN \033[92mTCP + Private\033[93m Config\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    forward()
    if not os.path.isdir("/root/kcp"):
        try:
            downl()
        except Exception as e:
            print("Error downloading: ", e)
            return
    print('\033[93m══════════════════════════════════════════\033[0m')
    num_configs = int(input('\033[93mEnter the \033[96mnumber \033[93mof \033[92mconfigs\033[93m you want (\033[91mmax 5\033[93m): \033[0m'))
    num_configs = min(num_configs, 5)
    print('\033[93m══════════════════════════════════════════\033[0m')
    
    key_base = "381aa2ab019f563753fefa72bf0d82"
    
    for i in range(num_configs):
        print("\033[93m──────────────────────\033[0m")
        print(f"\033[96m       Config {i+1}\033[0m")
        print("\033[93m──────────────────────\033[0m")
        config_port = input('\033[93mEnter \033[92mKharej Config port\033[93m: \033[0m')
        tunnel_port = input('\033[93mEnter \033[92mTunnel Port\033[93m for this config \033[96m[Single or Port Range]\033[93m: \033[0m')
        key = key_base + str(i)
        
        command = f"/root/kcp/./client -r \"[2002:0db8:1234:a220::1]:{tunnel_port}\" -l \":{config_port}\" --rcvwnd 2048 --sndwnd 1024 --smuxver 2 --smuxbuf 16777216 --streambuf 4194304 --mode fast3 --crypt aes --quiet --log 0 --autoexpire 900 --sockbuf 16777217 --dscp 46 --key \"{key}\" --tcp"
       

        service_file_name = f"kcpiran{i+1}"
        service_pi_multi(command, service_file_name)
        print("\033[93m──────────────────────────\033[0m")
        print(f"\033[92mConfig {i+1} created successfully.\033[0m")
        print("\033[93m──────────────────────────\033[0m")
        print()
        current_ipv4 = get_ipv4()
        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            print(f"\033[93m| Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    up_up()    
    res_kcp_im()    
    display_checkmark("\033[92mConfigs Completed!\033[0m")
   

    
def start_ic_kharej():
    display_notification("\033[93mConfiguring ICMPtunnel \033[92mKharej\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    ignore()
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()
    
    if os.path.exists("/etc/icmp.sh"):
        os.remove("/etc/icmp.sh")

    with open("/etc/icmp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/root/icmptunnel/icmptunnel -s -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.1 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp.sh\n"
    with open("/etc/cron.d/icmp-kharej", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")

def start_ic_iran():
    display_notification("\033[93mConfiguring ICMPtunnel \033[92mIRAN \033[93m...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    ignore()

    if not os.path.exists("/root/icmptunnel"):
        try:
            install_icmp()
        except Exception as e:
            print("Error downloading: ", e)
            return
            
    os.chdir("/root/icmptunnel")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address:\033[0m ")

    if os.path.exists("/etc/icmp-iran.sh"):
        os.remove("/etc/icmp-iran.sh")

    with open("/etc/icmp-iran.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"/root/icmptunnel/icmptunnel {server_ipv4} -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.2 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp-iran.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp-iran.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp-iran.sh\n"
    with open("/etc/cron.d/icmp-iran", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")

def forward():

    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])  
        
def ignore():
    icmpv4_status = subprocess.run(["sysctl", "net.ipv4.icmp_echo_ignore_all"], capture_output=True, text=True)
    if "net.ipv4.icmp_echo_ignore_all = 1" not in icmpv4_status.stdout:
        subprocess.run(["sudo", "sh", "-c", "echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all"])

    icmpv6_status = subprocess.run(["sysctl", "net.ipv6.icmp.echo_ignore_all"], capture_output=True, text=True)
    if "net.ipv6.icmp.echo_ignore_all = 0" not in icmpv6_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.icmp.echo_ignore_all=1"])

    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])   
        
main_menu()
