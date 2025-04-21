# Image Watermark App

A user-friendly desktop application for adding watermarks to your images, with support for both text and image watermarks.

![image](https://github.com/user-attachments/assets/c8259f57-13cd-426d-a79d-043de946a0dc)


## Features

- Add text or image watermarks to your photos
- Customize watermark position, opacity, and color
- Preview watermark before applying
- Save watermarked images in various formats (PNG, JPG)
- Simple and intuitive interface

## Requirements

- Python 3.7+
- Pillow (PIL) library
- ttkbootstrap library
- tkinter (usually included with Python)

## Installation

1. Clone this repository or download the source files
2. Install the required dependencies:

```bash
pip install pillow ttkbootstrap
Run the application:

bash
python watermarkUI.py
Usage
Select an Image: Click "Select Image" to choose the image you want to watermark

Choose Watermark Type:

For text watermarks: Enter your text and customize font settings

For image watermarks: Select your watermark image file

Adjust Settings:

Position: Choose where the watermark appears

Opacity: Set how transparent the watermark should be

Color: Select a color for text watermarks

Font: Choose font family and size (for text watermarks)

Preview: Click "Preview Watermark" to see how it will look

Save: Click "Apply and Save" to save your watermarked image

File Structure
watermarkUI.py - Main application GUI built with tkinter/ttkbootstrap

watermarkLogic.py - Core watermarking functionality using PIL

Customization
You can modify the default settings in the load_default_preferences() method in watermarkUI.py:

python
default_prefs = {
    "watermark_text": "Your Watermark",
    "position": "Bottom Right",
    "font": "Arial",
    "font_size": 30,
    "opacity": 80,
    "color": "white",
    "watermark_type": "Text"
}
Known Limitations
Limited font selection (uses system fonts)

Watermark image is automatically scaled to 30% of the original image size

Preview window doesn't show the exact final size

License
This project is open source and available under the MIT License.
