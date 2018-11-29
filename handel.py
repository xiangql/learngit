#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pandas as pd
import json
import time
import re
import os, sys

#仅适用标准小驼峰和下划线命名格式的数据
#################################  handel .txt function   ####################################################
#修改key
#flag替换字符串
#sign True 变全小写 False 不改变key
#pattern 匹配的字符串正则
def change_key(key=None,flag="_",sign=True,pattern=None):
    if key == None or pattern == None:
        return "none"
    for i in key:
        newStr = re.sub(pattern,lambda x: flag + x.group(0),key)
        if sign:            
            newStr = newStr.lower()
        return newStr

#去除字典的多重嵌套
def get_dict_item(item,retItem):
    pattern = "[A-Z]"
    for k, v in item.items():
        if type(v) == type(dict()):
            get_dict_item(v,retItem)
        else:
            k = change_key(key=k, flag="_", sign=True, pattern=pattern)
            retItem[k] = v
    return retItem

#对文件每行数据进行处理
def handel_listStrs(listStrs):
    listDicts = []
    for strData in listStrs:
        pattern = "^\<(.+?)\>"
        jsonData = re.sub(pattern,'',strData)
        dictData = json.loads(jsonData)
        dictItem = {}
        dictItem = get_dict_item(dictData,dictItem)
        listDicts.append(dictItem)
    return listDicts
    pass

#从txt文件中提取数据
def read_ftxt(filepath):
    try:
        with open(filepath,'r') as ftxt:
            listStrs = ftxt.readlines()
            listDicts = handel_listStrs(listStrs)
            return listDicts
    except Exception as e:
        print(e)
        sys.exit(-1)
    pass


# data = read_ftxt('test.txt')
# print(data)
# print(type(data[0]))


#################   handel .csv function     ###################################

def read_fcsv(filepath):
    listDicts = []
    csvdf = pd.read_csv(filepath)
    jsonData = csvdf.to_json(orient='index')
    dictData = json.loads(jsonData)
    listDatas =  dictData.values()
    pattern = "(vw_tt_ipress)"
    for data in listDatas:
        retItem = {}
        for k, v in data.items():
            kt = k.split(".")[1]
            if v == None:
                v = ""
            retItem[kt] = v
        listDicts.append(retItem)
    return listDicts
    pass


# data = read_fcsv("test.csv")
# print(data)

####################     handel .excel function   ##############################

def read_excel(filepath):
    pass



###############################   对文件的统一处理   #######################################
def read_file_to_dicts(filepath):
    if "txt" in filepath:
        ret = read_ftxt(filepath)
        pass
    elif "csv" in filepath:
        ret = read_fcsv(filepath)
        pass
    elif "xlsx" in filepath:
        pass
    return ret



# ret = read_file_to_dicts('test.txt')
# print(ret)


#对两个字典共有键值对的比较
def check_dict(dt1,dt2):
    for k in dt1:
        if k in dt2.keys():
            if str(dt1[k]) != str(dt2[k]):
                return[False,dt1]
    return[True,dt1]

#装饰器，统计文件处理时间
def fun(test):
    def innerFun(path1,path2,ret):
        print("start:",end='')
        stime = time.time() 
        test(path1,path2,ret)
        etime = time.time()
        tt = etime - stime
        print("\n\n",tt,"s function end!")
    return innerFun


#对两个文件的数据进行比较，将文件一的差异数据写入结果文件中
@fun
def compare_data_write_to_file(path0,path1,ret):
    listData0 = read_file_to_dicts(path0)
    listData1 = read_file_to_dicts(path1)
    if os.path.exists(ret):
        if input("result file exist,confirm rewrite(y/n)") == "n":
            ret = input("reinput result file name:  ")
    with open(ret,"w") as wfile:
        for i, dt1 in enumerate(listData0):
            if i%50 == 0:
                print("#",end='',flush=True)
            ret = []
            for dt2 in listData1:
                ret = check_dict(dt1,dt2)
                if ret[0]:
                    break
            if ret[0] == False:
                wfile.write(str(ret[1])+"\n")



compare_data_write_to_file("../d11291/1.csv","../d11291/0.txt","ret.txt")

















