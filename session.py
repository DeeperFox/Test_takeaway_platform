import requests


def session1():
    s = requests.Session()
    data = {'accountname': 'yonghu', 'password': '123'}
    rps = s.post('http://127.0.0.1:5000/login', data=data)
    return s

def session2():
    s = requests.Session()
    data = {'accountname': 'shangjia', 'password': '123'}
    rps = s.post('http://127.0.0.1:5000/login', data=data)
    return s


def session3():
    s = requests.Session()
    data = {'accountname': 'qishou', 'password': '123'}
    rps = s.post('http://127.0.0.1:5000/login', data=data)
    return s

def session4():
    s = requests.Session()
    data = {'accountname': '111', 'password': '111'}
    rps = s.post('http://127.0.0.1:5000/login', data=data)

    return s

def session5():
    s = requests.Session()
    data = {'email': 'test2@qq.com', 'password': '123456'}
    rps = s.post('http://127.0.0.1:5000/login', data=data)
    return s