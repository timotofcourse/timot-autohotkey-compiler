import os
import shutil
import subprocess
from pathlib import Path
 
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "Compiled"
ICON_PATH = SCRIPT_DIR / "icon.ico"  # one icon for every script
AHK2EXE = Path(r"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe")
 
# Per-user Startup folder (no admin rights needed)
STARTUP_DIR = Path(os.environ["APPDATA"]) / r"Microsoft\Windows\Start Menu\Programs\Startup"
 
 
def build_all():
    OUTPUT_DIR.mkdir(exist_ok=True)
 
    for ahk_file in SCRIPT_DIR.glob("*.ahk"):
        exe_file = OUTPUT_DIR / ahk_file.with_suffix(".exe").name
        command = [str(AHK2EXE), "/in", str(ahk_file), "/out", str(exe_file)]
        if ICON_PATH.exists():
            command += ["/icon", str(ICON_PATH)]
 
        print(f"Compiling {ahk_file.name}...")
        result = subprocess.run(command)
        if result.returncode != 0:
            print(f"  Failed (exit code {result.returncode})")
 
 
def add_to_startup():
    for exe_file in OUTPUT_DIR.glob("*.exe"):
        shutil.copy2(exe_file, STARTUP_DIR / exe_file.name)
        print(f"Copied {exe_file.name} to Startup")
 
 
if __name__ == "__main__":
    build_all()
    add_to_startup()