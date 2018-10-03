from skimage.io import imshow,show,imread
from numpy import roll,dstack
from skimage import img_as_float
class ColorProkudinGorskiy:
    def __init__(self,img):
        self.img=img_as_float(img)
        self.width = img.shape[1]
        self.height =img.shape[0] // 3

    def cutImage(self,cutImg, portionPr):
        portionHeight = int(self.width * portionPr)
        portionWidth = int(self.height * portionPr)
        return cutImg[portionHeight:self.height - portionHeight, portionWidth:self.width - portionWidth]

    def calcCor(self,imEt,im, shift):
        bestCorr = 0
        shiftVer, shiftHor = 0, 0
        for i in range(-shift, shift + 1):
            shiftP = roll(im, i, 0)
            for j in range(-shift, shift + 1):
                p = roll(shiftP, j, 1)
                cor = (p * imEt).sum()
                if cor > bestCorr:
                    bestCorr = cor
                    shiftVer = j
                    shiftHor = i
        # for i in range(-shift, shift+1):
        #      shiftP=roll(im,i,0)
        #      cor = (shiftP * imEt).sum()
        #      if cor > bestCorr:
        #         bestCorr = cor
        #         shiftHor = i
        #
        # bestCorr= 0
        #
        # for i in range(-shift, shift+1):
        #      shiftP=roll(im,i,1)
        #      cor = (shiftP * imEt).sum()
        #      if cor > bestCorr:
        #         bestCorr = cor
        #         shiftVer = i
        return (shiftVer, shiftHor)

    def align(self,shift,portion,g_coord):
        x, y = g_coord

        img2 = self.img[self.height:self.height * 2, :self.width]
        img1 = self.img[:self.height, :self.width]
        img3 = self.img[self.height * 2:self.height * 3, :self.width]

        img1 = self.cutImage(img1, portion)
        img2 = self.cutImage(img2, portion)
        img3 = self.cutImage(img3, portion)

        (blueShiftVer, blueShiftHor) = self.calcCor(img2, img1,shift)
        (redShiftVer, redShiftHor) = self.calcCor(img2, img3,shift)
        img1 = roll(img1, blueShiftHor, 0)
        img3 = roll(img3, redShiftHor, 0)
        img1 = roll(img1, blueShiftVer, 1)
        img3 = roll(img3, redShiftVer, 1)

        newX1 = x - blueShiftHor - img.shape[0] // 3
        newY1 = y - blueShiftVer

        newX3 = x - redShiftHor + img.shape[0] // 3
        newY3 = y - redShiftVer

        res=dstack((img3, img2, img1))

        return res,(newX1, newY1), (newX3, newY3)




if __name__=="__main__":
    img=imread("00.png")
    img,r,b=ColorProkudinGorskiy(img).align(15,0.07,(508,237))
    imshow(img)
    show()
    print(r)
    print(b)


