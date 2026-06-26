---
name: webpack-config-validator
description: Validate JSON-exported webpack configuration files for structural issues, deprecated loaders/plugins, optimization gaps, and best practices. Use when auditing webpack configs, preparing production builds, or enforcing CI standards.
---

# Webpack Config Validator

Validate webpack configuration files exported as JSON for structural correctness, entry/output issues, deprecated loaders and plugins, optimization configuration, and best practices. Pure Python 3 stdlib — no external dependencies.

**Note:** webpack configs are JS/TS, not directly parseable. This validator works with JSON-exported configs. Export via:

```bash
node -e "console.log(JSON.stringify(require('./webpack.config.js')))" > config.json
python3 scripts/webpack_config_validator.py validate config.json
```

## Commands

### validate — Full validation with all rules

```bash
python3 scripts/webpack_config_validator.py validate config.json
python3 scripts/webpack_config_validator.py validate config.json --strict
python3 scripts/webpack_config_validator.py validate config.json --format json --mode production
```

### check — Quick check (errors and warnings only)

```bash
python3 scripts/webpack_config_validator.py check config.json
python3 scripts/webpack_config_validator.py check config.json --format summary
```

### explain — Show all rules with descriptions

```bash
python3 scripts/webpack_config_validator.py explain config.json
python3 scripts/webpack_config_validator.py explain config.json --format json
```

### suggest — Run validation and propose fixes

```bash
python3 scripts/webpack_config_validator.py suggest config.json
python3 scripts/webpack_config_validator.py suggest config.json --format json
```

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Treat warnings as errors — exit code 1 (CI-friendly) |
| `--format text` | Human-readable output (default) |
| `--format json` | Machine-readable JSON |
| `--format summary` | Compact summary with counts |
| `--mode production` | Override mode context for mode-specific rules (E3, O3) |
| `--mode development` | Override mode context for mode-specific rules |

## Validation Rules (24)

### Structure (5)

| Rule | Severity | Description |
|------|----------|-------------|
| S1 | error | File not found or unreadable |
| S2 | error | Empty config file |
| S3 | error | Invalid JSON syntax |
| S4 | error | Missing required fields (entry, output) |
| S5 | warning/info | Unknown or deprecated top-level keys |

### Entry/Output (4)

| Rule | Severity | Description |
|------|----------|-------------|
| E1 | error | Empty entry point (empty string, object, or array) |
| E2 | error | Output section missing 'path' property |
| E3 | warning | Output filename without content hash in production mode |
| E4 | warning | publicPath not set |

### Module/Rules (4)

| Rule | Severity | Description |
|------|----------|-------------|
| M1 | warning | Module rule without 'test' pattern |
| M2 | warning | Duplicate loader for same test pattern |
| M3 | warning | Deprecated loaders (raw-loader, url-loader, file-loader, json-loader) |
| M4 | info | No babel-loader/ts-loader/esbuild-loader/swc-loader for JS/TS |

### Plugins (4)

| Rule | Severity | Description |
|------|----------|-------------|
| P1 | error | Deprecated plugins (UglifyJsPlugin, ExtractTextPlugin, CommonsChunkPlugin) |
| P2 | warning | Duplicate plugin instances |
| P3 | info | HtmlWebpackPlugin without explicit template |
| P4 | warning | MiniCssExtractPlugin without corresponding loader in rules |

### Optimization (3)

| Rule | Severity | Description |
|------|----------|-------------|
| O1 | info | Missing splitChunks configuration |
| O2 | info | Missing custom minimizer configuration |
| O3 | warning/info | devtool set to eval or source-map in production mode |

### Best Practices (4)

| Rule | Severity | Description |
|------|----------|-------------|
| B1 | info | Missing resolve.extensions |
| B2 | warning | Hardcoded absolute filesystem paths in config |
| B3 | warning | No mode set (development/production/none) |
| B4 | info | Missing devServer configuration |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings allowed unless `--strict`) |
| 1 | Errors found (or warnings in `--strict` mode) |
| 2 | File not found / parse error |

## CI Integration

```yaml
# GitHub Actions example
- name: Validate webpack config
  run: |
    node -e "console.log(JSON.stringify(require('./webpack.config.js')))" > /tmp/wp-config.json
    python3 scripts/webpack_config_validator.py validate /tmp/wp-config.json --strict --mode production --format json
```

## Example Output

```
webpack.config validate — config.json
======================================
[ERROR  ] S4: Missing required top-level field(s): output
         Every webpack config needs at least 'entry' and 'output'.
[WARNING] E4: output.publicPath not set
         Set publicPath to ensure assets are loaded from the correct URL. Common values: '/', '/assets/', 'auto'.
[WARNING] M3: Deprecated loader 'file-loader' in rule 2
         Replace with asset/resource (webpack 5 built-in).
[ERROR  ] P1: Deprecated plugin 'UglifyJsPlugin' at index 0
         Replace with TerserPlugin (terser-webpack-plugin).
[INFO   ] O1: No optimization.splitChunks configuration
         splitChunks enables automatic code splitting for shared dependencies. Add optimization: { splitChunks: { chunks: 'all' } } for better caching.
[WARNING] B3: No 'mode' set (development/production/none)
         Set mode to enable webpack's built-in optimizations. Without mode, webpack defaults to 'production' with a warning.

Result: INVALID
Summary: 2 error(s), 3 warning(s), 1 info
```
