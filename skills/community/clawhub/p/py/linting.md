# Formatting and Linting — One Formatter, One Linter, Both In CI

Formatting is a solved problem the moment a tool owns it: the only wrong answer is a human arguing about it in review. Linting is different work — it finds bugs, not layout — and it is the one that needs a ratchet.

## The Split

| Job | Tool | What it must never do |
|---|---|---|
| Layout: line breaks, quotes, trailing commas | `ruff format` or `black` (compatible output; ruff is the same rules, much faster) | Change behavior. A formatter diff that alters semantics is a bug report |
| Import order and grouping | `ruff` rule set `I` (isort rules, built in) | Live in a second tool with a second config |
| Bug patterns and dead code | `ruff check` (`F`, `B`, `SIM`, `RUF`) | Overlap with the formatter — the formatter owns `E501` |
| Types | mypy or pyright (`type-checking.md`) | Be replaced by lint rules; they check different things |
| Security patterns | `ruff` rule set `S` (bandit rules) — `security.md` for what they mean | Be the only control; most of `security.md` is invisible to a linter |
| Anything else | `ruff check` with the starter set below | Grow by `--select ALL` |

## Config — One File

```toml
[tool.ruff]
line-length = 88            # matches the line_length variable; the formatter enforces it
target-version = "py311"    # matches requires-python; drives the UP rules

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]
ignore = ["E501"]           # the formatter owns line length; the linter re-flagging it is noise

[tool.ruff.lint.isort]
known-first-party = ["myapp"]   # without this, a src/ layout scatters your own imports (packaging.md)
```

- `F` (pyflakes) and `B` (bugbear) are where real defects live: `F821` undefined name, `F841` unused assignment that was meant to be a return, `B006` mutable default argument (Core Rule 1), `B008` function call evaluated once in a default, `B905` `zip()` without `strict=`.
- `UP` rewrites to the syntax your `target-version` supports and is the cheapest way to retire `typing.List` and `%`-formatting across a codebase.
- `target-version` set below your real floor silently disables rules; set above it emits syntax your interpreter cannot parse. Keep it equal to `requires-python` (`packaging.md`).
- `select = ["ALL"]` is the same mistake as `mypy --strict` on day one: thousands of findings, a week of churn, and a revert. Add rule families one at a time, each in its own commit (`type-checking.md`).
- `D` (docstring style) needs a convention chosen (`[tool.ruff.lint.pydocstyle] convention = "google"`) and is the rule family most likely to be enabled and then blanket-ignored. Enable it for new packages, not for a legacy tree.

## Adoption Without A Week Of Churn

1. Run the formatter over the whole tree in ONE commit that changes nothing else.
2. Record that commit's hash in `.git-blame-ignore-revs` and set `git config blame.ignoreRevsFile .git-blame-ignore-revs`. Without it, every line in the repository is now blamed on the reformat and `git blame` stops being useful — the single most common regret of adopting a formatter.
3. Turn the linter on with the starter set, `--fix` the mechanical families (`I`, `UP`), and read the diff before committing it.
4. Whatever is left goes into `per-file-ignores` or a narrow `ignore` list with a comment naming the plan, not a blanket suppression.
5. Only then gate CI.

## Suppressions

- `# noqa: B006` with the code, never bare `# noqa` — a bare one also silences the next rule that fires on that line, exactly like a bare `# type: ignore` (`type-checking.md`).
- Enable `RUF100` to make an unused `noqa` an error; otherwise suppressions accumulate for years past the bug they hid.
- `# ruff: noqa` at the top of a file disables the file entirely. That is a decision to stop linting a module, so it belongs in `per-file-ignores` where it is visible, not in the file where nobody looks.
- Autofix on save is fine for imports and formatting; `--unsafe-fixes` changes behavior by design and belongs in a reviewed diff, never in an editor hook.

## Pre-commit And CI

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: ""          # pin an exact tag; an unpinned hook updates under you and fails everyone's commit
    hooks:
      - id: ruff-format
      - id: ruff
        args: [--fix]
```

- Hooks run on STAGED files only, so a rule that fires elsewhere passes locally and fails in CI. `pre-commit run --all-files` when adopting and after every rule change.
- CI runs check-only (`ruff format --check`, `ruff check`) and never rewrites the branch: a CI job that pushes formatting commits fights with the developer's own push and produces merge conflicts nobody caused.
- Pin the same tool version in the hook and in the dev dependencies. A version skew means CI rejects what your machine just formatted, which teaches people to skip the hook.
- `pre-commit autoupdate` on a schedule, in its own PR, with `--all-files` run once — never as a drive-by in a feature branch.
- `--no-verify` exists; a team that uses it routinely has a hook that is too slow or too noisy, and the fix is the hook, not the discipline.

## What Linting Does Not Buy You

- Correctness. A fully clean lint run says nothing about whether the function returns the right answer (`testing.md`).
- Naming that means something, an API worth using, or the right abstraction — the only review comments actually worth a human's time once formatting is automated.
- Cross-module dead code: ruff sees one file at a time. `vulture` or coverage from the test suite finds the rest.
- Dependency hygiene and known CVEs: `pip-audit` and lockfile discipline are separate gates (`packaging.md`).
