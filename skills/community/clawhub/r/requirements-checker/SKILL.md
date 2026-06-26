---
name: requirements-checker
description: Validate, lint, and sort Python requirements.txt files for best practices and CI.
version: 1.0.0
---

# requirements-checker

Validate, lint, sort, and compare Python `requirements.txt` files. Pure stdlib — no external dependencies required.

## Validate

Check a requirements file for format errors, invalid specifiers, duplicates, and problematic patterns.

```bash
python3 scripts/requirements-checker.py validate requirements.txt

# JSON output for automation
python3 scripts/requirements-checker.py validate requirements.txt --format json

# Strict mode — exit 1 on any issue (CI)
python3 scripts/requirements-checker.py validate requirements.txt --strict
```

## Lint

All validation checks plus best-practice rules: unpinned deps, missing upper bounds, VCS deps, non-alphabetical order, mixed operator styles.

```bash
python3 scripts/requirements-checker.py lint requirements.txt

# Markdown output (for PR comments, reports)
python3 scripts/requirements-checker.py lint requirements.txt --format markdown

# Strict mode — exit 1 on warnings too
python3 scripts/requirements-checker.py lint requirements.txt --strict

# Ignore specific rules
python3 scripts/requirements-checker.py lint requirements.txt --ignore unpinned --ignore no-upper-bound
```

## Duplicates

Find packages listed more than once (case-insensitive, PEP 503 normalised).

```bash
python3 scripts/requirements-checker.py duplicates requirements.txt

python3 scripts/requirements-checker.py duplicates requirements.txt --format json
```

## Sort

Sort requirements alphabetically. By default writes to stdout; use `--write` to update the file in-place.

```bash
# Preview sorted output
python3 scripts/requirements-checker.py sort requirements.txt

# Write sorted file in-place
python3 scripts/requirements-checker.py sort requirements.txt --write
```

## Compare

Diff two requirements files — shows added, removed, and changed packages with version changes.

```bash
python3 scripts/requirements-checker.py compare requirements.txt requirements-new.txt

python3 scripts/requirements-checker.py compare base.txt updated.txt --format markdown
```

## Global Options

| Option | Description |
|--------|-------------|
| `--format text\|json\|markdown` | Output format (default: `text`) |
| `--strict` | Exit code 1 on any issue, including warnings/info (CI mode) |
| `--ignore RULE` | Ignore a named rule; repeatable |

## Validation Checks

| Rule | Severity | Description |
|------|----------|-------------|
| `invalid-format` | error | Line doesn't match PEP 508 |
| `invalid-specifier` | error | Unknown operator or unparseable version spec |
| `duplicate-package` | error | Same package name appears more than once |
| `editable-install` | warning | `-e` editable installs in production requirements |
| `vcs-dependency` | warning | `git+`, `hg+`, `svn+`, `bzr+` URL dependencies |
| `custom-index-url` | warning | `--index-url` / `--extra-index-url` present |
| `url-dependency` | info | Direct URL dependencies |
| `requirement-include` | info | `-r` nested includes |
| `trailing-whitespace` | info | Line has trailing spaces or tabs |
| `whitespace-only-line` | info | Line contains only whitespace |
| `missing-final-newline` | info | File doesn't end with newline |

## Lint Rules (in addition to validation)

| Rule | Severity | Description |
|------|----------|-------------|
| `unpinned` | warning | Dependency has no version specifier |
| `no-upper-bound` | warning | `>=` used without a `<` / `<=` upper bound |
| `non-alphabetical` | warning | Packages are not in alphabetical order |
| `mixed-operators` | info | File mixes `==` exact pins and `>=` range specifiers |

## Example Output

```
File: requirements.txt
  [ERROR] line 4  (duplicate-package)  Duplicate package 'requests' (first seen on line 2)
           requests==2.31.0
  [WARNING] line 7  (no-upper-bound)  'django' uses >= without an upper bound
           django>=4.0
  [WARNING] line 1  (non-alphabetical)  'zope' is out of alphabetical order
           zope==5.0

Summary: 3 issue(s) — 1 error(s), 2 warning(s), 0 info(s)
```
