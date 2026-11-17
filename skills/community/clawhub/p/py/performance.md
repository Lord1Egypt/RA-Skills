# Performance — Measure, Then Change One Thing

Python is fast enough until a specific line is not. The order is always: measure, find the top line, change the algorithm or leave the interpreter — micro-optimizing untargeted code is the most common wasted day.

## Measure First

| Question | Tool | Note |
|---|---|---|
| Where does the wall time go? | `python -m cProfile -o out.prof script.py`, then `pstats`/snakeviz | Deterministic; adds overhead per call, so call-heavy code looks worse than it is |
| Where does a LIVE or production process spend time? | `py-spy top --pid <pid>` / `py-spy record` | Sampling, no code change, no restart |
| Is this line faster than that line? | `timeit` (`python -m timeit -s 'setup' 'stmt'`) | Report the MINIMUM of repeats: noise is one-sided. `timeit` disables gc, so it flatters allocation-heavy code |
| One block inside a real run | `t = time.perf_counter()` … `time.perf_counter() - t` | `perf_counter` is monotonic and high-resolution; never `time.time()` (`datetime.md`) |
| Which allocations grow? | `tracemalloc` snapshots + `compare_to` | Line-level attribution (`debugging.md`) |
| Why does startup take 1.5 s? | `python -X importtime script.py` | Usually one heavy import at module scope |

Amdahl, as the sanity check before you start: total speedup = `1 / ((1 - p) + p/s)`. Making a function 10× faster when it is 20% of runtime buys 1.22×. If the top profile line is not what you are about to optimize, stop.

## The Cost Model Worth Internalizing

- A Python-level function call costs roughly 50–100 ns; an attribute lookup tens of ns; a simple bytecode op single-digit ns. Order of magnitude: CPython does tens of millions of simple operations per second, not billions.
- That means: 10^4 iterations of anything reasonable is free; 10^7 per-item Python function calls cost 0.5–1 s of call overhead alone; at 10^8 that overhead is 5–10 s before the loop body does any work, which is the size where you leave the interpreter rather than tune the loop.
- Consequence: the winning move is almost never "make the loop body faster", it is "run the loop fewer times", "push the loop into C" (numpy, `str.join`, `sorted`, `sum`, `re`), or "do not run it at all" (cache, index, filter earlier).

## The Wins, In Order Of Payoff

1. **Wrong complexity.** `x in list` inside a loop is O(n²) over the pair; a set makes it O(n) (`collections.md`). Same for repeated `list.pop(0)` (use `deque`), repeated `min()` scans (use `heapq`), and re-sorting inside a loop.
2. **Doing I/O per item.** One query per row, one HTTP call per item, one `open()` per line. Batch it: the fix is 10–100×, not 10%. For I/O-bound work, concurrency is the lever (`concurrency.md`), not CPU tricks.
3. **Recomputation.** `functools.lru_cache`/`functools.cache` on pure functions with repeated arguments; precompute a dict index instead of scanning. Watch the memory: `cache` is unbounded, and caching methods pins instances (`functions.md`).
4. **Leaving the interpreter for array math.** numpy on whole arrays instead of Python loops is typically 10–100× on numeric workloads — the range is real and depends on how much of the loop you vectorize. Pandas for tabular, `re` for scanning, `str.join` for building.
5. **Upgrading the interpreter.** `python >=3.11` runs roughly 1.25× faster than 3.10 on pyperformance (python.org release notes) with no code change (`versions.md`). PyPy is often several times faster on pure-Python CPU work but pays a C-extension compatibility tax. Cython/mypyc/Rust extensions only for a hot kernel that profiling has already named.
6. **Micro-optimizations** (hoisting attribute lookups into locals, comprehension instead of append-loop, avoiding a temporary list): single-digit to ~30% on the line itself. Worth it only inside the top profile line.

## Memory

- The peak is what kills the process (`MemoryError`, or exit 137 from the OOM killer). Streaming beats size: iterate `for line in f` instead of `f.read()`, use generators between stages, and `pandas.read_csv(chunksize=…)` for files that do not fit.
- Per-object overhead dominates for small records: a plain instance carries a `__dict__`. `dataclass(slots=True)` (`python >=3.10`) or `__slots__` typically cuts small-object memory by roughly a third to a half and speeds attribute access slightly (`classes.md`). For millions of homogeneous numbers, `array.array` or numpy is an order of magnitude better than a list of ints.
- `sys.getsizeof` measures the object alone, not what it references — a list of 1M ints reports ~8 MB while the ints themselves cost far more. Use `tracemalloc` for the real answer.
- Freeing objects does not always return RSS to the OS (allocator arenas). Steady-state RSS above the live-object total is fragmentation, not a leak — the fix is fewer peaks, not more `del`.
- Generators reduce memory, not CPU. A generator chain that is consumed once is strictly better than a list; one that is consumed twice is a bug (`functions.md`).

## Concurrency As A Performance Tool

- I/O-bound: threads or asyncio turn N sequential waits into one (`concurrency.md`). This is where 10× lives for most applications.
- CPU-bound pure Python: only processes escape the GIL, and each process pays startup plus pickling of arguments and results — a worker pool is a loss below roughly a millisecond of work per task. Batch small tasks into chunks before parallelizing.
- Threads around numpy/C extension calls work: those release the GIL.

## Benchmarking Discipline

- Fix the input and the machine state; run 5+ repeats; report the minimum for microbenchmarks and the median plus spread for end-to-end. A single timing is a rumor.
- Compare against the previous implementation on the same run, not against a number in a commit message from another laptop.
- Warm the caches you will have in production (JIT-less Python has few, but the OS page cache, DNS, and connection pools are real) or you are measuring cold-start.
- State the input size with every result: "2.3 s for 50k rows" is a fact; "2.3 s" is not.

Deeper method — profile types, flame graphs, sampling vs instrumentation: the `profiling` skill (https://clawic.com/skills/profiling).
