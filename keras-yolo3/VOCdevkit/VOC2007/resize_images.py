import PIL
from PIL import Image
import os
from datetime import datetime

for image_file_name in os.listdir('C:\\Users\\Public\\Mirror\\University\\Year 4 Sem 1\\CAPSTONE\\SmartGym\\keras-yolo3\\VOCdevkit\\VOC2007\\test\\'):
    if image_file_name.endswith(".jpeg"):
        now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')

        im = Image.open('C:\\Users\\Public\\Mirror\\University\\Year 4 Sem 1\\CAPSTONE\\SmartGym\\keras-yolo3\\VOCdevkit\\VOC2007\\test\\'+image_file_name)
        new_width  = 640
        new_height = 480
        im = im.resize((new_width, new_height), Image.ANTIALIAS)
        im.save('C:\\Users\\Public\\Mirror\\University\\Year 4 Sem 1\\CAPSTONE\\SmartGym\\keras-yolo3\\VOCdevkit\\VOC2007\\resized\\' + image_file_name)
