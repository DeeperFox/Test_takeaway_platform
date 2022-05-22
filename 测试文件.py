import pytest
import requests
from session import session1,session2,session3,session4


class Test_login:

    def login(self,accountname,password):
        data = {'accountname':accountname,'password': password}
        ans = requests.post('http://127.0.0.1:5000/login',data=data)
        return ans.text

    def test_01(self):
        assert self.login('yonghu','123') == '登录用户界面'

    def test_02(self):
        assert self.login('shangjia','123') == '登录商家界面'

    def test_03(self):
        assert self.login('qishou','123') == '登录骑手界面'

    def test_04(self):
        assert self.login('buchunzai','123') == '错误页面'

    def test_05(self):
        assert self.login('yonghu','') == '错误页面'



class Test_rigister:
    def register(self,accountname,password,password2,type):
        data = {'accountname':accountname,'password':password,'password2':password2,'type':type}
        ans=requests.post('http://127.0.0.1:5000/register',data=data)
        return ans.text


    def test_01(self):
        assert self.register('111@qq.com','123','123','0') == '注册成功'


    def test_02(self):
        assert self.register('111@qq.com','123','111','0') == '注册失败'


    def test_03(self):
        assert self.register('111@qq.com','123','','0') == '注册失败'



class Test_changepw:


    def changepw_post(self,session,password,password2):
        data={'password':password,'password2':password2}
        ans=session().post('http://127.0.0.1:5000/user/changePW',data=data)
        return ans.text


    def test_01(self):
        assert self.changepw_post(session4,'123','123') == '修改密码成功'


    def test_02(self):
        assert self.changepw_post(session4,'111','456') == '两次密码不一致'


    def test_03(self):
        assert self.changepw_post(session4, '333', '') == '两次密码不一致'


class Test_changeadress:


    def changeadress_post(self,session,name,adress,number):
        data={'name':name,'adress':adress,'number':number}
        ans=session().post('http://127.0.0.1:5000/user/change_adress',data=data)
        return ans.text


    def test_01(self):
        assert self.changeadress_post(session1,'张三','山东菏泽曹县','123456') == '修改地址成功'


    def test_02(self):
        assert self.changeadress_post(session1,'张三','山东菏泽曹县','') == '信息填写不完整'



class Test_dianzan:


    def dianzan_post(self,session,shop_name):
        ans =session().post('http://127.0.0.1:5000/user/order/dianzan/'+ shop_name)
        return ans.text


    def test_01(self):
        assert self.dianzan_post(session1,'一家店') =='点赞成功'



class Test_changeimg:


    def img_post(self, session, file):
        with open(file,'rb') as f:
            file={'file':f}
            ans = session().post('http://127.0.0.1:5000/user/change_head',files=file)
            return ans.text


    def test_01(self):
        assert self.img_post(session1,'img.jpg') == '修改头像成功'



class Test_shoucang:


    def shoucang_post(self,session,name,photo,shop_accountname):
        data = {'name':name,'photo':photo,'shop_accountname':shop_accountname}
        ans = session().post('http://127.0.0.1:5000/user/order/shoucang', data=data)
        return ans.text


    def test_01(self):
        assert self.shoucang_post(session1,'一家店','/static/img/QQ20220120145157.jpg','shangjia') == '收藏成功'



class Test_changeshop:


    def changeshop_post(self,session,shopname,describtion,type,file):
        data ={'shopname':shopname,'describtion':describtion,'type':type}
        with open(file,'rb') as f:
            file={'file':f}
            ans = session().post('http://127.0.0.1:5000/shop/changeshop', data=data,files=file)
            return ans.text


    def test_01(self):
        assert self.changeshop_post(session2,'一家店','tnnd为什么不吃','0','img.jpg') == '修改店铺信息成功'



class Test_uplord:


    def uplord(self,session,name,price,describtion,file):
        data={'name':name,'price':price,'describtion':describtion}
        with open(file,'rb') as f:
            file={'file':f}
            ans = session().post('http://127.0.0.1:5000//shop/detail/uplord', data=data,files=file)
            return ans.text


    def test_01(self):
        assert self.uplord(session2,'name','price','descirbtion','img.jpg') == '上传菜品成功'



class Test_takeorder:


    def takeoder(self,session,id):
        ans = session().post('http://127.0.0.1:5000/rider/oder_receiving/' + id)
        return ans.text


    def test_01(self):
        assert self.takeoder(session3,'12345651') == '接单成功'


class Test_get:


    def index_get(self):
        ans = requests.get('http://127.0.0.1:5000/')
        return ans.text


    def test_01(self):
        assert self.index_get() == '前导页'


    def login_get(self):
        ans = requests.get('http://127.0.0.1:5000/login')
        return ans.text


    def test_02(self):
        assert self.login_get() == '登录页面'


    def register_get(self):
        ans = requests.get('http://127.0.0.1:5000/register')
        return ans.text


    def test_03(self):
        assert self.register_get() == '注册页面'


    def changepw_get(self):
        ans = requests.get('http://127.0.0.1:5000/user/changePW')
        return ans.text


    def test_04(self):
        assert self.changepw_get() == '修改密码页面'


    def changeimg_get(self):
        ans = requests.get('http://127.0.0.1:5000/user/change_head')
        return ans.text


    def test_05(self):
        assert self.changeimg_get() == '修改头像页面'


    def changeadress_get(self):
        ans = requests.get('http://127.0.0.1:5000/user/change_adress')
        return ans.text


    def test_06(self):
        assert self.changeadress_get() == '修改地址页面'


    def myshoucang_get(self):
        ans = requests.get('http://127.0.0.1:5000/user/my_shoucang')
        return ans.text


    def test_07(self):
        assert self.myshoucang_get() == '我的收藏页面'


    def changeshop_get(self):
        ans = requests.get('http://127.0.0.1:5000/shop/changeshop')
        return ans.text


    def test_08(self):
        assert self.changeshop_get() == '修改店铺信息页面'


    def shopdetail_get(self):
        ans = requests.get('http://127.0.0.1:5000/shop/detail/一家店')
        return ans.text


    def test_09(self):
        assert self.shopdetail_get() == '店铺详情页'


    def uplord_get(self):
        ans = requests.get('http://127.0.0.1:5000/shop/detail/uplord')
        return ans.text


    def test_10(self):
        assert self.uplord_get() == '上传菜品页面'


    # def usercenter_get(self):
    #     ans = requests.get('http://127.0.0.1:5000/usercenter')
    #     return ans.text
    #
    #
    # def test_11(self):
    #     assert self.usercenter_get() == '个人中心页面'


    def takeorder_get(self):
        ans = requests.get('http://127.0.0.1:5000/rider/oder_receiving')
        return ans.text


    def test_12(self):
        assert self.takeorder_get() == '接单页面'


    def myorder_get(self):
        ans = requests.get('http://127.0.0.1:5000/user/show_order')
        return ans.text


    def test_13(self):
        assert self.myorder_get() == '我的订单页面'


    def order_get(self):
        ans = requests.get('http://127.0.0.1:5000/user/order')
        return ans.text


    def test_14(self):
        assert self.order_get() == '点餐页面'


    def mytaking_get(self):
        ans = requests.get('http://127.0.0.1:5000/rider/oder_receiving/my_taking')
        return ans.text


    def test_15(self):
        assert self.mytaking_get() == '我的接单页面'



if __name__ == '__main__':
    pytest.main(['-vs','测试文件.py'])



