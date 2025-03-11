import os
import string
import msvcrt
import random
import subprocess
from CrypTools import CipherUtilities

def main_menu():
    cipherutil = CipherUtilities()
    stored_key = None
    stored_xor_key = None

    while True:
        cipherutil.clear_screen()
        print("\nMain Menu:")
        print("A. Caesar Cipher")
        print("B. Monoalphabetic Cipher")
        print("C. Bitwise XOR Cipher")
        print("D. DNA Cipher")
        print("(Press ESC to Exit)")

        print("Select an option (A-D): ", end="", flush=True)
        key = cipherutil.wait_for_key()
        if key == b'\x1b':  # ESC key
            print("\nExiting... Goodbye!")
            break
        choice = key.decode().upper()

        if choice in ["A", "B", "C", "D"]:
            cipherutil.clear_screen()
            text = ""
            while not text.strip():
                print("Enter text:")
                text = input().strip()
                if not text:
                    print("Input cannot be empty. Please enter valid text.")

            action = ""
            while action not in ["e", "d"]:
                print("Encrypt or Decrypt? (e/d):")
                action = input().lower()
            decrypt = action == 'd'

            if choice == "A":
                shift = None
                while shift is None:
                    try:
                        print("Enter shift value:")
                        shift = int(input())
                    except ValueError:
                        print("Invalid input. Please enter a numeric shift value.")
                result = cipherutil.caesar_cipher(text, shift, decrypt)

            elif choice == "B":
                if decrypt and stored_key:
                    print("Use stored key? (y/n):")
                    use_stored = input().lower()
                    if use_stored == 'y':
                        key = stored_key
                    else:
                        print("Enter 26-letter substitution key:")
                        key = input()
                else:
                    key = ""
                    while not key or len(key) != 26 or not all(c.isalpha() for c in key):
                        print("Do you want to enter a key or generate a random one? (enter/generate):")
                        key_choice = input().lower()
                        if key_choice == "generate":
                            key = cipherutil.generate_random_key()
                            stored_key = key
                            print("Generated Key:", key)
                        else:
                            print("Enter 26-letter substitution key:")
                            key = input()
                            if len(key) != 26 or not all(c.isalpha() for c in key):
                                print("Invalid key. Must be 26 unique letters.")
                                key = ""
                    stored_key = key
                print("Using Key:", key)
                result = cipherutil.monoalphabetic_cipher(text, key, decrypt)

            elif choice == "C":
                if decrypt and stored_xor_key is not None:
                    print("Use stored key? (y/n):")
                    use_stored = input().lower()
                    if use_stored == 'y':
                        key = stored_xor_key
                    else:
                        key = None
                else:
                    key = None
                while key is None:
                    try:
                        print("Enter key: ")
                        key = input()
                    except:
                        pass
                stored_xor_key = key
                result = cipherutil.xor_cipher(text, key)

            elif choice == "D":
                if decrypt:
                    result = cipherutil.dna_to_text(text)
                else:
                    result = cipherutil.text_to_dna(text)

            print("\nResult:", result)

            if not decrypt:
                print("\nCopy result to clipboard? (y/n):")
                copy_choice = input().lower()
                if copy_choice == 'y':
                    cipherutil.copy_to_clipboard(result)
                    print("Result copied to clipboard.")

            print("\nPress any key to return to the main menu...")
            cipherutil.wait_for_key()
        else:
            print("Invalid choice. Please select a letter between A and D.")

        cipherutil.clear_screen()

if __name__ == "__main__":
    main_menu()
    