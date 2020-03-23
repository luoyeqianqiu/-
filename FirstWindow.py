#include <QDesktopWidget>
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QPushButton, QLineEdit, QMenuBar, QStatusBar,QDesktopWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import Ui_oneWindow as u1
import Ui_twoWindow as u2
import ThreeWindow as u3

class FirstWindow(QMainWindow,QtWidgets.QWidget):

    def __init__(self, parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        #设置大小
        super(FirstWindow, self).__init__(parent)
        self.setWindowTitle('测试工具')
        self.resize(800,600)
        #位置居中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        #设置菜单栏
        menubar = self.menuBar()
        # 添加菜单
        fileMenu = menubar.addMenu('&File')
        # 添加菜单
        #设置底栏
        self.statusBar()

        self.btn1 = QPushButton(self)
        self.btn1.setText('窗口测试')
        self.btn1.move(150, 50)

        self.btn2 = QPushButton(self)
        self.btn2.setText('奖励转换器')
        self.btn2.move(350, 50)

        self.btn3 = QPushButton(self)
        self.btn3.setText('表格检验器')
        self.btn3.move(550, 50)

        self.btn1.clicked.connect(self.btn1_click)
        self.btn2.clicked.connect(self.btn2_click)
        self.btn3.clicked.connect(self.btn3_click)
    #
    #事件处理
    def btn1_click(self):
        self.hide()
        self.oneWindow = QMainWindow()
    # designer方式
        self.ui = u1.Ui_MainWindow()
        self.ui.setupUi(self.oneWindow)
        self.oneWindow.show()

    def btn2_click(self):
       self.hide()
       self.ui = u2.Ui_towWindow()
       self.ui.show()

    def btn3_click(self):
      self.hide()  # 隐藏此窗口
      self.ui = u3.UI_threeWindow()  # 将第二个窗口换个名字
      self.ui.show()  # 经第二个窗口显示出来


if __name__ == "__main__":
    #初始化窗口
    app = QApplication(sys.argv)
    fistWindow = FirstWindow() #实例化窗口
    fistWindow.show()
    sys.exit(app.exec_())

