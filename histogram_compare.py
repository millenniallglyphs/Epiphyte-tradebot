import numpy as np
import glob
import cv2
from datetime import datetime

def GetLatest():
     archive_format = datetime.now().strftime("*.jpg")
     archives = glob.glob(archive_format)

     if len(archives) > 0:
          return archives[-1]
     else:
          return None

def GetHisto(mypic):
     img = cv2.imread(mypic)
     colorcd = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     hist = cv2.calcHist(colorcd, [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
     hist = cv2.normalize(hist, hist).flatten()
     return hist

def GetcvPic(mypic):

    img = cv2.imread(mypic)
    return img

lastpic = GetcvPic(GetLatest())
lasthisto = GetHisto(GetLatest())
standard = GetHisto(#path to reference) #fill in path to reference file

OPENCV_METHODS = (
     ("Correlation", cv2.HISTCMP_CORREL),
     ("Chi-Squared", cv2.HISTCMP_CHISQR),
     ("Intersection", cv2.HISTCMP_INTERSECT),
     ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))

for (methodName, method) in OPENCV_METHODS:
     # initialize the results dictionary and the sort
     results = {}
     d =cv2.compareHist(standard, lasthisto, method)

     print(d)
