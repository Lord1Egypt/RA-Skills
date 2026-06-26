# pyproject-toml-validator

Validate `pyproject.toml` files for Python projects against PEP 517/621 standards.

## What it does

Checks your `pyproject.toml` for common mistakes across three areas:

- **[project]** — name format (PEP 508), version, license (SPDX), classifiers, dependency specs, authors, dynamic fields
- **[build-system]** — requires, build-backend validation, known backends
- **[tool.*]** — ruff, mypy, pytest, black, isort section validation with tool-specific rules

### Rules (30+)

| Category | Rules | Examples |
|----------|-------|---------|
| Project metadata (10) | Missing name/version, invalid name format, unknown fields, malformed requires-python, unknown classifiers, empty authors, name in dynamic | `name = "My Package!"` → invalid PEP 508 name |
| Dependencies (4) | Duplicate deps, unpinned deps, overlapping optional groups | `requests` and `Requests` both listed |
| Build system (4) | Missing requires/build-backend, empty requires, unknown fields | No `[build-system]` table |
| Tool sections (12+) | Ruff select/ignore overlap, mypy type mismatches, black/ruff conflict, isort/ruff conflict, unusual line lengths, invalid target versions | `[tool.ruff.lint] select = ["E501"]` + `ignore = ["E501"]` |

### Output formats

- **text** — human-readable with severity icons (❌ ⚠️ ℹ️)
- **json** — structured with summary counts
- **summary** — one-line PASS/WARN/FAIL

### Exit codes

- `0` — no errors (warnings/info allowed)
- `1` — errors found (or `--strict` with any issue)
- `2` — file not found or parse error

## Commands

### validate

Full validation of all sections.

```bash
python3 scripts/pyproject_validator.py validate pyproject.toml
python3 scripts/pyproject_validator.py validate --format json pyproject.toml
python3 scripts/pyproject_validator.py validate --strict pyproject.toml
```

### project

Validate only the `[project]` table.

```bash
python3 scripts/pyproject_validator.py project pyproject.toml
```

### build

Validate only `[build-system]`.

```bash
python3 scripts/pyproject_validator.py build pyproject.toml
```

### tools

Validate only `[tool.*]` sections (ruff, mypy, pytest, black, isort).

```bash
python3 scripts/pyproject_validator.py tools --min-severity warning pyproject.toml
```

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--format` | text, json, summary | text | Output format |
| `--min-severity` | error, warning, info | info | Filter by minimum severity |
| `--strict` | flag | off | Exit 1 on any issue |

## Requirements

- Python 3.11+ (uses `tomllib` from stdlib)
- Falls back to built-in simple TOML parser on Python 3.10

## Examples

```bash
# Quick check
python3 scripts/pyproject_validator.py validate pyproject.toml

# CI pipeline
python3 scripts/pyproject_validator.py validate --strict --format summary pyproject.toml

# Check only tool configs
python3 scripts/pyproject_validator.py tools --format json pyproject.toml

# Filter noise
python3 scripts/pyproject_validator.py validate --min-severity warning pyproject.toml
```
