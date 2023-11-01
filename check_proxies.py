import threading
import queue
import requests

q = queue.Queue()


valid_proxies = []

with open("unchecked_proxy_list.txt", "r") as f:

    proxies = f.read().split("\n")

    for p in proxies:

        q.put(p)



def check_proxies():
    global q

    while not q.empty():
        proxy = q.get()

        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies={
                                   "http" : proxy,
                                   "https" : proxy
                               },timeout=2)
            
        except:
            continue

        if res.status_code == 200:
            with open("checked_proxy_list.txt", "a") as f:

                f.write(proxy+"\n")


for _ in range(100):
    threading.Thread(target=check_proxies).start()

