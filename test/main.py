from skimage.io import imshow,imread,show
from skimage import img_as_float
from numpy import roll,dstack,min,max
from math import fabs
def calcCor(imEt,im):
    bestCorr = 0
    shiftVer, shiftHor = 0, 0
    shift=20
    for i in range(-shift, shift+1):
        shiftP = roll(im, i, 0)
        for j in range(-shift, shift+1):
            p = roll(shiftP, j, 1)
            cor = (p * imEt).sum()
            if cor > bestCorr:
                bestCorr = cor
                shiftVer = j
                shiftHor = i

    return (shiftVer,shiftHor)

def align(img,g_coord):
    img=img_as_float(img)
    x,y=g_coord
    pr=0.05
    newWidth=img.shape[1]
    newHeight=img.shape[0]//3
    img2 = img[newHeight:newHeight*2, :newWidth]
    img1=img[:img2.shape[0],:newWidth]
    img3 = img[newHeight*2:newHeight*3,:newWidth]

    img1 = img1[int(newHeight * pr):newHeight - int(newHeight * pr),int(newWidth * pr):newWidth - int(newWidth * pr)]
    img2 = img2[int(newHeight*pr):newHeight-int(newHeight*pr),int(newWidth*pr):newWidth-int(newWidth*pr)]
    img3 = img3[int(newHeight*pr):newHeight-int(newHeight*pr),int(newWidth*pr):newWidth-int(newWidth*pr)]

    (blueShiftVer,blueShiftHor)=calcCor(img2, img1)
    (redShiftVer, redShiftHor) = calcCor(img2, img3)
    img1 = roll(img1, blueShiftHor, 0)
    img3 = roll(img3, redShiftHor, 0)
    img1 = roll(img1, blueShiftVer, 1)
    img3 = roll(img3, redShiftVer, 1)


    newX1=x-blueShiftHor-img.shape[0]//3
    newY1 = y - blueShiftVer

    newX3=x-redShiftHor+img.shape[0]//3
    newY3 = y - redShiftVer

    imshow(dstack((img3,img2,img1)))
    show()
    return (newX1,newY1),(newX3,newY3)

img=imread("00.png")
img=img-img.min()*(255/img.max()-img.min())
img.astype('uint8')

