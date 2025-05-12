import threading
import time
# import multiprocessing

def formula(start, end):
    total = 0
    for i in range(start, end + 1):
        total += 1 / (i ** 2)
    return total

def run_multithread(j, num_threads=4):
    start_time = time.time()
    step = j // num_threads
    threads = []
    results = [0] * num_threads

    def partial(start, end, index):
        results[index] = formula(start, end)

    for i in range(num_threads):
        s = i * step + 1
        e = (i + 1) * step if i != num_threads - 1 else j
        t = threading.Thread(target=partial, args=(s, e, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total = sum(results)
    elapsed = time.time() - start_time
    return total, elapsed

def run_single(j):
    start_time = time.time()
    result = formula(1, j)
    elapsed = time.time() - start_time
    return result, elapsed