'''''''''
JG November 22, 2020
from the VoTT CSV file you can now convert to Darknet Format
'''''''''

import os
import pandas as pd
import cv2
pd.options.mode.chained_assignment = None  # default='warn'

jpeg_images = os.path.join(os.getcwd(), 'JPEGImages')  # path=
txt_darknet = os.path.join(os.getcwd(), 'Darknet')  # darknet=
manifest_file = os.path.join(os.getcwd())  # manifest_target=
multi_df = pd.read_csv('JJvideo-export.csv')
labels = multi_df["label"].unique()
labeldict = dict(zip(labels, range(len(labels))))
multi_df.drop_duplicates(subset=None, keep="first", inplace=True)


def manifest_generator(vott_df, manifest_target, path):
    images_name = vott_df['image'].unique()
    for i in range(len(images_name)):
        file = open(os.path.join(manifest_target,'manifest.txt'), "a")
        file.write(os.path.join(path, images_name[i])+'\n')
        file.close()
    print('INFO: Total number of images: %s' % len(images_name))


def csv2darknet(vott_df, labeldict, path, darknet):
    print('INFO: wait while converting to darknet ...')
    # Encode labels according to labeldict if code's don't exist
    if not "code" in vott_df.columns:
        vott_df['code'] = vott_df["label"].apply(lambda x: labeldict[x])
    # Round float to ints
    for col in vott_df[["xmin", "ymin", "xmax", "ymax"]]:
        vott_df[col] = (vott_df[col]).apply(lambda x: round(x))

    txt_file = ''
    last = ''
    for index, row in vott_df.iterrows():
        img = cv2.imread(os.path.join(path, row["image"]), 0).shape
        # print(img[1], img[0])  # width and height
        xcen = float((row['xmin'] + row['xmax'])) / 2 / img[1]
        ycen = float((row['ymin'] + row['ymax'])) / 2 / img[0]
        w = float((row['xmax'] - row['xmin'])) / img[1]
        h = float((row['ymax'] - row['ymin'])) / img[0]
        xcen = round(xcen, 3)
        ycen = round(ycen, 3)
        w = round(w, 3)
        h = round(h, 3)
        target_name = row['image'].split('.')
        target = os.path.join(darknet, target_name[0] + '.txt')
        if not last == row['image']:
            txt_file = ''
            txt_file += "\n"
            txt_file += " ".join([str(x) for x in (row["code"], xcen, ycen, w, h)])
        else:
            txt_file += "\n"
            txt_file += " ".join([str(x) for x in (row["code"], xcen, ycen, w, h)])
            # txt_file += "\n"
        last = row['image']
        file = open(target, "w")
        file.write(txt_file[1:])  # the line with the calculation per annotation
        file.close()

    print('INFO: READY! VoTT CSV has been converted to Darknet Format')
    return True


manifest_generator(multi_df, manifest_target=manifest_file, path=jpeg_images)
csv2darknet(multi_df, labeldict, path=jpeg_images, darknet=txt_darknet)
