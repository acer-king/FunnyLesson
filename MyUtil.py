
import numpy as np
import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget,QFileDialog
from PyQt5.QtCore import QRect,QPoint
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen,QColor
from desktopmagic.screengrab_win32 import (
getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
getRectAsImage, getDisplaysAsImages)

from PIL.ImageQt import ImageQt
from Setting import Settings
import logging

import pytesseract as pyt
from PIL import Image
from pytesseract import Output
import os

def getPixmapFromScreen(posx,posy,W,H):
        """
        get screenshot with posx,posy,w,h and save it to local file 
        and return the created file name
        else return None
        """
        if(W == 0 or H == 0):
            return None
        
        imDisplay = getRectAsImage((posx,posy,posx+W,posy+H))
        qim = ImageQt(imDisplay)
        pix = QtGui.QPixmap.fromImage(qim)

        return pix.copy()

def convertCV2ImageToPixmap(cv2_img=None):

    if(cv2_img is None):
        return
    
    height, width, channel = cv2_img.shape
    bytesPerLine = 3 * width
    qImg = QImage(cv2_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    
    return qImg

def isImageUrl(url):

    url = str(url)
    if( 'jpg' in url):
        return True
    if( 'JPG' in url):
        return True
    if( 'jpeg' in url):
        return True
    if( 'JPEG' in url):
        return True
    if( 'png' in url):
        return True
    if( 'PNG' in url):
        return True
    if( 'bmp' in url):
        return True
    if( 'BMP' in url):
        return True
    
    return False
     
#just a resizing function to resize the template image while checking..
# Resizes a image and maintains aspect ratio
def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the 0idth and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)

#this function matches the template by resizing template from 0.7x to 1.3x of the original size to cater different screen sizes..
def match_image(url,parentx,parenty,parentwidth,parentheight):
    gray_image = getWholeScreen()
    template = loadImageFromUrl(url)
    (tH, tW) = template.shape[::-1]  # get the width and height
    # match the template using cv2.matchTemplate
    match = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = Settings.getSetting()['tolerance']
    
    position = np.where(match >= threshold)  # get the location of template in the image
    
    found = 0
    X = 0
    Y = 0
    W = 0
    H = 0
    R = 1

    scales = np.linspace(0.5, 1.9, 25)[::-1]
    scales = np.insert(scales, 0, 1.0, axis=0)

    for scale in scales:
        # Resize image to scale and keep track of ratio
        resized = maintain_aspect_ratio_resize(template, width=int(template.shape[1] * scale))
        r = template.shape[1] / float(resized.shape[1])

        match = cv2.matchTemplate(gray_image, resized, cv2.TM_CCOEFF_NORMED)
        threshold = Settings.getSetting()['tolerance']
        logging.info("threshold value is: %s, and scale value is : %s",threshold, scale)
        position = np.where(match >= threshold)  # get the location of template in the image

        for point in zip(*position[::-1]):  # draw the rectangle around the matched template
            found = 1
            (X,Y,W,H,R) = (int(point[0]),int(point[1]),int( tW / r),int(tH / r) , r)
            
            if X < parentx or X + W > parentx +parentwidth or Y < parenty or Y + H > parenty + parentheight:
                break
            else:
                (X,Y,W,H,R) = (0,0,0,0,0)
                found = 0
                continue
            break

        if (found):
            break

    return (found,X,Y,W,H,R)

    #if returns ( template_found? , (X,Y,W,H of the area found), R resized template ratio...

def convertImageToGray(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image

def loadImageFromUrl(url):
    img = cv2.imread(url,0)
    return img

def convertPixmapToGray(pixmap=None,isgray=True):
    if(pixmap is not None):
        image = pixmap.toImage()
        _width = image.width()
        _height = image.height()
        channels_count = 4
        s = image.bits().asstring(_width * _height * channels_count)
        gray = np.fromstring(s, dtype=np.uint8).reshape((_height, _width, channels_count)) 
        if(isgray == True):
            gray = convertImageToGray(gray)
        # cv2.imshow("ttest",test)
        # cv2.waitKey(0)
        return gray
    else:
        pass

def getWholeScreen(isgray=True):
    
    if(isgray):
        entireScreen = getScreenAsImage()
        image = np.array(entireScreen)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        return image
    else:
        entireScreen = getScreenAsImage()
        image = np.array(entireScreen)
        return convertImageToGray(image)

def getScreenSize():
    entireScreen = getScreenAsImage()
    image = np.array(entireScreen)
    return image.shape[0],image.shape[1]

def openFileDlg(parent = None):
    
    """
    pls give parent to open dlg 'ex:parent = self'
    """
    
    fname = QFileDialog.getOpenFileName(parent, 'Open file', 'c:\\', "Image files (*.jpg *.gif,*.bmp,*.tiff,*.png)")
    imagePath = fname[0]
    if(imagePath is not None and len(imagePath)):
        return imagePath

def drawRectToPixmap(self,x,y,w,h,pixmap=None):
    if(pixmap is None):
        return
    painter = QPainter(pixmap)
    pen = QPen(QColor(*Settings.childAnchorMarkLineColor))
    pen.setWidth(Settings.childAnchorMarkLineWidth)
    painter.setPen(pen)
    painter.drawRect(QRect(x,y,w,h))
    pass




############################################ Text Match and Tesseract ###################################################

'''Set path to tessaract.ext '''
pyt.pytesseract.tesseract_cmd = os.path.join(os.getcwd(),"Tesseract-OCR","tesseract")

#this function reads the MEAN color value of the image
def find_clr(img):
    data = np.reshape(img, (-1, 3))
    # print(data.shape)
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

    # print(sum(centers[0])/(3))
    return (sum(centers[0]) / (3))


def get_marked_image(correct,image):

    rects = []
    if correct is None or image is None:
        return rects
    #reading the image..
    img = image.copy()
    
    #print("Clr: ", find_clr(img))
    '''
    if ( find_clr(img) > 125):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (t,thresh) = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (t, thresh) = cv2.threshold(img, 75, 255,cv2.THRESH_BINARY_INV)

    #img = thresh
    '''

    (h,w,c) = img.shape
        
    
    # cv2.imwrite("1.png",img)
    # img = cv2.imread("1.png")
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    string = pyt.image_to_string(image)

    print("Expected string: ",correct)
    print("Got string: ",string)

    data = pyt.image_to_boxes(image)

    #image_to_boxes returns data as a string which can be split using "\n" character.
    data = data.split("\n")
    #print(data)
    errors = 0

    #removing spaces from the correct string, as img_2_boxes doesnt return spaces, carrage return etc.

    #NOTE: This function is for only single line matching,.
    correct = correct.replace(" ","")
    #print(len(correct),len(data))

    '''LOOPING through the characters and maching them, if there is not a match, then draw a rectangle around it..'''
    

    if(len(correct) != len(data)):
        print("Please enter the string of same length.")
        return rects
    for i in range(len(correct)):

        if (correct[i] != data[i][0]):
            #print(data[i][0])
            coords = data[i].split(" ")
            #print(coords)
            x1 = int(coords[1])
            y1 = h-int(coords[2])
            x2 = int(coords[3])
            y2 = h-int(coords[4])
            #print((x1,y2,x2,y2))
            rect = QRect(QPoint(x1,x2),QPoint(x2,y2))
            rects.append(rect)
            
            # cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),1)
            errors +=1

    
    return rects


def getTextFromImage(cv2_img = None):

    if(cv2_img is None):
        return

    string = pyt.image_to_string(cv2_img)

    return string
    



#basic function to mark an image...
#get_marked_image(expected_string, path_to_image)

'''tHIS function is to only mark the values for:
    - 1 line input.
    - Exact same length of strings (expected and received), if not Same, we can ask the user to write the string of same length as expected.
    - Capitalization should be exact too.
    '''
############################################ End ###############################################