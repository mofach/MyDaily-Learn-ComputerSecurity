#APLIKASI ENKRIPSI/DEKRIPSI DENGAN ALGORITMA 3DES (Triple Data Encryption Standard)
#AQIL MUHAMMAD FACHREZI
#22552011065
#TIF222PC(CNS)
#COMPUTER SECURITY
#TEKNIK INFORMATIKA
#UNIVERSITAS TEKNOLOGI BANDUNG

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_key():
    while True:
        key = input("Masukkan kunci (harus 24 karakter): ")
        if len(key) == 24:
            return key
        else:
            print("Kunci harus memiliki panjang 24 karakter.")

def encrypt_3des(key, plaintext):
    # Padding data agar sesuai dengan blok cipher
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(plaintext)
    padded_data += padder.finalize()

    # Generate kunci
    key_bytes = key.encode()
    key = key_bytes[:24]  # Panjang kunci harus 24 bytes untuk 3DES

    # Inisialisasi cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Enkripsi data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Encode hasil enkripsi sebagai string base64
    return base64.b64encode(ciphertext).decode()

def decrypt_3des(key, ciphertext):
    # Decode string base64 ciphertext
    ciphertext = base64.b64decode(ciphertext)

    # Generate kunci
    key_bytes = key.encode()
    key = key_bytes[:24]  # Panjang kunci harus 24 bytes untuk 3DES

    # Inisialisasi cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # Dekripsi data
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad data
    unpadder = padding.PKCS7(64).unpadder()
    unpadded_data = unpadder.update(decrypted_data)
    unpadded_data += unpadder.finalize()

    return unpadded_data

def main():
    while True:
        clear_screen()  # Membersihkan layar
        print("Program Enkripsi/Dekripsi Symetric dengan Algoritma 3DES (Triple Data Encryption Standard)")
        print("Program By AqilMF with python language")
        print("\nMenu:")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            clear_screen()  # Membersihkan layar
            print("MENU ENKRIPSI ALGORITMA 3DES\n")
            key = get_valid_key()
            plaintext = input("Masukkan plaintext: ")
            encrypted = encrypt_3des(key, plaintext.encode())
            print("Encrypted:", encrypted)
            input("Tekan Enter untuk kembali ke menu...")
        elif choice == "2":
            clear_screen()  # Membersihkan layar
            print("MENU DEKRIPSI ALGORITMA 3DES\n")
            key = get_valid_key()
            ciphertext = input("Masukkan ciphertext: ")
            decrypted = decrypt_3des(key, ciphertext)
            print("Decrypted:", decrypted.decode())
            input("Tekan Enter untuk kembali ke menu...")
        elif choice == "3":
            print("Terima kasih!")
            input("This App Was Make By Aqil Muhammad Fachrezi (NPM : 22552011065)...")
            clear_screen()  # Membersihkan layar
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main()
