#include <QDesktopWidget>
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, qApp,QLabel,\
    QPushButton,QFileDialog,QLineEdit, QMenuBar, QStatusBar,QDesktopWidget,QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import os
import FirstWindow as Fist
import tools
import xlrd

class Ui_towWindow(QMainWindow,QWidget):
    #定义成员变量,用来存储物品表指定字段的字典
    dit={}

    #创建初始文件
    tools.create_starFiles()

    def __init__(self):
        super(Ui_towWindow,self).__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('奖励转换器')
        self.resize(1000,800)
        # 位置居中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

        # 创建一个菜单栏
        menubar = self.menuBar()
        # 添加菜单
        fileMenu = menubar.addMenu('File')

        impMenu = QtWidgets.QMenu('跳转', self)
        impAct =QtWidgets.QAction('返回主界面', self)
        #调用窗口
        impAct.triggered.connect(self.returnFistWindow)

        impMenu.addAction(impAct)

        newAct =QtWidgets.QAction('New', self)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        # 设置底栏
        self.statusBar()

        #功能标题
        self.goodsAddressLabe = QtWidgets.QLabel("物品表地址:",self)
        self.goodsAddressLabe.move(110, 65)

        self.tipsLabel = QtWidgets.QLabel("请输入数值:", self)
        self.tipsLabel.move(110, 135)

        self.resultLabel = QtWidgets.QLabel("请输出物品价值:", self)
        self.resultLabel.resize(140,40)
        self.resultLabel.move(80, 460)

        #地址栏
        self.goodsAddress = QtWidgets.QLineEdit(self)
        self.goodsAddress.setText(tools.Txt_read('address'))
        self.goodsAddress.resize(500, 30)
        self.goodsAddress.move(210, 67)

        #文本框
        self.goodsList = QtWidgets.QTextEdit(self)
        self.goodsList.setLineWrapMode(0)
        self.goodsList.resize(500, 280)
        self.goodsList.move(210, 130)

        self.resultList = QtWidgets.QTextEdit(self)
        self.resultList.setLineWrapMode(0)
        self.resultList.resize(500, 280)
        self.resultList.move(210, 460)

        # 按钮位置
        self.onpenButton = QPushButton('打开', self)
        self.onpenButton.setToolTip('打开指定文件夹')
        self.onpenButton.resize(100,30)
        self.onpenButton.move(730,65)

        self.saveButton = QPushButton('保存',self)
        self.saveButton.resize(100, 30)
        self.saveButton.move(830,65)

        self.transformButton = QPushButton('转换', self)
        self.transformButton.resize(100, 30)
        self.transformButton.move(730, 130)

        #绑定事件
        self.onpenButton.clicked.connect(self.OnOpenFile)
        self.saveButton.clicked.connect(self.save)
        self.transformButton.clicked.connect(self.transform)

    #处理事件
    def returnFistWindow(self):
        self.hide()
        self.ui = Fist.FirstWindow()  # 将第一个窗口换个名字
        self.ui.show()  # 将第一个窗口显示出来

    def OnOpenFile(self, event):
        # _translate = QtCore.QCoreApplication.translate
        directory1 = QFileDialog.getOpenFileName(None, "选择文件", os.getcwd())
        # 文件夹路径
        path = directory1[0]
        self.goodsAddress.setText(path)

    # 保存按钮方法
    def save(self, event):
        #把输入的地址存入指定文件夹
        tools.Txt_write('address',self.goodsAddress.text(), 1)
        # tools.create_starFiles()


    # 转换按钮方法
    def transform(self, event):
        if self.goodsAddress.text() is '':
            reply =QMessageBox.warning(self,'提示', '文件地址输入错误',QMessageBox.Yes | QMessageBox.No)
            return

        # 清空结果目录文件内容
        tools.Txt_delete('output')
        tools.Txt_delete('input')

        # 打开excel文件，创建一个workbook对象,book对象也就是fruits.xlsx文件,表含有sheet名
        # rbook = xlrd.open_workbook('C:/Users/lzj/Desktop/Test2.xlsx')

        rbook = xlrd.open_workbook(self.goodsAddress.text())


        # sheets方法返回对象列表
        rbook.sheets()
        #xls默认有3个工作簿,Sheet1,Sheet2,Sheet3
        rsheet = rbook.sheet_by_index(0)  # 取第一个工作簿

        # 循环工作簿的所有行
        for row in rsheet.get_rows():
            product_column = row[0]  # 商品名所在的列
            product_id = product_column.value  # 项目名
            if product_id != '物品ID':  # 排除第一行
                price_column = row[2]  # 道具价值所在的列
                price_value = price_column.value
                name_column = row[1]
                name_value = name_column.value
                # 打印
                print("物品ID", product_id, "道具名称", name_value, "道具价值",price_value)
                self.dit[int(product_id)] = [name_value, price_value]

        # 读取输入框的内容并存储进input文件
        input =self.goodsList.toPlainText()
        tools.Txt_write("input", input, 1)

        # path = "C:/Users/DELL/Desktop/input.txt"
        path = os.getcwd()+'\\file\\'+'input'+'.txt'
        file = open(path, "r")
        while True:
            myStr = file.readline()  # 表示一次读取一行
            if not myStr:
                # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
                break
            dataList = tools.getDataFromStr(myStr)

            sum = 0
            for i in dataList:
                key = int(i['code'])
                item_price = self.dit[key][1]
                item_name = self.dit[key][0]
                item_num = int(i['amount'])

                tools.Txt_write('output', item_name + '*' + str(item_num) + ' ', 2)
                sum = sum + item_price * item_num

            tools.Txt_write('output', "总价值为：" + str(sum) + '\r', 2)

            self.resultList.setText(tools.Txt_read('output'))
        print("转换成功")













