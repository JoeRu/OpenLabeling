import glob
import cv2
import logging
from lxml import etree
import xml.etree.cElementTree as ET
import os
import argparse


parser = argparse.ArgumentParser(description='Open-source image extracting tool')
parser.add_argument('-i', '--input', default='output/tfImages/', type=str, help='Path to images (inkl subdirs)')
parser.add_argument('-g', '--glob', default='*.jpg', type=str, help='Path to output directory of cropped category Images')

args = parser.parse_args()
INPUT = args.input
GLOB = args.glob
######### Debug and Log-Preparations

# create logger with 'spam_application'
logger = logging.getLogger('img-to-yolo')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.ERROR)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Input Directory: {}, glob: {}'.format(INPUT, GLOB))

search =  os.path.join(INPUT,GLOB)
counter = 0
subdir_pref = 'xxx'
for subdir, dirs, files in os.walk(INPUT):
    if subdir_pref == 'xxx':
        subdir_pref = subdir

    if subdir != subdir_pref:
        subdir_pref = subdir
        counter = counter + 1

    obj_class =  counter - 1
    for file in files:
        logger.debug('ObjectClass: {}, Pfad: {}, Datei: {}'.format(str(obj_class), subdir, file))
    #load-image
#    img = cv2.imread(img_path)
#    height, width, channels = img.shape
        fileName,fileExtension = os.path.splitext(file)
        newFileName = os.path.join(subdir,str(fileName+'.txt'))

        xfile = open(newFileName,"w")
        xfile.write("{} 1.0 1.0 1.0 1.0".format(str(obj_class)))
        xfile.close
    #calculate yolo Size
    """
    <class_number> (<absolute_x> / <image_width>) (<absolute_y> / <image_height>) (<absolute_width> / <image_width>) (<absolute_height> / <image_height>)
    ie:
    0 (30/360) (40/480) (200/360) (200/480)
    0 1.0 1.0 1.0 1.0
    0 0.0833 0.0833 0.556 0.417
    """
