#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from pathlib import Path
import winshell
from win32com.client import Dispatch


DOCS_FOLDER = Path(os.environ.get('USERPROFILE', Path.home())) / "Documents"
if not DOCS_FOLDER.exists():

    DOCS_FOLDER = Path("D:/Documents")

SCRIPTS_FOLDER = DOCS_FOLDER / "AutoHotkey"
OUTPUT_FOLDER = DOCS_FOLDER / "AutoHotkey" / "Compiled"
ICON_PATH = SCRIPTS_FOLDER / "icon.ico"  # ONE icon to rule them all
AHK2EXE = Path(r"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe")
# =======================================


def compile_script(script_path):
    """Compile a single script."""
    
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        return False
    
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    
    exe_name = script_path.stem + ".exe"
    exe_path = OUTPUT_FOLDER / exe_name
    

    ahk_base = AHK2EXE.parent.parent / "v2" / "AutoHotkey64.exe"
    if not ahk_base.exists():

        ahk_base = AHK2EXE.parent.parent / "AutoHotkey64.exe"
    
    cmd = [
        str(AHK2EXE),
        "/in", str(script_path),
        "/out", str(exe_path),
        "/base", str(ahk_base),
    ]
    
    if ICON_PATH.exists():
        cmd.extend(["/icon", str(ICON_PATH)])
    
    print(f"Compiling {script_path.name}...")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Compiled to: {exe_path}")
        return exe_path
    except subprocess.CalledProcessError:
        print(f"Compilation failed for {script_path.name}")
        return False


def create_startup_shortcut(exe_path):
    """Create startup shortcut for the exe."""
    
    startup_folder = Path(winshell.startup())
    shortcut_path = startup_folder / f"{exe_path.stem}.lnk"
    
    print(f"Creating startup shortcut...")
    
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(exe_path)
        shortcut.WorkingDirectory = str(exe_path.parent)
        shortcut.IconLocation = str(exe_path)
        shortcut.save()
        print(f"Shortcut created: {shortcut_path}")
        return True
    except Exception as e:
        print(f"Shortcut failed: {e}")
        return False


def compile_and_setup(script_name):
    """Compile script, add icon, create startup shortcut."""
    
    if not script_name.endswith('.ahk'):
        script_name += '.ahk'
    
    script_path = SCRIPTS_FOLDER / script_name
    
    exe_path = compile_script(script_path)
    if not exe_path:
        return False
    
    create_startup_shortcut(exe_path)
    print(f"\nDone! {script_name} will run on startup.")
    return True


def compile_all():
    """Compile all .ahk scripts in the folder."""
    
    if not SCRIPTS_FOLDER.exists():
        print(f"Scripts folder not found: {SCRIPTS_FOLDER}")
        sys.exit(1)
    
    scripts = list(SCRIPTS_FOLDER.glob("*.ahk"))
    
    if not scripts:
        print(f"No .ahk scripts found in {SCRIPTS_FOLDER}")
        sys.exit(1)
    
    print(f"\nFound {len(scripts)} script(s) to compile\n")
    
    success = 0
    failed = 0
    
    for script in scripts:
        exe_path = compile_script(script)
        if exe_path:
            create_startup_shortcut(exe_path)
            success += 1
            print()
        else:
            failed += 1
            print()
    
    print(f"\n{'='*50}")
    print(f"Compiled: {success}")
    print(f"Failed: {failed}")
    print(f"{'='*50}")


def run_all():
    """Run all compiled executables."""
    
    if not OUTPUT_FOLDER.exists():
        print(f"Output folder not found: {OUTPUT_FOLDER}")
        sys.exit(1)
    
    exes = list(OUTPUT_FOLDER.glob("*.exe"))
    
    if not exes:
        print(f"No compiled executables found in {OUTPUT_FOLDER}")
        sys.exit(1)
    
    print(f"\nRunning {len(exes)} executable(s)\n")
    
    for exe in exes:
        print(f"Starting {exe.name}...")
        subprocess.Popen([str(exe)], cwd=exe.parent)
    
    print(f"\nAll executables started!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compile AHK scripts with icon and create startup shortcuts \nThis is suposed to be an automated tool to make my life easier"
    )
    parser.add_argument(
        "--compile-all",
        action="store_true",
        help="Compile all .ahk scripts in the folder"
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run all compiled executables"
    )
    
    args = parser.parse_args()
    
    if args.compile_all:
        compile_all()
    elif args.run_all:
        run_all()
    elif args.script_name:
        compile_and_setup(args.script_name)
    else:
        parser.print_help()
        print(f"\nScripts folder: {SCRIPTS_FOLDER}")
        print(f"Output folder: {OUTPUT_FOLDER}")
        print(f"Icon: {ICON_PATH}")