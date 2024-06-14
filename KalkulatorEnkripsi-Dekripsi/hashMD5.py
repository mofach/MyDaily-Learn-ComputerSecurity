#APLIKASI ENKRIPSI/DEKRIPSI DENGAN ALGORITMA 3DES (Triple Data Encryption Standard)
#AQIL MUHAMMAD FACHREZI
#22552011065
#TIF222PC(CNS)
#COMPUTER SECURITY
#TEKNIK INFORMATIKA
#UNIVERSITAS TEKNOLOGI BANDUNG

import hashlib
import os

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def md5_encrypt(text):
    # Membuat objek hash MD5
    hash_object = hashlib.md5()
    # Mengupdate objek hash dengan teks yang diberikan
    hash_object.update(text.encode())
    # Mengembalikan nilai hash dalam format hexadecimal
    return hash_object.hexdigest()

def main():
    clear_screen()  # Membersihkan layar
    print("Program Hash MD5 (Message Digest Algorithm 5)")
    print("Program By AqilMF with python language\n")
    # Menerima input teks dari pengguna
    plaintext = input("Masukkan teks yang ingin dienkripsi: ")
    # Memanggil fungsi md5_encrypt untuk mengenkripsi teks
    encrypted_text = md5_encrypt(plaintext)
    # Menampilkan hasil enkripsi
    print("Hasil enkripsi MD5:", encrypted_text)

if __name__ == "__main__":
    main()
