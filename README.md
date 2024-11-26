# Short Description (TLDR) Convert Images
This project is a Python-based GUI tool for converting image files, including HEIC, to JPG format. It provides an intuitive interface for directory selection, image preview, and batch conversion.

# Image Converter - Convert HEIC, JPG, PNG, WEBP to JPG, PNG, 
## Overview
This is a Python application with a graphical user interface (GUI) built using `tkinter` and `Pillow`. The tool allows users to select a directory, preview image files, and convert them (including HEIC format) to JPG with ease. 

## Features
- **Directory Browsing:** Easily select a folder to process images.
- **Image Preview:** Preview selected images in the GUI.
- **Batch Conversion:** Convert multiple HEIC and other supported image formats to JPG.
- **Progress Tracking:** Displays a progress bar during the conversion process.
- **Error Handling:** Provides alerts for invalid files or processing errors.

# Prerequisites
- Python 3.8+
- Required Libraries:
  - `Pillow`
  - `pillow_heif`
  - `tkinter` (standard with Python)

## Installation
1. Clone the repository:
    ```
    bash
    git clone https://github.com/andre0341/image-converter.git
    cd image-converter
    ```

## 2. Install dependencies:
    ```
    bash
    pip install pillow pillow_heif
    ```

## Usage
    ```
    bash python convert_img_files_OK.py
    ```

Use the "Select Directory" button to choose a folder containing image files.
Select images from the listbox and click "Convert to JPG".
Monitor the progress bar and view conversion status.

# Development Notes
UI Design: The application uses tkinter for GUI elements, ensuring a lightweight and responsive interface.
HEIC Support: Added via pillow_heif for decoding HEIC files.
Error Management: Handles missing files, unsupported formats, and general conversion errors gracefully.

## 📌Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📌Author

👤 ** andre0341 **

- Github: [@kishanrajput23](https://github.com/andre0341)

## 📌Show your support

Please ⭐️ this repository if this project helped you!

## 📌License

This project hasn't been licensed yet.


