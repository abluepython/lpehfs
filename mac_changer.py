#!/usr/bin/python3

# This script allow you to change the mac address of
# a linux host who already has installed net-tools.

import subprocess
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface', help="Interface to change it's MAC address.")
    parser.add_argument('-m', '--mac', dest='mac', help='The new MAC address.')
    args = parser.parse_args()

    if not args.interface:
        argparse.error("Please specify an interface, --help for more information.")
    elif not args.mac:
        argparse.error("Please specify a MAC, --help for more information.")

    return args

def mac_changer(interface, mac):
    print(f"[+] Changinc MAC address for {interface} to {mac}.")
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", mac])
    subprocess.run(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode('ISO-8859-1')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Cloud not read MAC address.")


options = get_arguments()
current_mac = get_current_mac(options.interface)

print(f"Current MAC = {str(current_mac)}")

mac_changer(options.interface, options.mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.mac:
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print("[-] MAC address did not get changed.")
