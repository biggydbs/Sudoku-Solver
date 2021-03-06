import cv2
import numpy as np
#import matplotlib.pyplot as plt


def show(im):
    cv2.imshow('Sudoku', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]
     
    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

# Read the image
im = cv2.imread('./img/1.jpg', cv2.IMREAD_GRAYSCALE)

# Show image
show(im)

# GuassianBlur for better thresholding
gray = cv2.GaussianBlur(im, (5, 5), 0)
show(gray)

# Thresholding - Black becomes blacker and white becomes whiter
thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
show(thresh)

# Finding out all the contours
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Finding maximum possible square inside the image
biggest = None
max_area = 0
for i in contours:
    area = cv2.contourArea(i)
    if area > 100:
        peri = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * peri, True)
        if area > max_area and len(approx) == 4:
            biggest = approx
            max_area = area

# Rectifying the square for optimal coordinates
approx=rectify(biggest)

# Creating array equalent to maximum size of the image
h = np.array([ [0,0],[489,0],[489,367],[0,367] ],np.float32)

# Taking out the square grid from the grayscale image
retval = cv2.getPerspectiveTransform(approx,h)
warp = cv2.warpPerspective(gray,retval,(490,368))

# Showing the grid
show(warp)
