---
name: vitest-config-validator
description: Validate vitest.config.ts/js and vitest workspace configurations for syntax, deprecated options, plugin conflicts, and best practices. Use when validating Vitest test runner configs, auditing test setups, or linting vitest.config files.
---

# Vitest Config Validator

Validate `vitest.config.ts` and `vitest.config.js` files for syntax errors, deprecated options, plugin conflicts, and best practices. Parses config files as text using regex patterns — no JS execution required.

## Commands

```bash
# Full validation (all rules)
python3 scripts/vitest_config_validator.py validate vitest.config.ts

# Quick syntax-only check (structure rules only)
python3 scripts/vitest_config_validator.py check vitest.config.ts

# Explain config in human-readable form
python3 scripts/vitest_config_validator.py explain vitest.config.ts

# Suggest improvements
python3 scripts/vitest_config_validator.py suggest vitest.config.ts

# JSON output
python3 scripts/vitest_config_validator.py validate vitest.config.ts --format json

# One-line PASS/WARN/FAIL summary
python3 scripts/vitest_config_validator.py validate vitest.config.ts --format summary

# Strict mode (warnings become errors)
python3 scripts/vitest_config_validator.py validate vitest.config.ts --strict
```

## Rules (22)

| # | Category | Severity | Rule |
|---|----------|----------|------|
| S1 | Structure | E | File not found or unreadable |
| S2 | Structure | E | Empty config or no defineConfig call |
| S3 | Structure | W | No default export found |
| S4 | Structure | W | Both vitest.config and vite.config with test section detected |
| S5 | Structure | W | Unknown top-level config keys |
| T1 | Test Settings | E | Invalid test environment (must be jsdom/happy-dom/node/edge-runtime) |
| T2 | Test Settings | W | Empty include or exclude patterns |
| T3 | Test Settings | E | Invalid glob pattern in include/exclude |
| T4 | Test Settings | I | Coverage provider not set (recommend c8/v8/istanbul) |
| T5 | Test Settings | W | testTimeout set unreasonably high (>60000ms) or low (<100ms) |
| P1 | Performance | W | singleThread: true used with forks pool (disables parallelism) |
| P2 | Performance | W | isolate: false without comment (risky for test isolation) |
| P3 | Performance | I | No pool configuration (defaults may not be optimal) |
| P4 | Performance | W | globals: true without type declaration reference |
| C1 | Compatibility | W | Deprecated option used |
| C2 | Compatibility | W | css.modules without css.include (potential miss) |
| C3 | Compatibility | W | deps.inline and deps.external conflict |
| B1 | Best Practices | I | No reporter configured |
| B2 | Best Practices | I | Missing coverage configuration |
| B3 | Best Practices | W | setupFiles references potentially non-existent pattern |
| B4 | Best Practices | I | snapshotFormat not explicitly configured |
| B5 | Best Practices | I | passWithNoTests not set (CI may fail on empty test suite) |

## Output Formats

- **text** (default): Human-readable with `[E]`/`[W]`/`[I]` severity prefix
- **json**: Machine-readable structured output
- **summary**: Single-line `PASS` / `WARN` / `FAIL`

## Exit Codes

- `0` — No errors
- `1` — Errors found (or warnings in `--strict` mode)
- `2` — File not found or parse error
