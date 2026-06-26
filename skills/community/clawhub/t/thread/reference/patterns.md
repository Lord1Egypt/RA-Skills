# Concurrency Patterns

Use when the user asks about locks, race conditions, thread-safe code, deadlock, or producer–consumer.

## Shared mutable state

- **Problem**: Two or more threads read/write the same variable → race condition, undefined behavior.
- **Solutions**:
  1. **Lock (mutex)**: Only one thread holds the lock; others block until release. Use around the minimal critical section.
  2. **Thread-safe data structures**: Queue, concurrent map, atomic counters (language-dependent).
  3. **Avoid sharing**: Pass copies or use per-thread storage; or send work via queue so only one thread touches data.

## Lock (mutex) discipline

- Always release the lock (use try/finally or context manager like `with lock:`).
- **Deadlock**: Thread A holds lock1 and waits for lock2; Thread B holds lock2 and waits for lock1. Both block forever.
- **Avoid deadlock**: Use a **consistent lock order** (e.g. always take lock1 then lock2), or use a single lock; or use timeouts and back off.

## Producer–consumer

- **Pattern**: One or more producers put items into a **thread-safe queue**; one or more consumers take items. Queue handles blocking when full/empty (bounded) or when no items.
- Prefer the standard queue type (e.g. `queue.Queue` in Python, `BlockingQueue` in Java) instead of hand-rolled signaling.

## Thread pool

- **Pattern**: Fixed number of worker threads; submit tasks (e.g. callables or futures); pool assigns work. Avoids creating/destroying many threads.
- Use when: many small tasks, I/O or mixed; limit concurrency (e.g. max 10 concurrent requests).
- APIs: Python `concurrent.futures.ThreadPoolExecutor`, Java `ExecutorService`, C# `Task.Run` + limited concurrency, etc.

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Lock held too long | Shrink critical section; do heavy or I/O work outside the lock. |
| Forgetting to release lock on exception | Use try/finally or context manager. |
| Nested locks | Use consistent order or one lock; consider lock-free structures where applicable. |
| Too many threads | Use a pool; for I/O consider async. |

## Minimal lock example (pseudo)

```text
lock = Lock()
# In each thread that touches shared state:
with lock:
    # read/modify shared state only here
    pass
```

Refer to [languages.md](languages.md) for real API in each language.
