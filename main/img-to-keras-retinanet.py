import glob
import cv2
import logging
from lxml import etree
import xml.etree.cElementTree as ET
import os
import argparse

category1 = { 'bee': '0', 'wasp': '1', 'hornet': '2'}


parser = argparse.ArgumentParser(description='Open-source image extracting tool')
parser.add_argument('-i', '--input_dir', default='output/PASCAL_VOC', type=str, help='Path to input directory of VOC Files')
parser.add_argument('-o', '--output', default='output/Annotations.csv', type=str, help='Annotations.csv for https://github.com/fizyr/keras-retinanet')
parser.add_argument('-b', '--imagebasepath', default='input', type=str, help='Complete path of Input Directory of Images to fix potential movements')


args = parser.parse_args()
INPUT_DIR = args.input_dir
OUTPUT = args.output
BASEPATH = args.imagebasepath
######### Debug and Log-Preparations

# create logger 
logger = logging.getLogger('img-to-keras-retinanet')
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
#ch.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.ERROR)

# create formatter and add it to the handlers
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Input Directory: {}'.format(INPUT_DIR))
logger.info('Output Directory: {}'.format(OUTPUT))

search =  os.path.join(INPUT_DIR,'*.xml')
xfile = open(OUTPUT,"w")
basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),BASEPATH)
logger.info('Image-Basepath Directory: {}'.format(basepath))


xglob = glob.glob(search)
logger.info('Reading now : {} : XML-Files and save Boxes'.format(len(xglob)))
for filename in xglob:
#    logger.info(filename)
    tree = ET.parse(filename)
    for e in tree.findall('.//filename'):
        logger.debug('Filename: {}'.format(e.text))
        img_path = e.text

    for e in tree.findall('.//path'):
        logger.debug('VOC-PATH: {}'.format(e.text))
#        img_path = e.text


    image = os.path.join(basepath, img_path)
    logger.debug('Image: {}'.format(image))
    exists = os.path.isfile(image)
#    if not exists:
    if exists:
        xobject = tree.findall('.//object')
        logger.info('found : {} : Objects'.format(len(xobject)))
        for e in xobject:
                logger.debug(e.find('name').text)
                kategorie = e.find('name').text

                kag_code = category1.get(kategorie)
                bndbox = e.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                x_width = xmax - xmin
                y_height = ymax - ymin
                logger.debug("{},{},{},{},{},{},{}".format(image,xmin,ymin,xmax,ymax,kategorie,kag_code))
                xfile.write("{},{},{},{},{},{}\n".format(image,xmin,ymin,xmax,ymax,kategorie))
xfile.close
