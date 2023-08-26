# Image Processing Script

This Python script is designed to download random images from the internet, crop them, add a white border with text, and save the processed images. It's a demonstration of using various image processing techniques using the Pillow library.

## Features

- Downloads random images from the internet using the Lorem Picsum API.
- Crops the images to a custom aspect ratio.
- Adds a white border with customizable size.
- Embeds text with customizable content and font.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Montralis/adaptive-color-frame.git
   cd image-processing-script
   ```

2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```


## Usage
1. Run the script:
   ```bash
    python main.py
   ```

2. The script will download random images, process them, and save the results in the "img" folder.

3. Adjust the parameters in the script to customize the cropping, border, and text.

## Parameters
You can customize the following parameters in the script:

- `num_images`: Number of images to download and process.
- `left_border`, `top_border`, `right_border`, `bottom_border`: Border sizes in pixels.
- `text`: Text to be added to the image.
- `font_size`: Size of the font used for the text.

## Notes
- The script uses the Pillow library for image processing. Make sure you have it installed.
- You can replace the font with your preferred font by providing the correct font file path.
- Images are downloaded from the Lorem Picsum API. You can replace it with other image sources if desired.

## Notes
This project is licensed under the MIT License. Feel free to modify and use it for your own purposes.

For issues or suggestions, please [open an issue](https://github.com/Montralis/adaptive-color-frame/issues).
