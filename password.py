import string
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox
from PIL import ImageTk as PILImageTk
from PIL import Image as PILImage
import pygame
import json
import random
from PIL import Image, ImageTk

# Initialize the pygame mixer
pygame.mixer.init()

# Dosya adı ve yolunu belirle
file_path = "passwords.json"

# Şifrelerin saklanacağı sözlük
passwords = {}

# Kullanıcının seçtiği renkler
color_preferences = {}

# Maksimum platform sayısı
max_platforms = 6

# Bell sesini yükle
pygame.mixer.music.load("bell.mp3")

# Dosyadan şifreleri ve renkleri yükle
def load_data():
    global passwords, color_preferences
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            passwords = data.get("passwords", {})
            color_preferences = data.get("colors", {})
    except FileNotFoundError:
        passwords = {}
        color_preferences = {}

# Şifreleri ve renkleri dosyaya kaydet
def save_data():
    with open(file_path, "w") as file:
        data = {"passwords": passwords, "colors": color_preferences}
        json.dump(data, file)

# Şifreyi panoya kopyalamak için bu fonksiyonu çağır
def copy_password(website):
    if website in passwords:
        password = passwords[website]
        root.clipboard_clear()
        root.clipboard_append(password)
        pygame.mixer.music.play()
        root.after(5000, clear_password_from_clipboard)

def clear_password_from_clipboard():
    # "<unknown>"'ı panoya kopyala
    root.clipboard_clear()
    root.clipboard_append("5 saniye sonra clipboarda <" "> boş veri basılıyor. ")

def generate_secure_password():
    length = 12
    upper_case_count = 5
    special_char_count = 4

    # Büyük harfler
    upper_case_letters = ''.join(random.choices(string.ascii_uppercase, k=upper_case_count))

    # Küçük harfler
    lower_case_letters = ''.join(random.choices(string.ascii_lowercase, k=length-upper_case_count-special_char_count))

    # Özel karakterler
    special_characters = ''.join(random.choices('!@#$_', k=special_char_count))

    # Şifreyi birleştir
    password = upper_case_letters + lower_case_letters + special_characters
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)
    return password

# Yeni platform ve şifre eklemek için fonksiyon
def add_new_password():
    if len(passwords) >= max_platforms:
        messagebox.showinfo("Uyarı", f"En fazla {max_platforms} platform ekleyebilirsiniz.")
        return

    platform = askstring("Yeni Platform Ekle", "Platform Adı:")
    if platform:
        password = askstring("Yeni Platform Ekle", f"Şifre for {platform}:")
        if password:
            passwords[platform] = password
            update_buttons()
            save_data()

# Platform ve şifreyi silmek için fonksiyon
def delete_password(website):
    if website in passwords:
        del passwords[website]
        update_buttons()
        save_data()
    else:
        print(f"{website} için kayıtlı şifre bulunamadı.")

# Şifreyi düzenlemek için fonksiyon
def edit_password(website):
    if website in passwords:
        new_password = askstring("Şifre Güncelle", f"Yeni şifre for {website}:")
        if new_password:
            passwords[website] = new_password
            save_data()
    else:
        print(f"{website} için kayıtlı şifre bulunamadı.")

# Kullanıcı tercihlerini güncellemek için fonksiyon
def change_color(website):
    if website in passwords:
        random_color = random.choice(available_colors)
        color_preferences[website] = random_color
        for button_frame in frame.winfo_children():
            if button_frame.winfo_children()[0].cget('text') == website:
                button_frame.winfo_children()[0].config(bg=random_color)
        save_data()

def generate_password():
    platform = askstring("Güvenli Şifre Oluştur", "Platform Adı:")
    if platform:
        password = generate_secure_password()
        passwords[platform] = password
        update_buttons()
        save_data()

# Butonları güncelle
def update_buttons():
    for widget in frame.winfo_children():
        widget.destroy()

    for website in passwords:
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=5, fill='x')

        # Rastgele renk seç
        random_color = color_preferences.get(website, random.choice(available_colors))

        button = tk.Button(button_frame, text=website, width=13, height=2, font=("Courier", 10, "bold"), bg=random_color, fg="black", bd=2, relief="groove", command=lambda web=website: copy_password(web))
        button.pack(side='left', padx=(0, 10))

        # Silme
        delete_img = Image.open("silme2.png").resize((23, 23))
        delete_photo = ImageTk.PhotoImage(delete_img)
        delete_button = tk.Button(button_frame, image=delete_photo, width=25, height=25, bd=0, highlightthickness=0, command=lambda web=website: delete_password(web))
        delete_button.image = delete_photo
        delete_button.pack(side='left')

        # Düzenle butonu
        edit_img = Image.open("editle.png").resize((23, 23))
        edit_photo = ImageTk.PhotoImage(edit_img)
        edit_button = tk.Button(button_frame, image=edit_photo, width=25, height=25, bd=0, highlightthickness=0, command=lambda web=website: edit_password(web))
        edit_button.image = edit_photo
        edit_button.pack(side='left')

        # Renk değiştir butonu
        renk_img = Image.open("palet.png").resize((23, 23))
        renk_photo = ImageTk.PhotoImage(renk_img)
        renk_button = tk.Button(button_frame, image=renk_photo, width=25, height=25, bd=0, highlightthickness=0, command=lambda web=website: change_color(web))
        renk_button.image = renk_photo
        renk_button.pack(side='left')

root = tk.Tk()
root.title("Şifre Yönetici")
root.geometry("250x370")  # Pencere boyutu
root.resizable(False, False)
root.iconbitmap("py.ico")

# Dosyadan şifreleri ve renkleri yükle
load_data()

# Platform isimleri için butonları oluştur
frame = tk.Frame(root)
frame.pack(pady=10)

# Ekle butonu
add_button = tk.Button(root, text="Ekle", width=10, height=1, font=("Courier", 10), command=add_new_password, bd=2, relief="groove")
add_button.pack(side='left', anchor='sw', padx=(10, 0), pady=(0, 10))

generate_button = tk.Button(root, text="Güvenli", width=10, height=1, font=("Courier", 10), command=generate_password, bd=2, relief="groove")
generate_button.pack(side='right', anchor='se', padx=(0, 10), pady=(0, 10))

# Kullanılacak renkler
available_colors = ["red", "dark orange", "SkyBlue2", "DarkOrchid3", "bisque3", "NavajoWhite4", "navajo white", "cyan", "DodgerBlue3", "AntiqueWhite3", "LightCyan4", "salmon1", "LightPink3", "SeaGreen1"]

# İlk buton güncelleme
update_buttons()

# Uygulamayı kapatırken şifreleri ve renkleri kaydet
root.protocol("WM_DELETE_WINDOW", lambda: [save_data(), root.destroy()])

# Uygulamayı çalıştır
root.mainloop()
