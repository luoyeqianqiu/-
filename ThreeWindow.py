from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, qApp,QLabel,\
    QPushButton,QFileDialog,QLineEdit, QMenuBar, QStatusBar,QDesktopWidget,QComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import os
import FirstWindow as Fist
import tools
import xlrd
import time
from datetime import datetime
from xlrd import xldate_as_tuple

class UI_threeWindow(QMainWindow,QWidget):
    def __init__(self):
        super(UI_threeWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('表格检测器')
        self.resize(1000, 800)
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
        impAct = QtWidgets.QAction('返回主界面', self)
        # 调用窗口
        impAct.triggered.connect(self.returnFistWindow)

        impMenu.addAction(impAct)

        newAct = QtWidgets.QAction('New', self)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        # 设置底栏
        self.statusBar()

        self.goodsAddressLabe = QtWidgets.QLabel("文件选择：", self)
        self.goodsAddressLabe.move(110, 65)

        self.tipsLabel = QtWidgets.QLabel("字段选择：", self)
        self.tipsLabel.move(110, 130)

        self.resultLabel = QtWidgets.QLabel("结果输出：", self)
        self.resultLabel.resize(110, 40)
        self.resultLabel.move(110, 430)

        self.baseruleLabe = QtWidgets.QLabel("基础规则：", self)
        self.baseruleLabe.move(110, 190)

        self.linkruleLabe = QtWidgets.QLabel("关联规则：", self)
        self.linkruleLabe.move(110, 250)

        self.specialruleLabe = QtWidgets.QLabel("特殊规则：", self)
        self.specialruleLabe.move(110, 310)




        #文本框
        self.goodsAddress = QtWidgets.QLineEdit(self)
        self.goodsAddress.resize(550, 30)
        self.goodsAddress.move(210, 67)

        self.resultList = QtWidgets.QTextEdit(self)
        self.resultList.setLineWrapMode(0)
        self.resultList.resize(550, 300)
        self.resultList.move(210, 440)

        # 按钮位置
        self.onpenButton = QPushButton('打开', self)
        self.onpenButton.setToolTip('打开指定文件夹')
        self.onpenButton.resize(100, 30)
        self.onpenButton.move(780, 67)

        self.checkButton = QPushButton('开始检测', self)
        self.checkButton.resize(100, 30)
        self.checkButton.move(210, 370)

        self.saveButton = QPushButton('保存已选择规则', self)
        self.saveButton.resize(130, 30)
        self.saveButton.move(400, 370)

        self.clearnButton = QPushButton('清除记录', self)
        self.clearnButton.setToolTip("重置当前选项并清除已保存的表格记录")
        self.clearnButton.resize(130, 30)
        self.clearnButton.move(630, 370)

        #----- 下拉框位置布局 -----
        #字段选择
        self.wordselectButton = QComboBox(self)
        self.wordselectButton.resize(230,30)
        self.wordselectButton.move(210,130)
        # 单个添加条目
        self.wordselectButton.addItem('请选择要检验的字段')


        #基础规则
        self.baseruleButton = QComboBox(self)
        self.baseruleButton.resize(230, 30)
        self.baseruleButton.move(210, 190)
        # 单个添加条目
        self.baseruleButton.addItem('请选择要检验的规则')
        # 多个添加条目
        self.baseruleButton.addItems(['唯一性检查', '递增', '递减', '是否有空值', '日期格式检查', 'json格式检查', '字符串全角检查'])

        # 关联规则
        self.linkruleButton = QComboBox(self)
        self.linkruleButton.resize(230, 30)
        self.linkruleButton.move(210, 250)
        # 单个添加条目
        self.linkruleButton.addItem('请选择要检验的规则')
        # 多个添加条目
        self.linkruleButton.addItems(['检查主表字段是否在子表出现'])

        # 特殊规则
        self.specialruleButton = QComboBox(self)
        self.specialruleButton.resize(230, 30)
        self.specialruleButton.move(210, 310)
        # 单个添加条目
        self.specialruleButton.addItem('请选择要检验的规则')
        # 多个添加条目
        self.specialruleButton.addItems(['公式运算字段值'])

    #----绑定事件------
        self.onpenButton.clicked.connect(self.OnOpenFile)
        self.checkButton.clicked.connect(self.check)

    #----事件处理------
    #返回主界面
    def returnFistWindow(self):
        self.hide()
        self.ui = Fist.FirstWindow()  # 将第一个窗口换个名字
        self.ui.show()  # 将第一个窗口显示出来

    #打开文件
    def OnOpenFile(self, event):
        # _translate = QtCore.QCoreApplication.translate
        directory1 = QFileDialog.getOpenFileName(None, "选择文件", os.getcwd())
        # 文件夹路径
        path = directory1[0]
        self.goodsAddress.setText(path)

        # 先清空原有的选项
        self.wordselectButton.clear()
        self.wordselectButton.insertItem(0, "请选择要检验的字段")

        #遍历表后把字段填入下拉框
        rsheet =tools.readTable(self.goodsAddress.text())
        keys = rsheet.row_values(0)
        self.wordselectButton.addItems(keys)

    #开始检测
    def check(self, event):
        #取需要检验的字段
        selectWord = self.wordselectButton.currentText()
        if selectWord == '请选择要检验的字段':
            print('您没有选择要检验的字段')
            return

        #进行基础规则检验
        baseRulecheck = self.baseruleButton.currentText()

        #处理各种选项
        if baseRulecheck == '唯一性检查':
            print('您选择的是唯一性')
            #读取指定表
            rsheet = tools.readTable(self.goodsAddress.text())
            #根据列名得出所在列所在index坐标
            index = tools.getColumnIndex(rsheet,selectWord)
            #打印指定列的值
            list = rsheet.col_values(index)
            #删除列名
            del list[0]
            #进行判断是否唯一性
            tools.checkuniqueness(list)

        elif baseRulecheck == '递增':
            print('您选择的是递增')
            rsheet = tools.readTable(self.goodsAddress.text())
            # 根据列名得出所在列所在index坐标
            index = tools.getColumnIndex(rsheet, selectWord)
            # 打印指定列的值
            list = rsheet.col_values(index)
            # 删除列名

            del list[0]
            # if not type(list[0])
            tools.increasing(list)


        elif baseRulecheck == '递减':
            print('您选择的是递减')
            rsheet = tools.readTable(self.goodsAddress.text())
            # 根据列名得出所在列所在index坐标
            index = tools.getColumnIndex(rsheet, selectWord)
            # 打印指定列的值
            list = rsheet.col_values(index)
            # 删除列名
            del list[0]
            # if not type(list[0])
            tools.decrease(list)

        elif baseRulecheck == '是否有空值':
            print('您选择的是是否有空值')
            rsheet = tools.readTable(self.goodsAddress.text())
            # 根据列名得出所在列所在index坐标
            index = tools.getColumnIndex(rsheet, selectWord)
            # 打印指定列的值
            list = rsheet.col_values(index)
            # 删除列名
            del list[0]
            # if not type(list[0])
            tools.ifnull(list)

        elif baseRulecheck == '日期格式检查':
            print('您选择的是日期格式检查')
            rsheet = tools.readTable(self.goodsAddress.text())
            # 根据列名得出所在列所在index坐标
            cellIndex = tools.getColumnIndex(rsheet, selectWord)
            # 打印指定列的值
            list = rsheet.col_values(cellIndex)
            # 删除列名
            del list[0]
            # for index in range(len(list)):
            #     date = datetime(*xldate_as_tuple(list[index], 0))
            #     cell = date.strftime('%Y-%m-%d')  # ('%Y/%m/%d %H:%M:%S')
            #     type(cell)
            #     print(cell)
            #     print(tools.isVaildDate(cell))
            # 根据Ctype返回的数据来判断返回的格式是否正确
            #ctype： 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
            flag=0
            for index in range(len(list)):
                ctype = rsheet.cell(index+1, cellIndex).ctype
                if ctype!=3:
                    flag=1
                    break
            if flag==1:
                print('该列数据存在不符合日期格式的数据')
            else:
                print('该列数据符合日期格式')

        elif baseRulecheck == '字符串全角检查':
            print('您选择的是字符串全角检查')
            rsheet = tools.readTable(self.goodsAddress.text())
            # 根据列名得出所在列所在index坐标
            index = tools.getColumnIndex(rsheet, selectWord)
            # 打印指定列的值
            list = rsheet.col_values(index)
            # 删除列名
            del list[0]
            # if not type(list[0])
            flag=0
            for index in range(len(list)):
                list2=tools.stringQ2B(list[index])
                if tools.ifquanjiao(list2)==1:
                    flag=1
                    break
            if flag == 1:
                print('该列数值存在全角字符')
            else:
                print('该列字符不存在全角字符')

        elif baseRulecheck == 'json格式检查':
            print('您选择的是json格式检查')
            rsheet = tools.readTable(self.goodsAddress.text())
            # 根据列名得出所在列所在index坐标
            index = tools.getColumnIndex(rsheet, selectWord)
            # 打印指定列的值
            list = rsheet.col_values(index)
            # 删除列名
            del list[0]
            tools.is_json(list)







        # tools.checkuniqueness()