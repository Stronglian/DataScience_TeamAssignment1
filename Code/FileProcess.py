# -*- coding: utf-8 -*-
"""
Team Assignment 1 - part4 - FileProcess - read file
windows 7
"""
from datetime import datetime
import json
import codecs
import os

def GetForderls(pwd = '.'):
    jsonFileList = []
    for dirname, dirnames, filenames in os.walk(pwd):
        #print(filenames)
        # print path to all filenames.
        for filename in filenames:
            #print(filename[-5:])
            if filename[-5:] == ".json":
                #print(os.path.join(dirname, filename))
                jsonFileList.append(os.path.join(dirname, filename))
        break #只抓當前資料夾內
    #print(jsonFileList)
    return jsonFileList

def GetTAGFileList(TAGs):
    fileLs = GetForderls()
    TAGFileList = [] #[TAG1List, TAG2List, ...]
    for i in range(len(TAGs)):
        TAGFileList.append([])
    for filenameWithLoca in fileLs:
        #取得位置與標籤
        filename = filenameWithLoca.split('\\')[1]
        TAG = filename.split('_')[-1].split('.')[0]
        #分類
        for i in range(len(TAGs)):
            if TAG == TAGs[i]:
                TAGFileList[i].append(filename)
    return TAGFileList
    
def MergeJSON(filename1, filename2):
    #print("#讀取檔案")
    with open(filename1, encoding='utf-8') as f:
        dict1 = json.load(f)
    with open(filename2, encoding='utf-8') as f:
        dict2 = json.load(f)
    #print("#merge and reset number")
    dict1['article'].update(dict2['article'])
    dict1['article_amount'] = len(dict1['article'])
    #print("#儲存檔案")
    #filenameNew = SaveMergeDICT2JSON(dict1, filename1)
    TAG = filename1.split("_")[-1].split('.')[0]
    mergeTimeTag = "_merge_"+str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) +'_'+TAG
    filenameNew = filename1.split("_",1)[0] + '_' +filename1.split("_")[1].split('.')[0] + mergeTimeTag + ".json"
    with codecs.open(filenameNew, "w+", encoding='utf-8') as f:
        f.write(json.dumps(dict1, sort_keys=True, ensure_ascii=False))
    #print("#del old file")
    if filename1 != filenameNew:
        os.remove(filename1)
    os.remove(filename2)
    dict1.clear()
    dict2.clear()
    return filenameNew
    
def MergeJSONWithTAGs(TAGs):
    #get file list
    TAGFileList = GetTAGFileList(TAGs)
    for i in range(len(TAGFileList)):
        if len(TAGFileList[i]) > 1:
            #print(TAGs[i], "多於一個檔案")
            #print("檔案名稱:", TAGFileList[i])
            for j in range(1, len(TAGFileList[i])):
                #print("MergeJSON:",TAGFileList[i][0], TAGFileList[i][j])
                TAGFileList[i][0] = MergeJSON(TAGFileList[i][0], TAGFileList[i][j])
            #print("+++")
    return
    
def JSONFileVvrification(TAGs):
    TAGFileList = GetTAGFileList(TAGs)
    for FileList in TAGFileList:
        for filename in FileList:
            try:
                with open(filename, encoding='utf-8') as f:
                    dict1 = json.load(f)
            except:
                print("FormatERROR:",filename)
                #os.remove(filename)
    return

if __name__ == '__main__':
    TAGs = ["politics", "entertainment"]
    MergeJSONWithTAGs(TAGs)