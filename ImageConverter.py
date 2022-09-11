import os
import tkinter as tk
from PIL import Image
from tkinter import filedialog
from pillow_heif import register_heif_opener

# All supported files to convert from
FILE_TYPES = [
    (('PNG Files'),('*.png')),
    (('JPG Files'),('*.jpg', "*.jpeg")),
    (('WEBP Files'), ("*.webp")),
    (('HEIF Files'), ('*.heif', '*.heic'))
]

# Supported files to convert to
CONVERSION = ["ico", "png", "jpeg", "webp"]

class Converter:

    # Default constructor for fields
    def __init__(self):
        # Setup root panel
        self.root = tk.Tk()
        self.root.title('Image Converter')
        self.root.geometry('300x200')

        # fields used by multiple methods
        
        # Label for indicating state of program
        self.file_label = tk.Label(self.root,text='', font='Calibri',fg='Blue')
        
        # Selected type from dropdown menu
        self.type = tk.StringVar(self.root)
        self.type.set(CONVERSION[0])

        # Submit button to convert
        self.submit = tk.Button( self.root, text="Submit", command=self.convert, state= tk.DISABLED )

    # Pack and run loop
    def main(self):
        # Pack all the components
        self.file_label.pack()
        tk.Button(self.root, text='Choose Image', command=self.dir_dialog).pack()
        tk.OptionMenu(self.root, self.type, *CONVERSION ).pack()
        self.submit.pack()
        # Main loop
        self.root.mainloop()

    # Open current directory to select a image file
    def dir_dialog(self):

        # Open file dialogue
        self.root.filename = filedialog.askopenfilename(initialdir='.', title='Select an image file', filetypes= FILE_TYPES )
        # Check if a file is opened
        # No file
        if(self.root.filename == ''):
            self.file_label.config(text="No File Selected")
            self.submit.config(state= tk.DISABLED)
        # Opened file
        else:
            file_name = os.path.basename(self.root.filename)
            self.file_label.config(text= file_name)
            self.submit.config(state= tk.NORMAL)

    # Logic for converting between the file types
    def convert(self):

            full_file = os.path.basename(self.root.filename)
            file_name = full_file.split('.')[0]
            ext = full_file.split('.')[-1].lower()
            type = self.type.get()

            # Check for RGBA compatibility
            if((ext == "png" or ext == "webp") and type != "jpeg"):
                img = Image.open(self.root.filename)
            # Not compatible
            else:
                img = Image.open(self.root.filename).convert("RGB")
            
            # Save in current directory
            img.save(file_name + "." + type , type)
            self.file_label.config(text="File Converted!")

# Initialize and run main program
if __name__ == '__main__':

    # plugin for heif and heic support
    register_heif_opener()

    Main = Converter()
    Main.main()