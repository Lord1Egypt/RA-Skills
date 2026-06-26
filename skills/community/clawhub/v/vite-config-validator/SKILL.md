---
name: vite-config-validator
description: Validate Vite configuration files (JSON-exported) for structural correctness, build settings, server security, resolve/CSS hygiene, plugin deprecations, and best practices. Use when auditing Vite projects, enforcing config standards in CI, or reviewing vite.config.ts changes.
---

# Vite Config Validator

Validate Vite configuration files exported as JSON for structural correctness, build settings, server configuration, resolve/CSS options, plugin hygiene, and best practices. Uses pure Python 3 stdlib (`json`, `argparse`, `re`, `os`, `sys`) -- no external dependencies.

Since Vite configs are JS/TS (`vite.config.ts`), the validator works with JSON-exported snapshots. Export your config first:

```bash
node -e "import('./vite.config.ts').then(m => console.log(JSON.stringify(m.default)))" > vite.config.json
```

Then validate the JSON output.

## Commands

### validate -- Full validation with all rules

```bash
python3 scripts/vite_config_validator.py validate vite.config.json
python3 scripts/vite_config_validator.py validate vite.config.json --strict
python3 scripts/vite_config_validator.py validate vite.config.json --format json
```

### check -- Quick check (errors and warnings only)

```bash
python3 scripts/vite_config_validator.py check vite.config.json
python3 scripts/vite_config_validator.py check vite.config.json --format summary
```

### explain -- Show all rules with descriptions

```bash
python3 scripts/vite_config_validator.py explain vite.config.json
python3 scripts/vite_config_validator.py explain vite.config.json --format json
```

### suggest -- Run validation and propose fixes

```bash
python3 scripts/vite_config_validator.py suggest vite.config.json
python3 scripts/vite_config_validator.py suggest vite.config.json --format json
```

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Treat warnings as errors -- exit code 1 (CI-friendly) |
| `--format text` | Human-readable output (default) |
| `--format json` | Machine-readable JSON |
| `--format summary` | Compact summary with counts |

## Validation Rules (25)

### Structure (5)

| Rule | Severity | Description |
|------|----------|-------------|
| S1 | error | File not found or unreadable |
| S2 | error | Empty config file |
| S3 | error | Invalid JSON syntax |
| S4 | warning | Unknown top-level keys (not in Vite's valid config options) |
| S5 | info | defineConfig() wrapper hint (cannot verify in JSON export) |

### Build (5)

| Rule | Severity | Description |
|------|----------|-------------|
| B1 | info | Missing build.outDir (defaults to 'dist') |
| B2 | error | Invalid build.target value |
| B3 | error | Invalid build.minify value (not boolean, 'terser', or 'esbuild') |
| B4 | warning | build.sourcemap set to 'hidden' in development mode |
| B5 | warning | Deprecated Rollup plugins (rollup-plugin-* vs @rollup/plugin-*) |

### Server (4)

| Rule | Severity | Description |
|------|----------|-------------|
| V1 | error/warning | server.port out of valid range or privileged port |
| V2 | warning | server.host set to true/0.0.0.0 (security: exposes to network) |
| V3 | warning | server.proxy with invalid target URLs |
| V4 | warning | server.https without cert/key paths |

### Resolve (3)

| Rule | Severity | Description |
|------|----------|-------------|
| R1 | warning | resolve.alias with absolute paths (portability risk) |
| R2 | info | Missing resolve.extensions for TypeScript projects |
| R3 | warning | resolve.dedupe with empty array |

### CSS (3)

| Rule | Severity | Description |
|------|----------|-------------|
| C1 | info | css.preprocessorOptions without corresponding preprocessor dependency hint |
| C2 | warning | css.modules with invalid or unknown options |
| C3 | warning | css.postcss pointing to non-existent file |

### Plugins (2)

| Rule | Severity | Description |
|------|----------|-------------|
| P1 | info | Empty plugins array |
| P2 | warning | Deprecated Vite plugin names |

### Best Practices (3)

| Rule | Severity | Description |
|------|----------|-------------|
| X1 | info | No mode set in config |
| X2 | info | Missing base path for non-root deployments |
| X3 | warning | build.chunkSizeWarningLimit too high (>2000 kB) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings allowed unless `--strict`) |
| 1 | Errors found (or warnings in `--strict` mode) |
| 2 | File not found / parse error |

## CI Integration

```yaml
# GitHub Actions
- name: Validate Vite config
  run: |
    node -e "import('./vite.config.ts').then(m => console.log(JSON.stringify(m.default)))" > /tmp/vite.config.json
    python3 scripts/vite_config_validator.py validate /tmp/vite.config.json --strict --format json
```

## Example Output

```
vite.config validate -- vite.config.json
=========================================
[ERROR  ] B2: Invalid build.target value: 'ie11'
         Valid targets: 'modules', 'esnext', 'es20XX', or browser versions like 'chrome87', 'firefox78', 'safari13'.
[WARNING] V2: server.host exposes dev server to all network interfaces
         Setting host to true or '0.0.0.0' makes the dev server accessible from any device on the network. Use 'localhost' or '127.0.0.1' for local-only.
[WARNING] X3: build.chunkSizeWarningLimit is very high (5000 kB)
         A limit above 2000 kB effectively silences chunk size warnings. Large chunks hurt load performance. Consider code splitting instead of raising the limit. Default is 500 kB.
[INFO   ] S5: JSON export cannot verify defineConfig() wrapper
         Wrap your config with defineConfig() in vite.config.ts for type safety and IDE autocompletion: export default defineConfig({ ... })
[INFO   ] X1: No mode set in config
         Vite defaults to 'development' for serve and 'production' for build. Set mode explicitly if you need environment-specific behavior in the config itself.

Result: INVALID
Summary: 1 error(s), 2 warning(s), 2 info
```
