import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Use first GPU

import argparse
import logging
import sys
from image_handler import ImageHandler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process 2D Photos & Videos")
    parser.add_argument("--photo", type=str, help="a file path to a photo")

    args = parser.parse_args()
    photo_filename = args.photo

    if photo_filename:
        image_handler = ImageHandler(photo_filename)
        image_handler.make_3d_image()
    else:
        logging.info("Please add a photo or video if you want to see anything happen!")