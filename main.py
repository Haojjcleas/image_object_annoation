# -*- coding:utf-8 -*-

from Bright_Field_Image import BrightFieldImage
import cv2
import os

base_path = '/Users/jjhao/Desktop/images/'

for path in os.listdir(base_path):
    path = base_path + path
    print(path)
    if not path.endswith('jpg'):
        continue
    new_img = BrightFieldImage(file_path=path)
    new_img.show()
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            new_img.mode = new_img.MSC_LABEL
        elif k == ord('f'):
            new_img.mode = new_img.FIB_LABEL

        # press n to save the change and switch to next image
        elif k == ord('n'):
            with open('label.json', 'a') as fo:
                fo.write(str(new_img)+'\n')
            cv2.destroyAllWindows()
            break

        # if esc is pressed, exit the program
        elif k == 27:
            cv2.destroyAllWindows()
            exit()
