# Testing Gotchas

Accumulated from real testing failures.

| What happened | Rule |
|---------------|------|
| Recommended Jest for a Go project | Check package manager first; match framework to language |
| Used mocks for database tests, missed SQL syntax errors in production | Integration tests must use real databases (testcontainers or transaction rollback) |
| 50+ snapshot tests to update on every change | Only snapshot stable outputs; frequently changing components aren't snapshot candidates |
| Flaky CI tests passing locally every time | Check time dependencies, test ordering, timezone/locale |
| E2E suite taking 30 minutes | E2E covers 3-10 critical flows, not 100+ |
| 95% coverage but production bugs still appear | Coverage ≠ correctness; check for actual assertions on boundary conditions |
| Mocked everything, tests stayed green after breaking implementation | Mocks verify calls, not outcomes. Test results, not interactions |
| Test files everywhere but no conftest.py | Shared fixtures go in conftest.py; avoid copy-paste |
| `datetime.now()` breaking tests at midnight | Freeze time: `freezegun` (Python), `jest.useFakeTimers()` (JS) |
| test_b depends on data test_a created | Every test must be independent: setup → execute → assert → teardown |
| Integration tests in pre-commit hook | Pre-commit: fast unit tests only. Integration/E2E: CI |
| Skipped input validation states in E2E plan | Every form field has validation behaviors — investigate all of them |
| Missed empty/error/loading states in test plan | Every UI element has 3+ states. Happy path is the minimum |
| `--watchAll` in CI script | CI needs `--ci` mode; `--watchAll` hangs forever |
| Recommended Playwright for a CLI tool | CLI tools test input/output; no browser needed |
| Test asserts on a surface production never runs | Ensure the test entry point matches what users actually reach |
| Refactoring without confirming test coverage exists | Read existing tests before refactoring; add characterization tests first |
