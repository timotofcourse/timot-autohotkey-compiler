#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from pathlib import Path
import winshell
from win32com.client import Dispatch
import shutil


OUTPUT_FOLDER = "Compiled"
ICON_PATH = "icon.ico"  # ONE icon to rule them all
AHK2EXE = Path(r"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe")

def build_all():
    current_path = os.path.abspath(".")
    
    # Make the Compiled folder in case it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    for file in os.path.abspath("."):
        compiled_file = os.path.abspath(f"Compiled/{file}")
        if file.endswith(".ahk"):
            build_command = [AHK2EXE, "/in", file, "/out", compiled_file, "/icon", ICON_PATH, "/NoDecompile"]
            # Ahk2Exe.exe /in "MyScript.ahk" /out "MyScript.exe" /icon "MyIcon.ico" /NoDecompile   
            build_all_files = subprocess.Popen(build_command, shell=True)
            build_all_files.wait()

def add_to_startup():

    compiled_dir = os.path.abspath("./Compiled")
    shutil.copy2(compiled_dir, "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")

if __name__ == "__main":
    build_all()
    add_to_startup()

