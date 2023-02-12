import time
import threading


def worker1():
    print("Worker 1 started")
    for i in range(5):
        time.sleep(1)
        print("Worker 1 counting:", i + 1)
    print("Worker 1 finished")


def worker2():
    print("Worker 2 started")
    for i in range(5):
        time.sleep(1)
        print("Worker 2 counting:", i + 1)
    print("Worker 2 finished")


if __name__ == '__main__':
    t1 = threading.Thread(target=worker1)
    t2 = threading.Thread(target=worker2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("All workers finished")
