import os

import qrcode

# Characters that can't be used in a filename on Windows, macOS or Linux.
BAD_CHARACTERS = '\\/:*?"<>|'

# How the preview draws one square of the QR code (two characters wide,
# so the squares look roughly square in a terminal).
DARK = "██"
LIGHT = "  "

# Skip the preview if it would be wider than this many characters.
MAX_PREVIEW_WIDTH = 100


def ask_for_text():
    """Ask for the text or URL. Returns an empty string if nothing was typed."""
    return input("Enter text or a URL: ").strip()


def check_filename(name):
    """Return a message describing the problem, or "" if the name is fine."""
    for character in name:
        if character in BAD_CHARACTERS:
            return "A filename can't contain any of these: " + BAD_CHARACTERS
    if name.strip(".") == "":
        return "A filename needs some letters or numbers."
    return ""


def add_extension(name):
    """Add .png to the end of the name if it isn't already there."""
    if not name.lower().endswith(".png"):
        name = name + ".png"
    return name


def ask_for_filename():
    """Keep asking until the filename is usable.

    Returns the filename, or None if the user presses Enter to cancel.
    """
    while True:
        name = input("Filename for the image (press Enter to cancel): ").strip()
        if name == "":
            return None

        problem = check_filename(name)
        if problem != "":
            print(problem)
            continue

        filename = add_extension(name)
        if os.path.exists(filename):
            answer = input(filename + " already exists. Replace it? (y/n): ")
            if answer.strip().lower() != "y":
                continue
        return filename


def build_qr_code(text):
    """Use the qrcode library to build the QR code for the text."""
    qr = qrcode.QRCode()
    qr.add_data(text)
    qr.make(fit=True)  # picks the smallest QR code size that fits the text
    return qr


def show_preview(qr):
    """Print the QR code in the terminal, one row of squares per line."""
    grid = qr.get_matrix()  # a list of rows; each square is True (dark) or False (light)

    if len(grid[0]) * len(DARK) > MAX_PREVIEW_WIDTH:
        print("This QR code is too big to preview here, but the image will still be saved.")
        return

    lines = []
    for row in grid:
        line = ""
        for square in row:
            if square:
                line = line + DARK
            else:
                line = line + LIGHT
        lines.append(line)

    try:
        print()
        for line in lines:
            print(line)
        print()
    except UnicodeEncodeError:
        print("Your terminal can't show the preview, but the image will still be saved.")


def save_qr_code(qr, filename):
    """Save the QR code as an image. Returns the full path, or None if saving failed."""
    try:
        image = qr.make_image()
        image.save(filename)
    except OSError as error:
        print("Could not save the image:", error)
        return None
    return os.path.abspath(filename)


def make_one_qr_code():
    """Do one round: ask, preview, save. Returns the saved path, or None."""
    text = ask_for_text()
    if text == "":
        print("Nothing was entered, so no QR code was created.")
        return None

    try:
        qr = build_qr_code(text)
    except ValueError:
        print("That text is too long to fit in a QR code. Try something shorter.")
        return None

    show_preview(qr)

    filename = ask_for_filename()
    if filename is None:
        print("No filename was entered, so nothing was saved.")
        return None

    path = save_qr_code(qr, filename)
    if path is not None:
        print("QR code saved to:", path)
    return path


def show_menu():
    print()
    print("1. Make a QR code")
    print("2. Quit")


def main():
    print("QR Code Generator")
    saved_files = []  # the full path of each image saved during this run

    try:
        while True:
            show_menu()
            choice = input("Choose 1 or 2: ").strip()

            if choice == "1":
                path = make_one_qr_code()
                if path is not None and path not in saved_files:
                    saved_files.append(path)
            elif choice == "2":
                break
            else:
                print("Please type 1 or 2.")
    except (KeyboardInterrupt, EOFError):
        print()  # Ctrl+C or Ctrl+D quits cleanly instead of showing an error

    if len(saved_files) > 0:
        print("Images saved this time:")
        for path in saved_files:
            print(" -", path)
    print("Goodbye!")


main()
