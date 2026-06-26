# Thread pool example (Python).
# Use when the user wants to run many I/O-bound or mixed tasks with limited concurrency.

from concurrent.futures import ThreadPoolExecutor, as_completed

def task(n):
    # Simulate work (I/O or mixed)
    return n * n

def main():
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task, i) for i in range(10)]
        for f in as_completed(futures):
            print(f.result())

# Or map-style:
# with ThreadPoolExecutor(max_workers=4) as executor:
#     results = list(executor.map(task, range(10)))

if __name__ == "__main__":
    main()
