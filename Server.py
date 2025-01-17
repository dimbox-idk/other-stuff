from flask import Flask
from flask import request
import random
import os
import subprocess
import base64
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

def get_temp_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.abspath(sys._MEIPASS)
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return base_path

alphanumeric = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

app = Flask(__name__)

@app.route('/decompile', methods=['POST'])
def decompile():
    bytecode = request.get_data()
    filename = 'temp_'

    for _ in range(32):
        filename += random.choice(alphanumeric)

    filename += '.bin'

    try:
        bytecode = base64.b64decode(bytecode)
    except:
        print('Invalid data! @ ' + filename)
        return 'Invalid data! Bytecode:\n' + str(bytecode)

    with open(filename, 'wb') as file:
        file.write(bytecode)

    result = subprocess.run(['luau-lifter.exe', filename, '-e'], stdout=subprocess.PIPE)

    if result.returncode != 0:
        print('Error decompiling bytecode! @ ' + filename)
        os.remove(filename)
        return 'Error decompiling bytecode! Bytecode:\n' + str(bytecode)
    else:
        print('Decompiled bytecode successfully!')
    
    os.remove(filename)

    decompiled_code = result.stdout

    try:
        decompiled_code = base64.b64encode(decompiled_code)
    except:
        print('Unknown error while was trying to encode in base64')
        return 'Unknown error while was trying to encode in base64'

    return decompiled_code

if __name__ == '__main__':
    temp_path = get_temp_path()
    os.chdir(temp_path)
    app.run(host='localhost', port=3366)