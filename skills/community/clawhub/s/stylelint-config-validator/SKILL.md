# stylelint-config-validator

Validate Stylelint configuration files for correctness, deprecated rules, and best practices.

## What it does

Checks `.stylelintrc` / `.stylelintrc.json` / `.stylelintrc.yaml` for:

- **Rules** — unknown rules, deprecated rules (70+ deprecated in Stylelint 16), null values, many disabled rules
- **Config structure** — unknown config keys, extends/plugins arrays, override validation
- **Deprecated rules** — blacklist→disallowed-list renames, removed formatting rules (use Prettier instead)
- **Extends** — duplicate entries, prettier config ordering (must be last)
- **Plugins** — duplicates, plugin-prefixed rules without declared plugins
- **Overrides** — missing files property, deprecated rules in overrides

### Rules (20+)

| Category | Rules | Examples |
|----------|-------|---------|
| Config structure (4) | Unknown keys, invalid types, no rules or extends, invalid defaultSeverity | `customConfig: true` → unknown key |
| Rules validation (5) | Deprecated rules (70+), unknown rules, null values, disabled rule ratio | `indentation: 2` → deprecated in v16 |
| Extends (3) | Duplicate entries, non-array type, prettier ordering | prettier before standard → wrong order |
| Plugins (3) | Duplicate plugins, non-array type, plugin rules without plugins | `scss/no-dollar-variables` without plugin |
| Overrides (3) | Non-array type, missing files, deprecated rules in overrides | Override without `files` property |
| Ignore files (1) | Catch-all patterns | `ignoreFiles: "*"` matches everything |

### Output formats

- **text** — human-readable with severity icons (❌ ⚠️ ℹ️)
- **json** — structured with summary counts
- **summary** — one-line PASS/WARN/FAIL

### Exit codes

- `0` — no errors
- `1` — errors found (or `--strict` with any issue)
- `2` — file not found or parse error

## Commands

### lint / validate

Full config validation.

```bash
python3 scripts/stylelint_validator.py lint .stylelintrc.json
python3 scripts/stylelint_validator.py validate --format json .stylelintrc
```

### rules

Check rules only (deprecated, unknown, conflicts).

```bash
python3 scripts/stylelint_validator.py rules .stylelintrc.json
```

### deprecated

List only deprecated rules in the config.

```bash
python3 scripts/stylelint_validator.py deprecated .stylelintrc.json
```

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--format` | text, json, summary | text | Output format |
| `--min-severity` | error, warning, info | info | Filter by minimum severity |
| `--strict` | flag | off | Exit 1 on any issue |

## Requirements

- Python 3.8+
- No external dependencies (pure stdlib)

## Examples

```bash
# Quick check
python3 scripts/stylelint_validator.py lint .stylelintrc.json

# CI pipeline
python3 scripts/stylelint_validator.py lint --strict --format summary .stylelintrc

# Find deprecated rules to upgrade
python3 scripts/stylelint_validator.py deprecated .stylelintrc.json

# JSON output for tooling
python3 scripts/stylelint_validator.py validate --format json .stylelintrc.yaml
```
