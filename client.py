import socket
import string
import dell_system_sudoku
from config import *
import json

def find_whitespace(st):
    for index, character in enumerate(st):
       if character in string.whitespace:
            yield index

def create_client():
    socket_conn = socket.socket()
    socket_conn.connect((HOST, PORT))

    message = input(' -> ')
    whitespace_indices = list(find_whitespace(message))
    message = message.replace(" ", "")
    length = len(message)

    sudoku_coder = dell_system_sudoku.SudokuCoder()
    sudoku_encrypted = sudoku_coder.encode(message)

    while message != 'q':
        data_dict = {"encrypted": str(sudoku_encrypted), "whitespace": whitespace_indices, "length": length}
        serialized_dict = json.dumps(data_dict)
        socket_conn.send(serialized_dict.encode())
        print(f'Client: Sent encrypted message => {sudoku_encrypted}')
        data = socket_conn.recv(1024).decode()
        message = input(' -> ')
        whitespace_indices = list(find_whitespace(message))
        message = message.replace(" ", "")
        length = len(message)
        sudoku_coder = dell_system_sudoku.SudokuCoder()
        sudoku_encrypted = sudoku_coder.encode(message)

    socket_conn.close()


if __name__ == '__main__':
    create_client()
