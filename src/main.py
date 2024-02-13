import random
import time
import os
from termcolor import colored

def main_menu():
    print(colored('>>>>>>>=====[ MENU UTAMA ]=====<<<<<<<', 'light_yellow', 'on_white', ['bold']))
    print(colored("1. Masukan via CLI", "red"))
    print(colored("2. Masukan via file (*.txt)", "green"))
    print(colored("3. Exit", "blue"))

    option = int(input("Pilihan (1/2/3): "))
    while option > 3 or option < 1:
        print(colored("Pilihan tersebut tidak ada, pastikan memilih nomor yang tersedia", 'red'))
        option = int(input("Pilihan (1/2/3): "))
    return option

def startscreen():
    ascii_text = '''
    _____          __                                  __          ___   ___  ____ ____     
   / ___/  __ __  / /  ___   ____   ___  __ __  ___   / /__       |_  | / _ \/_  //_  /     
  / /__   / // / / _ \/ -_) / __/  / _ \/ // / / _ \ /  '_/      / __/ / // / / /  / /      
  \___/   \_, / /_.__/\__/ /_/    / .__/\_,_/ /_//_//_/\_\      /____/ \___/ /_/  /_/       
     ___ /___/                   /__         ___              __                   __       
    / _ )  ____ ___  ___ _ ____  / /        / _ \  ____ ___  / /_ ___  ____ ___   / /       
   / _  | / __// -_)/ _ `// __/ / _ \      / ___/ / __// _ \/ __// _ \/ __// _ \ / /        
  /____/ /_/   \__/ \_,_/ \__/ /_//_/     /_/    /_/   \___/\__/ \___/\__/ \___//_/         
                                                                                              
    '''

    colored_ascii_text = colored(ascii_text, color='yellow')
    print(colored_ascii_text)

def gun():
    ascii_text = '''
    +--^----------,--------,-----,--------^-,
     | |||||||||   `--------'     |          O
     `+---------------------------^----------|
       `\_,---------,---------,--------------'
         / XXXXXX /'|       /'
        / XXXXXX /  `\    /'
       / XXXXXX /`-------'
      / XXXXXX /
     / XXXXXX /
    (________(                by
     `------'      Marzuli Suhada M - 13522070
    '''

    colored_ascii_text = colored(ascii_text, color='yellow')
    print(colored_ascii_text)

def generate_random_matrix(kolom_matriks, baris_matriks):
    matrix = []
    for i in range(baris_matriks):
        row = [random.choice(token) for _ in range(kolom_matriks)]
        matrix.append(row)
        colored_row = [colored(symbol, 'yellow') for symbol in row]
        print(" ".join(colored_row))
    return matrix

def generate_random_sequences(jumlah_sequence, ukuran_maksimal_sequence):
    sequences = []
    rewards = []
    for i in range(jumlah_sequence):
        sequence_size = random.randint(2, ukuran_maksimal_sequence)
        reward = random.randint(-100, 100)
        sequence = "".join(random.choice(token) for _ in range(sequence_size))
        sequences.append(sequence)
        rewards.append(reward)
    return sequences, rewards

def sequenceInPath(sequences, currentPath):
    return currentPath in sequences

def possibilities(current_buffer, index, currentPath, currentPosition, seenPath, ukuran_buffer, paths, matrix_size, matrix, position, sequences):
    if current_buffer == ukuran_buffer or sequenceInPath(sequences, currentPath):
        paths.append(currentPath)
        position.append(currentPosition)
        return None
    if current_buffer == 0:
        for i in range(matrix_size[0]):
            possibilities(1, i, matrix[0][i], currentPosition + ([i + 1, 1]), [[i, 0]], ukuran_buffer, paths, matrix_size,
                          matrix, position, sequences)
    elif current_buffer % 2 == 1:
        for j in range(matrix_size[1]):
            seen = False
            for positions in seenPath:
                if positions[0] == index and positions[1] == j:
                    seen = True
                    break
            if seen:
                continue
            seenPath.append([index, j])
            possibilities(current_buffer + 1, j, currentPath + matrix[j][index], currentPosition + ([index + 1, j + 1]),
                          seenPath, ukuran_buffer, paths, matrix_size, matrix, position, sequences)
            seenPath.pop()
    else:
        for i in range(matrix_size[0]):
            seen = False
            for positions in seenPath:
                if positions[1] == index and positions[0] == i:
                    seen = True
                    break
            if seen:
                continue
            seenPath.append([i, index])
            possibilities(current_buffer + 1, i, currentPath + matrix[index][i], currentPosition + ([i + 1, index + 1]),
                          seenPath, ukuran_buffer, paths, matrix_size, matrix, position, sequences)
            seenPath.pop()
    return paths, position

def getReward(paths, sequences, rewards, listOfReward):
    for path in paths:
        reward = 0
        for i in range(len(sequences)):
            if (sequences[i] in path):
                reward += rewards[i]
        listOfReward.append(reward)
    return listOfReward

def getOptimal(listOfReward, paths):
    maximal = 0
    imax = 0
    for i in range(len(paths)):
        if (listOfReward[i] > maximal):
            maximal = listOfReward[i]
            imax = i
        elif listOfReward[i] == maximal:
            if len(paths[i]) < len(paths[imax]):
                maximal = listOfReward[i]
                imax = i
    return maximal, imax

def save_solution(sequences, rewards, maximal, outputBuffer, outputposition, execution_time, matrix, filename):
    folderpath = "/Users/azulsuhada/Documents/Semester4/Stima/Tucil-1-Stima/test/output"  
    filepath = os.path.join(folderpath, filename + ".txt")
    with open(filepath, "w") as file:
        if (option == 1):
            for row in matrix:
                file.write(" ".join(row) + "\n")
            for i in range(len(sequences)):
                outputSequence = ""
                inputSequence = sequences[i]
                for j in range(0, len(sequences[i]), 2):
                    outputSequence += inputSequence[j:j+2] + " "
                outputSequence = outputSequence.rstrip()
                file.write(outputSequence + "\n")
                file.write(str(rewards[i]) + "\n")
            file.write("\n")
        file.write(str(maximal) + "\n")
        if (maximal > 0) :
            file.write(outputBuffer + "\n")
            for i in range(0, len(outputposition), 2):
                file.write("{}, {}\n".format(outputposition[i], outputposition[i + 1]))
            print("\n")
        file.write("\n{} ms".format(execution_time))

if __name__ == "__main__":
    run = True
    startscreen()
    gun()
    while run:
        option = main_menu()
        token = []
        sequences = []
        rewards = []
        listOfReward = []

        if option == 1:
            valid = False
            valid2 = False
            while not valid:
                valid = True
                jumlah_token_unik = int(input("Masukkan jumlah token unik: "))
                while not valid2:
                    inputTokens = input("Masukkan token (pisahkan dengan spasi): ").split()
                    token_set = set()  
                    for token in inputTokens:
                        if len(token) == 2 and token.isalnum() and token not in token_set:
                            token_set.add(token)  
                            valid2 = True
                        else:
                            print("Token harus terdiri dari dua karakter alfanumerik dan bersifat unik.")
                            valid2 = False
                            break
                token = list(token_set)  
                ukuran_buffer = int(input("Masukkan ukuran buffer: "))
                ukuran_matriks = input("Masukkan ukuran matriks (kolom baris): ")
                kolom_matriks, baris_matriks = map(int, ukuran_matriks.split())
                jumlah_sequence = int(input("Masukkan jumlah sequence: "))
                ukuran_maksimal_sequence = int(input("Masukkan ukuran maksimal sequence: "))

                print(colored("\nMatrix:", "light_red"))
                matrix = generate_random_matrix(kolom_matriks, baris_matriks)
                print(colored("\nSequences & Reward:", 'light_red'))
                sequences, rewards = generate_random_sequences(jumlah_sequence, ukuran_maksimal_sequence)
                for i in range(0, jumlah_sequence):
                    outputSequence = ""
                    inputSequence = sequences[i]
                    for j in range(0, len(sequences[i]), 2):
                         outputSequence += colored(inputSequence[j:j+2], 'green') + " "
                    outputSequence = outputSequence.rstrip()
                    print(outputSequence)
                    colored_reward = colored(str(rewards[i]), 'blue')
                    print(rewards[i])
                start_time = time.time()
                paths, position = possibilities(0, 0, '', [], [], ukuran_buffer, [], [kolom_matriks, baris_matriks], matrix, [], sequences)
                listOfReward = getReward(paths, sequences, rewards, listOfReward)
                maximal, imax = getOptimal(listOfReward, paths)
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000
                print(colored("\nMaximal Reward:", 'light_red'))
                print(maximal)
                inputBuffer = paths[imax]
                if maximal == 0 :
                    print(colored("\nTidak ada optimal path yang memenuhi", 'light_red'))
                else :
                    outputBuffer = ""
                    print(colored("\nOptimal Path:", 'light_red'))
                    for i in range (0, len(paths[imax]), 2):
                        outputBuffer += inputBuffer[i:i+2] + " "
                    outputBuffer = outputBuffer.rstrip()
                    print(outputBuffer)
                    outputposition = position[imax]
                    print(colored("\nOptimal Path position:", 'light_red'))
                    for i in range(0, len(position[imax]), 2):
                        print("{}, {}".format(outputposition[i], outputposition[i + 1]))
                print(colored("\nExecution Time:", 'light_red'))
                print(execution_time, "ms")

                # Pilihan apakah ingin menyimpan ke dalam file .txt
                answer = input("Apakah ingin menyimpan solusi? (y/n): ")
                if answer.lower() == 'y':
                    filename = input("Masukkan nama file untuk menyimpan solusi: ")
                    save_solution(sequences, rewards, maximal, outputBuffer, outputposition, execution_time, matrix, filename)
                    print("Solusi telah disimpan dalam file", filename + ".txt")
                elif answer.lower() == 'n':
                    print("Keluar dari program.")
                else:
                    print("Masukan tidak valid. Silakan masukkan 'y' atau 'n'.")

        elif option == 2:
            valid = False
            validSequence = True
            while not valid:
                valid = True
                fileName = input("Masukkan nama file yang akan diproses: ")
                try:
                    with open(f"/Users/azulsuhada/Documents/Semester4/Stima/Tucil-1-Stima/test/input/{fileName}.txt", 'r') as file:
                        lines = file.readlines()
                        ukuran_buffer = int(lines[0])
                        kolom_matriks, baris_matriks = map(int, lines[1].split())
                        matrix = []
                        for i in range(baris_matriks):
                            matrix.append(lines[i+2].split())
                        jumlah_sequence = int(lines[2 + baris_matriks])
                        # Pengecekan apakah matriks yang dibaca dari file sesuai dengan kolom dan baris yang diharapkan
                        if len(matrix) != baris_matriks or any(len(row) != kolom_matriks for row in matrix):
                            print(colored("Matriks yang dibaca tidak sesuai dengan kolom dan baris yang tertulis pada file!\n", 'red'))
                            break

                        sequence_reward_map = {}
                        for i in range(3 + baris_matriks, len(lines), 2):
                            sequence = (lines[i].replace(' ', '')).rstrip()
                            reward = int(lines[i + 1])
                            if sequence in sequence_reward_map:
                            # Jika sequence sudah ada dalam map, periksa apakah reward sama
                                if sequence_reward_map[sequence] != reward:
                                    print(colored("Ada sequence yang sama namun rewardnya berbeda.\n", 'red'))
                                    validSequence = False
                            else:
                            # Jika sequence belum ada dalam map, kita tambahkan sequence dan reward ke dalam map
                                sequence_reward_map[sequence] = reward

                            sequences.append(sequence)
                            rewards.append(reward)
                        # Pengecekan apakah jumlah sequence yang dibaca dari file sesuai dengan yang tertulis di file
                        if validSequence == False:
                            break
                        if len(sequences) != jumlah_sequence:
                            print(colored("Jumlah sequence yang dibaca tidak sesuai dengan yang tertulis di file!\n", 'red'))
                            break

                except FileNotFoundError:
                    valid = False
                    print("File tidak ditemukan. Silahkan coba kembali.")
                    print("================================================")

                if valid:
                    start_time = time.time()
                    paths, position = possibilities(0, 0, '', [], [], ukuran_buffer, [], [kolom_matriks, baris_matriks], matrix, [], sequences)
                    listOfReward = getReward(paths, sequences, rewards, listOfReward)
                    maximal, imax = getOptimal(listOfReward, paths)
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000
                    for i in range(0, jumlah_sequence):
                        outputSequence = ""
                        inputSequence = sequences[i]
                        for j in range(0, len(sequences[i]), 2):
                            outputSequence += colored(inputSequence[j:j+2], 'green') + " "
                        outputSequence = outputSequence.rstrip()
                        print(outputSequence)
                        colored_reward = colored(str(rewards[i]), 'blue')
                        print(rewards[i])
                    print(colored("\nMaximal Reward:", 'light_red'))
                    print(maximal)
                    inputBuffer = paths[imax]
                    outputBuffer = ""
                    outputposition = position[imax]
                    if maximal == 0 :
                        print(colored("\nTidak ada optimal path yang memenuhi", 'light_red'))
                    else :
                        print(colored("\nOptimal Path:", 'light_red'))
                        for i in range (0, len(paths[imax]), 2):
                            outputBuffer += inputBuffer[i:i+2] + " "
                        outputBuffer = outputBuffer.rstrip()
                        print(outputBuffer)
                        print(colored("\nOptimal Path position:", 'light_red'))
                        for i in range(0, len(position[imax]), 2):
                            print("{}, {}".format(outputposition[i], outputposition[i + 1]))
                    print(colored("\nExecution Time:", 'light_red'))
                    print(execution_time, "ms")

                    # Pilihan apakah ingin menyimpan ke dalam file .txt
                    answer = input("Apakah ingin menyimpan solusi? (y/n): ")
                    if answer.lower() == 'y':
                        filename = input("Masukkan nama file untuk menyimpan solusi: ")
                        save_solution(sequences, rewards, maximal, outputBuffer, outputposition, execution_time, matrix, filename)
                        print("Solusi telah disimpan dalam file", filename + ".txt\n")
                    elif answer.lower() == 'n':
                        print("Keluar dari program.")
                    else:
                        print("Masukan tidak valid. Silakan masukkan 'y' atau 'n'.")

        elif option == 3:
            run = False
            print(colored("Thank you for using this program!", 'yellow'))
            print(colored("You're ready for the next Martinez!", 'yellow'))
            input(colored("Press enter to exit... and byeee 👋", 'yellow'))

        valid = False