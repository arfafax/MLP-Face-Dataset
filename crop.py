from PIL import Image

from os import listdir
from os.path import isfile, join
import pandas as pd
import os.path
ponies = pd.read_csv("derpi_faces.csv")
def pad_img(img, size=512):
    img = img.convert('RGBA')
    width, height = img.size
    if width > height:
        new_width = size
        new_height = new_width * height // width
        image = img.resize((new_width, new_height), resample=Image.ANTIALIAS)
        new_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        upper = (size - image.size[1]) // 2
        new_image.paste(image, (0, upper))
        return new_image
    else:
        new_height = size
        new_width = new_height * width // height
        image = img.resize((new_width, new_height), resample=Image.ANTIALIAS)
        new_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        left = (size - image.size[0]) // 2
        new_image.paste(image, (left, 0))
        return new_image

def crop_img(filename, xmin, ymin, xmax, ymax):
    print(filename)
    img = Image.open(filename)

    width, height = img.size
    w = xmax - xmin
    h = ymax - ymin

    new_dim = max(w, h)
    center_x, center_y = (xmax - w//2), (ymax - h//2)
    xmin = int(max(0, center_x - new_dim//2))
    xmax = int(min(width, center_x + new_dim//2))
    ymin = int(max(0, center_y - new_dim//2))
    ymax = int(min(height, center_y + new_dim//2))

    cropped_img = img.crop((xmin, ymin, xmax, ymax))
    return pad_img(cropped_img, max(w, h))

def crop(row):
    filename = row['id'].split('/')[-1]
    out_name = ".".join([str(row['id']), str(row['index']),  str(round(row['confidence']*100)), 'png'])
    fid = filename.split(".")[0]
    g = row['group']

    if os.path.exists(path + "/" + filename) and not isfile(join(path + "/" + g + "/", out_name)):
        print("Cropping id %s, face %s" % (row['id'], row['index']))
        try:
          img = crop_img(path + "/" + filename,
                             int(row['xmin']),
                             int(row['ymin']),
                             int(row['xmax']),
                             int(row['ymax']))
          img.save(path + '/' + g + '/' + out_name)
        except Exception as inst:
          print("Error", inst)

path = "./crop/"
ponies = ponies.sample(frac=1).reset_index(drop=True)

try:
    os.makedirs(path + 'downscale')
    os.makedirs(path + 'waifu2x')
    os.makedirs(path + 'waifu3x')
    os.makedirs(path + 'waifu4x')
except:
    print("Dir exists")

def get_group(row):
    if row['w'] >= 1024 or row['h'] >= 1024:
        return 'downscale'
    elif row['w'] >= 512 or row['h'] >= 512:
        return 'waifu2x'
    elif row['w'] >= 1024//3 or row['h'] >= 1024//3:
        return 'waifu3x'
    else:
        return 'waifu4x'
ponies['group'] = ponies.apply(get_group, axis=1)
ponies.apply(crop, axis=1)
