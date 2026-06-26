# Language Quick Reference

Minimal API and module names. Use when writing code in a specific language.

## Python

| Need | API |
|------|-----|
| Thread | `threading.Thread(target=fn, args=(...))` → `.start()`, `.join()` |
| Lock | `threading.Lock()` → `.acquire()` / `.release()` or `with lock:` |
| Queue | `queue.Queue()` → `.put(item)`, `.get()` (blocking); thread-safe |
| Thread pool | `concurrent.futures.ThreadPoolExecutor(max_workers=n)` → `.submit(fn, *args)` or `.map(fn, iterable)` |
| Process pool | `concurrent.futures.ProcessPoolExecutor(max_workers=n)` |
| Async | `asyncio.run(main())`, `async def`, `await`; I/O with `aiohttp`, `asyncio.to_thread()` for blocking |

## Java

| Need | API |
|------|-----|
| Thread | `new Thread(() -> { ... }).start()` or `ExecutorService` |
| Lock | `ReentrantLock` → `lock()`, `unlock()` (prefer in try/finally); or `synchronized (obj) { }` |
| Queue | `BlockingQueue` (e.g. `LinkedBlockingQueue`) → `put()`, `take()` |
| Thread pool | `Executors.newFixedThreadPool(n)` → `executor.submit(Callable)` or `execute(Runnable)` |
| Async | `CompletableFuture`, or reactive (Project Reactor, RxJava) |

## C#

| Need | API |
|------|-----|
| Thread | `new Thread(() => { ... }).Start()`; prefer `Task` / `Task.Run` |
| Lock | `lock (obj) { }` or `Monitor.Enter/Exit`; `Mutex` for cross-process |
| Queue | `BlockingCollection<T>` or `Channel<T>` |
| Thread pool | `Task.Run(() => ...)`, `Parallel.ForEach`, or `Task.WhenAll(tasks)` |
| Async | `async` / `await`, `Task`, `ValueTask` |

## Node.js

| Need | API |
|------|-----|
| Thread | `worker_threads`: `new Worker(path)` or `worker_threads` with `postMessage` / `on('message')` |
| Concurrency | Single-threaded by default; use **async/await** and **Promise** for I/O |
| CPU in worker | `worker_threads` for CPU-heavy work; share via `SharedArrayBuffer` or message passing |
| Pool | Custom pool of Workers or `workerpool` (npm) |

## Go

| Need | API |
|------|-----|
| Goroutine | `go fn()` — lightweight; no direct “thread” API |
| Sync | `sync.Mutex` → `Lock()` / `Unlock()`; `sync.WaitGroup` for join |
| Queue / channel | `ch := make(chan T)` or `make(chan T, n)`; send `ch <- v`, receive `<-ch`; close when done |
| Pattern | Prefer **channels** for communication; mutex when protecting a simple shared struct |
