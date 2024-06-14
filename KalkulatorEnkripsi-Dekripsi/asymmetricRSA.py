#APLIKASI ENKRIPSI/DEKRIPSI DENGAN ALGORITMA 3DES (Triple Data Encryption Standard)
#AQIL MUHAMMAD FACHREZI
#22552011065
#TIF222PC(CNS)
#COMPUTER SECURITY
#TEKNIK INFORMATIKA
#UNIVERSITAS TEKNOLOGI BANDUNG

import random
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime():
    while True:
        prime_candidate = random.randint(2**10, 2**12)
        if is_prime(prime_candidate):
            return prime_candidate

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randint(2, phi - 1)
        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    encrypted_msg = [pow(ord(char), e, n) for char in plaintext]
    return encrypted_msg

def decrypt(private_key, ciphertext):
    d, n = private_key
    decrypted_msg = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(decrypted_msg)

def main():
    while True:
        clear_screen()
        print("Program Enkripsi/Dekripsi Asymmetric dengan Algoritma RSA (Rivest-Shamir-Adleman)")
        print("Program By AqilMF with python language")
        print("\nSelamat datang di Kalkulator RSA!")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")

        choice = input("Pilih tindakan (1, 2, atau 3): ")

        if choice == '1':
            clear_screen()
            print("\nEnkripsi dipilih.")
            public_key, private_key = generate_keypair()
            print("Public key:", public_key)
            print("Private key:", private_key)

            plaintext = input("Masukkan pesan untuk dienkripsi: ")
            encrypted_msg = encrypt(public_key, plaintext)
            print("Pesan terenkripsi:", encrypted_msg)
            input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '2':
            clear_screen()
            print("\nDekripsi dipilih.")
            private_key = tuple(map(int, input("Masukkan kunci privat (d, n): ").split(',')))

            ciphertext = input("Masukkan pesan terenkripsi (dipisahkan dengan spasi): ").split()
            print("Nilai ciphertext setelah pemisahan:", ciphertext)
            ciphertext = [int(char) for char in ciphertext if char != '']
            decrypted_msg = decrypt(private_key, ciphertext)
            print("Pesan terdekripsi:", decrypted_msg)
            input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '3':
            print("Terima kasih!")
            input("This App Was Make By Aqil Muhammad Fachrezi (NPM : 22552011065)...")
            clear_screen()  # Membersihkan layar
            sys.exit()
        
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main()
