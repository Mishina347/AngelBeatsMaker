#coding:utf-8

import speech_recognition as sr
import json
import time
import random
import urllib
import MeCab
from websocket import create_connection
ws = create_connection("ws://localhost:9999")

mecab = MeCab.Tagger ('-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
#文字列がGCされるのを防ぐ

soundlist = []
jsonDataList = []
noun_list = []
num = 1

json_data = {}

def randomint():
    t = random.randint(300,800)
    r = random.randint(100,1000)
    b = random.randint(300,800)
    l = random.randint(100,1000)
    flag = random.randint(0,3)
    return {"t":t,"r":r,"b":b,"l":l,"f":flag}

def get_nouns(sentence, nounlist):
    count = len(sentence)

    isSplited = False
    if count > 1:
        text = ""
        pre_word =""
        isSplited = False
        node = mecab.parseToNode(sentence)
        
        while node:
            word = node.surface
            try:
                yomi = node.feature.split(",")[7]
                hinshi = node.feature.split(",")[0]
                hinshi_ = node.feature.split(",")[1]
            except:
                yomi = ""
            if word == yomi :
                jsonDataList.append(text)
                jsonDataList.append(word)
                isSplited = True
                text =""
            elif hinshi_ == "一般" and len(text)>8 :
                jsonDataList.append(text)
                jsonDataList.append(word)
                isSplited = True
                text =""
            elif hinshi == "動詞" and len(text)>8:
                jsonDataList.append(text)
                jsonDataList.append(word)
                isSplited = True
                text =""
            elif hinshi == "名刺" and hinshi_ == "非自立":
                jsonDataList.append(text)
                jsonDataList.append(word)
                isSplited = True
                text =""
            elif(hinshi == "終助詞"):
                tmp = pre_text + word
                jsonDataList.pop()
                jsonDataList.append(tmp)
                isSplited = True
                text =""
            else:
                text += word
                pre_text = word
            node = node.next
        else:
            jsonDataList.append(text)

    print("json : "+ str(jsonDataList))


def makeJson():
    ver = num
    margins = randomint()
    scene_num =  "[c "+ str(ver)+ "]"
    print("jsonList : "+str(jsonDataList))
    data ={"t": margins["t"],"r": margins["r"],"b":margins["b"],"l":margins["l"],"f":margins["f"],"texts":jsonDataList,"scene_num":scene_num}
    ws.send(json.dumps(data,indent=2))
    result =  ws.recv()
    print(result)
    print(data)    

while True:
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("何か言って...")
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print ("解析中")

    try:
        text = r.recognize_google(audio, language='ja-JP')
        print("認識:"+ text)
        soundlist.append(text)
        if len(soundlist) > 0:
            for sentence in soundlist:
                get_nouns(sentence, noun_list)
            if len(jsonDataList) > 0:
                # depict_word_cloud(noun_list)
                makeJson()
        soundlist = []
        jsonDataList = []

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        print("わかんなかった")
        margins = randomint()
        scene_num = "[c "+ str(num)+ "]"
        data ={"t": margins["t"],"r": margins["r"],"b":margins["b"],"l":margins["l"],"f":margins["f"] ,"texts":["髯堺ｸ�菴懈姶繝ｻ繝ｻ"],"scene_num":scene_num}
        ws.send(json.dumps(data,indent=2))
        result =  ws.recv()
        print(result)

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        margins = randomint()
        scene_num =  "[c "+ str(num)+ "]"
        data ={"t": margins["t"],"r": margins["r"],"b":margins["b"],"l":margins["l"],"f":margins["f"] ,"texts":["髯堺ｸ�菴懈姶繝ｻ繝ｻ"],"scene_num":scene_num}
        ws.send(json.dumps(data,indent=2))
        result =  ws.recv()
        print(result)

    num += 1
