from PIL import Image

from os import listdir
from os.path import isfile, join
import pandas as pd
import random
import os.path
import numpy as np

def premultiply(filename):
    I = np.asarray(Image.open(filename))
    J = I.copy()
    A = J[:,:,3]/255.0
    J[:,:,0] = J[:,:,0] * A
    J[:,:,1] = J[:,:,1] * A
    J[:,:,2] = J[:,:,2] * A
    return Image.fromarray(J)

path = "./crop/"

imgs = [ f for f in listdir(path + 'ds/') if (isfile(join(path + 'ds/', f)) and 'png' in f)]
random.shuffle(imgs)

try:
    os.makedirs(path + 'premult')
except:
    print("Dir exists")

for img in imgs:
    fname = img.split('/')[-1]
    if not isfile(join(path + 'premult/' + fname)):
        print("premultiplying", fname)
        premult = premultiply(path + 'ds/' + img)
        premult.save(path + 'premult/' + fname)
