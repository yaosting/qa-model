#coding:utf8
import aiml
import os
import pymysql
import sys
import json
import chardet
    
reload(sys)
sys.setdefaultencoding('utf8')
from QA.QACrawler import baike
from QA.Tools import Html_Tools as QAT
from QA.Tools import TextProcess as T
from QA.QACrawler import search_summary
from socket import socket, AF_INET, SOCK_STREAM

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

mybot = aiml.Kernel()
initQA(mybot)
input_message = raw_input("Enter your message >> ") #输入晚安 对程序而言，以utf8从内存中读取一个gbk编码的数据
#通过输入的是cmd下的输入，为gbk编码 所以输出也是显示正常，但是mybot.respond('晚安')有返回值，说明传入的参数应该是utf8编码，gbk编码找不到
#对input_mesage和‘晚安’分别进行ord输出，可以看出一个是长度是4，一个是6，uft8中文占3个字节，gbk是2个字节 ，因此证明上述推断
#python2用来支持多语言，不同编码类型的str转换需要通过它 
#unicode表示字符串属于逻辑层面，字节串(str)表示存放格式属于物理层面，如ascii,utf-8,gbk属于字节串
# print ord('鏅氬畨')  <------鏅氬畨是晚安在gbk下的输出
#TypeError: ord() expected a character, but string of length 6 found
#

#print(sys.getdefaultencoding())#已经重载过 为utf8
print u'gbk下的输入',input_message

print u'utf-8下的返回值', mybot.respond('晚安')  #ok
s =  mybot.respond('晚安')
s1 = s.decode('utf-8')#将utf8格式的返回值转化为unicoda
print u'转化为unicoda后',s1,type(s1)
s2 = s1.encode("gbk") # unicode 转成 gbk，encode(编码)需要注明生成的编码格式
print u'unicoda转化为gbk输出',s2,type(s2)

print '---------------'

s3 = input_message.decode('gbk') # gbk转unicoda
s4 = s3.encode("utf-8")
print mybot.respond(s4) #此返回值应该===mybot.respond('晚安'),返回仍是utf8，导致乱码

print '++++++++++++++'

print mybot.respond(input_message) #no
#print mybot.respond('上海大学的主要领导')