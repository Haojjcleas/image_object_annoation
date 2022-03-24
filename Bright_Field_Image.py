# -*- coding:utf-8 -*-

import cv2
import os
from Annotation import Annotation

MSC_LABEL = True
FIB_LABEL = False
drawing = False  # true if mouse is pressed

# if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1


# mouse callback function

class BrightFieldImage(object):

    def __str__(self):
        return str(self.to_json())

    def __init__(self, file_path):
        """
        load image and do the annotation to generate the json file
        file_path: path to the target image
        """

        self.MSC_LABEL = True
        self.FIB_LABEL = False
        self.mode = self.MSC_LABEL

        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.annotation = Annotation()
        self.annotations = []
        self.img = cv2.imread(self.file_path)

    def draw_circle(self, event, x, y, _, __):
        global ix, iy, drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            self.annotation = Annotation()
            self.annotation.x, self.annotation.y = x, y
            print(x, y, event)
            drawing = True
            ix, iy = x, y
        # elif event == cv.EVENT_MOUSEMOVE:
        #     if drawing == True:
        #         if mode == True:
        #             cv.rectangle(img,(ix,iy),(x,y),(0,255,0),3)
        #         else:
        #             cv.circle(img,(x,y),5,(0,0,255),-1)
        elif event == cv2.EVENT_LBUTTONUP:
            print(x, y, event)
            drawing = False
            # to label the image with multiple label
            if self.mode == self.MSC_LABEL:
                cv2.rectangle(self.img, (ix, iy), (x, y), (0, 255, 0), 2)
                cv2.imshow(self.file_name, self.img)
                self.annotation.height = y - self.annotation.y
                self.annotation.width = x - self.annotation.x
                self.annotation.label = 'MSC'
                self.add_annotation()
            else:
                cv2.rectangle(self.img, (ix, iy), (x, y), (255, 0, 0), 2)
                cv2.imshow(self.file_name, self.img)
                self.annotation.height = y - self.annotation.y
                self.annotation.width = x - self.annotation.x
                self.annotation.label = 'FIB'
                self.add_annotation()

    def show(self):
        """
        open a window show the image
        """
        cv2.namedWindow(self.file_name)
        cv2.imshow(self.file_name, self.img)

        cv2.setMouseCallback(self.file_name, self.draw_circle)

    def add_annotation(self) -> None:
        """
        add one annotation to the image
        """
        self.annotations.append(self.annotation)

    def to_json(self) -> dict:
        """
        return the annotation in json format
        """
        json_result = {'image': self.file_name, "annotations": []}
        for i in self.annotations:
            json_result["annotations"].append({
                'label': i.label,
                'coordinates': {
                    'x': i.x,
                    'y': i.y,
                    'width': i.width,
                    'height': i.height
                }
            })

        return json_result


if __name__ == '__main__':
    new_img = BrightFieldImage(file_path='image1.jpg')
    new_img.add_annotation()
    print(new_img.to_json())
