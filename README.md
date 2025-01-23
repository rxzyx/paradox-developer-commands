<h1 align="center">Paradox Patcher</h1>
<h3 align="center">A Python patcher for Paradox games, like <a href="https://www.paradoxinteractive.com/games/hearts-of-iron-iv/about">HOI4</a> that gives you developer access to commands and more!</h3>

#### Made by rxzyx (rzx). This is purley for education purposes.
- 📫 Have a problem? **Just write an issue and I will do my best to respond.**

## Features:

### HOI4
- Add developer access to commands in the console
    - This means that you can use commands like `normals`, `aircombat` and more!

### EU4
- Add developer access to commands in the console
    - This means that you can use commands like `debug_smooth`
- Allow console access in Ironman mode and multiplayer

#### I am not responsible for your actions with this. Please rememeber to use these fairly.

## How To Use (Python):

- Firstly, remember to backup the original file you intend to patch.
- For how to retrieve the .app file, look up a tutorial or simply open Steam, navigate to the supported app of choice, click the Settings icon, then Manage and finally Browse local files

### MacOS
### Method 1
- To patch a Mach-O file (which can be found in hoi4.app/Contents/MacOS/hoi4 or eu4.app/Contents/MacOS/eu4), copy it into another directory, and you can then either pass the file path as an argument, like:
    - `python3 main.py path/to/macho`
- or input it when running the script. You can then replace the original Mach-O file with the patched one.

### Method 2
- Additionally, you can patch the whole .app file (same functionality as giving the Mach-O file path in the .app), but this requires root access, which can be done via:
    - `sudo python3 main.py path/to/game.app`
- The original .app file can now be replaced with the patched one this way.

- I would really appreciate some pull requests—whether for style, logic, efficiency, or features. Anything would be helpful!

### Windows
### .exe files
- .exe is not yet supported for EU4, however, it is as of now supported for HOI4.
- Simply use the script as normal but input a .exe as the path, this will be patched and you can replace the original file with it.
- However, it hasn't actually been tested properly, so feedback will be appreciated!


## 🤖 Features with Problems:

- Patching the hoi4.exe file has not been tested. Feedback will be appreciated, you can submit an error in the "Issues" section. Make sure to backup the original file.


<h3 align="left">Made With Python </h3>
<p align="left"> <a href="https://www.python.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/>

#### This is protected by the MIT license.
#### Copyright &copy; 2025 rxzyx (rzx).
