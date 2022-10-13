# Это код отправляет новый POST-запрос на сервер  каждые 5 секунд
import requests
import random
import threading

def setInterval(func, time):
    e = threading.Event()
    while not e.wait(time):
        func()


def sendrequest():
    index = random.randint(0, len(newslist) - 1)
    requests.post('http://localhost:8080/news', data={'text': newslist[index]})
    return False


newslist = ['news@111', 'news@222', 'news@333',
            'news@444', 'news@555', 'news@666',
            'news@777']

# setinterval(3.0, sendrequest)

setInterval(sendrequest, 5)
