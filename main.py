import re
import sys
import os

print("Paradox Developer Access and Patcher Script by rxzyx on Github.",
      "Make sure the original file is backed up\n",
      "Supports:\nhoi4\neu4", sep='\n')

def is_sudo():    # needed for .app files
    return os.geteuid() == 0

patches = [
    [
        "Remove Dev Check #1",      # title
        "74 20 41 C6 04 24 00 C6",  # original
        "EB 20 41 C6 04 24 00 C6"   # replacement
    ],
    [
        "Remove Dev Check #2",
        "74 40 41 C6 04 24 00 C6",
        "EB 40 41 C6 04 24 00 C6"
    ]
]
pattern = [0x74, None, 0x41, 0xC6, 0x04, 0x24, 0x00, None] # 0xC6

is_orig_uef = True
filename = "hoi4"
add_to = ["EB", 2]

file_path = sys.argv[1] if len(sys.argv) > 1 else input(
    "Enter the file path: ").strip()

if file_path.endswith(".app"):
    if is_sudo():
        if os.path.isfile("/Contents/MacOS/eu4"):
            filename = "eu4"
        file_path += f"/Contents/MacOS/{filename}"

        is_orig_uef = False
    else:
        print("\nFor an application file, you need to have root privileges.")
        print(f'This can be done by doing sudo python3 "{sys.argv[0]}"')
        raise SystemExit
elif file_path.endswith(".exe"):    # not confirmed!
    print("Using .exe BETA mode.")
    patches = [
        [
            "Remove Dev Check #1",
            "74 12 41 B8 26 00 00 00",
            "EB 12 41 B8 26 00 00 00"
        ],
        [
            "Remove Dev Check #2",
            "41 80 7E 10 00 0F 85 A8 FE FF FF",
            "39 C0 90 90 90 0F 85 A8 FE FF FF",
            # if the above replacement crashes the game / does not work,
            # try 41 80 7E 10 01 0F 85 A8 FE FF FF instead
        ]

    ]
    # pattern = [0x74, None, 0x41, 0xB8, 0x26, 0x00, 0x00, 0x00, 0x48, 0x8D]
    pattern = [0x74, None, 0x41, 0xB8, 0x26, 0x00, 0x00, 0x00, 0x48, 0x8D,
               0x15, 0x64, 0x25]
orig_patches = patches
headers = {
    "Mach-O (64-bit)": [
        bytes.fromhex("FE ED FA CF"),
        bytes.fromhex("CF FA ED FE")
    ],
    "Mach-O (32-bit)": [
        bytes.fromhex("FE ED FA CE"),
        bytes.fromhex("CE FA ED FE")
    ],
    "DOS MZ executable": [
        bytes.fromhex("4D 5A")
    ]
}


with open(file_path, 'rb') as f:
    data = f.read()
    if data.count(bytes("Europa Universalis IV", "utf8")):
        pattern = [0x0F, 0x84, None, 0xFF, 0xFF, 0xFF,
                   0xC6, 0x85, 0x60, 0xFF, 0xFF, 0xFF]
        patches = [
            [
                "Remove Dev Check #1",                  # title
                "0F 84 38 FF FF FF C6 85 60 FF FF FF",  # original
                "E9 39 FF FF FF 90 C6 85 60 FF FF FF",  # replacement
            ],
            [
                "Ironman Console",
                "5B 41 5E 41 5F 5D C3 90 55 48 89 E5 8A 47 08" + \
                "5D C3 90 55 48 89 E5 41 57 41 56 41 55 41 54 53 48",
                "5B 41 5E 41 5F 5D C3 90 55 48 89 E5 30 C0 90" + \
                "5D C3 90 55 48 89 E5 41 57 41 56 41 55 41 54 53 48",
            ],
            [
                "Multiplayer Console",
                "48 8B 5B 58 EB D8 31 C0 EB 02 B0 01",
                "48 8B 5B 58 EB D8 31 C0 EB 02 B0 00"
            ]
        ]
        if file_path.endswith(".exe"):
            raise NotImplementedError(".exe not supported for eu4!")
        print("EU4 file confirmed.")
        try:
            console_mode = int(input(
                "Enter 1 for dev check, 2 for allow console, 3 for all: "
            ))
        except ValueError:
            print("Enabling console only mode.")
            console_mode = 1

        if console_mode == 1:
            patches = patches[:1]
        elif console_mode == 2:
            patches = patches[1:]
        filename = "eu4"

        add_to = ["E9 39 FF FF FF 90", 17]
    elif data.count(bytes("Hearts of Iron IV", "utf8")):
        print("HOI4 file confirmed.")

    elf_header = f.read(64)
    for hn, heads in headers.items():
        for h in heads:
            if elf_header[:len(h)] == h:
                print(hn, "detected.")
                if hn == "Mach-O (32-bit)" and filename == "hoi4":
                    patches = [     # test
                        [
                            "Remove Dev Check #1",
                            "0F 84 1C 10 00 00 C6 03 00",
                            "E9 1D 10 00 00 C6 03 00"
                        ], [
                            "Remove Dev Check #2",
                            "0F 84 3C 10 00 00 C6 03 00",
                            "E9 3D 10 00 00 C6 03 00"
                        ]
                    ]
                    pattern = [0x0F, 0x84, None, 0x10,
                               0x00, 0x00, 0xC6, 0x03, 0x00]

n = a = 0
for patch in patches:
    print(patch[1])
    find_result = data.find(bytes.fromhex(patch[1]))
    if find_result != -1:
        print("Found", patch[0])
        n += 1
        print(data.count(bytes.fromhex(patch[1])))
    elif data.find(bytes.fromhex(patch[2])) != -1:
        print(f"`{patch[0]}` is already patched.")
        a += 1
    else:
        print(f"Error! Patch `{patch[0]}` was not found!")

if a == len(patches):
    print("File already patched. Quitting...")
    raise SystemExit

if n == len(patches):
    print("Search successful! {0} pattern{1} found.".format(
        len(patches), 's' if len(patches) > 1 else ''))
else:
    print(f"The pattern amount ({n}) is not equal. Hard searching instead...")
    patches = []

    for i in range(len(data) - len(pattern) + 1):
        match_found = True
        for j in range(len(pattern)):
            if (pattern[j] is not None and data[i + j] != pattern[j]):
                match_found = False
                break
        if match_found:
            title = f"Remove Dev Check #{len(patches) + 1}"
            print("Found", title)
            matched_pattern = ' '.join(
                f"{data[i + j]:02X}" for j in range(len(pattern)))
            patches.append([
                title,
                matched_pattern,
                add_to[0] + matched_pattern[add_to[1]:]
            ])

    d, fpatchlen = {}, len(patches)
    for p in patches:
        k = p[1][-2:]
        d[k] = d.get(k, 0) + 1
    patches = [p for p in patches if d[p[1][-2:]] > 1]
    print(f"Filtered patches from len {fpatchlen} to {len(patches)}")
  
    if len(patches) != len(orig_patches):
        print(
            "The pattern {0} amount does not equal to {1}. Quitting.".format(
                len(patches), len(orig_patches))
        )
        raise SystemExit

patch_mode = input("Would you like to patch the file? (y/n): ").strip().lower()
if patch_mode == 'y':
    for patch in patches:
        print(f"Editing data with patch `{patch[0]}`...")
        data = data.replace(
            bytes.fromhex(patch[1]),
            bytes.fromhex(patch[2])
        )
    print("Applying patches...")
    with open(file_path, 'wb') as f:
        f.write(data)
    print(
        "All patches complete. The file is now patched."
    )
    if is_orig_uef and not file_path.endswith(".exe"):
        print("Now just right-click on the application, click " + \
              "'Show Package Contents', navigate to Contents/MacOS " + \
              f"and replace the '{filename}' file with the patched one.")
    else:
        print("Now replace the application with the patched one.")
        
