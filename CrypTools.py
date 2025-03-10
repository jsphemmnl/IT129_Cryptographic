import os
import string
import random
import subprocess
import msvcrt

class CipherUtilities:
    def __init__(self):
        self.stored_key = None
        self.stored_xor_key = None

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
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

    @staticmethod
    def generate_random_key():
        alphabet = list(string.ascii_lowercase)
        random.shuffle(alphabet)
        return "".join(alphabet)

    @staticmethod
    def monoalphabetic_cipher(text, key, decrypt=False):
        alphabet = string.ascii_lowercase
        if decrypt:
            key_map = {key[i]: alphabet[i] for i in range(26)}
        else:
            key_map = {alphabet[i]: key[i] for i in range(26)}
        return "".join(key_map.get(char, char) for char in text.lower())

    @staticmethod
    def xor_cipher(text, key):
        valid_chars = string.ascii_letters + string.digits + string.punctuation + " "
        return ''.join(chr(((ord(char) ^ key) % 95) + 32) if 32 <= ((ord(char) ^ key) % 95) + 32 <= 126 else char for char in text)

    @staticmethod
    def wait_for_key():
        while not msvcrt.kbhit():
            pass
        return msvcrt.getch()

    @staticmethod
    def copy_to_clipboard(text):
        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=text.encode('utf-8'))
