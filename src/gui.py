import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
from main import main_menu

def masukan_via_cli():
    subprocess.run(["python", "src/main.py"])

def masukan_via_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        subprocess.run(["python", "src/main.py", "--file", file_path])

def on_option_selected(option):
    if option == 1:
        masukan_via_cli()
    elif option == 2:
        masukan_via_file()
    elif option == 3:
        confirm_exit = messagebox.askyesno("Exit", "Anda yakin ingin keluar?")
        if confirm_exit:
            exit()

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
                           command=lambda idx=idx: on_option_selected(idx))
        button.pack(pady=5)

    pistol_image = Image.open("image/Gui.jpeg")
    pistol_photo = ImageTk.PhotoImage(pistol_image)
    pistol_label = tk.Label(main_window, image=pistol_photo, bg="black")
    pistol_label.image = pistol_photo
    pistol_label.pack(pady=15)

    main_window.mainloop()

if __name__ == "__main__":
    main_menu()