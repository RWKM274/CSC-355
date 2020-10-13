"Name: Qingyuan Liu"
"Date: 12/10/2020"
"Today i am going to change the picture's shape and color " \
"I am going to use ImageEnhance and try point transform today. "

import numpy as np
import PIL
from PIL import Image
from PIL import ImageEnhance


class imageChange:
    #I have tryed the ImageEnhance is follow part, it makes picture lighter or darker.
    image1 = Image.open("/Users/rwkm/Documents/Python study/0001.jpg")
    imageEnchance = ImageEnhance.Contrast(image1)
    imageEnchance.enhance(0.6).show("60% more contrast")

    #I have mutilply the the pixel by 1.7, it seems did the same thing on top.
    imagePiexlChange = image1.point(lambda i: i * 1.7)
    imagePiexlChange.show()

    #more code about pixel.
    image2 = Image.open("/Users/rwkm/Documents/Python study/test2.jpg")
    changeIndex = np.array(image2) *2
    newImage = Image.fromarray(changeIndex,"RGB")
    newImage.show()
    print(changeIndex)



def main():
    print("hello world!")
    imageChange


if __name__ == '__main__':
    main()
