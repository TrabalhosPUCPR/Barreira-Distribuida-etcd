import time

import etcd3

tag_processos_total = "processos_total"
tag_processos_finalizados = "processos_finalizados"
tag_barreira = "barreira"

client = etcd3.client()

barreira: etcd3.Lock = client.lock(tag_barreira)
processos = client.get(tag_processos_total)
if processos is None:
    processos = 0
client.put(tag_processos_total, processos+1)

for i in range(0, 10, 1):
    print(i)
    time.sleep(1)

print("Chegou na barreira")
if client.get(tag_processos_total) == client.get(tag_processos_finalizados):
    barreira.release()
barreira.acquire()
barreira.release()

print("Saiu da barreira")

