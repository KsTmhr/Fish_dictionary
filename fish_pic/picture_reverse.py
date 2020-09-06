import os
from PIL import Image,ImageOps
file=input("filename:")

while True:
    directry=os.listdir("new_images")
    if directry:
        for i in directry:
            img=Image.open("new_images/"+i)
            img_m=ImageOps.mirror(img)
            img_m.save(file+"/new_"+i)
            os.remove("new_images/"+i)
