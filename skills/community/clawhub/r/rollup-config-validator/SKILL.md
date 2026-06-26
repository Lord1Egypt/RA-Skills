---
name: rollup-config-validator
description: Validate Rollup config files (rollup.config.js/mjs/ts) for output format conflicts, plugin ordering issues, deprecated options, and best practices. Use when validating Rollup bundler configs, auditing build pipelines, migrating Rollup versions, or linting rollup config files.
---

# Rollup Config Validator

Validate Rollup config files (exported JSON or parsed config objects) for output format conflicts, external/bundle mismatches, plugin ordering issues, deprecated options, treeshake settings, and best practices. Supports text, JSON, and summary output formats with CI-friendly exit codes.

## Commands

```bash
# Full validation (all 22+ rules)
python3 scripts/rollup_config_validator.py validate rollup.config.json

# Quick syntax-only check (structure rules only)
python3 scripts/rollup_config_validator.py check rollup.config.json

# Explain config in human-readable form
python3 scripts/rollup_config_validator.py explain rollup.config.json

# Suggest improvements
python3 scripts/rollup_config_validator.py suggest rollup.config.json

# JSON output (CI-friendly)
python3 scripts/rollup_config_validator.py validate rollup.config.json --format json

# Summary only (pass/fail + counts)
python3 scripts/rollup_config_validator.py validate rollup.config.json --format summary

# Strict mode (warnings become errors)
python3 scripts/rollup_config_validator.py validate rollup.config.json --strict
```

## Input Format

Since Rollup configs are typically JavaScript, this tool validates **JSON representations** of Rollup config objects. Export your config as JSON or use a wrapper:

```bash
# Extract config as JSON from rollup.config.js
node -e "const c = require('./rollup.config.js'); console.log(JSON.stringify(c, null, 2))" > rollup.config.json
python3 scripts/rollup_config_validator.py validate rollup.config.json
```

Or validate directly from a JSON config file.

## Rules (22+)

| # | Category | Severity | Rule |
|---|----------|----------|------|
| S1 | Structure | Error | File not found or unreadable |
| S2 | Structure | Error | Empty config or no content |
| S3 | Structure | Warning | Unknown top-level config keys |
| S4 | Structure | Error | Invalid JSON syntax |
| S5 | Structure | Error | Missing input entry point |
| O1 | Output | Error | Missing output configuration |
| O2 | Output | Warning | Missing output.format (defaults to 'es') |
| O3 | Output | Warning | output.file and output.dir both specified |
| O4 | Output | Warning | format: 'iife' or 'umd' without output.name |
| O5 | Output | Warning | Multiple outputs with same format and no distinct file/dir |
| O6 | Output | Warning | output.sourcemap: true without sourcemapExcludeSources consideration |
| E1 | External | Warning | Bare module in external should match import pattern |
| E2 | External | Warning | Regex pattern in external (fragile) |
| E3 | External | Warning | Node built-in not in external (path, fs, etc.) |
| P1 | Plugins | Warning | Plugin ordering: resolve before commonjs |
| P2 | Plugins | Warning | commonjs plugin without @rollup/plugin-node-resolve |
| P3 | Plugins | Warning | json plugin missing (importing .json files) |
| P4 | Plugins | Warning | Deprecated plugin (rollup-plugin-* → @rollup/plugin-*) |
| T1 | Treeshake | Warning | treeshake: false disables dead code elimination |
| T2 | Treeshake | Warning | moduleSideEffects: false may break libraries |
| B1 | Best Practices | Warning | Missing preserveEntrySignatures for library builds |
| B2 | Best Practices | Warning | Large number of manual chunks without shared dependencies |
| B3 | Best Practices | Warning | watch mode config without clearScreen setting |

## Output Formats

- `text` (default): Human-readable with severity icons
- `json`: Machine-parseable JSON array of findings
- `summary`: Pass/fail with error/warning counts

## Exit Codes

- `0`: No errors (warnings only or clean)
- `1`: One or more errors found
- `2`: File not found or invalid input

## Requirements

- Python 3.8+
- No external dependencies (pure stdlib)
