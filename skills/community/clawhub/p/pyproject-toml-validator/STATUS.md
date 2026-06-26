# pyproject-toml-validator — STATUS

**Status:** Built, tested, ready to publish.

**Price:** $59

**Category:** Python, packaging, code quality, linters

## Built
- [x] Script: `scripts/pyproject_validator.py` (pure Python stdlib, ~400 lines)
- [x] SKILL.md with commands, rules, formats, exit codes, examples
- [x] 30+ rules across 4 categories (project, dependencies, build-system, tool sections)
- [x] Tool-specific validation: ruff, mypy, pytest, black, isort
- [x] 3 output formats (text, json, summary)
- [x] CI-friendly exit codes and --min-severity filter
- [x] Tested with valid and intentionally-broken pyproject.toml files

## Market fit
- ZERO competition on ClawHub for dedicated pyproject.toml validation
- Generic toml-validator exists (ours) but doesn't understand PEP 517/621 semantics
- Every modern Python project uses pyproject.toml
