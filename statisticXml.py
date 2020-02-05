import sys
import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
def getallstatisticData(xmldir):
    finalDictSize={}
    finalDictClasses={}#  classes num
    finalDictClassesPerImage={}#classes pic num  未统计，统计是否有意义？
    errorPath=[]
    errorSizePath=[]
    for file in os.listdir(xmldir):
        if file.endswith('.xml'):
            with open(os.path.join(xmldir,file),'r') as f:
                tree=ET.parse(f)
                root=tree.getroot()
                size=root.find('size')
                w = int(size.find('width').text)
                h = int(size.find('height').text)
                if w<=3 or h<=3:
                    strerrorpath = 'error:the size is  invalid!(' + str(f.name) + ')' + '\n'
                    print(strerrorpath)
                    errorSizePath.append(strerrorpath)
                finalDictSize=getnewdictSize(finalDictSize,w,h)# test 形参是否有效
                for obj in root.iter('object'):
                    #difficult = obj.find('difficult').text
                    cls = obj.find('name').text
                    finalDictClasses=getnewUnit(cls,finalDictClasses)
                    xmlbox = obj.find('bndbox')
                    b = (
                    float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                    float(xmlbox.find('ymax').text))
                    if b[0]>b[1] or b[2]>b[3] or b[1]-b[0]<=3 or b[3]-b[2]<=3 :#3个像素的差距的rect 不作为检测目标，视为标注失败
                        strerrorpath='error:the rect is  invalid!('+str(f.name)+')'+'\n'
                        errorPath.append(strerrorpath)
                        print(strerrorpath)

    wfile=open(os.path.join(xmldir,'allStatistic.txt'),'w')
    wfile.write('Error_Path>>>>>>>>>>>>>>>>>>>>>>>>(Size_h<=3 or Size_w<=3 ):' + '\n')
    for strvalue in errorSizePath:
        wfile.write(str(strvalue))
    wfile.write('Error_Path>>>>>>>>>>>>>>>>>>>>>>>>(span<=3 or rect is invalid):'+ '\n')
    for strvalue in errorPath:
        wfile.write(str(strvalue))
    wfile.write('Classes_statistic>>>>>>>>>>>>>>>>>>>>>>>>:'+ '\n')
    for k,v in finalDictClasses.items():
        wfile.write(str(k) + ' ' + str(v) + '\n')
    wfile.write('Sizes_statistic>>>>>>>>>>>>>>>>>>>>>>>>:'+ '\n')
    for k, v in finalDictSize.items():
        wfile.write(str(k) + ' ' + str(v) + '\n')
    wfile.close()
    drawHistogram(finalDictClasses,xmldir)



def getnewdictSize(dictSize,w,h):
    if (w,h) in dictSize:
        dictSize[(w,h)]+=1
        return  dictSize
    else:
        dictSize[(w,h)]=1
        return dictSize


def getnewUnit(element,orgUnit):
    if element  in orgUnit:
        orgUnit[element]+=1
        return orgUnit
    else:
        orgUnit.update({element:1})
        return  orgUnit

def drawHistogram(showdict,path):
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % int(height))

    cols =[]
    rows=[]
    plt.figure(figsize=(20, 8))
    for k,v in showdict.items():
        rows.append(str(k))
        cols.append(v)
    autolabel(plt.bar(range(len(rows)),cols,color='rgb',tick_label=rows))
    plt.xticks(rotation=45)

    plt.xlabel('Classes')
    plt.ylabel('Numbers')
    plt.title('Statistic of Classes')
    plt.savefig(path+'\Statistic.png')
    plt.show()


def main():

    strDir=input('input your statistic dir:')
    #classes,numperclass,sizes  =\
    getallstatisticData(strDir)
    print('end!')
    pass
if __name__=='__main__':
    main()