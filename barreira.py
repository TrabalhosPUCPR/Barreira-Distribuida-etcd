import time
import etcd3
from sys import argv


def etcd3_get_int(client, key) -> int:
    res = client.get(key)[0]
    if (res == None):
        return 0
    else:
        return int(res.decode('utf-8'))


def etcd3_put(client, key, value):
    client.put(key, str(value))


def run():
    client = etcd3.client()
    lock: etcd3.Lock = client.lock("b", ttl=60)
    assert (len(argv) > 1)
    processos = int(argv[1])
    locks = []
    for i in range(0, processos):
        locks.append(client.lock(str(i), ttl=60))

    for i in range(0, 10, 1):
        print(i)
        time.sleep(1)
    print("Chegou na barreira...")

    for l in locks:
        l.acquire()
        l.release()

    print("Passou a barreira")
    lock.refresh()
    print("Fim")


if __name__ == "__main__":
    run()
