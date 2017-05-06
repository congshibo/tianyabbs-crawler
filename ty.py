import os
import requests
from bs4 import BeautifulSoup
import time
jieguo = {}
yichang ={}
def xieruwenjian(yichang,jieguo):#写入文件函数----传入有无异常的字典及结果字典
    resultname = time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))+'扫描结果'
    if yichang != {}:
        yw = '有异常请查看'
        wj = os.getcwd() + '\\' + resultname + yw + '.txt'
        f = open(wj, 'w')
        f.write('-----------------\n')
        f.write('本次共扫描'+str(len(jieguo))+'个帖子\n')
        f.write('发现含有关键词的帖子为:\n')
        f.write('-----------------\n')
        for i in yichang:
            f.write('  '+i + ':' +  '\n')
            f.write('  网址：' + jieguo[i]+ '\n')
            f.write('------\n')
        f.write('\n\n-----------------\n')
        f.write('本次扫描全部扫描结果为:\n')
        f.write('-----------------\n')
        for i in jieguo:
            f.write(i + ':' +  '\n')
            f.write('  网址：'+jieguo[i]+ '\n')
            f.write('------\n')
        f.close()
    else:
        yw = '无异常'
        #os.getcwd()
        wj = os.getcwd()+ '\\' +resultname + yw+ '.txt'
        print(wj)
        f = open(wj, 'w')
        f.write('本次共扫描'+str(len(jieguo))+'个帖子\n')
        f.write('-----------------\n')
        f.write('本次扫描未发现关键词，以下为扫描结果:\n')
        f.write('-----------------\n')
        for i in jieguo:
            f.write('  '+i+':'+'\n')
            f.write('  网址：' + jieguo[i]+ '\n')
            f.write('------\n')
        f.close()
def duquguanjianci():#读取关键词txt中的关键词并返回一个数组
    f = open('关键词.txt','r')
    g = f.read()
    f.close()
    guanjianci = g.split('-')
    return guanjianci
def duquwangzhi():
    f = open('检测网址.txt','r')
    g = f.read()
    f.close()
    wangzhi = g.split('\n')
    return wangzhi
def gethtml(url):
    try:
        html = requests.get(url)
        return html.text
    except:
        jieguo['网络错误'] ='网络错误'
def chaci(bt):#如果标题中有关键词，则将该内容加入异常字典
    for ci in guanjianci:
        if bt.find(ci) > 0:
            yichang[bt]=jieguo[bt]
def fenxi(wangzhi,guanjianci):
    for wz in wangzhi:
        soup = BeautifulSoup(gethtml(wz), "html.parser")
        i = soup.findAll(title="普通帖")
        for i1 in i:
            #print('--------')
            t = i1.parent.a.string  # 如果a包含多个tag，则string为None
            if t != None:  # t不为空，则为标题
                #print(t.strip())
                #print(i1.parent.a.get('href'))
                bt = t.strip()
                nr = i1.parent.a.get('href')
                jieguo[bt]='http://bbs.tianya.cn'+nr
                chaci(bt)
            else:  # t为空，则a内含别的标签
                x = list(i1.parent.a.strings)  # 将a的srings变为列表，显示不为空的列表
                for x1 in x:
                    if x1.strip() ==  '':  # 如果x1为空
                        pass
                    else:
                        #print(x1.strip())
                        bt = x1.strip()
                #print(i1.parent.a.get('href'))
                nr = i1.parent.a.get('href')
                jieguo[bt] = 'http://bbs.tianya.cn'+nr
                chaci(bt)

guanjianci = duquguanjianci()
wangzhi =  duquwangzhi()
fenxi(wangzhi,guanjianci)
xieruwenjian(yichang,jieguo)








