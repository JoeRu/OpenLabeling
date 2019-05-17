import glob
import cv2
import logging
from lxml import etree
import xml.etree.cElementTree as ET
import os
import argparse


parser = argparse.ArgumentParser(description='Open-source image extracting tool')
parser.add_argument('-i', '--input_dir', default='output/PASCAL_VOC', type=str, help='Path to input directory of VOC Files')
parser.add_argument('-o', '--output_dir', default='output/tfImages', type=str, help='Path to output directory of cropped category Images')

args = parser.parse_args()
INPUT_DIR = args.input_dir
OUTPUT_DIR = args.output_dir
######### Debug and Log-Preparations

# create logger with 'spam_application'
logger = logging.getLogger('voc-to-tf')
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

logger.info('Input Directory: {}'.format(INPUT_DIR))
logger.info('Output Directory: {}'.format(OUTPUT_DIR))

search =  os.path.join(INPUT_DIR,'*.xml')
for filename in glob.glob(search):
#    logger.info(filename)
    tree = ET.parse(filename)
    for e in tree.findall('.//path'):
        logger.debug('Filename: {}'.format(e.text))
        img_path = e.text
    #load-image
    img = cv2.imread(img_path)
    counter = 1
    #extract every bndbox
    for e in tree.findall('.//object'):
#        logger.debug(e.find('name').text)
            kategorie = e.find('name').text
            #./name == Kategorie
            #Folder existent - create
            cat_dir = os.path.join(OUTPUT_DIR,kategorie)
            try:
                os.makedirs(cat_dir)
            except FileExistsError:
                # directory already exists
                pass
            except OSError as dir_error:
                logger.error(dir_error)

            #read box-size
            bndbox = e.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            x_width = xmax - xmin
            y_height = ymax - ymin
            logger.debug("Object: {} Size - xmin {} - ymin {} - xmax {} - ymax {}".format(kategorie, xmin, ymin, xmax, ymax))

            #crop image to new
            crop_img = img[ymin:ymax, xmin:xmax]
#            cv2.imshow("cropped", crop_img)
#            cv2.waitKey(0)
            #save new cropped image
            fileName,fileExtension = os.path.splitext(img_path)
            path,fileName = os.path.split(fileName)
            exportName = fileName + '_' + str(counter) + fileExtension
            logger.debug("newName: {} fileExtension {} - Filename {}".format(exportName, fileExtension, fileName ))
            abs_out_file = os.path.join(cat_dir, exportName)
            cv2.imwrite(abs_out_file,crop_img)
            counter = counter + 1
