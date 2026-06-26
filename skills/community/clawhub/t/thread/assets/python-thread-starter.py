# Minimal Python threading + lock example.
# Use when the user wants a starter for thread-safe shared state.

import threading

shared_counter = 0
lock = threading.Lock()

def increment():
    global shared_counter
    for _ in range(100_000):
        with lock:
            shared_counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(shared_counter)  # 400_000 if no race
