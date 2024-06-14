#APLIKASI KALKULATOR ENKRIPSI CAESAR
#AQIL MUHAMMAD FACHREZI
#22552011065
#TIF222PC(CNS)
#COMPUTER SECURITY
#TEKNIK INFORMATIKA
#UNIVERSITAS TEKNOLOGI BANDUNG

import os

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def encrypt_caesar(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - shift + key) % 26 + shift)
            ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext

def decrypt_caesar(ciphertext, key):
    return encrypt_caesar(ciphertext, -key)

def main():
    while True:
        clear_screen()  # Membersihkan layar
        print("Program Kalkulator Enkripsi Caesar")
        print("Program By AqilMF with python language")
        print("\nMenu:")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")

        choice = input("Pilih menu (1/2/3): ")

        if choice == '1':
            clear_screen()  # Membersihkan layar
            print("Menu Enkripsi")
            plaintext = input("Masukkan teks yang ingin dienkripsi: ")
            key = int(input("Masukkan kunci enkripsi (bilangan bulat): "))
            ciphertext = encrypt_caesar(plaintext, key)
            print("Hasil enkripsi:", ciphertext)
            input("Tekan Enter untuk kembali ke menu...")
        elif choice == '2':
            clear_screen()  # Membersihkan layar
            print("Menu Dekripsi")
            ciphertext = input("Masukkan teks yang ingin didekripsi: ")
            key = int(input("Masukkan kunci enkripsi (bilangan bulat): "))
            decrypted_text = decrypt_caesar(ciphertext, key)
            print("Hasil dekripsi:", decrypted_text)
            input("Tekan Enter untuk kembali ke menu...")
        elif choice == '3':
            print("Terima kasih!")
            input("This App Was Make By Aqil Muhammad Fachrezi (NPM : 22552011065)...")
            clear_screen()  # Membersihkan layar
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main()
