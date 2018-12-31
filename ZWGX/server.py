#coding:utf8

import aiml
import os
import pymysql
import sys
import json


reload(sys)
sys.setdefaultencoding('utf8')
from QA.QACrawler import baike
from QA.Tools import Html_Tools as QAT
from QA.Tools import TextProcess as T
from QA.QACrawler import search_summary
from socket import socket, AF_INET, SOCK_STREAM

def gbk_to_utf8(message):
    uni = message.decode('gbk') # gbk转unicoda
    utf = uni.encode("utf-8")
    return utf

def utf_to_bgk(message):
    uni = message.decode('utf-8')#将utf8格式的返回值转化为unicoda
    gk = uni.encode("gbk")
    return gk

def initQA(mybot):
    # 初始化jb分词器
    T.jieba_initialize()

    # 切换到语料库所在工作目录
    mybot_path = './'
    os.chdir(mybot_path)


    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/std-startup.xml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/bye.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/tools.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/bad.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/funny.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/OrdinaryQuestion.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/Common conversation.aiml")
    mybot.respond('Load Doc Snake')
    # 载入百科属性列表
    #print '''
    #Frank：你好，我是Frank o(*≧▽≦)ツ
    #'''

def FindSchool(dbip,dbusername,dbpassword,dbname,word):
    db = pymysql.connect(host=dbip, user=dbusername, passwd=dbpassword, db=dbname, charset="utf8")
    cursor = db.cursor()
    sql = u"SELECT `学校名称` FROM allschool WHERE `学校名称`='" + word + "'"
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    if len(results) > 0:
        return word
    else:
        return ""

def QA(input_message,mybot):
    findAns = False
    reply=''
    ansdict={}
    dbname='zwgx' #数据库名
    dbip='localhost'#数据库IPlocalhost
    dbport=3306#数据库端口
    dbusername='yst'#数据库用户名
    dbpassword='yst1998'#数据库密码root
    schoolname = ''
    intention = ''
    if len(input_message) > 60:
        reply = mybot.respond("句子长度过长")
        findAns = True
    elif input_message.strip() == '无':
        reply = mybot.respond("无")
        findAns = True

    if (findAns == False):
        #print input_message
        #传入一个b''未加工的对象
        message = T.wordSegment(input_message)
        # 分词去标点
        if message == 'q':
            exit()
        else:
            print 'word Seg:' + message
            print utf_to_bgk('词性：')
            words = T.postag(input_message) #词性标注 格式 词/词性
            for w in words:
                print w.word, w.flag
                if w.flag=='school':
                    try:
                        #先用自定义的分词处理得到对应的词性，然后根据词性到数据库查询
                        db = pymysql.connect(host=dbip, user=dbusername, passwd=dbpassword, db=dbname, charset="utf8")
                        cursor = db.cursor()
                        sql = u"SELECT `学校名` FROM 学校简称 WHERE `简称`='" + w.word + "'"
                        # 执行SQL语句
                        cursor.execute(sql)
                        # 获取所有记录列表,已验证数据库查询跑通
                        results = cursor.fetchall()
                        #print results 
                        #替换简称
                        if len(results) > 0:
                            input_message=input_message.replace(w.word,results[0][0]).__str__()
                            w.flag = 'nt'
                            w.word = results[0][0]
                        print utf_to_bgk(input_message), utf_to_bgk(w.word), utf_to_bgk(w.flag)      
                        # 关闭数据库连接
                        db.close()
                    except Exception as e:
                        print(e)
                # 识别学校简称并配对数据库中已存内容
                if w.flag == 'x' or w.flag == 'nt':
                    try:
                        db = pymysql.connect(host=dbip, user=dbusername, passwd=dbpassword, db=dbname,charset="utf8")
                        cursor = db.cursor()
                        sql=u"SELECT `属性`,`内容` FROM school WHERE `学校`='"+w.word+"'"
                        # 执行SQL语句
                        cursor.execute(sql)

                        # 获取所有记录列表
                        results = cursor.fetchall()
                        #print u'flag转化之后的查询',results
                        if len(results)>0:
                            for row in results:
                                ansdict[row[0]]=row[1]
                                #print row[0],row[1]
                                # reply +=row[0].encode("utf8")
                                # reply+=" ".encode("utf8")
                            # shuxing=raw_input('Frank：你想了解什么属性 ' + reply+">>")
                            # sql = u"SELECT `内容` FROM school WHERE `学校`='" + w.word + u"'AND `属性`='"+shuxing+"'"
                            # cursor.execute(sql)
                            # results = cursor.fetchall()
                            # if len(results)>0:
                            #     print "Frank： "+results[0][0].encode("utf8")
                            #     reply=results[0][0].encode("utf8")
                            #     return reply
                        # 关闭数据库连接
                            #print u'查询之后的结果储存',ansdict 将数据库中的所有信息写入到ansdict中
                        db.close()
                    except Exception as e:
                        print(e)
                #todo： 每个词去找查数据库可以优化一下 加一下词性判断
                #获得学校的名称
                if FindSchool(dbip, dbusername, dbpassword, dbname, w.word) != "":
                    schoolname = FindSchool(dbip, dbusername, dbpassword, dbname, w.word)

            uni = input_message.strip().decode('utf-8') 
            print u'查看返回值',uni,utf_to_bgk(input_message.strip())
            response = mybot.respond(input_message.strip())#如果未给传入参数转化为utf8则报错

            print "======="
            #print response
            print "=======+"

            if response == "":
                reply = mybot.respond('找不到答案')
                findAns = True
                print 'Frank1：' + utf_to_bgk(reply)
# *********************************************************************************
            # 百科搜索  aiml机器人没有没有
            elif response[0] == '#':  
                # 匹配百科
                # if response.__contains__("searchbaike"):
                #     print "searchbaike"
                #     print response
                #     res = response.split(':')
                #     # 实体
                #     entity = str(res[1]).replace(" ", "")
                #     # 属性
                #     attr = str(res[2]).replace(" ", "")
                #     print entity + '<---->' + attr
                #
                #     ans = baike.query(entity, attr)
                #     # 如果命中答案
                #     if type(ans) == list:
                #         print 'Frank：' + QAT.ptranswer(ans, False)
                #         reply = QAT.ptranswer(ans, False)
                #         findAns = True
                #     elif ans.decode('utf-8').__contains__(u'::找不到'):
                #         # 百度摘要+Bing摘要
                #         print "通用搜索"
                #         ans = search_summary.kwquery(input_message)
                #
                # # 匹配不到模版，通用查询
                # elif response.__contains__("NoMatchingTemplate"):
                #     print "NoMatchingTemplate"
                #
                #当复杂问题时，通过分类器模型进行分类再查询
                if (schoolname != ""):
                    sock = socket(AF_INET, SOCK_STREAM)
                    sock.connect(('127.0.0.1', 50009))
                    sock.sendall(input_message.encode("utf-8"))
                    intention = sock.recv(1024)
                    sock.close()
                    print utf_to_bgk(intention),u'经过分类器处理后的结果'

                #经过dl识别后分类问题，如果问题在数据库中，即把问题分类为数据库的一个属性，再调用属性值，可以增加数据库的属性分类和值
                if unicode(intention) in ansdict:
                    reply = ansdict[unicode(intention)]
                    #print 'Frank：' + reply.encode("utf8")
                    #print 'Frank2：' + utf_to_bgk(reply)

                #如果问题没有在数据库预存储
                else:
                    TempDict = search_summary.kwquery(input_message,intention,schoolname)
                    ansdict['schoolname']=TempDict['schoolname']
                    ansdict['intention']=TempDict['intention']
                    ansdict['index']=TempDict['index']
                    ans=TempDict['answer']
                    if (findAns == False):
                        if len(ans) == 0:
                            ans = mybot.respond('找不到答案')
                            #print 'Frank3：' + utf_to_bgk(ans)
                            reply = ans
                            findAns = True
                        elif len(ans) > 1:
                            print u"不确定候选答案"
                            print 'Frank4: '
                            for a in ans:
                                print a.encode("utf8")
                                reply += a.encode("utf8") + '\n'
                            findAns = True
                        else:
                            #print 'Frank5：' + ans[0].encode("utf8")
                            reply = ans[0].encode("utf8")
                            findAns = True

            # 匹配模版
            else:
                print 'Frank6：' + utf_to_bgk(response)
                reply = response
                findAns = True

    ansdict['baidu']=reply
    json_s=json.dumps(ansdict)
    return json_s

if __name__ == '__main__':
    mybot = aiml.Kernel()
    initQA(mybot)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('127.0.0.1',50008))
    sock.listen(5)

    while True:

        # if(reply!=''):
        #     conn.send(reply)
        #     reply=''
        try:
            conn,addr = sock.accept()
            data = conn.recv(4096)
            input_message = data

            print "input_message====="
            print utf_to_bgk(input_message)
            print "=========="

            reply=QA(input_message,mybot)
            # print reply
            conn.send(reply)
        except Exception as ex:
            print ex



