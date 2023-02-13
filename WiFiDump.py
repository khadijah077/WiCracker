# import modules
import subprocess
import re
from colorama import Fore

C = '\033[36m'  # cyan
G = '\033[32m'  # green
W = '\033[0m'   # white


class WifiDump():

    def __init__(self):
        pass

    # this method will run a command to retrieve stored passwords on Windows computer System
    @staticmethod
    def StoredPasswords():
        # run 'netsh wlan show profiles' and  store the profiles data into a variable after decoding the result
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"],
                                        capture_output=True).stdout.decode('cp1252')

        # get lines that only contain "All User Profile"
        profile_names_list = re.findall("All User Profile     : (.*)\r", command_output)

        wifi_list = []
        # looping through all profiles
        if len(profile_names_list) != 0:
            for Pname in profile_names_list:
                wifi_profiles = {}
                profile_info = subprocess.run(
                    ["netsh", "wlan", "show", "profile", Pname], capture_output=True).stdout.decode('cp1252')

                # check the passwords if exists
                if re.search("Security key           : Absent", profile_info):
                    continue

                # if password exists run the command to store the password after decoding it
                else:
                    wifi_profiles["SSID"] = Pname
                    profile_pass = subprocess.run(["netsh", "wlan", "show", "profile", Pname, "key=clear"],
                                                  capture_output=True, ).stdout.decode('cp1252')

                    password = re.search("Key Content            : (.*)\r", profile_pass)
                    if password is None:
                        wifi_profiles["Password"] = None

                    else:
                        wifi_profiles["password"] = password[1]

                    wifi_list.append(wifi_profiles)
        return wifi_list

    @staticmethod
    def printInfo(wifi_List):
        # print the profiles with passwords (output)
        for x in range(len(wifi_List)):
            print(C + ('-' * 15) + 'Network [', (x + 1), ']' + ('-' * 15) + W)

            for i in wifi_List[x]:
                print(G + i, ": " + W, str(wifi_List[x][i]))

        print(f"{Fore.YELLOW}" + '\n*NOTE*: None in password field means >> The wifi has no password '
                                 'or has undefined encoding !' + W + '\n')
