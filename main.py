from func import *
import argparse

# python main.py --baseroot <your_image_baseroot> --save_dir <save_path>

## setup arguments
parser = argparse.ArgumentParser(description='Threshold-based mask algorithm')

## Path
parser.add_argument('--baseroot', type=str, default='./STEMimg/', help='path to the dataset directory')
parser.add_argument('--save_dir', type=str, default='./STEMimg_results/', help='saves results here')

## setting
parser.add_argument('--segmentation', default=False, help='4 corner segmentation of image') # Use 'True' or 'False' if you want to split the image
parser.add_argument('--img_fill', default=True, help='Refill extracted pixel values') # Use 'True' or 'False' if you want to refill the pixels
parser.add_argument('--img_show', default=False, help='Show the image') # Use 'True' or 'False' if you want to show the figure
parser.add_argument('--save_fig', default=True, help='Save the figure') # Use 'True' or 'False' if you want to save the figure
parser.add_argument('--threshold', type=int, default=200, help='threshold setting')


if __name__ == "__main__":
    args = parser.parse_args()
    args.baseroot = os.path.expanduser(args.baseroot)
    args.save_dir = os.path.expanduser(args.save_dir)

    main(args)