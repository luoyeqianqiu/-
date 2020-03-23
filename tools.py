#!/usr/bin/env python3
# coding: utf-8
import xlrd
import re
import os
import time
import json

#创建初始文件
def create_starFiles():
    # 设置路径
    file_path = os.getcwd() + '\\file\\'
    if not os.path.exists(file_path):  # 判断文件夹是否已经存在
        os.makedirs(file_path)
        f1 = open(file_path + 'address' + '.txt','w')
        f2 = open(file_path + 'input' + '.txt','w')
        f3 = open(file_path + 'output' + '.txt','w')
        f1.write('')
        f2.write('')
        f3.write('')
        print('初始文件创建成功')
    else:
        f1 = file_path + 'address' + '.txt'
        f2 = file_path + 'input' + '.txt'
        f3 = file_path + 'output' + '.txt'

        if not os.path.exists(f1):
            f = open(file_path + 'address' + '.txt', 'w')
            f.write('')

        if not os.path.exists(f2):
            f = open(file_path + 'input' + '.txt', 'w')
            f.write('')

        if not os.path.exists(f3):
            f = open(file_path + 'output' + '.txt', 'w')
            f.write('')


# 创建txt文件并往里面存入数据
def Txt_write(name,msg,type):
    #设置路径
    file_path = os.getcwd()+'\\file\\'
    fullPath = file_path+name+'.txt'
    # 1代表覆写，2代表续写
    if type == 1:
        f = open(fullPath, 'w')
        f.write(msg)
    if type == 2:
        f = open(fullPath, 'a')
        f.write(msg)
    f.close()



# 读取数据
def Txt_read(name):
    file_path = os.getcwd() + '\\file\\'
    fullPath = file_path + name + '.txt'
    f = open(fullPath, 'r')
    msg=f.read()
    f.close()
    return msg


#把字符串转换成集合
def getDataFromStr(Str):
    # 获取所有大括号配对
    rewardList = []
    # 左括号索引
    leftIndex = None
    for i in range(len(Str)):
        s = Str[i]
        if s == '{':
             leftIndex = i
        elif s == '}':
            assert(leftIndex != None)
            cut = Str[leftIndex + 1 : i]
            rewardList.append(cut)
            leftIndex = None

    # print('rewardList--', rewardList)
    dataList = []
    # 正则表达式修饰符
    lable = '"(.*)"\s?:\s?(.*)'
    for reward in rewardList:
        keyValueList = reward.split(',')
        data = {}
        for keyValue in keyValueList:
            gg = re.findall(lable, keyValue)
            key = gg[0][0]
            value = gg[0][1]
            data[key] = value
        dataList.append(data)
    return dataList

# 清空文件内容
def Txt_delete(name):
    file_path = os.getcwd() + '\\file\\'
    fullPath = file_path + name + '.txt'
    with open(fullPath, 'r+') as f:
        f.seek(0)
        f.truncate(0)
        f.close()

#判断列表元素是否有重复值
def checkuniqueness(list):
    # 建立字典，这种方法建立字典，会把列表里的元素当做字典的键，由于字典的键不能重复，所以会自动去重
    dic = {}.fromkeys(list)
    #判断两个字段之间的长度
    if len(dic) == len(list):
        print('列表里的元素互不重复！')
    else:
        print('列表里有重复的元素！')

#判断列表元素是否递增
def increasing(list):
    flag = 1
    for index in range(len(list)-1):
        # print(index,list[index])
        if list[index]>list[index+1]:
            flag = 0
            break
    if flag==0:
        print("该数组不是递增")
    else:
        print("该数组递增")

#判断列表元素是否递增
def decrease(list):
    flag = 1
    for index in range(len(list)-1):
        # print(index,list[index])
        if list[index]<list[index+1]:
            flag = 0
            break
    if flag==0:
        print("该数组不是递减")
    else:
        print("该数组递减")

#判断列表元素是否有空值
def ifnull(list):
    flag = 1
    for index in range(len(list)):
        if list[index] == '':
            flag=0
            break
    if flag==0:
        print("该数组存在空值")
    else:
        print("该数值不存在空值")

#判断列表元素是否有空值
def ifquanjiao(list):
    flag = 0
    for index in range(len(list)):
        if list[index] == 1:
            flag=1
            return flag
    return flag

#判断列表元素是否符合日期格式
"""
功能：判断是否为日期
"""
def isVaildDate(sDate):
    try:
        if ":" in sDate:
            time.strptime(sDate, "%Y-%m-%d %H:%M:%S")
        elif ":" in sDate:
            time.strptime(sDate, "%Y/%m/%d %H:%M:%S")
        else:
            time.strptime(sDate, "%Y-%m-%d")
        return True
    except:
        return False


#根据列名得出所在列的index
def getColumnIndex(table,columnName):
    columnIndex = None
    # print table
    for i in range(table.ncols):
        # print columnName
        # print table.cell_value(0, i)
        if (table.cell_value(0, i) == columnName):
            columnIndex = i
            break
    return columnIndex

#读取表格并返回数据
def readTable(tableaddress):
    rbook = xlrd.open_workbook(tableaddress)
    rbook.sheets()
    # xls默认有3个工作簿,Sheet1,Sheet2,Sheet3
    rsheet = rbook.sheet_by_index(0)  # 取第一个工作簿
    return rsheet

#判断列表是否为递增
def judge(alist):
    if any(alist[i+1] <= alist[i] for i in range(0,len(alist)-1)):
        print('该字段不是递增')

    else:
        print('该数组是递增')

"""全角转半角"""
def Q2B(uchar):
    flag=0
    inside_code = ord(uchar)
    # if inside_code == 0x3000:
    #     inside_code = 0x0020
    # else:
    #     inside_code -= 0xfee0
    #全角判断
    if inside_code < 0x0020 or inside_code > 0x7e:
        flag = 1
        return flag
    return flag

def stringQ2B(ustring):
    return [Q2B(uchar) for uchar in ustring]

#判断是否为json
def is_json(list):
    flag = 0
    for index in range(len(list)):
        try:
            json_object = json.loads(list[index])
        except Exception as e:
            flag=1
            print(index)
            break
    if flag == 1:
        print("该数组元素存在非json格式数据")
    else:
        print("该数组元素所有数据均为json格式")

#判断是否为int型
# def is_int(list):
#     flag = 0
#     print(type(list[0]))
#     for index in range(len(list)):
#         if type(list[index])!=int:
#             flag=1
#             break
#     if flag == 1:
#         print("该数组元素存在非int格式数据")
#     else:
#         print("该数组元素所有数据均为int格式")

# 逐行读取数据
# def line_read():
#     path = "C:/Users/DELL/Desktop/测试数据.txt"
#     file = open(path, "r")
#     while True:
#         myStr = file.readline()  # 表示一次读取一行
#         if not myStr:
#             # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
#             break
#         print(myStr, end="")  # 打印每次读到的内容

# 读取文件夹下的文件
# v_foleder = os.getcwd()
# Vname_list = os.listdir(v_foleder)
# print(Vname_list)
