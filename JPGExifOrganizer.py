# Author: Sebastian Torres
# Date: January 8, 2024
# Description: This script organizes a folder of files of type JPG based off it's metadata('imageDescription')

import tkinter as tk 
from tkinter import filedialog
import os 
from reportlab.pdfgen import canvas
from PIL import Image
from PIL.ExifTags import TAGS
import shutil

class JPGExifOrganizer:
    def __init__(self,root):
        self.root = root
        self.folder_path = ""
        self.output_folder_name = tk.StringVar()
        self.output_folder_status = tk.StringVar()
        self.input_folder_status = tk.StringVar()
        self.completion_status = tk.StringVar()
        self.initialize_ui()

    def rename_file(self):
        if not self.folder_path:
            print("Please select a folder first.")
            self.input_folder_status.set("Please select a folder first.")
            return

        new_folder_path = self.folder_path.replace('/', '\\')
        output_folder = self.output_folder_status.get()
        if not output_folder:
            print("Please create an output folder first.")
            return

        output_folder_path = output_folder.split(": ")[-1]  # Extracting folder path from the status string
        if not os.path.exists(output_folder_path):
            print("Output folder does not exist.")
            return

        os.chdir(self.folder_path)
        for f in os.listdir():
            self.completion_status.set("One Moment while your files are organized")
            f_name, f_ext = (os.path.splitext(f))
            if f_ext == ".JPG":
                image = Image.open(os.path.join(new_folder_path, f))
                exif = {}
                for tag, value in image._getexif().items():
                    if tag in TAGS:
                        exif[TAGS[tag]] = value
                if 'ImageDescription' in exif:
                    imgDesc = exif['ImageDescription']
                new_imgDesc = imgDesc.replace('\n', ' ').replace('<', '_').replace('>', '_').replace(':', '').replace('"', '').replace('\\','_').replace('/','_').replace('|','_').replace('*','').replace('?','')
                new_file = ('{}-{}{}').format(new_imgDesc, f_name, f_ext)

                image.close()
                shutil.copy(f, os.path.join(output_folder_path, new_file))
            else:
                print(f"{f} is not a jpg file.")
                shutil.copy(f,output_folder_path)
                
        print("Files organized into the output folder.")
        self.completion_status.set("Files were successfully organized into the output folder.")


    def select_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select Folder")
        self.input_folder_status.set(self.folder_path)
        print(self.folder_path)
        
    def create_output_file(self):
        if self.folder_path:
            parent_folder = os.path.dirname(self.folder_path)
            output_folder = os.path.join(parent_folder, self.output_folder_name.get())
            if os.path.exists(output_folder):
                index = 1
                while True:
                    new_output_folder = f"{self.output_folder_name.get()}_{index}"
                    output_folder = os.path.join(parent_folder, new_output_folder)
                    if not os.path.exists(output_folder):
                        break
                    index += 1
            os.makedirs(output_folder)
            print(f"Output folder created: {output_folder}")
            self.output_folder_status.set("Output folder created: "+output_folder)
        else:
            print("Please select a folder first.")
            self.output_folder_status.set("Please enter a folder name.")

    def initialize_ui(self):
        self.root.configure(bg='#161A30')
        title_label = tk.Label(self.root, text="JPG Exif Organizer", font=('Helvetica',20,"bold"),fg="#B6BBC4",bg='#161A30')
        title_label.pack(pady=10)

        instructions_text = tk.Text(self.root, height=7, width=50, font=('Helvetica',10,),fg="white",bg='#161A30',highlightthickness=0, bd=0)
        instructions_text.insert(tk.END, "Instructions:\n\n")
        instructions_text.insert(tk.END, "Step 1: Select the input folder containing JPG files.\n")
        instructions_text.insert(tk.END, "Step 2: Enter a name for the output folder.\n")
        instructions_text.insert(tk.END, "Step 3: Click the create output folder.\n")
        instructions_text.insert(tk.END, "Step 4: Click the button below to organize files to new folder.\n")

        instructions_text.tag_configure("center", justify="center")
        instructions_text.tag_add("center", "1.0", "1.end")

        instructions_text.config(state=tk.DISABLED) 
        instructions_text.pack(pady=(0,10))

        input_file_prompt = tk.Label(self.root, text="Select Input Folder: ", font=('Helvetica',12),fg="white",bg='#161A30',highlightthickness=0, bd=0)
        input_file_prompt.pack(pady=(0,10))

        input_folder_status_label = tk.Label(self.root, textvariable=self.input_folder_status, font=('Helvetica',9),fg="white",bg='#161A30',highlightthickness=0, bd=0)
        input_folder_status_label.pack(pady=(0,10))

        select_folder_button = tk.Button(self.root,text="Select Folder", command=self.select_folder,font=('Helvetica',10),fg="white",bg='#161A30',highlightbackground='black')
        select_folder_button.pack(pady=(0,10))

        output_file_prompt = tk.Label(self.root, text="Enter Output Folder Name: ", font=('Helvetica',12),fg="white",bg='#161A30',highlightthickness=0, bd=0)
        output_file_prompt.pack(pady=(0,10))

        output_file_entry = tk.Entry(self.root, textvariable=self.output_folder_name, width=40, justify='center',fg="white",bg='#161A30',highlightbackground='black')
        output_file_entry .pack(pady=(0,10))

        create_output_file_button = tk.Button(self.root, text= "Create Output File", command=self.create_output_file ,font=('Helvetica',11),fg="white",bg='#161A30',highlightbackground='black')
        create_output_file_button.pack(pady=(0,10))

        output_folder_status_label = tk.Label(self.root, textvariable=self.output_folder_status, font=('Helvetica',9),fg="white",bg='#161A30',highlightthickness=0, bd=0)
        output_folder_status_label.pack(pady=(0,10))

        rename_button = tk.Button(self.root,text="Organize Files", command=self.rename_file,font=('Helvetica',10),fg="white",bg='#161A30',highlightbackground='black')
        rename_button.pack(pady=(20,40))

        completion_status_label=tk.Label(self.root, textvariable=self.completion_status,font=('Helvetica',9),fg="white",bg='#161A30',highlightthickness=0, bd=0)
        completion_status_label.pack(pady=(0,10))

def main(): 
    root=tk.Tk()
    root.title("JPG Exif Organizer")
    rename = JPGExifOrganizer(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()







