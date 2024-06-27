import re
import csv
import os
import tkinter as tk

output_file = "Abomination.csv"

def extract_numbers_from_clipboard():
    try:
        text = root.clipboard_get()
    except tk.TclError:
        # If clipboard is empty or not text, ignore
        root.after(1000, extract_numbers_from_clipboard)
        return
    
    patterns = {
        "Item Quantity": r"(?<=Item Quantity: \+)\d+",
        "Item Rarity": r"(?<=Item Rarity: \+)\d+",
        "Monster Pack Size": r"(?<=Monster Pack Size: \+)\d+",
        "More Scarabs": r"(?<=More Scarabs: \+)\d+",
        "More Maps": r"(?<=More Maps: \+)\d+",
        "More Currency": r"(?<=More Currency: \+)\d+"
    }

    results = []
    found_any = False

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            results.append(match.group(0))
            found_any = True
        else:
            results.append("0")

    if found_any:
        result_text = "\n".join(results)
        root.clipboard_clear()
        root.clipboard_append(result_text)

        write_to_csv(results)

    root.after(1000, extract_numbers_from_clipboard)  # Check clipboard every second

def write_to_csv(data):
    file_exists = os.path.isfile(output_file)
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Item Quantity", "Item Rarity", "Monster Pack Size", "More Scarabs", "More Maps", "More Currency"])
        writer.writerow(data)

# Set up the main window
root = tk.Tk()
root.withdraw()  # Hide the main window as we don't need any UI

# Start monitoring the clipboard
root.after(1000, extract_numbers_from_clipboard)
root.mainloop()
