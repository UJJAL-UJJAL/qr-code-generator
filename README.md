# QR Code Generator

A small Python program that turns text or a URL into a QR code image.
It shows a preview in the terminal and saves each QR code as a PNG file with a name you choose.

The QR code itself is built by the `qrcode` library. This program handles the menu,
the filenames, the error messages and the terminal preview.

## Install

You need Python 3. Then install the one library the program uses:

```
pip install -r requirements.txt
```

## Run

```
python main.py
```

## How to use it

The program shows a menu:

```
1. Make a QR code
2. Quit
```

Choose `1`, then:

1. Type the text or URL.
2. A preview of the QR code is printed in the terminal.
3. Type a filename for the image. `.png` is added for you if you leave it out.

Choose `2` to quit. The program then lists the images it saved.

Example:

```
QR Code Generator

1. Make a QR code
2. Quit
Choose 1 or 2: 1
Enter text or a URL: https://example.com

(the QR code preview is printed here)

Filename for the image (press Enter to cancel): example
QR code saved to: /home/you/qr-code-generator/example.png

1. Make a QR code
2. Quit
Choose 1 or 2: 2
Images saved this time:
 - /home/you/qr-code-generator/example.png
Goodbye!
```

Images are saved in the folder you ran the command from.

### What the program checks

- **Blank text:** nothing is created and you go back to the menu.
- **Blank filename:** the QR code is not saved and you go back to the menu.
- **Bad filename:** a name containing any of `\ / : * ? " < > |`, or made only of dots, is refused and you are asked again.
- **Existing file:** the program asks before replacing it. Answer `n` to choose another name.
- **Text too long:** a QR code can only hold so much text, so you get a message instead of a crash.
- **Save problems:** if the image can't be written (for example, the name is too long for your system), you get a message.
- **Wrong menu choice:** you are asked to type 1 or 2.
- **Ctrl+C or Ctrl+D:** the program quits cleanly.

### About the preview

The preview draws the QR code with block characters. It is meant for a quick look.
For scanning, use the saved PNG file: some terminals (especially dark ones) invert the
colours of the preview, and a preview that is too big for the terminal is skipped.
If the blocks look wrong in your terminal, change `DARK` and `LIGHT` near the top of `main.py`
(for example `DARK = "##"`).

## Troubleshooting

- macOS/Linux: use `python3` and `pip3` instead of `python` and `pip`.
- `externally-managed-environment` error: run `python3 -m venv .venv`, activate it
  (`source .venv/bin/activate`, or `.venv\Scripts\activate` on Windows), then run the install command again.

## How the code is organised

| Function | What it does |
|---|---|
| `ask_for_text()` | Reads the text or URL and removes stray spaces |
| `check_filename(name)` | Returns a message if the filename has a problem, or `""` if it is fine |
| `add_extension(name)` | Adds `.png` if it is missing |
| `ask_for_filename()` | Asks until the filename is usable (or the user cancels) and checks for an existing file |
| `build_qr_code(text)` | Asks the `qrcode` library to build the QR code |
| `show_preview(qr)` | Prints the QR code's grid of dark and light squares in the terminal |
| `save_qr_code(qr, filename)` | Saves the image and reports any save error |
| `make_one_qr_code()` | One full round: ask, preview, save |
| `show_menu()` / `main()` | The menu loop and the list of saved images |
