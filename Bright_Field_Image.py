# -*- coding:utf-8 -*-

import cv2
from Annotation import Annotation

MSC_LABEL = True
FIB_LABEL = False

drawing = False  # true if mouse is pressed
mode = MSC_LABEL  # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1


# mouse callback function

class BrightFieldImage(object):
    def __init__(self, file_path):
        """
        load image and do the annoation to generate the json file
        file_path: path to the target image
        """

        self.file_path = file_path
        self.annotation = Annotation()
        self.annotations = []
        self.img = cv2.imread(self.file_path)

    def draw_circle(self, event, x, y, flags, param):
        global ix, iy, drawing, mode
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
            if mode == MSC_LABEL:
                cv2.rectangle(self.img, (ix, iy), (x, y), (0, 255, 0),2)
                self.annotation.heigh = y - self.annotation.y
                self.annotation.width = x - self.annotation.x
                self.annotation.label = 'MSC'
                self.add_annoation()
            else:
                cv2.rectangle(self.img, (ix, iy), (x, y), (255, 0, 0),2)
                self.annotation.heigh = y - self.annotation.y
                self.annotation.width = x - self.annotation.x
                self.annotation.label = 'FIB'
                self.add_annoation()

    def show(self):
        """
        open a window show the image
        """
        global mode
        img = self.img
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_circle)
        while (1):
            cv2.imshow('image', img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('m'):
                mode = MSC_LABEL
            elif k == ord('f'):
                mode = FIB_LABEL
            elif k == 27:
                break
        cv2.destroyAllWindows()

    def add_annoation(self) -> None:
        """
        add one annoation to the image

        x: x axis of the object in the image
        y: y axis of the object in the image
        width: width of the object in the image
        heigh: heigh of the object in the image
        """
        self.annotations.append(self.annotation)

    def to_json(self) -> list:
        """
        return the the annoation in json format
        """
        json_result = {'image': self.file_path}
        json_result["annotations"] = []
        for i in self.annotations:
            json_result["annotations"].append({
                'label': i.label,
                'coordinates': {
                    'x': i.x,
                    'y': i.y,
                    'width': i.width,
                    'height': i.heigh
                }
            })

        return json_result


if __name__ == '__main__':
    new_img = BrightFieldImage(file_path='image1.jpg')
    new_img.add_annoation()
    print(new_img.to_json())
