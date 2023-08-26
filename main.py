import os
import requests
import uuid
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Create the "img" folder if it doesn't exist
if not os.path.exists('img'):
    os.makedirs('img')

# Delete all existing images in the "img" folder
existing_images = os.listdir('img')
for image_file in existing_images:
    image_path = os.path.join('img', image_file)
    os.remove(image_path)
    print(f"Deleted existing image: {image_path}")

# Number of images to be downloaded
num_images = 5

for i in range(num_images):
    try:
        # Generate a random UUID for the ID
        image_id = str(uuid.uuid4())

        # Generate the timestamp in the format MMSS
        timestamp = datetime.now().strftime("%M%S")

        # Lorem Picsum API URL for a random image
        image_url = f"https://picsum.photos/1920/1080?random={i}"

        # Adjust the filename accordingly (ID_timestamp.png)
        image_filename = f"img/{image_id}_{timestamp}.png"

        # Download the image from the API URL
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded image {i+1}/{num_images}: {image_filename}")

            # Open the image using Pillow
            img = Image.open(image_filename)

            # Calculate the new height for the portrait aspect ratio (3:4)
            new_height = int(img.width * 4 / 3)

            # Crop the image to the new aspect ratio
            img = img.crop((0, 0, img.width / 2.5, new_height / 2.5))

            # Save the cropped image
            # Add a 1 cm white border
            top_border = left_border = right_border = 100  # 1 cm in pixels
            bottom_border = 190  # Slightly larger bottom border
            border_color = (255, 255, 255)  # White color
            img_with_border = Image.new(
                'RGB',
                (img.width + left_border + right_border,
                 img.height + top_border + bottom_border),
                border_color
            )
            img_with_border.paste(img, (left_border, top_border))

            # Add the text
            draw = ImageDraw.Draw(img_with_border)
            text = "ISO 600; 1/12s, 2.1f"
            text_color = (0, 0, 0)  # Black color for the text

            # Load a font and define font size
            font_size = 20
            font = ImageFont.truetype("RobotoSlab-Medium.ttf", font_size)

            # Calculate the position of the text at the bottom border
            text_width = draw.textlength(text, font=font)
            text_x = (img_with_border.width - text_width) // 2

            # Draw the text on the image
            draw.text((text_x, img_with_border.height -
                       bottom_border + 15), text, font=font, fill=text_color)

            # Save the image with the border
            img_with_border.save(image_filename)
            print(f"Cropped image saved: {image_filename}")

        else:
            print(f"Error downloading image {i+1}/{num_images}")

        # Pause for 1 second between downloads to avoid server load
        time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
