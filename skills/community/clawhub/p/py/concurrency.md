# Concurrency Traps

## Choosing a model

| Workload | Use |
|----------|-----|
| Pure-Python CPU-bound | `multiprocessing` / `ProcessPoolExecutor` (the only escape from the GIL) |
| CPU-bound inside numpy/C extensions | Threads are fine — C code releases the GIL |
| I/O-bound, blocking libraries (requests, DB drivers) | `ThreadPoolExecutor` |
| I/O-bound, very high concurrency, async-native libraries end to end | asyncio |
| An async app that must call one blocking library | asyncio + `await asyncio.to_thread(fn)` for that call only |
| Unsure | `ThreadPoolExecutor` — simplest model that is correct for I/O; one blocking call can't freeze siblings |

Whether asyncio beats threads at all is a real disagreement with a boundary condition: SKILL.md, Where Experts Disagree.

## GIL and threads
- The GIL lets one thread execute bytecode at a time, switching every ~5 ms by default (`sys.getswitchinterval()` → 0.005). Threads give zero speedup on pure-Python CPU work — they add switching overhead instead.
- The free-threaded (no-GIL) build is a separate binary: experimental in `python >=3.13`, supported in `python >=3.14`, and unsupported by many C extensions. Do not design production code around it (`versions.md`).
- The GIL does NOT make compound operations atomic: `x += 1` is read-modify-write and loses updates under contention. Guard shared mutable state with `threading.Lock`, or avoid sharing — hand off via `queue.Queue`.
- `ThreadPoolExecutor` default is `min(32, os.cpu_count() + 4)` workers — sized for I/O. An executor future's exception surfaces only when you call `.result()`; fire-and-forget means errors vanish. Iterate `as_completed` or check results.
- `executor.map` yields results in input order and re-raises the first exception when you reach it, so later successful results are never read. Use `submit` + `as_completed` when partial success matters.
- Daemon threads die at interpreter exit with NO cleanup — `finally` blocks and context managers do not run. Never let a daemon thread hold files, locks, or half-written state.
- Deadlock prevention is an ordering discipline, not a library feature: acquire multiple locks in one global order, always via `with lock:`, and pass `timeout=` on anything long-lived so a deadlock becomes a logged error instead of a hang (`debugging.md`).
- `threading.local()` does not follow `await`. Under asyncio use `contextvars` (`logging.md`).
- Signal handlers run only in the main thread, so `KeyboardInterrupt` never interrupts a worker (`cli.md`).

## Queues and shutdown
- Producer/consumer: one `queue.Queue`, N consumers, and one sentinel per consumer to stop them (`for _ in workers: q.put(None)`). A shared "done" flag races; sentinels do not.
- `q.join()` blocks until every item has had `task_done()` called. A consumer that dies first hangs the producer forever — call `task_done()` in a `finally`.
- Cancellation is limited: `executor.shutdown(cancel_futures=True)` (`python >=3.9`) drops QUEUED work but cannot stop a running task. Long tasks must poll a `threading.Event` themselves.
- Bound the queue (`Queue(maxsize=…)`) whenever producers outrun consumers — an unbounded queue turns a throughput problem into an out-of-memory crash (`performance.md`).

## Multiprocessing
- Start method: Windows and macOS (`python >=3.8`) use spawn; Linux switches its default from fork to forkserver in `python >=3.14` (fork + threads deadlocks). Spawn and forkserver RE-IMPORT your module in each child: unguarded top-level code re-executes — the classic infinite-spawn crash. Always `if __name__ == "__main__":` (SKILL.md rule 9).
- Everything crossing the process boundary must pickle: lambdas, local functions, open handles, and live connections fail — sometimes only on spawn platforms, so "works on my Linux box" is not evidence. A module-level `functools.partial` is the picklable substitute for a lambda.
- Each task pays argument pickling, result pickling, and process startup. Below roughly a millisecond of work per item a pool is slower than a plain loop: batch into chunks, or pass `chunksize=` to `Pool.map` (`performance.md`).
- With fork, children share the parent's memory copy-on-write; with spawn they re-import everything, so a large module-level global costs a full rebuild per child on macOS and Windows.
- A child killed by the OOM killer surfaces as `BrokenProcessPool` with no traceback — check the host's memory before debugging your code (`debugging.md`).
- Never fork from a process whose threads hold locks: the child inherits a locked lock that nobody will release.

## Asyncio
- A forgotten `await` returns a coroutine object that never runs; the "never awaited" warning appears only at garbage collection, far from the bug. Treat any unused coroutine value as an error.
- Blocking calls (`time.sleep`, `requests`, heavy CPU) freeze the entire event loop — every task stalls. Use `asyncio.sleep`, async clients, or `await asyncio.to_thread(blocking_fn)` (`python >=3.9`).
- KEEP a reference to `asyncio.create_task(...)` results — the loop holds only weak references, and an unreferenced task can be garbage-collected mid-execution. Store tasks in a set, or use `asyncio.TaskGroup` (`python >=3.11`), which also cancels siblings on first failure — structured, unlike bare `gather`.
- `asyncio.gather(..., return_exceptions=True)` converts failures into return VALUES — if you don't isinstance-check the results, errors pass silently as list elements.
- TaskGroup raises `ExceptionGroup`, which a plain `except ValueError` does NOT match. Migrating from `gather` to `TaskGroup` silently disables existing handlers until they become `except*` (`errors.md`).
- `asyncio.run()` inside a running loop raises — in notebooks and async frameworks a loop already runs; `await` directly or `create_task`.
- Cancellation arrives as `CancelledError`, which inherits from `BaseException` (`python >=3.8`) specifically so `except Exception` cannot swallow it. If you catch it to clean up, re-raise; a slow `finally` in a task blocks the whole shutdown.
- Every await on the network gets a deadline: `async with asyncio.timeout(5):` (`python >=3.11`), or `asyncio.wait_for` below that floor (`errors.md`).
- Bound concurrency explicitly — 10,000 tasks against one API is a denial of service you wrote. `asyncio.Semaphore(20)` around the call, or a worker pool over an `asyncio.Queue`.
- `asyncio.Queue` is NOT thread-safe. From another thread, use `loop.call_soon_threadsafe` or `asyncio.run_coroutine_threadsafe(coro, loop)`.
- A loop that stalls: run with `PYTHONASYNCIODEBUG=1` (or `asyncio.run(main(), debug=True)`) to log callbacks slower than 100 ms and every un-awaited coroutine. Deeper async theory — cancellation semantics, structured concurrency, the function-colour tax: the `async-patterns` skill (https://clawic.com/skills/async-patterns).
