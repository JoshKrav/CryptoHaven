from flask import Flask, render_template, request
from Crypto.Cipher import DES
from pycipher import Vigenere,SimpleSubstitution
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

"""Encrypts plaintext using railfence.
    ref: https://www.geeksforgeeks.org/rail-fence-cipher-encryption-decryption/"""
def railfence_encrypt(text, key):
    # create the matrix to cipher
    # plain text key = rows ,
    # length(text) = columns
    # filling the rail matrix
    # to distinguish filled
    # spaces from blank ones
    rail = [['\n' for i in range(len(text))]
                for j in range(key)]
     
    # to find the direction
    dir_down = False
    row, col = 0, 0
     
    for i in range(len(text)):
         
        # check the direction of flow
        # reverse the direction if we've just
        # filled the top or bottom rail
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
         
        # fill the corresponding alphabet
        rail[row][col] = text[i]
        col += 1
         
        # find the next row using
        # direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
    # now we can construct the cipher
    # using the rail matrix
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return("" . join(result))

"""Decrypts ciphertext using railfence.
    ref: https://www.geeksforgeeks.org/rail-fence-cipher-encryption-decryption/"""
def railfence_decrypt(text, key):
 
    # create the matrix to cipher
    # plain text key = rows ,
    # length(text) = columns
    # filling the rail matrix to
    # distinguish filled spaces
    # from blank ones
    rail = [['\n' for i in range(len(cipher))]
                for j in range(key)]
     
    # to find the direction
    dir_down = None
    row, col = 0, 0
     
    # mark the places with '*'
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
         
        # place the marker
        rail[row][col] = '*'
        col += 1
         
        # find the next row
        # using direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
             
    # now we can construct the
    # fill the rail matrix
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if ((rail[i][j] == '*') and
            (index < len(cipher))):
                rail[i][j] = cipher[index]
                index += 1
         
    # now read the matrix in
    # zig-zag manner to construct
    # the resultant text
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
         
        # check the direction of flow
        if row == 0:
            dir_down = True
        if row == key-1:
            dir_down = False
             
        # place the marker
        if (rail[row][col] != '*'):
            result.append(rail[row][col])
            col += 1
             
        # find the next row using
        # direction flag
        if dir_down:
            row += 1
        else:
            row -= 1
    return("".join(result))

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

"""Function that has key generation for the SavelsonCipher"""
def savelsonKeyGenerator():
    #divide each letter in my last namy ascii value by 7 because it's my favorite number
    key = "Savelson"
    key_values = []
    for char in key:
        key_values.append(ord(char) // 7)
    return key_values

"""Function that has logic for the SavelsonCipher, which uses my last name (Dylan) and some math to encrypt/decrypt"""
def savelson_cipher(text, decrypt=False):
    key_values = savelsonKeyGenerator()
    new_text = ""

    if decrypt:
        #add key value from ascii of character
        for i, char in enumerate(text):
            key_value = key_values[i % len(key_values)]  
            new_text += chr(ord(char) + key_value)
    else:
        #subtract key value from ascii of character
        for i, char in enumerate(text):
            key_value = key_values[i % len(key_values)]
            new_text += chr(ord(char) - key_value)  

    return new_text


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    text = ""
    algorithm = "base64"
    shift = 3  
    key = "" 
    operation = "encrypt"  

    if request.method == "POST":
        text = request.form["text"]
        algorithm = request.form["algorithm"]
        operation = request.form["operation"]


        if algorithm == "railfence":
            shift = int(request.form["shift"])
            if(operation == "decrypt"):
                result = railfence_decrypt(text,shift)
            else:
                result = railfence_encrypt(text,shift)
        
        elif algorithm == "caesar":
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

        elif algorithm == "viginere":
            key = str(request.form["key"])
            if(operation == "decrypt"):
                result = Vigenere(key.capitalize()).decipher(text.capitalize())
            else:
                result = Vigenere(key.capitalize()).encipher(text.capitalize())
        elif algorithm == "substitution":
            key = str(request.form["subkey"])
            if(operation == "decrypt"):
                result = SimpleSubstitution(key).decipher(text)
            else:
                result = SimpleSubstitution(key).encipher(text)
        elif algorithm == "savelson":
            result = savelson_cipher(text, decrypt=(operation == "decrypt"))
    
    return render_template(
        "index.html",
        result=result,
        originalText=text,
        selectedAlgorithm=algorithm,
        selectedOperation=operation,
        selectedShift=shift,
        selectedKey=key
    )
if __name__ == "__main__":
    app.run(debug=True)
