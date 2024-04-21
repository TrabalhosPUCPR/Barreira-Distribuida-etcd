import time
import etcd3
from sys import argv

tag_processos_total = "processos_total"
tag_barreira = "barreira"

def etcd3_get_int(client,key) -> int:
    res = client.get(key)[0]
    if(res == None): 
        return 0
    else: 
        return int(res.decode('utf-8'))        

def etcd3_put(client, key, value):
    client.put(key, f"{value}")

def run():
    client = etcd3.client()
    lock: etcd3.Lock = client.lock(tag_barreira, ttl=60)
    lock.acquire(None)
    if len(argv) > 1:
        processos = argv[1]
    else:
        processos = etcd3_get_int(client, tag_processos_total)

    if(etcd3_get_int(client, tag_processos_total) == 0):
        etcd3_put(client,tag_processos_total,processos) #+1)
    lock.release()

    for i in range(0, 10, 1):
        print(i)
        time.sleep(1)
    print("Chegou na barreira...")
    lock.acquire(None)
    processos = etcd3_get_int(client, tag_processos_total)   
    if processos > 0:
        etcd3_put(client, tag_processos_total, processos-1)
        processos = processos-1
    lock.release()
    while processos > 0:
        processos = etcd3_get_int(client, tag_processos_total)
    print("Passou a barreira")
    lock.refresh()
    print("Fim")

if __name__ == "__main__":
    run()

