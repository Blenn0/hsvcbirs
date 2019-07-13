#first attempt at anything in python, importing brain
#importing necessary packages
#building an image query engine

import numpy as np
from opencv-python import cv2
import imutils

class ColorDescriptor:
  def __init__(self, bins):
      #store the number of bins for the 3d histogram
      self.bins = bins

  def describe(self, image):
      #convert the image to HSV color space and initialize
      #the features used to quantify the image
      image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
      features = []

      #grab dimz find center of image
      (h,w) = image.shape[:2]
      (cX,cY) = (int(w*0.5), int(h*0.5))

      #divide the image into four rectangles/segments
      #top L/R, bottom L/R
      segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
          (0, cX, cY, h)]

      #construct an elliptical mask representing the center of the
      #of the image
      (axesX, axesY) = (int(w*0.75)//2, int(h*.75)//2)
      ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
      cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255,-1)

      #loop over the segments
      for (startX, endX, startY, endY) in segments:
          #construct a mask for each corner, subtracting
          # the elliptical center from it
          cornerMask = np.zeros(image.shape[:2], dtype="uint8")
          cv2.rectangle(cornerMask, (startX, startY), (endX, endY) 255, -1)
          cornerMask = cv2.subtract(cornerMask, ellipMask)

          #extract a color histogram from the image
          #then udate the feature vector
          hist = self.histogram(image, cornerMask)
          features.extend(hist)

      #extract a color histogram from the ellip region
      #update feature vector
      hist = self.histogram(image, ellipMask)
      features.extend(hist)a

      #return feature vector

      return features

      def histogram(self, image, mask):
          #extract 3d color histofram from masked region
          #using supplied bins per channel
          hist = cv2.calcHist([image], [0,1,2], mask, self.bins,
          [0, 180, 0, 256, 0, 256])

          #normalize the histogram perhaps clash here
          if imutils.is_cv2():
              hist = cv2.normalize(hist).flatten()

          #otherwise handle for open cv3
          else:
              hist = cv2.normalize(hist, hist).flatten()

          return hist
          
   # end phase 1, more phases still...
