#coding:utf8

import pymysql

dbname = 'zwgx'  # 数据库名
dbip = '127.0.0.1'  # 数据库IPlocalhost
dbport = 3306  # 数据库端口
dbusername = 'root'  # 数据库用户名
dbpassword = '981004tyy'  # 数据库密码root

#与数据库连接，进行增删改查操作
def EXSQL(sql):
    try:
        # 打开数据库连接
        db = pymysql.connect(host=dbip, user=dbusername, passwd=dbpassword, db=dbname, charset="utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        if(not sql.__contains__("SELECT")):
            # 提交，不然无法保存新建或者修改的数据
            db.commit()
        # 获取所有记录列表
        results = cursor.fetchall()
        db.close()
        return results
    except Exception as e:
        print (e)


def InitSchool(schoolname,intention,s):
    for i in range(3):
        sql = u"INSERT INTO `问答预存` VALUES('"+schoolname+"','"+intention+"','"+i.__str__()+"','"+s+"','4','1','4')"
        EXSQL(sql)

def PingFen(schoolname,intention,xuhao,fenshu,answer):
    if xuhao=='4' and fenshu>='4':
        Insert4(schoolname,intention,answer)
    else:
        sql = u"UPDATE `问答预存` set `评价次数`=`评价次数`+1,`总分`=`总分`+"+fenshu+" WHERE `学校名`='"+schoolname+"' and `意图`='"+intention+"' and `序号`="+xuhao
        EXSQL(sql)

def Insert4(schoolname,intention,s):
    sql = u"SELECT `均分`,`序号` FROM 问答预存 WHERE `学校名`='" + schoolname + "' AND `意图`='" + intention + "'ORDER BY `均分` DESC"
    result=EXSQL(sql)
    xuhao=result[2][1]
    sql=u"DELETE FROM `问答预存` WHERE `学校名`='" + schoolname + "' AND `意图`='" + intention + "' and `序号`="+xuhao.__str__()
    EXSQL(sql)
    sql = u"INSERT INTO `问答预存` VALUES('" + schoolname + "','" + intention + "','" + xuhao.__str__() + "','" + s + "','"+(result[1][0]+0.01).__str__()+"','1','"+(result[1][0]+0.01).__str__()+"')"
    EXSQL(sql)

def FanKui(Q,A):
    sql = u"INSERT INTO `用户反馈`(问题,反馈) VALUES('" + Q + "','" + A + "')"
    EXSQL(sql)