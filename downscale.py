from PIL import Image

from os import listdir
from os.path import isfile, join
import pandas as pd
import random
import os.path
def resize_img(filename, size=1024):
    img = Image.open(filename)
    img = img.convert('RGBA')
    img = img.resize((size, size), resample=Image.ANTIALIAS)
    return img

path = "./crop/"
folders = ['downscale', 'w2x', 'w3x', 'w4x']

try:
    os.makedirs(path + 'ds')
except:
    print("Dir exists")

for folder in folders:
    print(folder)
    imgs = [ f for f in listdir(path + folder) if (isfile(join(path + folder, f)) and 'png' in f)]
    random.shuffle(imgs)
    for img in imgs:
        fname = img.split('/')[-1]
        if not isfile(join(path + 'ds/' + fname)):
            print("downscaling", fname)
            downscaled = resize_img(path + folder + '/' + img, 1024)
            downscaled.save(path + 'ds/' + fname)
