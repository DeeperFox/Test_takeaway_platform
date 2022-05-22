from flask import *
import pymysql
import os
import time
app = Flask(__name__)
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
app.secret_key = 'abc123'
from werkzeug.utils import secure_filename
from coverage import Coverage


# 测试版app  将返回值修改为易于测试的格式


# 主页
@app.route('/')
def mainpage():
    return '前导页'


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '登录页面'
    if request.method == 'POST':
            accountname = request.form.get('accountname')
            password = request.form.get('password')
            db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
            cursor = db.cursor()
            cursor.execute("select password,type from member where accountname = '%s'" % accountname)
            result = cursor.fetchone()
            print(result)
            if not result:
                return '错误页面'
            elif result[0] == password:
                print("登陆成功")
                session['accountname'] = accountname
                session['type'] = result[1]
                session.permanent = True
                cursor.close()
                print(result[1])
                if result[1] == '0':
                    return '登录用户界面'
                elif result[1] == '1':
                    return '登录商家界面'
                elif result[1] == '2':
                    return '登录骑手界面'
            else:
                return '错误页面'



# 用户注销
@app.route('/logout')
def logout():
    session.clear()
    return '注销成功'


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '注册页面'
    if request.method == 'POST':
        accountname = request.form.get('accountname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        type = request.form.get('type')
        if password != password2:
            return "注册失败"
        else:
            db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
            cursor = db.cursor()
            cursor.execute("insert into member(accountname,password,type) values(%s,%s,%s)",
                           [accountname, password, type])
            db.commit()
            print('注册成功', type)
            return '注册成功'


# 修改密码
@app.route('/user/changePW', methods=['GET', 'POST'])
def change1():
    if request.method == 'GET':
        return '修改密码页面'
    if request.method == 'POST':
        newpassword = request.form.get('password')
        newpassword2 = request.form.get('password2')
        accountname = session.get('accountname')
        if newpassword != newpassword2:
            return '两次密码不一致'
        else:
            db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
            cursor = db.cursor()
            cursor.execute("update member set password = '%s' where accountname = '%s'" % (newpassword, accountname))
            db.commit()
            return '修改密码成功'

#修改头像
@app.route('/user/change_head', methods=['GET','POST'])
def changehead():
    if request.method=='GET':
        return '修改头像页面'
    if request.method=='POST':
            f = request.files['file']
            path = os.path.join('/static/img/', secure_filename(f.filename))
            accountname = session.get('accountname')
            db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
            cursor = db.cursor()
            cursor.execute("update member set img = '%s' where accountname = '%s'" % (path,accountname))
            db.commit()
            return '修改头像成功'


#修改地址
@app.route('/user/change_adress',methods=['GET','POST'])
def change_adress():
    if request.method=='GET':
        return '修改地址页面'
    if request.method=='POST':
        accountname=session.get('accountname')
        name=request.form.get('name')
        number=request.form.get('number')
        adress=request.form.get('adress')

        if name and number and adress:
            db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
            cursor = db.cursor()
            cursor.execute("insert into adress(accountname,adress,number,name) values(%s,%s,%s,%s)",
                               [accountname, adress, number,name])
            db.commit()
            return '修改地址成功'
        else:
            return '信息填写不完整'

#点赞
@app.route('/user/order/dianzan/<Ino>',methods=['GET','POST'])
def dianzan(Ino):
    if request.method=='POST':
        try:
            db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
            cursor = db.cursor()
            cursor.execute("select dianzan from shop where shop_name = '%s'" % Ino)
            db.commit()
            result = cursor.fetchone()
            result2=result[0]+1
            cursor.execute("update shop set dianzan = '%s' where shop_name = '%s' " % (result2,Ino))
            db.commit()
            return '点赞成功'
        except:
            return '点赞失败'

#收藏
@app.route('/user/order/shoucang',methods=['GET','POST'])
def shoucang():
    if request.method == 'POST':
        accountname=session.get('accountname')
        name=request.form.get('name')
        img=request.form.get('photo')
        shop=request.form.get('shop_accountname')
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("select shoucang from shop where shop_name = '%s'" % name)
        db.commit()
        result = cursor.fetchone()
        result2 = result[0] + 1
        cursor.execute("update shop set shoucang = '%s' where shop_name = '%s' " % (result2, name))
        db.commit()
        cursor.execute("insert into shoucang(accountname,shop_name,img,shop_accountname) values(%s,%s,%s,%s)",[accountname,name,img,shop])
        db.commit()
        return '收藏成功'

#我的收藏
@app.route('/user/my_shoucang',methods=['GET','POST'])
def my_shoucang():
    if request.method=='GET':
        accountname=session.get('accountname')
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("select shop_name,img,shop_accountname from shoucang where accountname = '%s'" % accountname)
        db.commit()
        form=cursor.fetchall()
        return '我的收藏页面'

#修改店铺信息
@app.route('/shop/changeshop', methods=['GET','POST'])
def changeshop():
    if request.method=='GET':
        return '修改店铺信息页面'
    if request.method=='POST':
        accountname=session.get('accountname')
        shopname = request.form.get('shopname')
        describtion = request.form.get('describtion')
        type = request.form.get('type')
        dianzan=0
        shoucang=0
        f = request.files['file']
        path = os.path.join('/static/img', secure_filename(f.filename))
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("insert into shop(shop_name,type,describtion,accountname,img,dianzan,shoucang) values(%s,%s,%s,%s,%s,%s,%s)",[shopname,type,describtion,accountname,path,dianzan,shoucang])
        db.commit()
        print('编辑成功', type)
        return '修改店铺信息成功'

#店铺详情
@app.route('/shop/detail/<id>', methods=['GET','POST'])
def shop_detail(id):
    if request.method=='GET':
        type = session.get('type')
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("select shop_name,type,describtion,accountname,img from shop where accountname = '%s'" % id)
        form = cursor.fetchone()
        cursor.execute("select name,price,describtion,img from issue where accountname = '%s'" % id)
        form1=cursor.fetchall()
        cursor.close()
        print(form1)
        return '店铺详情页'



#上传菜品
@app.route('/shop/detail/uplord', methods=['GET','POST'])
def uplord():
    if request.method == 'GET':
       return '上传菜品页面'
    if request.method=='POST':
        accountname=session.get('accountname')
        name=request.form.get('name')
        price = request.form.get('price')
        describtion = request.form.get('describtion')
        f = request.files['file']
        path=os.path.join('\static\img', secure_filename(f.filename))
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("insert into issue(name,price,describtion,img,accountname) values(%s,%s,%s,%s,%s)",[name,price,describtion,path,accountname])
        db.commit()
        return '上传菜品成功'


#个人中心
@app.route('/usercenter')
def usercenter():
    type=session.get('type')
    accountname = session.get('accountname')
    if type=='0':
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("select name,adress,number from adress where accountname = '%s'" % accountname)
        form = cursor.fetchone()
        cursor.execute("select img from member where accountname = '%s'" % accountname)
        img=cursor.fetchone()
        return '用户个人中心'
    elif type=='1':
        return '商家个人中心'
    elif type=='2':
        return '骑手个人中心'


#接单页面
@app.route('/rider/oder_receiving', methods=['GET'])
def oder_receiving():
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("select 下单时间,下单人,住址,订单店铺,订单内容,id from order_receiving where 订单状态='0'")
        form = cursor.fetchall()
        return '接单页面'



#我的订单
@app.route('/user/show_order')
def show_oder():
    accountname=session.get('accountname')
    db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
    cursor = db.cursor()
    cursor.execute("select 下单时间,下单人,住址,订单店铺,订单内容,订单状态,接单时间,送达时间,骑手 from order_receiving where 下单人='%s'" % accountname)
    form = cursor.fetchall()
    return '我的订单页面'


# 点餐
@app.route('/user/order', methods=['GET', 'POST'])
def order():
    if request.method=='GET':
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("select * from shop")
        form = cursor.fetchall()
        print(form)
        return '点餐页面'
    if request.method=='POST':
        db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
        cursor = db.cursor()
        cursor.execute("insert into oder receiving(下单时间,下单人,住址,订单店铺,订单内容) values(%s,%s,%s,%s,%s)",[])
        return '点餐成功'


#接单
@app.route('/rider/oder_receiving/<id>',methods=['GET','POST'])
def take_oder(id):
    accountname=session.get('accountname')
    print(accountname)
    time1=time.strftime('%Y/%m/%d %H:%M',time.localtime())
    db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
    cursor = db.cursor()
    cursor.execute("update order_receiving set 订单状态 ='%s',接单时间='%s',送达时间='%s',骑手='%s' where id='%s'"%(1,time1,time1,accountname,id))#送达时间不会搞
    db.commit()
    print('接单成功')
    return '接单成功'


#我接的单
@app.route('/rider/oder_receiving/my_taking')
def my_taking():
    accountname = session.get('accountname')
    db = pymysql.connect(host='localhost', user='root', password='js1110923', database='takeaway platform')
    cursor = db.cursor()
    cursor.execute("select 下单时间,下单人,住址,订单店铺,订单内容,订单状态,接单时间,送达时间,骑手 from order_receiving where 骑手='%s'" % accountname)
    form = cursor.fetchall()
    return '我的接单页面'


if __name__ == '__main__':
    cov = Coverage()
    cov.start()
    app.run()
    cov.stop()
    cov.save()
    cov.html_report()
