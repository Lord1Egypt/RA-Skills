# Debugging — Symptom to Cause

Python tells you exactly where it died and almost never why. Work symptom-first; every step below is a check, not a guess.

## The Universal First Three

1. Read the traceback from the BOTTOM: the last line is the exception, the frame directly above it is where it raised, and the frames above that are how you got there. `python >=3.11` prints carets under the exact failing sub-expression — the difference between `a.b.c()` and `a.b().c`.
2. `python -X dev script.py` — dev mode turns on the checks that are off in production: unclosed files and sockets (`ResourceWarning`), `-W default` for deprecations, and extra allocator checks. Most "mystery" bugs announce themselves here.
3. `python -c "import sys; print(sys.executable, sys.version)"` — before theorizing, confirm you are debugging the interpreter you think you are. Wrong venv is the single most common cause of "but I installed it".

## pdb In Under A Minute

- `breakpoint()` at the suspect line (`python >=3.7`); `PYTHONBREAKPOINT=0` disables every one of them without editing code, so debug breakpoints can survive a commit and stay inert in prod.
- Post-mortem beats stepping: `python -m pdb -c continue script.py` runs at full speed and drops into the frame that raised. In a REPL/notebook, `import pdb; pdb.pm()` after the exception. Under pytest: `pytest -x --pdb`.
- The six commands that matter: `w` (where am I in the stack), `u`/`d` (walk frames), `p obj` / `pp obj.__dict__`, `n`/`s`/`c`, `b file.py:42, cond` (conditional breakpoint), `interact` (a full REPL in that frame).
- Print `repr()`, never `str()`: `' 12 '` vs `12` vs `'12'` are three different bugs that print identically.

## Error Message → Cause

| Message | Cause and first move |
|---|---|
| `ModuleNotFoundError: No module named 'x'` | Wrong interpreter or unactivated venv. Always `python -m pip install`, never bare `pip` (`packaging.md`) |
| `ImportError: cannot import name 'X' from partially initialized module` | Circular import; the traceback names both ends (`imports.md`) |
| `AttributeError: module 'json' has no attribute 'loads'` | A local file shadows the stdlib module: `print(json.__file__)` (`imports.md`) |
| `AttributeError: 'NoneType' object has no attribute 'x'` | Something returned None — usually an in-place method: `xs = xs.sort()`, `s = s.replace(...)` forgotten, or a function with a missing `return` |
| `UnboundLocalError: local variable 'x' referenced before assignment` | The name is assigned somewhere later in the same function (`functions.md`) |
| `TypeError: 'X' object is not subscriptable / not callable` | You have the class where you wanted an instance, or a shadowed builtin (`list = [...]` earlier in the file) |
| `RecursionError: maximum recursion depth exceeded` | Real recursion, or `__getattr__`/`__eq__`/`__repr__` calling itself. Raising `sys.setrecursionlimit` converts it into a segfault, not a fix |
| `RuntimeError: dictionary changed size during iteration` | Mutating while iterating (`collections.md`) |
| `RuntimeWarning: coroutine 'f' was never awaited` | A missing `await`; the warning fires at GC, far from the bug (`concurrency.md`) |
| `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x93 in position N` | The file is cp1252/latin-1 or binary, and `open()` used the platform default (`files.md`) |
| `UnicodeEncodeError: 'charmap' codec can't encode` | Output encoding, not input: a Windows console or a redirected stdout (`cli.md`) |
| `ValueError: I/O operation on closed file` | A generator or lazy object outlived the `with` block that opened its file (`files.md`) |
| `TypeError: can't compare offset-naive and offset-aware datetimes` | Mixed naive/aware datetimes (`datetime.md`) |
| `error: externally-managed-environment` | PEP 668: the OS owns that interpreter — create a venv (`packaging.md`) |
| `ImportError: ... incompatible architecture` / `symbol not found` | A wheel built for another CPU or Python version (`packaging.md`) |
| Killed, exit 137, no traceback | The OOM killer, not Python (`performance.md` memory section) |
| Segfault with no traceback at all | A C extension or a mismatched wheel; run with `PYTHONFAULTHANDLER=1` to get the C-level stack |
| `pytest` collected 0 items | File/function naming or rootdir (`testing.md`) |

## Chain: Wrong Answer, No Exception

1. Bisect the pipeline, not the code: print `repr()` of the value at three points (input, midpoint, output) and find the first place it is already wrong. One well-placed `repr` beats ten `print("here")`.
2. At that point ask three questions in order: is it aliasing (someone else holds this same list — `collections.md`), is it a type coercion (`"3" + "4"`, `True` counting as 1, float rounding — `types.md`), or is it stale state (a default argument, a class attribute, a module-level cache — `functions.md`)?
3. Freeze the suspicion into an assertion — `assert isinstance(v, Decimal), repr(v)` — and run again. An assertion that never fires eliminates a whole branch of the search.
4. If the value is only wrong sometimes: iteration order (`PYTHONHASHSEED` randomizes set order per process), concurrency (`concurrency.md`), or wall-clock/timezone (`datetime.md`).

## Chain: It Hangs

1. Get the stack of the LIVE process without restarting it: `py-spy dump --pid <pid>` (no code change, works on production processes). Stdlib fallback: run under `PYTHONFAULTHANDLER=1` and send `SIGABRT`, or arm `faulthandler.dump_traceback_later(30, exit=True)` in code.
2. Read which frame is on top:
   - blocked in `recv`/`read` → a network call with no timeout (`errors.md` timeout rule)
   - blocked in `acquire` → lock ordering deadlock, or a lock held across an `await`/blocking call
   - blocked in `Popen.wait` → the child filled a 64 KiB pipe buffer nobody drains (`subprocess.md`)
   - blocked in `queue.get` / `join` → a producer died and never signalled; workers wait forever
   - the event loop looks idle but nothing progresses → a blocking call inside a coroutine (`concurrency.md`)
3. Reproduce with a timeout so the hang becomes a traceback: `asyncio.timeout(5)` (`python >=3.11`), `timeout=` on every subprocess and HTTP call, `Lock.acquire(timeout=…)`.

## Chain: Memory Grows Until It Dies

1. Confirm it is Python objects, not RSS fragmentation: `tracemalloc.start()` early, then `snapshot2.compare_to(snapshot1, 'lineno')[:10]` — the top line names the allocation site.
2. Usual owners, in order of frequency: an unbounded cache (`lru_cache` on a method pins `self` — `functions.md`), a global list/dict that only grows, log records or exceptions held in a retry list, an open generator holding a large frame.
3. Cycles with `__del__` used to be uncollectable; since `python >=3.4` they are collected, but a `__del__` that resurrects or raises still leaks quietly — check `gc.collect()` return value and `gc.garbage`.
4. Peak vs steady: a job that dies loading a file is not a leak (`performance.md` — stream it instead).

## Chain: Works Locally, Fails in CI or Prod

| Difference | Check |
|---|---|
| Different interpreter or venv | `python -VV` and `python -m pip freeze` on both sides; compare, do not assume |
| Package installed editable locally, versioned in CI | `pip show <pkg>` — a stale wheel in CI is not your source tree |
| Missing env var | The code reads `os.environ["X"]` behind a branch that never runs locally; grep for `environ` and `getenv` |
| Timezone (servers run UTC) | Any naive `datetime.now()` shifts (`datetime.md`) |
| Locale and encoding | `LANG=C` makes the default `open()` encoding ASCII (`files.md`); explicit `encoding="utf-8"` immunizes |
| Case-sensitive filesystem on Linux | `import Utils` and a file named `utils.py` work on macOS, fail on Linux |
| Hash randomization | `PYTHONHASHSEED` differs per run; set iteration order and `hash()` values are not stable (`collections.md`) |
| CPU architecture / wheels | arm64 laptop vs amd64 runner: `pip debug --verbose` lists supported tags (`packaging.md`) |
| Working directory | Relative paths resolve against the caller's cwd, not the file's; anchor with `Path(__file__).parent` |
| Network egress blocked | A test that quietly hits the internet passes locally and times out in CI |

## Minimal Reproduction

`python -I -c "<the five suspect lines>"` runs isolated: no `PYTHONPATH`, no user site-packages, no environment leakage. Re-add one import, one env var, one flag at a time — the addition that breaks it names the subsystem and the file to open next in SKILL.md Quick Reference.

## Two Tools Worth Knowing Before You Need Them

- `python -X importtime script.py` — a per-import cost table; a CLI that takes 1.5 s to print `--help` is almost always one heavy import at module scope (`performance.md`).
- `python -m dis` / `dis.dis(f)` — settles arguments about what an expression actually does (evaluation order, whether a comprehension builds a list). Rarely needed, decisive when it is.
