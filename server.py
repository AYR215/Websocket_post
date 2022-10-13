import os
import asyncio
import threading
from queue import Queue

from aiohttp import web

WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket.html')

# Создаем очередь, для ленты новостей
newsfeed = asyncio.Queue()


# функция таймера для ping клиента
def setInterval(func, time):
    e = threading.Event()
    while not e.wait(time):
        func()


# обработчик для POST - запросов с новостями
async def newshandler(request):
    result = await request.post()
    print('POST:', result)
    await newsfeed.put(result)
    return web.Response(text='OK')


# обработчик для GET - запросов
async def wshandler(request):
    resp = web.WebSocketResponse()
    available = resp.can_prepare(request)
    if not available:
        with open(WS_FILE, "rb") as fp:
            return web.Response(body=fp.read(), content_type="text/html")

    await resp.prepare(request)
    print("Cоздано новое подключение")
    request.app["sockets"].append(resp)

    while True:
        res = await newsfeed.get()
        for ws in request.app["sockets"]:
            await ws.send_str(res['text'])
            print('Текст отправлен')
            await ws.ping('Ping')
    return resp


async def on_shutdown(app: web.Application):
    for ws in app["sockets"]:
        await ws.close()


loop = asyncio.get_event_loop()
app = web.Application()
app["sockets"] = []
app.add_routes([web.get('/', wshandler),
                web.post('/news', newshandler)])
#app.on_shutdown.append(on_shutdown)

web.run_app(app, loop=loop)
if __name__ == '__main__':
    web.run_app(app)

# web.run_app(init())
