from PIL import Image
import os

INPUT_DIRECTORY = 'input_images/'
OUTPUT_DIRECTORY = 'output_images/'
WATERMARK_FILE = 'watermark.png'


def main():
    for file in os.listdir(OUTPUT_DIRECTORY):
        os.remove(OUTPUT_DIRECTORY + file)

    for file in os.listdir(INPUT_DIRECTORY):
        if file.endswith(('.jpg', '.png')):
            watermark_with_transparency(file)
            print(file, 'is ready')


def watermark_with_transparency(file_name):
    image = Image.open(INPUT_DIRECTORY + file_name).convert("RGBA")

    watermark = Image.open(WATERMARK_FILE)
    watermark = watermark.resize(image.size)

    transparency_mask = watermark.convert('L').point(lambda x: min(x, 30))
    watermark.putalpha(transparency_mask)

    file_name = file_name.replace('jpg', 'png')
    Image.alpha_composite(image, watermark).save(OUTPUT_DIRECTORY + 'watermarked_' + file_name, 'png')


if __name__ == '__main__':
    main()
