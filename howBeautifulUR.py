import tkinter as tk
import cv2
from PIL import Image, ImageTk
# encoding:utf-8
import requests
import base64
from tkinter import filedialog
import queue
import numpy as np


def getImage(imagePath,panel):
    # img=cv2.imread(imagePath)
    img = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), -1)
    x, y = img.shape[0:2]
    img = cv2.resize(img, (int(y/3*2), int(x/3*2)))
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
    current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
    imgtk = ImageTk.PhotoImage(image=current_image)
    panel.imgtk = imgtk
    panel.config(image=imgtk)

def getToken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=T5nEHWRnTQ6LZS0DwxHD11VE&client_secret=TxFTseepNPkAMeAV14tYYKM23BYtiOq4'
    response = requests.get(url=host,verify=False)
    if response:
        # print(response.json())
        accessToken=response.json()['access_token']
        return accessToken
    else:
        raise ValueError('无网络连接')

# 将一张图片转换为字符格式
def getImage2Base64(imagePath):
    f = open(imagePath, 'rb')
    img = base64.b64encode(f.read()).decode('utf-8')
    return img

def getAttribute(imagePath):
    img=getImage2Base64(imagePath)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {"image": img, "image_type": "BASE64",
              "face_field": "age,gender,beauty"}
    header = {'Content-Type': 'application/json'}

    access_token = getToken()

    request_url = request_url + "?access_token=" + access_token
    response1 = requests.post(url=request_url, data=params, headers=header,verify=False)
    json1 = response1.json()
    # print("性别为", json1["result"]["face_list"][0]['gender']['type'])
    # print("年龄为", json1["result"]["face_list"][0]['age'], '岁')
    print(json1)
    theSex=json1["result"]["face_list"][0]['gender']['type']
    theAge=json1["result"]["face_list"][0]['age']
    theBeauty=json1["result"]["face_list"][0]['beauty']
    return theSex,str(theAge),theBeauty

# 获取性别和年龄
def get_Attribute_Of_Face(imagePath):

    theSex,theAge,theBeauty=getAttribute(imagePath)

    sexClass=tk.StringVar()
    sexClass.set(theSex)
    # sexStr=tk.StringVar()
    # sexStr.set(theSex)


    ageClass=tk.StringVar()
    ageClass.set(theAge)
    # ageStr=tk.StringVar()
    # ageStr.set(theAge)

    beautyClass=tk.StringVar()
    beautyClass.set(theBeauty)

    return sexClass,ageClass,beautyClass

def selectPath():
    path_ = filedialog.askopenfilename()
    path.set(path_)


def secondWindow(imagePath):
    print("进入:",imagePath)
    win=tk.Toplevel()
    panel = tk.Label(win)  # initialize image panel
    win.config(cursor="arrow")
    getImage(imagePath,panel)  # 用于在gui界面上显示图片

    fm2 = tk.Frame(win)
    L1 = tk.Label(fm2, text="性别")
    sexStr, ageStr, beautyStr = get_Attribute_Of_Face(imagePath)
    E0 = tk.Entry(fm2, textvariable=sexStr, bd=2)
    L2 = tk.Label(fm2, text="年龄")
    E1 = tk.Entry(fm2, textvariabl=ageStr, bd=2)
    L3 = tk.Label(fm2, text="颜值")
    E2 = tk.Entry(fm2, textvariable=beautyStr, bd=2)
    L1.pack(side=tk.LEFT)
    E0.pack(side=tk.LEFT)
    L2.pack(side=tk.LEFT)
    E1.pack(side=tk.LEFT)
    L3.pack(side=tk.LEFT)
    E2.pack(side=tk.LEFT)
    fm2.pack(side=tk.TOP)

    panel.pack(padx=10, pady=10)
    win.mainloop()



root = tk.Tk()
root.title("GUI")

# imagePath="C:/Users\FGX\Desktop/test.jpg"
fm1=tk.Frame(root)

path = tk.StringVar()

Ltop=tk.Label(fm1,text="请选择图片路径")

# print("path:",path.get())
# B1=tk.Button(fm1, text = "路径选择", command =selectPath)
# E1=tk.Entry(fm1, textvariable =path,bd=5)
# B2=tk.Button(fm1, text = "确定", command =lambda:secondWindow(path.get()))


B1=tk.Button(fm1, text = "路径选择", command =selectPath)
E1=tk.Entry(fm1, textvariable =path,bd=5)
# imagePath=path.get()
B2=tk.Button(fm1, text = "确定", command =lambda:secondWindow(path.get()))

Ltop.pack(side = tk.TOP)
B1.pack(side=tk.LEFT)
E1.pack(side = tk.LEFT)
B2.pack(side=tk.LEFT)
fm1.pack(side=tk.TOP)
root.mainloop()
