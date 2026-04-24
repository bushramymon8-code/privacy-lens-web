import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import piexif
import os
import csv
import json

class PrivacyTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Privacy Lens Pro")
        self.root.geometry("750x550")

        self.files = []

        # Buttons
        tk.Button(root, text="Select Images", command=self.select_images).pack(pady=5)
        tk.Button(root, text="Scan Metadata", command=self.scan_metadata).pack(pady=5)
        tk.Button(root, text="Remove Metadata", command=self.remove_metadata).pack(pady=5)
        tk.Button(root, text="Export Report (CSV)", command=self.export_csv).pack(pady=5)

        # Listbox
        self.listbox = tk.Listbox(root, width=90)
        self.listbox.pack(pady=10)

        # Output box
        self.text = tk.Text(root, height=15, width=90)
        self.text.pack()

    # Select multiple images
    def select_images(self):
        self.files = filedialog.askopenfilenames(
            filetypes=[("Images", "*.jpg *.jpeg *.png")]
        )
        self.listbox.delete(0, tk.END)

        for f in self.files:
            self.listbox.insert(tk.END, f)

    # Scan metadata
    def scan_metadata(self):
        self.text.delete(1.0, tk.END)

        for file in self.files:
            try:
                img = Image.open(file)
                exif_data = img.info.get("exif")

                self.text.insert(tk.END, f"\nFILE: {file}\n")

                if exif_data:
                    data = piexif.load(exif_data)

                    risk = "LOW Risk"

                    for ifd in data:
                        for tag in data[ifd]:
                            value = data[ifd][tag]

                            # Simple risk check (GPS or camera info)
                            if "GPS" in str(ifd):
                                risk = "HIGH Risk"

                            self.text.insert(tk.END, f"{tag}: {value}\n")

                    self.text.insert(tk.END, f"RISK LEVEL: {risk}\n")

                else:
                    self.text.insert(tk.END, "No metadata found Medium Risk\n")

            except Exception as e:
                self.text.insert(tk.END, f"Error: {e}\n")

    # Remove metadata
    def remove_metadata(self):
        for file in self.files:
            try:
                img = Image.open(file)
                clean = Image.new(img.mode, img.size)
                clean.putdata(list(img.getdata()))

                new_path = file.replace(".jpg", "_clean.jpg")
                clean.save(new_path)

            except:
                pass

        messagebox.showinfo("Done", "Metadata Removed Successfully!")

    # Export CSV report
    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["File", "Status"])

            for file in self.files:
                writer.writerow([file, "Checked"])

        messagebox.showinfo("Exported", "CSV Report Saved!")

# Run app
root = tk.Tk()
app = PrivacyTool(root)
root.mainloop()