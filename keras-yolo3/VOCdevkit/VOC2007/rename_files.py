import os
path = 'test'
files = os.listdir(path)

for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, "".join(['IMG_',str(index+200).zfill(4),'.jpeg'])))