from flask import Flask, render_template, request
from Crypto.Cipher import DES
import binascii
import base64

app = Flask(__name__)

"""Method to encrypt/decrypt using the ceasar cipher"""
def caesar_cipher(text, shift, decrypt=False):
    UPPERCASE_ASCII = 65 
    LOWERCASE_ASCII = 97 
    ALPHABET_SIZE = 26
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = UPPERCASE_ASCII if char.isupper() else LOWERCASE_ASCII
            result += chr((ord(char) - shift_base + shift) % ALPHABET_SIZE + shift_base)
        else:
            result += char
    return result

"""Method to encrypt/decrypt using the base64 cipher"""
def base64_cipher(text, decrypt=False):
    if decrypt:
        return base64.b64decode(text.encode()).decode()
    return base64.b64encode(text.encode()).decode()

"""Encrypts plaintext using DES."""
def des_encrypt(text, key):
    des = DES.new(key, DES.MODE_ECB)
    text = ciphertext = binascii.unhexlify(text)
    ciphertext = des.encrypt(text)
    return binascii.hexlify(ciphertext).decode()

"""Decrypts ciphertext using DES."""
def des_decrypt(ciphertext, key):
    des = DES.new(key, DES.MODE_ECB)  # Decode hex to binary
    ciphertext = binascii.unhexlify(ciphertext)
    decrypted_text = des.decrypt(ciphertext)
    return binascii.hexlify(decrypted_text).decode()

"""Class that has logic for the IdCipher, which uses my student Id(Josh) to encrypt/decrypt
    A class was used as it makes it easier to read and also is more efficient."""
class IdCipher:
    def __init__(self, key="2271524"):
        self.key = []
        # Convert key into a list of integers
        for digit in key:
            self.key.append(int(digit))
    
    def encrypt(self, text):
        ciphertext = ""
        for i, char in enumerate(text):
            #Gets int
            shift = self.key[i % len(self.key)]
            #Shifts character forward
            ciphertext += chr(ord(char) + shift)  
        return ciphertext

    def decrypt(self, ciphertext):
        text = ""
        for i, char in enumerate(ciphertext):
            #Gets int
            shift = self.key[i % len(self.key)]
            #Shifts character backwards
            text += chr(ord(char) - shift)  
        return text

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        algorithm = request.form["algorithm"]
        operation = request.form["operation"]
        
        if algorithm == "caesar":
            shift = int(request.form["shift"]) 
            result = caesar_cipher(text, shift, decrypt=(operation == "decrypt"))
        elif algorithm == "base64":
            result = base64_cipher(text, decrypt=(operation == "decrypt"))
        elif algorithm == "idcipher":
            cipher = IdCipher("2271524")
            if(operation == "decrypt"):
                result = cipher.decrypt(text)
            else:
                result = cipher.encrypt(text)
        elif algorithm == "des":
            key = str(request.form["key"]) 
            key = binascii.unhexlify(key)
            assert len(key) == 8, "Key must be exactly 8 bytes for DES."
            if(operation == "decrypt"):
                result = des_decrypt(text,key)
            else:
                result = des_encrypt(text,key)
        return render_template("index.html", result=result, originalText = text)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
