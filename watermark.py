import os

from PIL import Image


INPUT_DIRECTORY = 'input_images/'
OUTPUT_DIRECTORY = 'output_images/'
WATERMARK_FILE = 'watermark.png'


def clean_input_dir():
    """
    Clears files in INPUT_DIRECTORY
    """

    for file in os.listdir(OUTPUT_DIRECTORY):
        os.remove(OUTPUT_DIRECTORY + file)


def input_dir_files_handler():
    """
    Handles files in INPUT_DIRECTORY and calls watermark function
    """

    files_amount: int = len(os.listdir(INPUT_DIRECTORY))
    counter: int = 0

    for file in os.listdir(INPUT_DIRECTORY):
        counter += 1
        if file.endswith(('.jpg', '.png', 'jpeg')):
            watermark_with_transparency(file)
            print("{}% - '{}' is ready!".format(round(counter/files_amount * 100, 2), file))


def resize_watermark(image: Image) -> (int, int, Image):
    """
    Gets size of source image and resize watermark to this size
    :param image: source image
    :type image: Image
    :return: tuple of width, height of source image and resized watermark
    """

    width, height = image.size

    watermark = Image.open(WATERMARK_FILE)
    watermark = watermark.resize((height, height))

    return width, height, watermark


def put_transparency_mask(watermark: Image) -> Image:
    """
    Puts transparency mask to watermark (transparency effect)
    :param watermark: watermark
    :type watermark: Image
    :return: watermark with transparency mask
    """

    transparency_mask = watermark.convert('L').point(lambda x: min(x, 35))
    watermark.putalpha(transparency_mask)

    return watermark


def calculate_watermarks_amount_and_border(width: int, height: int) -> (int, int):
    """
    Calculates amount of watermarks and space between watermarks on image
    :param width: width of image/watermark
    :param height: height of image/watermark
    :returns: tuple of watermarks amount and space between watermarks
    """

    watermarks_amount: int = width // height
    width_border = int((width - (watermarks_amount * height)) / (watermarks_amount + 1))
    return watermarks_amount, width_border


def save_file_with_watermark(image: Image, file_name: str):
    """
    Saves file with watermark to OUTPUT_DIRECTORY
    :param image: image with watermark
    :param file_name: old filename for watermarked image
    :type image: Image
    :type file_name: str
    """

    image.save(OUTPUT_DIRECTORY + 'watermarked_' + file_name, 'png')


def watermark_with_transparency(file_name: str):
    """
    Draws watermark on file_name file
    :param file_name: main picture for drawing watermark
    :type file_name: str
    :return:
    """

    image = Image.open(INPUT_DIRECTORY + file_name).convert("RGBA")
    width, height, watermark = resize_watermark(image)
    watermark = put_transparency_mask(watermark)
    watermarks_amount, width_border = calculate_watermarks_amount_and_border(width, height)

    print("DEBUG: {} watermark(s) for '{}'".format(watermarks_amount, file_name))

    for cf in range(watermarks_amount):
        start_width = width_border + cf * (image.width // watermarks_amount)
        image.paste(watermark, (start_width, 0), mask=watermark)

    save_file_with_watermark(image, file_name)


def main():
    clean_input_dir()
    input_dir_files_handler()


if __name__ == '__main__':
    main()
