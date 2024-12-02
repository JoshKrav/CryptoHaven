from flask import Flask, render_template, request
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
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
