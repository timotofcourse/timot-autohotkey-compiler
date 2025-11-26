
## Experimental tool

This tool is highly experimental and was made to automate my compilations of my AutoHotKey scripts because I change my scripts a lot and i want them to startup with my Windows system

## Requirements

- AutoHotKey V2
- Ahk2exe
- Python
- Python modules listed in the requirements.txt

## Usage

This tool only works if the .ahk files are in the same folder as the python script

Compile Scripts

```powershell
python .\ahkcompiler.py --compile-all
```

Run Scripts

```powershell
python .\ahkcompiler.py --run-all
```