import os

from PIL import Image

INPUT_DIRECTORY = 'input_images/'
OUTPUT_DIRECTORY = 'output_images/'
WATERMARK_FILE = 'watermark.png'


def main():
    files_amount = len(os.listdir(INPUT_DIRECTORY))
    counter = 0

    for file in os.listdir(OUTPUT_DIRECTORY):
        os.remove(OUTPUT_DIRECTORY + file)

    for file in os.listdir(INPUT_DIRECTORY):
        counter += 1
        if file.endswith(('.jpg', '.png', 'jpeg')):
            watermark_with_transparency(file)
            print("{}% - '{}' is ready!".format(round(counter/files_amount * 100, 2), file))


def watermark_with_transparency(file_name):
    image = Image.open(INPUT_DIRECTORY + file_name).convert("RGBA")

    width, height = image.size

    watermark = Image.open(WATERMARK_FILE)
    watermark = watermark.resize((height, height))

    transparency_mask = watermark.convert('L').point(lambda x: min(x, 35))
    watermark.putalpha(transparency_mask)

    watermarks_amount = width // height

    print("DEBUG: {} watermark(s) for '{}'".format(watermarks_amount, file_name))

    width_border = int((width - (watermarks_amount * height)) / (watermarks_amount + 1))

    for cf in range(watermarks_amount):
        start_width = width_border + cf * (image.width // watermarks_amount)
        image.paste(watermark, (start_width, 0), mask=watermark)

    image.save(OUTPUT_DIRECTORY + 'watermarked_' + file_name, 'png')


if __name__ == '__main__':
    main()
