from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse
# Create your views here.

from django.template import loader, Context
from socket import socket, AF_INET, SOCK_STREAM

import sys,importlib
import json
from django.views.decorators.csrf import csrf_protect
import app1.pingjia as pj

importlib.reload(sys)

def client(content):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('127.0.0.1',50008))

    sock.send(bytes(content,encoding='utf8'))

    # sock.send(content)
    reply = sock.recv(40960)
    sock.close()
    print('client got:[%s]' % reply)
    return reply


def index(request):
    return render(request,'index.html')


@csrf_protect
def submit(req):
    question = ''
    if req.POST:
        if 'Question' in req.POST:
            question = req.POST['Question']
            print(question)
            print ("===")
            if question.strip()=='':
                print (question)
                question = '无'
            print ("===")
    answer = client(question.strip())
    print (answer)
    return HttpResponse(answer, content_type = 'application/json')


def pingfen(req):
    if req.POST:
        if 'grade' in req.POST:
            grade = req.POST['grade']
        if 'schoolname' in req.POST:
            schoolname = req.POST['schoolname']
        if 'intention' in req.POST:
            intention = req.POST['intention']
        if 'index' in req.POST:
            index = req.POST['index']
        if 'answer' in req.POST:
            answer = req.POST['answer']
        pj.PingFen(schoolname,intention,index,grade,answer)
    return HttpResponse("OK", content_type = 'application/text')

def fankui(req):
    if req.POST:
        if 'qfeedback' in req.POST:
            qfeedback = req.POST['qfeedback']
        if 'afeedback' in req.POST:
            afeedback = req.POST['afeedback']
        pj.FanKui(qfeedback,afeedback)
    return HttpResponse("OK", content_type = 'application/text')

def searchresult(req):
    question = ""
    if req.POST:
        if 'question' in req.POST:
            question = req.POST['question']
            print(question)
            print ("===")
            if question.strip()=='':
                print (question)
                question = '无'
            print ("===")
    answer = client(question.strip())
    answer = json.loads(answer)
    print(answer)
    return render(req,'searchresult.html',{'answer':json.dumps(answer)})
