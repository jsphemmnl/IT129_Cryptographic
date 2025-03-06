import os
import string
import msvcrt
import random
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def generate_random_key():
    alphabet = list(string.ascii_lowercase)
    random.shuffle(alphabet)
    return "".join(alphabet)

def monoalphabetic_cipher(text, key, decrypt=False):
    alphabet = string.ascii_lowercase
    if decrypt:
        key_map = {key[i]: alphabet[i] for i in range(26)}
    else:
        key_map = {alphabet[i]: key[i] for i in range(26)}
    return "".join(key_map.get(char, char) for char in text.lower())

def xor_cipher(text, key):
    valid_chars = string.ascii_letters + string.digits + string.punctuation + " "
    return ''.join(chr(((ord(char) ^ key) % 95) + 32) if 32 <= ((ord(char) ^ key) % 95) + 32 <= 126 else char for char in text)

def wait_for_key():
    while not msvcrt.kbhit():
        pass
    return msvcrt.getch()

def copy_to_clipboard(text):
    process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, close_fds=True)
    process.communicate(input=text.encode('utf-8'))

def main_menu():
    stored_key = None
    stored_xor_key = None
    
    while True:
        clear_screen()
        print("\nMain Menu:")
        print("A. Caesar Cipher")
        print("B. Monoalphabetic Cipher")
        print("C. Bitwise XOR Cipher")
        print("D. Future Cipher (To Be Added)")
        print("(Press ESC to Exit)")
        
        print("Select an option (A-D): ", end="", flush=True)
        key = wait_for_key()
        if key == b'\x1b':  # ESC key
            print("\nExiting... Goodbye!")
            break
        choice = key.decode().upper()
        
        if choice in ["A", "B", "C"]:
            clear_screen()
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
                result = caesar_cipher(text, shift, decrypt)
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
                            key = generate_random_key()
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
                result = monoalphabetic_cipher(text, key, decrypt)
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
                        print("Enter key (numeric value between 0-255):")
                        key = int(input())
                        if key < 0 or key > 255:
                            raise ValueError
                    except ValueError:
                        print("Invalid input. Please enter a numeric key between 0 and 255.")
                stored_xor_key = key
                result = xor_cipher(text, key)
            
            print("\nResult:", result)
            
            if not decrypt:
                print("\nCopy result to clipboard? (y/n):")
                copy_choice = input().lower()
                if copy_choice == 'y':
                    copy_to_clipboard(result)
                    print("Result copied to clipboard.")
            
            print("\nPress any key to return to the main menu...")
            wait_for_key()
        elif choice == "D":
            print("Future cipher placeholder.")
        else:
            print("Invalid choice. Please select a letter between A and D.")
        
        clear_screen()

if __name__ == "__main__":
    main_menu()
