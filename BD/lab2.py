import numpy as np
import time
import threading
import queue

def matrix_multiply(a, b):
    m, n1 = a.shape
    n2, l = b.shape
    if n1 != n2:
        raise ValueError("Invalid matrix dimensions")
    c = np.zeros((m, l))
    for i in range(m):
        for j in range(l):
            for k in range(n1):
                c[i][j] += a[i][k] * b[k][j]
    return c

def atomic_multiply(a, b, c, lock):
    m, n1 = a.shape
    n2, l = b.shape
    if n1 != n2:
        raise ValueError("Invalid matrix dimensions")
    for i in range(m):
        for j in range(l):
            for k in range(n1):
                with lock:
                    c[i][j] += a[i][k] * b[k][j]


def individual_multiply(a, b, c, i, j):
    m, n1 = a.shape
    n2, l = b.shape
    if n1 != n2:
        raise ValueError("Invalid matrix dimensions")
    for k in range(n1):
        c[i][j] += a[i][k] * b[k][j]


def worker(q, a, b, c):
    while True:
        i, j = q.get()
        if i == None and j == None:
            break
        individual_multiply(a, b, c, i, j)
        q.task_done()


def parallel_multiply(a, b, c, num_threads):
    m, n1 = a.shape
    n2, l = b.shape
    if n1 != n2:
        raise ValueError("Invalid matrix dimensions")
    threads = []
    q = queue.Queue()
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(q, a, b, c))
        t.start()
        threads.append(t)
    for i in range(m):
        for j in range(l):
            q.put((i, j))
    for i in range(num_threads):
        q.put((None, None))
    q.join()
    for t in threads:
        t.join()

a = np.random.rand(100, 100)
b = np.random.rand(100, 100)

start_time = time.time()
c = matrix_multiply(a, b)
end_time = time.time()
print("Single thread time:", end_time - start_time)

lock = threading.Lock()
a = np.random.rand(100, 100)
b = np.random.rand(100, 100)
c_atomic = np.zeros((100, 100))
c_individual = np.zeros((100, 100))

start_time = time.time()
atomic_multiply(a, b, c_atomic, lock)
end_time = time.time()
print("Atomic time:", end_time - start_time)

start_time = time.time()

# вызываем функцию parall_multiply и передаем ей матрицы a и b, а также количество потоков
parallel_multiply(a, b, c_individual, 4)

end_time = time.time()
print("Parallel time:", end_time - start_time)

# создаем список времени выполнения каждого потока
thread_times = []
for i in range(4):
    thread_times.append(c_individual[i][-1])

# выводим общее время выполнения и время каждого из потоков
print("Total time for all threads:", sum(thread_times))
for i in range(4):
    print("Thread", i+1, "time:", thread_times[i])

start_time = time.time()
parallel_multiply(a, b, c_individual, 4)
end_time = time.time()
print("Individual time:", end_time - start_time)



#assert np.allclose(c, c_atomic)
#assert np.allclose(c, c_individual)