import os
import imghdr
import tkinter as tk
from tkinter import filedialog, Label, Button, Listbox, messagebox, Scrollbar, Frame
from tkinter.ttk import Progressbar, Style
from PIL import ImageTk, Image, UnidentifiedImageError
import pillow_heif

# Define background color
bg_color = '#fcfcfc'
bg_color2 = '#fcfcfc'
progress_bar_color = '#c2c2c2'
# Function to dynamically display additional UI elements
def show_main_ui():
    # Path label
    label_path.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Frame for Listbox and Scrollbar
    listbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Convert button
    button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    # Progress bar
    progress.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Status label for messages
    status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Image label for preview
    image_label.grid(row=0, column=2, rowspan=6, padx=10, pady=10, sticky="nsew")

    win.grid_rowconfigure(2, weight=1)
    win.grid_columnconfigure(2, weight=1)

# Function to hide additional UI elements initially
def hide_main_ui():
    label_path.grid_remove()
    listbox_frame.grid_remove()
    button.grid_remove()
    progress.grid_remove()
    status_label.grid_remove()
    image_label.grid_remove()

# WINDOW CREATION
win = tk.Tk()
win.title("Convert img 2 JPG")
win.geometry("800x600+200+200")
win['bg'] = bg_color

# Define a style for the progress bar
style = Style(win)
style.theme_use('default')
style.configure("red.Horizontal.TProgressbar", troughcolor=bg_color, background=progress_bar_color, borderwidth=0)

# Directory selection button
dialog_btn = Button(win, text='Select Directory', command=lambda: directory(), bg='white', fg="#000")
dialog_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Path label
label_path = Label(win, font=('italic 14'), bg=bg_color)

# Frame for Listbox and Scrollbar
listbox_frame = Frame(win, bg=bg_color)

# Listbox for file list
lbox = Listbox(listbox_frame, selectmode=tk.EXTENDED)
lbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for Listbox
scrollbar = Scrollbar(listbox_frame, orient="vertical")
scrollbar.config(command=lbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
lbox.config(yscrollcommand=scrollbar.set)

# Convert button
button = Button(win, text="Convert to JPG", command=lambda: convert2jpg(lbox), bg='white')

# Progress bar with red background
progress = Progressbar(win, orient=tk.HORIZONTAL, length=100, mode='determinate', style="red.Horizontal.TProgressbar")

# Status label for messages
status_label = Label(win, text="", font=('italic 12'), bg=bg_color)

# Image label for preview
image_label = Label(win, bg=bg_color)

# Hide additional UI elements initially
hide_main_ui()

def directory():
    # Clear existing Listbox items
    lbox.delete(0, tk.END)
    # Remove the previous image label if it exists
    image_label.config(image='')
    status_label.config(text='')

    # get a directory path by user
    global filepath
    filepath = filedialog.askdirectory(initialdir=r"/Users/andre/Pictures/", title="Dialog box")

    # If the user cancels the directory selection, filepath will be empty
    if not filepath:
        return

    # Show main UI elements after directory is selected
    show_main_ui()

    label_path.config(text=filepath)
    os.chdir(filepath)

    # get the list of files
    flist = os.listdir()

    # Filter and insert only image files, including HEIC
    image_files = []
    for item in flist:
        if os.path.isfile(os.path.join(filepath, item)):
            # Check if the file is a known image format or a HEIC file
            if imghdr.what(os.path.join(filepath, item)) or item.lower().endswith('.heic'):
                image_files.append(item)
    
    for item in image_files:
        lbox.insert(tk.END, item)
    
    # Force update the GUI to show the files immediately
    win.update_idletasks()

    # Select and preview the first image file if available
    if image_files:
        lbox.selection_set(0)
        showContent(None)

    # BINDING OF LISTBOX lbox
    lbox.bind("<<ListboxSelect>>", showContent)

def showContent(event):
    try:
        # Get the first selected file for preview
        x = lbox.curselection()[0]
        file = lbox.get(x)
        file_path = os.path.join(filepath, file)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file} does not exist.")
        
        # Open the image file
        if file.lower().endswith('.heic'):
            img = pillow_heif.read_heif(file_path)
            img = Image.frombytes(
                img.mode, 
                img.size, 
                img.data,
                "raw",
                img.mode,
                img.stride
            )
        else:
            img = Image.open(file_path)

        # Resize the image while maintaining aspect ratio
        img.thumbnail((image_label.winfo_width(), image_label.winfo_height()), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        
        # Update the Label Widget to display the image
        image_label.config(image=img)
        image_label.image = img  # Keep a reference to avoid garbage collection
    except FileNotFoundError as fnf_error:
        messagebox.showerror("Error", str(fnf_error))
        lbox.delete(x)
    except UnidentifiedImageError:
        messagebox.showerror("Error", "Selected file is not a valid image.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying the image: {e}")

def convert2jpg(lbox):
    try:
        selected_files = lbox.curselection()
        if not selected_files:
            status_label.config(text="Error: No files selected for conversion.")
            return
        
        progress['value'] = 0
        progress['maximum'] = len(selected_files)
        
        for index, selected in enumerate(selected_files):
            file = lbox.get(selected)
            file_path = os.path.join(filepath, file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file} does not exist.")
            
            if file.lower().endswith('.heic'):
                img = pillow_heif.read_heif(file_path)
                img = Image.frombytes(
                    img.mode, 
                    img.size, 
                    img.data,
                    "raw",
                    img.mode,
                    img.stride
                )
            else:
                img = Image.open(file_path)
            
            img = img.convert("RGB")
            img.save(os.path.join(filepath, os.path.splitext(file)[0] + ".jpg"), "JPEG")
            progress['value'] = index + 1
            win.update_idletasks()
        
        status_label.config(text="Success: Selected images successfully converted to JPG.")
    except FileNotFoundError as fnf_error:
        messagebox.showerror("Error", str(fnf_error))
        lbox.delete(selected)
    except UnidentifiedImageError:
        messagebox.showerror("Error", "One or more selected files are not valid images.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the conversion: {e}")

win.mainloop()
