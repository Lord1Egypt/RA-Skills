---
name: tailwind-config-validator
description: Validate JSON-exported Tailwind CSS configuration files for structural issues, content path problems, theme misconfiguration, and best practices. Use when auditing Tailwind configs, preparing production builds, or enforcing CI standards.
---

# Tailwind Config Validator

Validate Tailwind CSS configuration files exported as JSON for structural correctness, content path issues, theme misconfiguration, dark mode problems, plugin hygiene, and best practices. Pure Python 3 stdlib — no external dependencies.

**Note:** Tailwind configs are JS/TS, not directly parseable. This validator works with JSON-exported configs. Export via:

```bash
node -e "console.log(JSON.stringify(require('./tailwind.config.js')))" > config.json
python3 scripts/tailwind_config_validator.py validate config.json
```

## Commands

### validate — Full validation with all rules

```bash
python3 scripts/tailwind_config_validator.py validate config.json
python3 scripts/tailwind_config_validator.py validate config.json --strict
python3 scripts/tailwind_config_validator.py validate config.json --format json
```

### lint — Run all rules (alias for validate)

```bash
python3 scripts/tailwind_config_validator.py lint config.json
python3 scripts/tailwind_config_validator.py lint config.json --format summary
python3 scripts/tailwind_config_validator.py lint config.json --strict --format json
```

### content — Check content configuration

```bash
python3 scripts/tailwind_config_validator.py content config.json
python3 scripts/tailwind_config_validator.py content config.json --format json
python3 scripts/tailwind_config_validator.py content config.json --format summary
```

### theme — Check theme configuration

```bash
python3 scripts/tailwind_config_validator.py theme config.json
python3 scripts/tailwind_config_validator.py theme config.json --format json
python3 scripts/tailwind_config_validator.py theme config.json --format summary
```

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Treat warnings as errors — exit code 1 (CI-friendly) |
| `--format text` | Human-readable output (default) |
| `--format json` | Machine-readable JSON |
| `--format summary` | Compact summary with counts |

## Validation Rules (26)

### Structure (5)

| Rule | Severity | Description |
|------|----------|-------------|
| S1 | error | File not found or unreadable |
| S2 | error | Empty config file |
| S3 | error | Invalid JSON syntax |
| S4 | warning/info | Unknown top-level keys (valid: content, theme, plugins, presets, darkMode, prefix, important, separator, corePlugins, safelist, blocklist, future, experimental) |
| S5 | info | JS/TS config detected (hint to export as JSON) |

### Content (5)

| Rule | Severity | Description |
|------|----------|-------------|
| C1 | error | Missing content paths (required for tree-shaking) |
| C2 | warning | Empty content array |
| C3 | warning | Content paths include node_modules (performance) |
| C4 | warning | Content glob too broad (e.g. `**/*` without extension filter) |
| C5 | info | Suspicious content pattern (bare `*.css` or similar) |

### Theme (5)

| Rule | Severity | Description |
|------|----------|-------------|
| T1 | warning | Overriding entire theme key without extend (replaces defaults) |
| T2 | info | Empty theme.extend object |
| T3 | warning | Invalid color values (not strings) |
| T4 | info | Referencing default theme without callback (theme() needed) |
| T5 | warning | Custom screen breakpoints not in ascending order |

### Dark Mode (2)

| Rule | Severity | Description |
|------|----------|-------------|
| D1 | error | Invalid darkMode value |
| D2 | info | darkMode "class" deprecated in v3.4+ (use "selector") |

### Plugins (3)

| Rule | Severity | Description |
|------|----------|-------------|
| P1 | info | Empty plugins array |
| P2 | error | Plugins not an array |
| P3 | info | Deprecated official plugins (built-in in v4) |

### Best Practices (6)

| Rule | Severity | Description |
|------|----------|-------------|
| B1 | error | No content paths defined (tree-shaking broken) |
| B2 | warning | Using important: true globally (anti-pattern) |
| B3 | warning | Prefix with special characters |
| B4 | warning | corePlugins disabled entirely |
| B5 | warning | Large safelist (>50 patterns, bloats CSS) |
| B6 | warning | Missing theme.extend (all customizations override defaults) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings allowed unless `--strict`) |
| 1 | Errors found (or warnings in `--strict` mode) |
| 2 | File not found / parse error |

## CI Integration

```yaml
# GitHub Actions example
- name: Validate Tailwind config
  run: |
    node -e "console.log(JSON.stringify(require('./tailwind.config.js')))" > /tmp/tw-config.json
    python3 scripts/tailwind_config_validator.py validate /tmp/tw-config.json --strict --format json
```

## Example Output

```
tailwind.config validate — config.json
=======================================
[ERROR  ] C1: Missing 'content' paths — required for tree-shaking
         Without content paths, Tailwind cannot purge unused CSS. Add content: ['./src/**/*.{html,js,ts,jsx,tsx}'].
[WARNING] T1: theme.colors overrides all default colors — use theme.extend.colors instead
         Placing keys directly under 'theme' replaces the entire default set. Move to 'theme.extend' to merge with defaults.
[WARNING] B2: important: true applies !important to all utilities (anti-pattern)
         Prefer important: '#app' to scope specificity to a root selector instead of global !important.
[INFO   ] P3: Plugin '@tailwindcss/forms' is built-in since Tailwind v4
         In Tailwind v4, @tailwindcss/forms functionality is included by default. Remove the plugin if upgrading.
[INFO   ] D2: darkMode 'class' is deprecated since v3.4 — use 'selector' instead
         The 'class' strategy still works but 'selector' is the recommended replacement.

Result: INVALID
Summary: 1 error(s), 2 warning(s), 2 info
```
