#!/usr/bin/python
#coding:utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        #创建文本输入框并把他设置为窗口的布局
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitACtion = QAction(QIcon('2.jpg'),'Exit',self)
        exitACtion.setShortcut('Ctrl+Q')
        exitACtion.setStatusTip('Exit application')
        exitACtion.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitACtion)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitACtion)

        self.setGeometry(300,300,350,250)
        self.setWindowTitle('Main window')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
