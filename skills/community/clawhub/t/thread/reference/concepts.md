# Thread vs Process vs Async

Use this when the user asks "should I use threads or async?" or "threads vs processes."

## I/O-bound vs CPU-bound

| Type | Description | Examples |
|------|-------------|----------|
| **I/O-bound** | Waiting on network, disk, DB, API | HTTP requests, file read/write, DB queries |
| **CPU-bound** | Heavy computation in CPU | Image processing, crypto, parsing large data |

- **I/O-bound**: Prefer **async** (asyncio, async/await, Promise) or a **small thread pool** so many tasks can wait without one thread per task.
- **CPU-bound**: Prefer **processes** (or process pool) to use multiple cores; in Python avoid many threads due to GIL.

## Threads

- **Pros**: Shared memory, low overhead, good for I/O-bound and for wrapping blocking APIs.
- **Cons**: Shared state → need synchronization (locks, queues); in Python, GIL limits CPU parallelism.
- **Use when**: Many I/O waits, or language has true parallelism (Java, Go, C#, C++).

## Processes

- **Pros**: True parallelism, no GIL; separate memory space avoids many race conditions.
- **Cons**: Heavier startup; sharing data needs IPC (queue, pipe, shared memory).
- **Use when**: CPU-bound work (Python: `multiprocessing`); isolation between tasks.

## Async (coroutines / event loop)

- **Pros**: Single-threaded concurrency for I/O; no lock needed for cooperative tasks; scales to many connections.
- **Cons**: One thread → no CPU parallelism; blocking calls must be offloaded or made async.
- **Use when**: Many I/O-bound operations (Node.js, Python asyncio, async HTTP/server).

## Python GIL

- **GIL** (Global Interpreter Lock): Only one thread executes Python bytecode at a time.
- **Implication**: Multiple threads do not run Python code in parallel; they help when threads are waiting on I/O.
- **CPU-bound in Python**: Use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`, or C extensions that release the GIL.

## Quick decision

1. Many I/O waits, one language runtime (e.g. Node, Python) → **async** first.
2. CPU-heavy, need multi-core → **processes** (or process pool).
3. I/O + need to call blocking APIs from async → **thread pool** (e.g. `run_in_executor`) or dedicated thread.
4. Already in a threaded environment (e.g. Java server) → **threads + locks/queues** with clear discipline.
