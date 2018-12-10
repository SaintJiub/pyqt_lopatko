import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
import PIL
from PIL import Image


import numpy as np
import cv2
from matplotlib import pyplot as plt

def PhotoShop(x0,y0,x,y, filename):
    img = cv2.imread(filename)
    mask = np.zeros(img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    h,w = img.shape[:2]
    print(w,h )
    rect = (x0,y0,x-x0,y-y0)
    print(x0,y0,x-x0,y-y0)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img =  img*mask2[:,:,np.newaxis]
    plt.imshow(img),plt.show()
    return img

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.x0 =0
        self.y0 =0
        self.x =0
        self.y =0

        self.pixmap = QPixmap()
        self.cutButton.clicked.connect(self.run)
        self.imButton.clicked.connect(self.open_file)

    def open_file(self):
        try:
            W = self.imageframe.width()
            H = self.imageframe.height()
            self.pixmap.load(self.lineEdit.text())
            self.imageframe.setPixmap(self.pixmap.scaled(W, H, Qt.KeepAspectRatio))
            maxsize = (W, H)
            image = self.lineEdit.text()
            im = Image.open(image)
            tn_image = im.thumbnail(maxsize, PIL.Image.ANTIALIAS)
            im.save("temp.jpg")
        except Exception:
            pass

    def run(self):

        PhotoShop(self.x0, self.y0, self.x, self.y, "temp.jpg")
        '''
        W =self.imageframe.width()
        H = self.imageframe.height()
        self.pixmap.load(self.lineEdit.text())
        self.imageframe.setPixmap(self.pixmap.scaled(W,H, Qt.KeepAspectRatio))
        maxsize = (W, H)
        image = self.lineEdit.text()
        im = Image.open(image)
        tn_image = im.thumbnail(maxsize, PIL.Image.ANTIALIAS)
        im.save("temp.jpg")
      
        bytes = QByteArray()
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        self.pixmap.save(buffer, "PNG")'''

    def mousePressEvent(self, event):
        self.x0 = event.x()
        self.y0 = event.y()
    def mouseReleaseEvent(self, event):

        self.x = event.x()
        self.y = event.y()
        self.coord.setText("Координаты:{}, {},{},{}".format(self.x0,self.y0,self.x,self.y))

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
