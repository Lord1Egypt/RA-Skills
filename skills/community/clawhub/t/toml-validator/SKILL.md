---
name: toml-validator
description: Validate, lint, diff, and inspect TOML configuration files. Use when asked to check TOML syntax, compare TOML configs, show TOML structure, validate pyproject.toml or Cargo.toml, or lint TOML files. Triggers on "TOML", "toml validate", "pyproject.toml", "Cargo.toml", "TOML syntax", "TOML diff", "config file validation".
---

# TOML Validator & Linter

Validate TOML syntax, run lint checks, compare files, and inspect structure. Supports pyproject.toml, Cargo.toml, and any TOML config.

## Validate

```bash
# Basic syntax check
python3 scripts/toml_lint.py validate config.toml

# With lint checks (empty values, mixed arrays, etc.)
python3 scripts/toml_lint.py validate --lint pyproject.toml Cargo.toml
```

## Diff Two Files

```bash
python3 scripts/toml_lint.py diff config-prod.toml config-staging.toml
```

## Show Contents / Extract Key

```bash
# Pretty-print entire file
python3 scripts/toml_lint.py show pyproject.toml

# Extract specific key
python3 scripts/toml_lint.py show pyproject.toml --key tool.poetry.version
```

## Type Tree

```bash
python3 scripts/toml_lint.py types Cargo.toml
```

## Output Formats

```bash
python3 scripts/toml_lint.py -f json validate config.toml
python3 scripts/toml_lint.py -f markdown diff a.toml b.toml
```

## Lint Checks

| Check | Level | Description |
|-------|-------|-------------|
| Empty strings | Warning | String values that are blank |
| Empty tables | Warning | Tables with no keys |
| Mixed-type arrays | Warning | Arrays containing different types |
| Empty arrays | Info | Arrays with no elements |
| Spaced keys | Info | Keys containing spaces (valid but unusual) |
| Long strings | Info | String values exceeding 1000 chars |

## Requirements

- Python 3.11+ (has `tomllib` in stdlib)
- Or: `pip install tomli` for Python 3.10 and below
