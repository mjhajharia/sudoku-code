import socket
from rsa import get_decrypted_message
import dell_system_sudoku
from config import *
import json
import string

def start_server():
    mySocket = socket.socket()
    mySocket.bind((HOST, PORT))
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print('Connection from: ' + str(addr))
    while True:
        data = conn.recv(20480).decode()
        if not data:
            break
        a_dict = json.loads(data)
        data = a_dict["encrypted"]
        soduku_solver = dell_system_sudoku.SudokuCoder()
        print('Server: Data sent by client =>' + str(data))
        print('Server: Decrypting message..')

        decrypted_message = soduku_solver.decode(data)[:a_dict["length"]]
        whitespace_indices = a_dict["whitespace"]
        for i in whitespace_indices:
            res = list(decrypted_message)
            res.insert(i, " ")
            res = ''.join(res)
        if len(whitespace_indices)==0:
            res = decrypted_message
        print(f'Server: Message => {res}')
        acknoledgement = 'Message successfully received by Server.'
        print(f'Sending: {acknoledgement}')
        conn.send(acknoledgement.encode())

    conn.close()


if __name__ == '__main__':
    start_server()
