---
name: swc-config-validator
description: Validate SWC config files (.swcrc, package.json#swc) for parser settings, transform conflicts, module type issues, and best practices. Use when validating SWC transpiler configs, auditing Next.js/Turbopack build setups, or linting swc config files.
---

# SWC Config Validator

Validate `.swcrc` and `package.json#swc` for parser errors, invalid targets, transform conflicts, module type issues, minification problems, and best practices. Supports text, JSON, and summary output formats with CI-friendly exit codes.

## Commands

```bash
# Full validation (all 22+ rules)
python3 scripts/swc_config_validator.py validate .swcrc

# Quick syntax/structure check only
python3 scripts/swc_config_validator.py check .swcrc

# Explain config in human-readable form
python3 scripts/swc_config_validator.py explain .swcrc

# Suggest improvements
python3 scripts/swc_config_validator.py suggest .swcrc

# JSON output (CI-friendly)
python3 scripts/swc_config_validator.py validate .swcrc --format json

# Summary only (pass/fail + counts)
python3 scripts/swc_config_validator.py validate .swcrc --format summary

# Strict mode (warnings become errors)
python3 scripts/swc_config_validator.py validate .swcrc --strict

# Validate from package.json#swc
python3 scripts/swc_config_validator.py validate package.json
```

## Rules (22+)

| # | Category | Severity | Rule |
|---|----------|----------|------|
| S1 | Structure | Error | File not found or unreadable |
| S2 | Structure | Error | Empty config |
| S3 | Structure | Error | Invalid JSON syntax |
| S4 | Structure | Warning | Unknown top-level keys |
| S5 | Structure | Warning | Missing jsc key (most configs need it) |
| J1 | JSC Config | Error | Invalid parser syntax (must be ecmascript or typescript) |
| J2 | JSC Config | Warning | JSX enabled in parser without React transform |
| J3 | JSC Config | Warning | Deprecated loose mode in jsc.transform |
| J4 | JSC Config | Warning | Missing target (no compilation target specified) |
| J5 | JSC Config | Error | Invalid target value (not es3/es5/es2015-es2024/esnext) |
| M1 | Modules | Error | Unknown module type |
| M2 | Modules | Warning | isModule: false with ESM module type |
| M3 | Modules | Warning | CommonJS module with ESM-only parser features |
| T1 | Transform | Error | React transform without parser.jsx enabled |
| T2 | Transform | Warning | Legacy decorators without decoratorsBeforeExport |
| T3 | Transform | Warning | Conflicting useDefineForClassFields with TypeScript |
| T4 | Transform | Warning | Deprecated constModules in jsc.experimental |
| N1 | Minification | Warning | Minification enabled with compress: false |
| N2 | Minification | Warning | Mangle enabled without compress |
| N3 | Minification | Warning | Drop console in development config |
| B1 | Best Practices | Warning | sourceMaps not configured |
| B2 | Best Practices | Info | No env config for different environments |

## Output Formats

- `text` (default): Human-readable with severity icons
- `json`: Machine-parseable JSON array of findings
- `summary`: Pass/fail with error/warning counts

## Exit Codes

- `0`: No errors (warnings/info only or clean)
- `1`: One or more errors found
- `2`: File not found or invalid input

## Requirements

- Python 3.8+
- No external dependencies (pure stdlib)

## Supported Targets

`es3`, `es5`, `es2015` through `es2024`, `esnext`

## Supported Module Types

`es6`, `commonjs`, `umd`, `amd`, `nodenext`, `systemjs`

## Valid Top-Level Keys

`$schema`, `jsc`, `module`, `minify`, `env`, `isModule`, `sourceMaps`, `inlineSourcesContent`, `emitSourceMapColumns`, `inputSourceMap`, `test`, `exclude`, `filename`
