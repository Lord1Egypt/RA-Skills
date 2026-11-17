# Function Traps

## Defaults and scope
- Defaults evaluate ONCE at `def` time: `def f(xs=[])` shares one list across all calls; `def f(t=time.time())` freezes the timestamp. Fix: `xs=None` + `if xs is None: xs = []`. The `xs = xs or []` shortcut is a bug: a caller passing an empty list to be filled in place gets a fresh list — their reference never sees the appends (canonical rule → SKILL.md rule 1).
- Assigning to a name anywhere in a function makes it local for the WHOLE function — reading it before the assignment raises `UnboundLocalError` even if a global exists. Declare `global` (module scope) or `nonlocal` (enclosing function) before writing.
- Closures capture variables, not values: `[lambda: i for i in range(3)]` all return 2 — every lambda reads the same `i` after the loop ends. Fix: `lambda i=i: i` (default binds now) or `functools.partial`.
- Module-level mutable state (a cache dict, a counter, a configured client) is a default argument with extra steps: it persists across calls, across tests in the same process, and across `multiprocessing` fork children.

## Decorators
- Always `@functools.wraps(fn)` on the wrapper — without it `__name__`, docstring, and signature introspection report the wrapper, breaking debuggers, pickling, and `mock.patch` targeting by name.
- `@deco` and `@deco()` are different call graphs: the first receives the function, the second must return something that receives the function. Support both only via an explicit `if fn is None` factory branch.
- Stacking applies bottom-up and executes top-down: `@a` over `@b` means `a(b(fn))`, so `@a` runs FIRST at call time. Order matters whenever one decorator authenticates and another logs or caches.
- `@functools.lru_cache` on a METHOD stores strong references to `self` in the cache — instances never free (memory leak in long-lived services). Use `functools.cached_property` (`python >=3.8`) or cache on the instance. Default `maxsize=128`; `maxsize=None` grows without bound — size it deliberately (`performance.md`).
- A class used as a decorator loses method binding: the instance is not a function, so it never becomes a bound method and `self` arrives as the first positional argument of the wrapped call. Use a function-based decorator, or implement `__get__`.
- Decorators erase the signature for type checkers unless you annotate with `ParamSpec` (`python >=3.10`, `type-checking.md`).

## Generators
- A generator body does not run until first `next()` — argument validation inside the generator fires far from the call site. Split: a plain function validates, then returns the inner generator.
- Generators exhaust after one pass; a second `for` loop silently yields nothing. If consumed twice, materialize with `list()` or restructure — `itertools.tee` buffers everything the slower consumer hasn't read, so it is not a free replay.
- A generator that holds an open file keeps it open until exhausted or collected; abandoning it half-way leaves the handle alive, and returning one from inside a `with` block yields `ValueError: I/O operation on closed file` for the consumer (`files.md`).
- `return` inside `finally` swallows any in-flight exception from the `try` block — the function "succeeds" while the error vanishes. Same for `break`/`continue`; `python >=3.14` emits a SyntaxWarning for these (PEP 765).
- `yield from sub()` delegates iteration, `send`, and exceptions to the sub-generator; a manual `for x in sub(): yield x` loop silently drops `send` and `throw`.
- Generators reduce peak memory, not CPU (`performance.md`). Reach for one when the data does not fit or the consumer may stop early.

## Context managers
- `@contextlib.contextmanager` turns a generator into a `with`: setup, `yield`, teardown. Put the teardown in a `finally` inside the generator, or an exception in the body skips it entirely.
- A variable number of resources is `contextlib.ExitStack`, not nested `with` blocks built by string concatenation.
- `__exit__` returning a truthy value SWALLOWS the exception — return None (or nothing) unless suppressing is the manager's job.

## Signatures
- Force keyword-only for flags: `def move(src, dst, *, overwrite=False)` — prevents `move(a, b, True)` where True silently lands in the wrong positional slot after a refactor.
- `*args`/`**kwargs` pass-through hides the real contract from readers, checkers, and editors. Use it for genuine forwarding, not to avoid naming three parameters.
- Positional-only (`def f(x, /)`, `python >=3.8`) lets you rename a parameter later without breaking callers — worth it in library APIs.
- After an except block, the exception variable is DELETED (`except Exception as e:` — using `e` after the block raises NameError). Bind to another name inside the block if needed later.
- Return one type, not "a dict on success and False on failure". Callers cannot branch safely on that, and every wrong-value bug three layers down starts here (`errors.md`).
