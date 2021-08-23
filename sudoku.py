import numpy as np
import string
import random

def bin16(num):
    binary_number = '{0:b}'.format(int(num))
    binary_number = '0' * (16 - len(binary_number)) + binary_number
    return binary_number

def get_representation(character, row, column):
    idx = string.ascii_uppercase.index(character) + 1
    if 1 <= idx <= 9:
        return '1' + str(row) + str(column)
    elif 10 <= idx <= 18:
        return '2' + str(row) + str(column)
    elif 19 <= idx <= 26:
        return '3' + str(row) + str(column)

def from_representation(sudoku, representation):
    representation = str(representation)
    x = int(representation[0])
    row = int(representation[1]) - 1
    col = int(representation[2]) - 1
    element = sudoku[row, col]
    return string.ascii_uppercase[(x - 1) * 9 + element - 1]


def get_char_idx(character):
    print(character)
    return string.ascii_uppercase.index(character) + 1

def find_coordinate(sudoku, character):
    number = get_char_idx(character) % 9
    if number == 0:
        number = 9
        
    ans = []
    for i in range(9):
        for j in range(9):
            if sudoku[i, j] == number:
                ans.append(get_representation(character, i + 1, j + 1)) 
    return ans

def get_encrypted_character(sudoku, character):
    encryption_scheme = find_coordinate(sudoku, character)
    random_number = random.choice(encryption_scheme)
    binary_random_number = bin16(random_number)
    shifted_random_number = binary_random_number[12:] + binary_random_number[0:12]

    return int(shifted_random_number, 2)

def encrpyt_sudoku(sudoku, message):
    encypted = []
    for character in message:
        encypted.append(get_encrypted_character(sudoku, character))
    return encypted


def decrypt_sudoku(sudoku, encryted_message):
    ans = ''
    for encrpyt_number in encryted_message:
        binary_number = str(bin16(encrpyt_number))
        binary_number = binary_number[4:] + binary_number[:4]
        num = int(binary_number, 2)
        ans += from_representation(sudoku, num)
    return ans



def generate_sudoku(mask_rate=0.5):
    while True:
        n = 9
        m = np.zeros((n, n), np.int)
        rg = np.arange(1, n + 1)
        m[0, :] = np.random.choice(rg, n, replace=False)
        try:
            for r in range(1, n):
                for c in range(n):
                    col_rest = np.setdiff1d(rg, m[:r, c])
                    row_rest = np.setdiff1d(rg, m[r, :c])
                    avb1 = np.intersect1d(col_rest, row_rest)
                    sub_r, sub_c = r//3, c//3
                    avb2 = np.setdiff1d(
                        np.arange(0, n+1), m[sub_r*3:(sub_r+1)*3, sub_c*3:(sub_c+1)*3].ravel())
                    avb = np.intersect1d(avb1, avb2)
                    m[r, c] = np.random.choice(avb, size=1)
            break
        except ValueError:
            pass
    # print("Answer:\n", m)
    mm = m.copy()
    mm[np.random.choice([True, False], size=m.shape, p=[
                        mask_rate, 1 - mask_rate])] = 0
    print("\nMasked anwser:\n", mm)
    np.savetxt("./puzzle.csv", mm, "%d", delimiter=",")
    return mm


def solve(m):
    if isinstance(m, list):
        m = np.array(m)
    elif isinstance(m, str):
        m = np.loadtxt(m, dtype=np.int, delimiter=",")
    rg = np.arange(m.shape[0]+1)
    while True:
        mt = m.copy()
        while True:
            d = []
            d_len = []
            for i in range(m.shape[0]):
                for j in range(m.shape[1]):
                    if mt[i, j] == 0:
                        possibles = np.setdiff1d(rg, np.union1d(np.union1d(
                            mt[i, :], mt[:, j]), mt[3*(i//3):3*(i//3+1), 3*(j//3):3*(j//3+1)]))
                        d.append([i, j, possibles])
                        d_len.append(len(possibles))
            if len(d) == 0:
                break
            idx = np.argmin(d_len)
            i, j, p = d[idx]
            if len(p) > 0:
                num = np.random.choice(p)
            else:
                break
            mt[i, j] = num
            if len(d) == 0:
                break
        if np.all(mt != 0):
            break

    # print("\nTrail:\n", mt)
    return mt


def check_solution(m):
    if isinstance(m, list):
        m = np.array(m)
    elif isinstance(m, str):
        m = np.loadtxt(m, dtype=np.int, delimiter=",")
    set_rg = set(np.arange(1, m.shape[0] + 1))
    no_good = False
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            r1 = set(m[3 * (i // 3):3 * (i // 3 + 1), 3 * (j // 3)
                     :3 * (j // 3 + 1)].ravel()) == set_rg
            r2 = set(m[i, :]) == set_rg
            r3 = set(m[:, j]) == set_rg
            if not (r1 and r2 and r3):
                no_good = True
                break
        if no_good:
            break
    if no_good:
        print("\nChecked: not good")
    else:
        print("\nChecked: OK")

def load_solved_sudoku():
    return np.loadtxt('solved_puzzle.csv', dtype=np.int, delimiter=",")

solved_sudoku = load_solved_sudoku()
# np.savetxt("./solved_puzzle.csv", solve('puzzle.csv'), "%d", delimiter=",")


if __name__ == "__main__":
    encrpyted_message = encrpyt_sudoku(solved_sudoku, 'ANOOP')
    print(encrpyted_message)
    print(decrypt_sudoku(solved_sudoku, encrpyted_message))

    # puzzle = generate_sudoku(mask_rate=0.7)
    # solved = solve('puzzle.csv')
    # encryption = encrpyt_sudoku(solved, 'ANOOP')
    # print(decrypt_sudoku(solved, encryption))
    # print(solved)
    # check_solution(solved)

    # print("\nSolve in code:")
    # solve([
    #     [0, 5, 0, 0, 6, 7, 9, 0, 0],
    #     [0, 2, 0, 0, 0, 8, 4, 0, 0],
    #     [0, 3, 0, 9, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 2, 1, 0, 4],
    #     [0, 0, 0, 6, 0, 9, 0, 0, 0],
    #     [0, 0, 8, 5, 0, 0, 6, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 4, 9, 0, 0, 5, 0],
    #     [2, 1, 3, 7, 0, 0, 0, 0, 0]
    # ])

    # print("\nSolve in csv file:")
    # solve("puzzle.csv")