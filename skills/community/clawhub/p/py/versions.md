# Python Versions — Choosing, Upgrading, Surviving Removals

One minor release per year, in October; each gets 2 years of bugfixes and 3 more of security fixes, so a version is supported for 5 years from release.

## Which Version To Target

| Role | Choose |
|---|---|
| New application | The newest release that all your wheels support — in the first months after an October release that is usually the previous one, because C-extension wheels lag |
| Library | Support the oldest version still in security support, declare it in `requires-python`, and test the floor and the ceiling in CI |
| Existing service | Whatever it runs on, until the EOL date is within a year — then plan the upgrade as work, not as a chore |
| Anything the OS depends on | Not the system interpreter. Ever (PEP 668, `packaging.md`) |

End of support: 3.9 ended in October 2025; 3.10 ends October 2026, 3.11 in 2027, 3.12 in 2028, 3.13 in 2029, 3.14 in 2030. Past EOL there are no security patches — an unsupported interpreter is a standing finding, not a preference.

## The Upgrade Procedure

1. On the CURRENT version, run the test suite with `-W error::DeprecationWarning`. Everything the next release removes has been warning for at least one cycle; this converts a future outage into a list of files today.
2. Read the "Porting to Python 3.x" section of each intermediate What's New — not the highlights, the porting section. It is exhaustive and short.
3. Fresh venv on the new interpreter, reinstall from the lockfile. Failures here are wheels, not your code (`packaging.md`).
4. Run the suite. Then run the application with `-X dev` for a day (`debugging.md`).
5. Only then bump `requires-python`, the CI matrix, the container base image, and the pinned interpreter — in that order, one commit.

Roll back by pointing at the old interpreter, which is why step 3 uses a NEW venv rather than upgrading the existing one.

## What Each Release Removed Or Broke

| Version | What bites |
|---|---|
| 3.10 | `collections.Mapping` aliases finally gone (moved to `collections.abc` long before); stricter pattern-matching-era parser errors |
| 3.11 | int↔str conversion capped at 4300 digits (CVE-2020-10735, raise it with `sys.set_int_max_str_digits`); `inspect.getargspec` and `asyncio.coroutine` removed |
| 3.12 | `distutils` removed (PEP 632) — old `setup.py` scripts fail with `ModuleNotFoundError: No module named 'distutils'`; `imp` removed; `unittest` aliases (`assertEquals`, `failUnless`) removed; `ssl.wrap_socket` removed; `datetime.utcnow()`/`utcfromtimestamp()` deprecated (`datetime.md`); `asyncio.get_event_loop()` warns when no loop is running |
| 3.13 | The PEP 594 "dead batteries" are gone: `cgi`, `telnetlib`, `nntplib`, `imghdr`, `pipes`, `crypt` and friends — imports fail outright; `locals()` semantics tightened (PEP 667) |
| 3.14 | `multiprocessing` on Linux defaults to `forkserver` instead of `fork`, changing what children inherit (`concurrency.md`); annotations are evaluated lazily (PEP 649); `return`/`break`/`continue` inside `finally` now warns (PEP 765, `functions.md`) |

Deprecations to fix before they become removals: `pkg_resources` (use `importlib.metadata`/`importlib.resources`), `datetime.utcnow`, `typing.List`/`Dict`/`Optional` in favor of builtin generics and `|`, and `asyncio.get_event_loop()` outside a running loop.

## What You Get For Upgrading

- 3.11: roughly 1.25× faster than 3.10 on pyperformance (python.org release notes) with no code change, plus tracebacks that point at the exact sub-expression — the cheapest performance work available (`performance.md`).
- 3.11: `ExceptionGroup`/`except*`, `asyncio.TaskGroup`, `tomllib`, `Self`, `StrEnum`, `contextlib.chdir`.
- 3.12: PEP 695 generics (`def f[T]()`), `@override`, `itertools.batched`, clearer error messages, per-interpreter GIL groundwork.
- 3.13: a usable REPL (multiline editing, colors), better error messages, and the experimental free-threaded build.
- 3.14: free-threading supported as a build rather than an experiment; template strings; lazy annotations.

Free-threaded CPython is a SEPARATE binary and most C extensions are not ready for it. Treat it as an evaluation target, never as the default for production (`concurrency.md`).

## Running Several Versions

- `uv python install 3.12` or `pyenv install 3.12` to keep interpreters side by side; create each venv with the explicit binary: `python3.12 -m venv .venv`.
- A venv hard-codes the interpreter path, so upgrading the Python it was built from (a Homebrew or pyenv update) breaks it: `No module named encodings`, or a `python` that no longer exists. Delete and recreate — never patch `pyvenv.cfg` (`packaging.md`).
- Test a matrix with `tox` or `nox`. Testing the floor and the ceiling catches nearly everything; middle versions rarely fail alone.
- Docker: pin the full version (`python:3.12.7-slim`), not `python:3` — a base image that follows the latest tag upgrades your interpreter on a rebuild you did not intend. Container specifics: the `docker` skill (https://clawic.com/skills/docker).

## Feature Floors

Which syntax and stdlib features exist in which version: SKILL.md Version Floors. Floors that gate one specific instruction — a changed default, a new keyword argument, a deprecation — live inline next to that instruction in each guide, in the same `python >=X.Y` form.
