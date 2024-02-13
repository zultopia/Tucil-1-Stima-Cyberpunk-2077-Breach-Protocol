import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from termcolor import colored
import subprocess  
import time
from main import main_menu, generate_random_matrix, generate_random_sequences, sequenceInPath, possibilities, getReward, getOptimal, save_solution

def main_menu():
    main_window = tk.Tk()
    main_window.title("Menu Utama")
    main_window.configure(bg='black')

    title_label = tk.Label(main_window, text="Minigames Cyberpunk 2077 Breach Protocol", fg="yellow", bg="black",
                           font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    author_label = tk.Label(main_window, text="by Marzuli Suhada M", fg="yellow", bg="black",
                            font=("Helvetica", 12, "italic"))
    author_label.pack(pady=5)

    options = ["Masukan via CLI", "Masukan via file (*.txt)", "Exit"]

    for idx, option in enumerate(options, start=1):
        label_option = tk.Label(main_window, text=option, fg="black", bg="yellow", font=("Helvetica", 12, "bold"))
        label_option.pack(pady=5)
        button = tk.Button(main_window, text="Pilih", fg="green", bg="black", font=("Helvetica", 14, "bold"),
                           command=lambda idx=idx: on_option_selected(idx, option))
        button.pack(pady=5)

    pistol_image = Image.open("image/Gui.jpeg")
    pistol_photo = ImageTk.PhotoImage(pistol_image)
    pistol_label = tk.Label(main_window, image=pistol_photo, bg="black")
    pistol_label.image = pistol_photo
    pistol_label.pack(pady=15)

    main_window.mainloop()


def on_option_selected(option, option_text):
    if option == 1 or option == 2:
        subprocess.run(["python", "/Users/azulsuhada/Documents/Semester4/Stima/Tucil-1-Stima/src/main.py"])
    elif option == 3:
        confirm_exit = messagebox.askyesno("Exit", "Anda yakin ingin keluar?")
        if confirm_exit:
            exit()

if __name__ == "__main__":
    main_menu()
    run = True
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