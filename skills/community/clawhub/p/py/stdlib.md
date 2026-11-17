# The Standard Library You Forgot You Had

The most common Python code smell is thirty lines reimplementing something in the stdlib, badly. Scan this before writing a helper.

## Collections and Iteration

| Need | Use | The trap it removes |
|---|---|---|
| Count occurrences | `collections.Counter(xs)`, `.most_common(k)` | Hand-rolled `d[x] = d.get(x, 0) + 1` loops |
| Group by a key | `collections.defaultdict(list)` | `itertools.groupby` groups only CONSECUTIVE keys (`collections.md`) |
| Queue, stack, sliding window | `collections.deque(maxlen=n)` | `list.pop(0)` is O(n); deque is O(1) at both ends |
| Top-k of many | `heapq.nlargest(k, xs)` | Sorting everything to take 10 |
| Keep a list sorted / binary search | `bisect.insort`, `bisect.bisect_left` | Re-sorting after every insert |
| Chunks of n | `itertools.batched(xs, n)` (`python >=3.12`) | Index arithmetic off-by-ones |
| Flatten one level | `itertools.chain.from_iterable(xss)` | Nested comprehensions nobody can read |
| Running totals, pairs, first n | `itertools.accumulate`, `pairwise` (`python >=3.10`), `islice` | Manual index bookkeeping |
| Cartesian products, combinations | `itertools.product`, `combinations` | Nested loops that grow a level per dimension |
| Dedupe preserving order | `dict.fromkeys(xs)` | `set()` loses order (`collections.md`) |
| Topological order of a DAG | `graphlib.TopologicalSorter` (`python >=3.9`) | A recursive visit with a cycle bug |

## Functions and Caching

- `functools.cache` (`python >=3.9`) / `lru_cache(maxsize=…)` for pure functions; `cached_property` for per-instance lazy values (memory caveats in `functions.md`).
- `functools.partial` instead of a lambda that only binds arguments — it is picklable, so it survives `multiprocessing` (`concurrency.md`).
- `functools.singledispatch` for type-based dispatch instead of an `isinstance` ladder.
- `operator.itemgetter("name")` / `attrgetter` as sort keys: faster than a lambda and self-documenting. `sorted(xs, key=itemgetter(1, 0))` for multi-key.
- `contextlib.contextmanager` to write a `with` in five lines; `ExitStack` for a variable number of context managers; `suppress`, `redirect_stdout`, `closing`, `chdir` (`python >=3.11`).

## Text, Data, Formats

- `textwrap.dedent` for indented triple-quoted strings (test fixtures stop having leading spaces); `textwrap.shorten` for previews.
- `difflib.get_close_matches(word, options)` for "did you mean"; `difflib.unified_diff` to show what changed without shelling out to `diff`.
- `unicodedata.normalize("NFC", s)` before comparing strings that came from different systems (`files.md`).
- `string.Template` when the template itself is untrusted (`security.md`).
- `tomllib.load` (`python >=3.11`, read-only, binary mode) for TOML; `configparser` for INI; `json` and `csv` for the rest (`files.md`).
- `re` compiles and caches patterns internally — `re.compile` at module level is for readability and for reusing flags, not usually for speed. Deeper: the `regex` skill (https://clawic.com/skills/regex).

## Numbers, Time, Identity

- `statistics.mean/median/quantiles/stdev` — correct for small data and readable; numpy when the array is large (`performance.md`).
- `decimal.Decimal` for money, `fractions.Fraction` for exact ratios (`types.md`).
- `math.isclose`, `math.prod`, `math.comb`, `math.dist` — all of them beat the hand-rolled version.
- `datetime` + `zoneinfo` (`python >=3.9`) for calendars; `time.monotonic` for durations (`datetime.md`).
- `uuid.uuid4()` for random ids, `uuid.uuid5(namespace, name)` when the same input must always produce the same id.
- `secrets` for anything a user must not guess; `random` only for simulation (`security.md`).
- `hashlib.blake2b` for fast non-cryptographic-purpose digests of content, `hmac.compare_digest` for comparing them.

## Filesystem, Processes, Packaging

- `pathlib.Path` over `os.path`; `shutil` for `copy2`, `copytree`, `rmtree`, `which`, `disk_usage`, `make_archive`.
- `tempfile.TemporaryDirectory` as a context manager (`files.md`).
- `importlib.resources.files("pkg") / "data.json"` to read package data — the only form that works inside a wheel or a zipapp (`packaging.md`).
- `importlib.metadata.version("mypkg")` to report your own version without importing the package or parsing setup files.
- `subprocess.run` for external commands; `shutil.which` to check availability first (`subprocess.md`).
- `sqlite3` is a real database that ships with Python: use it for caches, queues, and test fixtures instead of a pickle file — with `?` placeholders, never string formatting, and WAL plus a busy timeout the moment a second process appears (`sqlite.md`).

## Debugging and Measurement

`timeit`, `cProfile`, `tracemalloc`, `faulthandler`, `warnings`, `traceback`, `inspect.signature`, `dis` — what each one answers is in `performance.md` and `debugging.md`.

## What The Stdlib Does NOT Have

Know these so you stop looking: an HTTP client with a sane API (`urllib.request` works and is unpleasant — httpx/requests, `http.md`), retry with backoff (write it, `errors.md`), a TOML writer, a deep-diff, a portable file lock (`files.md`), timezone data on Windows (`tzdata`), and dataframes. Everything else, check here first.
