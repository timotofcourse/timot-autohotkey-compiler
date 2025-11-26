
## Experimental tool

This tool is highly experimental and was made to automate my compilations of my AutoHotKey scripts because I change my scripts a lot and i want them to startup with my Windows system

## Requirements

- AutoHotKey V2
- Ahk2exe
- Python
- Python modules listed in the requirements.txt

## Usage

This tool only works if the .ahk files are in the same folder as the python script.
Replace the icon with another one or don't, I don't really care.

Compile Scripts

```powershell
python .\ahkcompiler.py --compile-all
```

Run Scripts

```powershell
python .\ahkcompiler.py --run-all
```

## Add it to your powershell profile (optional)

Powershell 7+ only

```powershell
function Compile-AHK {
    if (!(Test-Path "path\to\ahkcompiler.py")) {
        python "path\to\ahkcompiler.py" $args
    }
}
Set-Alias -Name ahkc -Value Compile-AHK
```
