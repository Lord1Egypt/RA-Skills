---
name: py
slug: py
version: 1.0.4
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
description: >-
  Writes, debugs, and reviews Python code — runtime traps, packaging, typing, async, tests,
  performance. Use when Python raises or misbehaves: ModuleNotFoundError, circular imports,
  AttributeError on None, UnboundLocalError, UnicodeDecodeError, mutable default arguments,
  `is` vs `==`, float rounding, naive vs aware datetimes, or a wrong answer with no
  exception; when pip, uv, poetry, venv, pyproject or a lockfile fight over dependencies,
  or a package installs but will not import; when threads, asyncio, multiprocessing or the
  GIL hang, deadlock, or leak memory; when pytest passes but should not, mocks patch the
  wrong module, or async tests never run; when mypy or pyright errors need clearing; when
  a script is slow, eats RAM, or gets OOM-killed; when subprocess calls hang or logs never
  appear; or when upgrading Python breaks the build. Not for library-specific problems —
  pandas, numpy, django, fastapi and flask have their own skills.
homepage: https://clawic.com/skills/py
metadata:
  clawdbot:
    emoji: 🐍
    requires:
      bins:
      - python3
    os:
    - linux
    - darwin
    - win32
    displayName: Python
    configPaths:
    - ~/Clawic/data/py/
---

User preferences live in `~/Clawic/data/py/config.yaml` (see Configuration); nothing else is stored on the user's machine. If you have data at an old location (`~/py/` or `~/clawic/py/`), move it to `~/Clawic/data/py/`.

## When To Use

- Writing or reviewing Python — scan Core Rules and Output Gates before committing
- Debugging wrong results without exceptions: state leaking across calls, aliased mutations, silent coercion
- Any traceback whose cause is not obvious in ten seconds, plus hangs, memory growth, and segfaults
- Environment and dependency work: venvs, lockfiles, editable installs, publishing, version upgrades
- Choosing a concurrency model, a data model, or a typing strategy, and living with the consequences
- Hardening a script into a tool: arguments, exit codes, logging, timeouts, retries, untrusted input
- Not for library-specific issues — `pandas`, `numpy`, `django`, `fastapi`, `flask` have their own skills

## Quick Reference

| Situation | Play |
|-----------|------|
| Wrong value, no exception | `repr()` at input, midpoint, output; the first wrong one is the bug — suspect aliasing, coercion, stale default → `debugging.md` |
| A traceback you have not seen before | Message → cause table, then the matching chain → `debugging.md` |
| Installed it, still `ModuleNotFoundError` | Wrong interpreter: check `sys.executable`, then use `python -m pip` → `packaging.md` |
| venvs, lockfiles, uv vs pip vs poetry, publishing | Applications pin everything with hashes; libraries declare ranges → `packaging.md` |
| `cannot import name X from partially initialized module` | Circular import; switch to `import a` + `a.f()` before restructuring → `imports.md` |
| `is` vs `==`, float rounding, money, NaN, string surgery | `is` only for `None`/`True`/`False`/sentinels; `Decimal` from strings → `types.md` |
| Aliasing, copies, ordering, membership cost | `[[]]*3` shares one list; `x in list` is O(n) → `collections.md` |
| State leaks across calls: defaults, closures, decorators, generators | Defaults evaluate once, at `def` time → `functions.md` |
| Class design: shared attributes, hashability, MRO, `__slots__` | `__eq__` without `__hash__` makes instances unhashable → `classes.md` |
| dict vs dataclass vs NamedTuple vs pydantic; validating input | Validate once at the boundary, plain objects inside → `data-modeling.md` |
| Slow, hanging, or racy: GIL, threads, asyncio, multiprocessing | Pure-Python CPU → processes; I/O → threads or asyncio → `concurrency.md` |
| Too slow, or too much memory | Profile first, then fix the top line or nothing → `performance.md` |
| Tests pass but should not; mock patches nothing; async tests skipped | Patch where the name is USED; `autospec=True` → `testing.md` |
| mypy or pyright errors, annotating a legacy codebase | Freeze a baseline, then ratchet one package at a time → `type-checking.md` |
| Formatting, import order, lint rules, pre-commit, style review comments | One formatter owns layout; `ruff check` for bugs; same versions in hook and CI → `linting.md` |
| `UnicodeDecodeError`, CSV and JSON traps, atomic writes, temp files | Declare `encoding="utf-8"`; write temp then `os.replace` → `files.md` |
| Timezones, DST, parsing dates, measuring elapsed time | Aware datetimes everywhere; `time.monotonic()` for durations → `datetime.md` |
| Calling git/ffmpeg/anything external, hanging or failing silently | `run([...], check=True, timeout=…)`, never `shell=True` with interpolation → `subprocess.md` |
| Writing a script or CLI: arguments, exit codes, pipes, signals | `sys.exit(main())`; stdout for data, stderr for logs → `cli.md` |
| Nothing appears in the logs, or deciding what to log | Four gates: basicConfig no-op, logger level, handler level, propagation → `logging.md` |
| Exception design, chaining, retries, timeouts | `raise X from exc`; exponential backoff with jitter → `errors.md` |
| Calling an HTTP API: sessions, status codes, redirects, streaming a big body | One client per process; `raise_for_status()` before `.json()` → `http.md` |
| A local database, cache, or queue in a file; `database is locked` | WAL plus an explicit busy timeout; one connection per thread → `sqlite.md` |
| Untrusted input: pickle, eval, SQL, paths, archives, secrets | Unpickling executes code; parameterize SQL; contain paths → `security.md` |
| "Is there something in the stdlib for this?" | Counter, deque, bisect, itertools, pathlib, secrets, sqlite3 → `stdlib.md` |
| Notebook works for you and nobody else; results change between runs | Restart and run all; `%pip` not `!pip`; strip outputs before committing → `notebooks.md` |
| Upgrading Python, choosing a version, a module that vanished | Run the suite with `-W error::DeprecationWarning` on the OLD version first → `versions.md` |
| Anything else | Core Rules below, then reproduce with `python -I -c '<the five suspect lines>'` and re-add one thing at a time |

Each file above is one sub-job and is self-contained: read SKILL.md by default, open exactly one guide when the situation matches.

## Core Rules

1. No mutable defaults: `def f(xs=None)` then `if xs is None: xs = []`. Never `xs = xs or []` — a caller passing an empty list to be filled gets a fresh list instead; their reference stays empty.
2. `is` only for `None`, `True`, `False`, and sentinel objects; `==` for everything else. Interning makes `is` on ints and strings pass in tests and fail in production (`types.md`).
3. Never mutate the collection you iterate — dicts raise `RuntimeError`, lists silently skip elements. Iterate a copy (`for x in list(xs)`) or collect changes and apply after.
4. Match concurrency to workload: pure-Python CPU → `multiprocessing`; I/O → threads or asyncio; threads never speed up pure-Python CPU work, because the GIL serializes bytecode (`concurrency.md`).
5. `except Exception:`, never bare `except:` — bare also catches `KeyboardInterrupt` and `SystemExit`, making the process unkillable. Re-raise with bare `raise`, keeping the original traceback (`errors.md`).
6. Files, locks, sockets, connections: always `with`. CPython's refcounting closes leaked handles by accident; exceptions and other interpreters (PyPy) expose the leak.
7. Money and exact decimals: `decimal.Decimal('1.10')` from strings — `Decimal(1.1)` imports the float error it was meant to avoid. Float comparisons via `math.isclose` (`types.md`).
8. Declare `encoding='utf-8'` at every I/O boundary — the default follows the platform locale until UTF-8 becomes the default (PEP 686, `python >=3.15`), so the code breaks first on Windows and in lean containers (`files.md`).
9. Guard entry points with `if __name__ == "__main__":` — top-level code runs on every import and again in every `multiprocessing` spawn child (`imports.md`).

## Version Floors

The syntax and stdlib floors that shape everyday code. Individual guides carry additional floors — mostly changed defaults and new keyword arguments — inline in this same `python >=X.Y` form, next to the instruction each one gates. Support windows, removals, and the upgrade procedure: `versions.md`.

| Feature | Needs |
|---|---|
| Guaranteed dict insertion order, dataclasses, `breakpoint()`, `from __future__ import annotations`, `sys.stdout.reconfigure` | python >=3.7 |
| Walrus `:=`, positional-only `/`, `functools.cached_property`, `TypedDict`/`Protocol`/`Literal`/`Final`, `basicConfig(force=)`, self-documenting `f"{value=}"` | python >=3.8 |
| Builtin generics `list[int]`, `d1 \| d2` (dict merge), `zoneinfo`, `removeprefix`/`removesuffix`, `functools.cache`, `asyncio.to_thread`, `importlib.resources.files`, `Path.is_relative_to`, `graphlib`, `argparse.BooleanOptionalAction`, `executor.shutdown(cancel_futures=)` | python >=3.9 |
| `X \| Y` unions, `match`, `zip(strict=True)`, dataclass `slots=`/`kw_only=`, `itertools.pairwise`, `ParamSpec`, `EncodingWarning` and `-X warn_default_encoding` | python >=3.10 |
| `ExceptionGroup`/`except*`, `asyncio.TaskGroup`, `tomllib`, `Self`, `StrEnum`, `exc.add_note()`, `contextlib.chdir`, full-ISO `fromisoformat`, `NotRequired` | python >=3.11 |
| PEP 695 generics (`def f[T]()`), `@override`, `itertools.batched`, `tarfile(filter="data")` | python >=3.12 |
| Experimental free-threaded build; PEP 594 module removals (`cgi`, `telnetlib`, …) | python >=3.13 |
| `forkserver` as the Linux multiprocessing default, lazy annotations (PEP 649) | python >=3.14 |
| UTF-8 as the default text encoding everywhere (PEP 686), retiring the locale default | python >=3.15 |

## Output Gates

Before delivering Python code, check:

- No mutable default argument, and no `xs or []` where an empty argument is meaningful
- Every text `open`, `subprocess`, and decode boundary declares `encoding="utf-8"`; every file, lock, socket, and connection is acquired in a `with`
- Every network, subprocess, lock, and queue call has a timeout
- Exceptions: narrowest class caught, chained with `from`, nothing swallowed without a log line or a written reason
- Logging through a module logger with lazy `%s` arguments and no secrets
- Syntax and stdlib stay within `min_python`; annotations match `type_strictness`
- Nothing user-supplied reaches `eval`, `pickle`, a shell string, an SQL string, or a path join without containment
- The new test was seen failing without the fix in place — `change_workflow` decides when that run happens, never whether it happened

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/py/config.yaml`. Never interview the user — record a preference the moment it is stated.

| Variable | Type | Default | Effect |
|---|---|---|---|
| min_python | 3.9 \| 3.10 \| 3.11 \| 3.12 \| 3.13 \| 3.14 | 3.11 | Gates which Version Floors features may be emitted unguarded, and which fallback appears instead |
| package_manager | pip \| uv \| poetry \| pdm \| conda | pip | Chooses the install, lock, and venv commands in every example (`packaging.md`) |
| type_strictness | none \| gradual \| strict | gradual | How far annotations go: none skips hints, gradual annotates public boundaries, strict turns on `disallow_untyped_defs` (`type-checking.md`) |
| test_runner | pytest \| unittest | pytest | Shape of emitted tests, fixtures, and mocking guidance (`testing.md`) |
| target_os | linux \| macos \| windows \| cross | cross | Path, encoding, and multiprocessing start-method assumptions; `cross` flags all three |
| src_layout | src \| flat | src | Project scaffolding, editable-install and import advice (`packaging.md`) |
| line_length | number (79-120) | 88 | Formatting of emitted code and the `ruff`/`black` config value (`linting.md`) |
| change_workflow | test-first \| fix-first | test-first | Order of the work: test-first writes the failing test before the fix, fix-first patches first and backfills the test against the reverted change (`testing.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: formatter and linter (ruff vs black+flake8), checker (mypy vs pyright), task runner, notebook vs module workflow — affects every emitted config block (`linting.md`)
- **Conventions**: docstring style (Google/NumPy/reST), naming, module granularity, error-message phrasing — affects generated code and review comments
- **Platform**: deployment target (container, serverless, desktop, embedded), CPU architecture, private package index, CI provider — affects `packaging.md` and `versions.md` guidance
- **Safety posture**: how aggressively to flag `pickle`, `eval`, `shell=True`, missing timeouts and unpinned dependencies — affects `security.md` and `cli.md`
- **Dependencies**: stdlib-only constraints, banned or mandated libraries (requests vs httpx, pydantic vs dataclasses), tolerance for new transitive dependencies — affects every recommendation
- **Output format**: whole file vs minimal diff, how much explanation, whether tests accompany every change — affects the shape of the answer, never the correctness rules
- **Work order**: which gates run before a change is proposed rather than after — checker and suite green first, a plan approved before editing, a `--dry-run` pass on destructive scripts, a profile before any optimization — affects the sequence of every task, never the correctness rules

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Bare `pip install` | Installs into whatever interpreter is first on PATH — the "installed it, still ModuleNotFoundError" loop | `python -m pip install` inside an activated venv (`packaging.md`) |
| `except Exception: pass` | Turns a crash into a wrong answer three layers away | Log with `logger.exception`, or write down why this failure is expected (`errors.md`) |
| `assert user.is_admin` as a check | `python -O` removes every assert, including that one | Raise explicitly (`security.md`) |
| `time.time()` to measure a duration | NTP can step the clock backwards mid-measurement and produce negative elapsed time | `time.monotonic()` (`datetime.md`) |
| `datetime.utcnow()` | Returns a NAIVE datetime holding UTC: compares wrong against aware values, deprecated in `python >=3.12` | `datetime.now(timezone.utc)` (`datetime.md`) |
| f-strings inside logging calls | Formats even when the level is disabled, and every line becomes a unique string to the aggregator | `log.info("user %s", uid)` (`logging.md`) |
| `sys.path.append(...)` to fix an import | Works from one entry point, breaks under pytest, packaging, and any other cwd | Editable install with a `src/` layout (`imports.md`) |
| `shell=True` with an interpolated value | Command injection — and `/bin/sh` is not bash | Argument list; `shlex.quote` if a shell is unavoidable (`subprocess.md`) |
| `verify=False` to silence an SSL error | Disables peer authentication for every request in the process | Install the CA bundle (`security.md`) |
| `pickle` across a process, user, or network boundary | Unpickling executes attacker-controlled code before you can inspect it | JSON/msgpack, or an HMAC-signed payload (`security.md`) |
| `raise e` when re-raising | Appends the current line and hides where the exception really came from | Bare `raise` (`errors.md`) |
| Type hints treated as validation | Never enforced at runtime: `def f(x: int)` happily takes a string | Checker in CI plus runtime validation at the boundary (`type-checking.md`) |
| `x in list` or `list.pop(0)` inside a loop | O(n) per operation makes the loop O(n²) | `set` for membership, `deque` for both ends (`collections.md`) |

## Where Experts Disagree

- **asyncio vs threads.** asyncio is not "faster Python": for moderate I/O concurrency, `ThreadPoolExecutor` matches it with far less ceremony. Boundary: high connection counts AND an async-native stack end to end → asyncio; one blocking driver anywhere in the chain forfeits the benefit (`concurrency.md`).
- **How much typing.** The strict school annotates everything and treats `Any` as a defect; the pragmatic school types boundaries and lets internals be inferred. Boundary: libraries and cross-team APIs → annotate fully; single-owner scripts and glue → boundaries only. Either way, one checker in CI (`type-checking.md`).
- **Packaging tooling.** `venv` + `pip` exists on every machine and surprises nobody; `uv`/`poetry`/`hatch` are faster and manage more. Boundary: a project with a real dependency problem, many contributors, or several interpreters justifies the tool; one that installs three libraries does not (`packaging.md`).
- **EAFP vs LBYL.** Python's culture prefers `try/except` over pre-checking, and it is genuinely more correct under concurrency — the file can disappear between `exists()` and `open()`. Boundary: LBYL when the operation is expensive or irreversible, EAFP when the failure is cheap and the race is real.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/py (install if the user confirms):
- `pandas` — DataFrame-specific traps and idioms
- `fastapi` — async web APIs in Python
- `django` — Django ORM and framework patterns
- `profiling` — when the question is "why is it slow", measure first
- `debugging` — language-agnostic fault isolation (bisection, hypothesis discipline, minimal repro); the Python-specific version of that job is this skill's `debugging.md`

## Feedback

- If useful, star it: https://clawic.com/skills/py
- Latest version: https://clawic.com/skills/py

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/py.
