import os
import sys
import requests
import uuid
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

# Read environment variables
BORDER_TOP = int(os.getenv("BORDER_TOP", 100))
BORDER_LEFT = int(os.getenv("BORDER_LEFT", 100))
BORDER_RIGHT = int(os.getenv("BORDER_RIGHT", 100))
BORDER_BOTTOM = int(os.getenv("BORDER_BOTTOM", 190))
BORDER_COLOR_R = int(os.getenv("BORDER_COLOR_R", 255))
BORDER_COLOR_G = int(os.getenv("BORDER_COLOR_G", 255))
BORDER_COLOR_B = int(os.getenv("BORDER_COLOR_B", 255))
TEXT = os.getenv("TEXT", "ISO 600; 1/12s, 2.1f")
TEXT_COLOR_R = int(os.getenv("TEXT_COLOR_R", 0))
TEXT_COLOR_G = int(os.getenv("TEXT_COLOR_G", 0))
TEXT_COLOR_B = int(os.getenv("TEXT_COLOR_B", 0))
FONT_SIZE = int(os.getenv("FONT_SIZE", 20))


def process_image(img):
    # Calculate the new height for the portrait aspect ratio (3:4)
    new_height = int(img.width * 4 / 3)

    # Crop the image to the new aspect ratio
    img = img.crop((0, 0, img.width / 2.5, new_height / 2.5))

    # Save the cropped image with a border
    img_with_border = Image.new(
        'RGB',
        (img.width + BORDER_LEFT + BORDER_RIGHT,
         img.height + BORDER_TOP + BORDER_BOTTOM),
        (BORDER_COLOR_R, BORDER_COLOR_G, BORDER_COLOR_B)
    )
    img_with_border.paste(img, (BORDER_LEFT, BORDER_TOP))

    # Add the text
    draw = ImageDraw.Draw(img_with_border)
    font = ImageFont.truetype("RobotoSlab-Medium.ttf", FONT_SIZE)
    text_width = draw.textlength(TEXT, font=font)
    text_x = (img_with_border.width - text_width) // 2
    draw.text((text_x, img_with_border.height -
               BORDER_BOTTOM + 15), TEXT, font=font, fill=(TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B))

    return img_with_border


def download_image(image_url, image_filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded image: {image_filename}")
        return True
    else:
        print(f"Error downloading image")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Process images in demo or production mode.")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--prod", action="store_true",
                        help="Run in production mode")
    args = parser.parse_args()

    if not args.demo and not args.prod:
        print("Please specify either --demo or --prod flag.")
        sys.exit(1)

    if args.demo and args.prod:
        print("Please specify only one mode using either --demo or --prod flag.")
        sys.exit(1)

    if args.demo:
        print("Running in demo mode...")
        image_source_folder = "demoImg"
    else:
        print("Running in production mode...")
        image_source_folder = "img"

    if args.prod:

        if not os.path.exists('img') or not  os.listdir('img'):
            print(f"Please provide images im folder 'img' ")

        existing_images = os.listdir('img')
        for image_file in existing_images:
            try:
                timestamp = datetime.now().strftime("%M%S")
                image_filename = f"img/{image_file[:len(image_file) - 4]}_{timestamp}.png"

                # In production mode, copy images from the image_source_folder
                source_image_path = os.path.join(
                    image_source_folder, image_file)
                img = Image.open(source_image_path)
                img_with_border = process_image(img)
                img_with_border.save(image_filename)
                print(
                    f"Processed image: {source_image_path}")

                # Pause for 1 second between processing to simulate production load
                time.sleep(1)

            except Exception as e:
                print(f"Error occurred: {e}")
    else:
        num_images = 5
        # Create the "img" folder if it doesn't exist
        if not os.path.exists('demoImg'):
            os.makedirs('demoImg')

        # Delete all existing images in the "img" folder
        existing_images = os.listdir('demoImg')
        for image_file in existing_images:
            image_path = os.path.join('demoImg', image_file)
            os.remove(image_path)
            print(f"Deleted existing image: {image_path}")

        for i in range(num_images):
            try:

                image_id = str(uuid.uuid4())
                timestamp = datetime.now().strftime("%M%S")
                image_url = f"https://picsum.photos/1920/1080?random={i}"
                image_filename = f"demoImg/{image_id}_{timestamp}.png"

                # In demo mode, download and process images from the internet
                if download_image(image_url, image_filename):
                    img = Image.open(image_filename)
                    img_with_border = process_image(img)
                    img_with_border.save(image_filename)
                    print(
                        f"Processed image {i + 1}/{num_images}: {image_filename}")

                # Pause for 1 second between processing to avoid server load
                time.sleep(1)

            except Exception as e:
                print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
