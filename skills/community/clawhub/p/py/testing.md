# Testing Traps

## Mocking
- Patch where the name is USED, not where it is defined: `views.py` does `from utils import now` → `mock.patch('app.views.now')`, not `'app.utils.now'`. The `from`-import copied the binding at import time; patching the origin changes an object nobody reads (`imports.md`).
- A plain `Mock` accepts ANY attribute: `m.called_once()` (missing `assert_` prefix) returns a truthy Mock and the test passes while asserting nothing. Mock guards misspellings starting with `assert`/`assret` (raises AttributeError), but not this one. Defense: `autospec=True` everywhere — it also fails the test when the real signature drifts, which plain Mock lets refactors slip past.
- Mock state persists across a test if shared (module-level mock, class-scoped patch): call counts accumulate and test B passes because test A ran. Prefer function-scoped `mock.patch` as decorator/context manager; `reset_mock()` is the last resort, not the design.
- `datetime.datetime` is a C type — you cannot patch `.now` on it. Patch the module reference where used (`mock.patch('app.views.datetime')`) or, better, inject a clock function so tests pass a fake (`datetime.md`).
- Mock at process boundaries (HTTP, clock, filesystem, queue) and use a FAKE — a small real implementation, like an in-memory repository — for anything you own. A mock asserts that your code called a function; a fake asserts that the behavior is right, and it survives refactors.
- Every mock is a duplicated assumption about someone else's API. Contract-test the boundary occasionally against the real thing, or the suite goes green while production is broken.

## Pytest essentials
- Discovery: files named `test_*.py` (or `*_test.py`), functions `test_*`, classes `Test*` WITHOUT an `__init__`. "collected 0 items" is always one of these four (`debugging.md`).
- `pytest.raises(Exception)` proves almost nothing — any bug raises something. Always the narrowest exception plus `match="..."` (regex) so the wrong error at the right place still fails.
- Fixture scope: `function` (default) rebuilds per test; `module`/`session` share ONE object — a mutable session fixture creates order-dependent tests that fail only in full runs. Session scope is for expensive immutable setup (DB schema, compiled artifacts) only.
- Fixture teardown belongs after `yield` in the fixture body — code after `return` never runs, and teardown after a failed test runs only with the yield pattern.
- `tmp_path` gives each test its own directory; `monkeypatch` (`setattr`, `setenv`, `delenv`, `chdir`, `syspath_prepend`) undoes itself at teardown — both beat hand-rolled setup that leaks when a test fails. Environment variables set with `os.environ[...] = ` and never restored are a classic cross-test leak.
- `autouse=True` fixtures apply invisibly to every test in scope; they are right for global isolation (a clean tmp cwd) and wrong for anything a reader needs to know about.
- `conftest.py` shares fixtures down its directory tree — one at the project root plus one per suite, never a chain of five.
- Float assertions: `assert total == 0.3` fails on binary float arithmetic; use `pytest.approx(0.3)` — default relative tolerance 1e-6 (`types.md`).
- An `async def` test without a plugin is not executed — pytest warns and the assertions never run, which reads as green in a quick scan. Install `pytest-asyncio` and mark tests (or set `asyncio_mode = auto`).
- Parametrize over copy-pasted test functions once you have 3+ input/expected pairs — `@pytest.mark.parametrize` with `ids=` makes each case its own failure line, and `pytest.param(..., marks=pytest.mark.xfail)` marks the known-broken one without deleting it.

## Configuration worth setting once

```toml
[tool.pytest.ini_options]
addopts = "-q --strict-markers --strict-config"
testpaths = ["tests"]
filterwarnings = ["error::DeprecationWarning"]   # upgrades stop being surprises (versions.md)
```

`--strict-markers` turns a typo'd `@pytest.mark.slwo` into an error instead of a silently ignored marker.

## Flaky Tests — Find The Shared State

Rerunning until green is not a fix. In order of frequency:

| Cause | Check |
|---|---|
| Order dependence | Run the failing test alone, then run the suite with a shuffled order (`pytest-randomly`). Passing alone and failing together means shared state |
| Module-level or session-scoped mutable state | A cache, a registry, a configured client, a mock (`functions.md`) |
| Real time | `time.sleep` races, timeouts near the threshold, midnight and month boundaries — inject a clock or freeze it |
| Timezone and locale | The suite runs on a laptop in one zone and CI in UTC (`datetime.md`) |
| Iteration order | `PYTHONHASHSEED` changes set ordering per run (`collections.md`) |
| Network or filesystem | A test that quietly hits the internet or writes outside `tmp_path` |
| Concurrency | Threads or asyncio in the code under test with no synchronization point (`concurrency.md`) |

## Semantics and Discipline
- `assert` disappears under `python -O` — never use it for runtime validation in production code (raise explicitly). In tests it is fine: pytest rewrites asserts and does not run optimized.
- A test you never saw fail proves nothing: run the failing test BEFORE writing the fix; red→green is the evidence the test guards the bug. Workflow: `pytest -x --lf` reruns last failures first.
- One behavior per test, named after the behavior (`test_refund_rejects_expired_charge`), so the failure line alone tells you what broke.
- Test the contract, not the implementation: asserting on a formatted log line or on the number of internal calls breaks on every refactor and catches nothing (`logging.md`).
- Coverage is a floor, not a goal: it shows which lines never ran, not which behaviors are verified. Branch coverage is worth more than line coverage; chasing 100% produces tests written to touch lines.
- Parsers, serializers, and anything with a round-trip invariant are where property-based testing (hypothesis) earns its keep: it finds the empty string, the surrogate pair, and the `-0.0` you would not have written.
- `pytest --durations=10` names the slow tests; a suite nobody waits for is a suite nobody runs.
