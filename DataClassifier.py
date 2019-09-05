import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
import sys

class ClassifyImages(QWidget):
    def __init__(self, classesfile, inputdir, outputfile):
        super().__init__()
        self.title = "ImageClassifier"
        self.left = 50
        self.top = 50
        self.width = 1024
        self.height = 768

        self.classes = open(classesfile, 'r').read().strip().split(',')
        self.nclass = len(self.classes)
        self.indir = inputdir
        self.outpath = outputfile

        self.availableImages = os.listdir(self.indir)
        self.currentImagePath = self.availableImages[0]
        self.currentIndex = 0

        self.classButtons = []
        self.initUI()

        self.fileAcess = open(self.outpath, 'at')
        self.classifications = {}

    def classButtonCallbackFactory(self, index):
        def classificationClick():
            self.classButtons[index].setChecked(~self.classButtons[index].isChecked())
            for i, btn in enumerate(self.classButtons):
                if i == index:
                    continue
                if btn.isChecked():
                    btn.setChecked(False)

        return classificationClick


    def nextImageClick(self):
        thisImageClass = None
        for i, btn in enumerate(self.classButtons):
            if btn.isChecked():
                thisImageClass = i

        self.fileAcess.write("{}, {}\n".format(self.currentImagePath, thisImageClass))
        self.fileAcess.flush()
        self.classifications[self.currentImagePath] = thisImageClass

        self.currentIndex += 1
        self.currentImagePath = self.availableImages[self.currentIndex]
        [a.setChecked(False) for a in self.classButtons]
        self.draw()


    def finishedClick(self):
        self.fileAcess.close()
        self.fileAcess = open(self.outpath, 'wt')
        for fname in self.classifications.keys():
            self.fileAccess.write("{},  {}\n".format(fname, self.classifications[fname]))
        self.fileAccess.close()
        sys.exit()

    def prevImageClick(self):
        self.currentIndex -= 1
        self.currentImagePath = self.availableImages[self.currentIndex]
        thisImageClass = self.classifications[self.currentImagePath]
        [a.setChecked(False) for a in self.classButtons]
        self.classButtons[thisImageClass].setChecked(True)
        self.draw()

    def draw(self):
        self.cur_pixmap = QPixmap(os.path.join(self.indir, self.currentImagePath))
        self.cur_pixmap = self.cur_pixmap.scaled(self.fixedImageWidth, self.fixedImageHeight)
        self.image.setPixmap(self.cur_pixmap)

    def initUI(self):
        self.setWindowTitle(self.title)

        self.setGeometry(self.left, self.top, self.width, self.height)


        self.layout = QGridLayout()
        self.setLayout(self.layout)
        for i, classification in enumerate(self.classes):
            self.classButtons.append(QPushButton(classification))
            self.layout.addWidget(self.classButtons[-1], i, 0, 1, 1)
            self.classButtons[-1].clicked.connect(self.classButtonCallbackFactory(i))
            self.classButtons[-1].setCheckable(True)

        prevBtn = QPushButton("Previous")
        prevBtn.clicked.connect(self.prevImageClick)
        self.layout.addWidget(prevBtn, self.nclass,1)
        
        nextBtn = QPushButton("Next")
        nextBtn.clicked.connect(self.nextImageClick)
        self.layout.addWidget(nextBtn, self.nclass , 2)

        nextBtn = QPushButton("Finish")
        nextBtn.clicked.connect(self.finishedClick)
        self.layout.addWidget(nextBtn, self.nclass , 3)

        

        self.image = QLabel(self)
        self.layout.addWidget(self.image, 0, 1, self.nclass, self.nclass)
        self.layout.setVerticalSpacing(0)
        self.show()

        self.cur_pixmap = QPixmap(os.path.join(self.indir, self.currentImagePath))
        self.cur_pixmap = self.cur_pixmap.scaled(self.image.width(), self.image.height())
        self.image.setPixmap(self.cur_pixmap)

        self.fixedImageWidth = self.image.width()
        self.fixedImageHeight = self.image.height()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("usage: DataClassifier.py <list of classes> <Directory of images> <output CSV name>")
        sys.exit(1)
    app = QApplication([])

    exe = ClassifyImages(sys.argv[1], sys.argv[2], sys.argv[3])

    app.exec_()
