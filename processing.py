import time
import multiprocessing
from threads import run_single

def formula(start, end):
    total = 0
    for i in range(start, end + 1):
        total += 1 / (i ** 2)
    return total

def partial(start, end, q):
    result = formula(start, end)
    q.put(result)

def run_single_processor(j):
    return run_single(j)

def run_multiprocessing(j, num_processes=4):
    start_time = time.time()
    step = j // num_processes
    queue = multiprocessing.Queue()
    processes = []

    for i in range(num_processes):
        s = i * step + 1
        e = (i + 1) * step if i != num_processes - 1 else j
        p = multiprocessing.Process(target=partial, args=(s, e, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total = 0
    while not queue.empty():
        total += queue.get()

    elapsed = time.time() - start_time
    return total, elapsed