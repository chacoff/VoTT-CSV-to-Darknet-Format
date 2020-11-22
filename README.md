# VoTT-CSV-to-Darknet-Format
If you are using VoTT to annotate RGB images and later on you want to feed a Yolo, you might need to convert those to Darknet format. 
In my case, I figured was easier to export VoTT annotations as CSV and later make a small script to get these in Darknet format

Description
- you will need the folder where the images are because we need to open each one of them in order know its size before we can calculate xcen, ycen, height and width for darknet format
- you can choose where to store the *.txt files, either in a brand new folder or in the same folder than the images
