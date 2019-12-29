from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re
import datetime
import sys

preAdd = "D:\\file\\py\\net\\"
fileName = preAdd + "BingPhoto\\ErrorFile.txt"

#利用datetime库将时间转化为字符串
curTime = datetime.datetime.now()
curDate = str(curTime.year)+"-"+str(curTime.month)+"-"+str(curTime.day)

#利用爬虫爬取必应首页照片的url
def getPhotoUrl():
    sourceLink = "https://cn.bing.com"
    html = urlopen(sourceLink)
    bsObj = BeautifulSoup(html)
    phototUrl = sourceLink + bsObj.find("link", {"id":"bgLink"}).attrs["href"]
    return phototUrl

#利用request中的urlretrieve下载照片到某一文件夹
def getPhoto(photoUrl):
    photoAdd = preAdd + "BingPhoto\\"
    photoName = photoAdd + curDate + ".jpg"
    urlretrieve(photoUrl, photoName)

#检查今日是否已经下载过照片
def notDownloaded():
    ret = True
    with open(fileName) as file:
        for line in file:
            if curDate in line and "successfully" in line:
                ret = False
    return ret

#写入错误文件
#若下载照片正常则写入正常
#若有异常则写入error
def writeFile(flag):
    if (flag==True):
        with open(fileName, 'a') as file:
            file.write("Photo download successfully on " \
                + curDate + "!\n")
        print("Download Successfully!")
    else:
        with open(fileName, 'a') as file:
            file.write("**********\n")
            file.write("There is an error on " + curDate + "\n")
            file.write("The error is " + str(flag) + "\n")
            file.write("**********\n")
        print("Error!")

#处理异常情况
if (notDownloaded()): 
    try:
        url = getPhotoUrl()
        getPhoto(url)
        writeFile(True)
    except Exception as e:
        writeFile(e)
else:
    print("Have downloaded!")

#运行完不关闭命令行窗口
if (input("Press <enter> to quit")==""):
    sys.exit()
    