import numpy as np
import cv2
from PIL import Image
import pytesseract

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening_img(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny_img(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 


# you can add more preprocess based on you image cases to improve accuracy
# the api can be found in cv_utils.py file, try it!
def img_preprocess(image):
    cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = get_grayscale(cv_img)
    thresh = thresholding(gray)
    # convert back to pil image
    im_pil = Image.fromarray(thresh)

    return im_pil

# see https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc 
# for custom_config options
# here it is only one line of digits, so set psm as 7
def read_with_tesseract(image):
    image = img_preprocess(image)
    # only get one line digits
    custom_config = r'--psm 7 --oem 3 outputbase digits'
    code = pytesseract.image_to_string(image, config=custom_config)
    return code, image

