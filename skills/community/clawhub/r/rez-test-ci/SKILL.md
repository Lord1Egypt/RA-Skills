---
name: rez-test-ci
description: "Declaring and running tests from a package definition — the `tests` attribute and its `command` / `requires` / `run_on` / `on_variants` fields, why a bare `rez-test` runs only tests tagged `default`, every `rez-test` flag, how the exit code is derived, and how to drive package tests from CI. Use when a package needs tests, when `rez-test` runs fewer tests than you declared, or when you are wiring rez package tests into a pipeline. Covers Rez 3.4.0."
---

# Rez package tests and CI

> **One-sentence summary**: tests live in the `tests` dict of `package.py` and run through
> `rez-test`, which resolves a **separate environment per test** from that test's own `requires` —
> so a test is a resolve, not just a command.

Skill scope: **declaring, running and automating package tests**. For the rest of the
build/release/test loop and the other commands' flags see `rez-cli`; for the `package.py` attributes
in general and `@early`/`@late` on `tests` see `rez-package-definition`; for the mistakes that make a
`package.py` fail to load see `rez-package-pitfalls`; for driving tests from Python see
`rez-python-api`.

## Declaring tests

`tests` is a dict mapping a test name to either a command, a list of commands, or a dict:

```python
name = "toolcheck"
version = "1.0.0"
tools = ["toolcheck"]

tests = {
    # shorthand: a command string
    "unit": "python -c \"import sys; sys.exit(0)\"",

    # or a list of commands
    "lint": ["python -m compileall -q python"],

    # full form
    "integration": {
        "command": "python -m pytest {root}/tests",
        "requires": ["pytest"],
        "run_on": ["pre_release"],
        "on_variants": {
            "type": "requires",
            "value": ["python-3"],
        },
    },
}
```

| Field | Meaning |
|---|---|
| `command` | the command, or a list of them; run inside the test's own environment |
| `requires` | extra request added to the test environment |
| `run_on` | a tag or list of tags; a test with no tag is `default` |
| `on_variants` | `True` to run on every variant, or `{"type": "requires", "value": [...]}` to run only on variants matching a request |

`tests` may be an `@early()` or `@late()` function, which is how a package can declare different
tests per variant.

Command strings automatically expand references such as `{root}`, so a test can reach files inside
its own package without hard-coding a path:

```python
tests = {
    "unit": "python -m unittest -s {root}/tests",
}
```

The command otherwise runs as an ordinary shell command in the test environment. Use `{root}` in
preference to an absolute path — a test that hard-codes a repository location breaks the moment the
package is released somewhere else.

## Running tests

```bash
rez-test toolcheck                # every test tagged 'default'
rez-test toolcheck unit           # one named test
rez-test toolcheck -l             # list every test, including non-default ones
rez-test toolcheck --dry-run      # show what would run, run nothing
rez-test toolcheck -s             # stop at the first failure
```

### A bare `rez-test` runs only `default` tests

This is the single most common surprise. Without a test name, `rez-test` selects tests whose
`run_on` tags include `default` — and a test declares no `run_on` at all **is** `default`. Anything
tagged otherwise, such as `run_on: ["pre_release"]`, is skipped.

So given a package with `unit`, `failing` and a `pre_release`-tagged `integration`:

```text
$ rez-test toolcheck -l
failing
integration
unit

$ rez-test toolcheck
1 succeeded, 1 failed, 0 skipped
```

`integration` is listed but never run. To run it, name it:

```bash
rez-test toolcheck integration
```

### Output and exit code

Every run ends with a summary table:

```text
Test results:
--------------------------------------------------------------------------------
1 succeeded, 1 failed, 0 skipped

Test     Status   Variant                          Description
----     ------   -------                          -----------
failing  failed   /packages/toolcheck/1.0.0        Test failed with exit code 3
unit     success  /packages/toolcheck/1.0.0        Test succeeded
```

The exit code is the exit code of the **first** test that failed, or `0` if none did. A test that
could not run at all — its environment would not resolve — yields `-1`. That is all a CI job needs:
a non-zero exit is a failure, and the exit code may be the test's own.

`--dry-run` reports each test as `skipped` with the description `Dry run mode`, and exits `0`. Use
it to check which tests *would* run before you trust a CI job's coverage.

Extra arguments after a single named test are passed through to that test's command, which is how you
forward flags to the tool a test wraps:

```bash
rez-test toolcheck unit -- --verbose
```

The `--` is **required**. Without it the arguments are consumed and the test command receives
nothing at all — silently, with the test still passing. Forwarding a flag to the tool a test wraps
therefore always needs the separator, and the flags behind it must not be `rez-test` flags you
also meant to set.

You can only pass extra arguments to **one** named test; naming two is a parser error.

### Flags

| Flag | Effect |
|---|---|
| `-l, --list` | list the package's tests and exit |
| `--dry-run` | show what would run without running it |
| `-s, --stop-on-fail` | stop on the first failure |
| `--inplace` | run in the **current** environment; tests whose requirements are unmet are skipped |
| `--extra-packages PKG ...` | add requests to every test environment |
| `--paths PATHS` | override the package search path |
| `--nl, --no-local` | ignore `local_packages_path` |
| `-v, --verbose` | verbose, repeatable |

`--inplace` is mutually exclusive with `--extra-packages`, `--paths` and `--no-local`:

```text
rez test: error: Cannot use --inplace in combination with --extra-packages/--paths/--no-local
```

`--inplace` also needs an active rez context — outside one it fails on a missing current package, so
it belongs inside a `rez-env`, not in a fresh CI shell.

A package with no tests is not an error. `rez-test` prints `No tests found in <uri>` to stderr and
exits `0`. If your CI must fail when a package declares no tests, check with `-l` and assert on the
output yourself.

## Wiring into CI

The pattern that works on every CI provider: make the runner rez-aware once, then run `rez-test` as
an ordinary command. Rez only needs to be on `PATH` and the package repository reachable.

```bash
python -m pip install "rez==3.4.0"
export REZ_PACKAGES_PATH=/path/to/packages
rez-test toolcheck unit
rez-test toolcheck integration
```

Name the tests you want rather than relying on the default tag — an explicit list is self-documenting
and cannot silently lose coverage when someone adds a `run_on` tag later.

A minimal GitHub Actions job:

```yaml
jobs:
  rez-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install rez
        run: python -m pip install "rez==3.4.0"
      - name: Build and install the package
        run: rez-build --install
      - name: Run package tests
        run: |
          rez-test toolcheck unit
          rez-test toolcheck integration
```

Build before you test. `rez-test` reads an **installed** package from the package path, so a package
that has only been edited and not built is invisible to it. Verify visibility first when a CI job
cannot find a package:

```bash
rez-search toolcheck
```

### Making CI reflect what the package declares

Because a bare `rez-test` skips non-default tests, a job that runs `rez-test <pkg>` alone will
happily report success while running a subset. Prefer enumerating tests, and gate the set in one
place so it cannot drift:

```bash
rez-test toolcheck -l          # what exists
rez-test toolcheck --dry-run   # what a bare run would do
```

Compare the two when a tag is added. The gap between them is exactly the coverage a bare run would
silently drop.

## Troubleshooting

| Symptom | Cause |
|---|---|
| Fewer tests ran than `-l` lists | a bare run only runs `default`-tagged tests; name them |
| `No tests found in <uri>` | the package declares none, **or** `rez-test` is reading a different installed copy than you edited |
| Test cannot find the package's files | the command runs in a fresh environment; paths must resolve there |
| `Cannot use --inplace in combination with ...` | `--inplace` excludes `--extra-packages` / `--paths` / `--no-local` |
| `--inplace` fails outside a context | it needs an active rez context; wrap it in `rez-env` |
| `You can only pass extra arguments to a single, specified test` | extra args are allowed for exactly one named test |
| A test ignores the arguments I passed it | the `--` separator is missing, so they were swallowed and the test still passed |
| Exit code is an odd number like `3` | that is the failing test's own exit code, passed through |
| CI cannot see the package | it was not built and installed; check `rez-search` |
| A test's dependency is missing | add it to the test's own `requires`, not the package's |

## Agent workflow

1. Confirm the package is installed and visible first: `rez-search <pkg>`.
2. List what exists with `rez-test <pkg> -l`, then check what a bare run would do with `--dry-run`.
3. Run named tests rather than relying on the default tag, so coverage cannot drift silently.
4. Read the summary table and the exit code — non-zero is the first failing test's own code.
5. Tag slow or release-only tests with `run_on` deliberately, and enumerate them in CI so the tag
   never removes coverage by accident.
6. Reach for `--inplace` only inside an active `rez-env`; in CI prefer a normal resolved environment.
