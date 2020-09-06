import os
from PIL import Image,ImageOps
file=input("filename:")
try:
    os.mkdir(file)
except FileExistsError:
    pass

count=0
while True:
    directry=os.listdir("new_images")
    if directry:
        for i in directry:
            img=Image.open("new_images/"+i)
            img.save(file+"/new_img"+str(count)+".jpg")
            os.remove("new_images/"+i)
        count+=1
