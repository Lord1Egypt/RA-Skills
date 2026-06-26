---
name: tsconfig-validator
description: Validate and lint tsconfig.json files for common mistakes, conflicting compiler options, strictness gaps, and best practices. Use when asked to lint, validate, audit, or check TypeScript configuration files. Triggers on "lint tsconfig", "check tsconfig", "validate typescript config", "audit tsconfig.json", "typescript settings".
---

# TSConfig Validator

Validates `tsconfig.json` files for common mistakes, conflicting options, and best practices.

## Commands

### `lint <file>`
Run all lint rules against a tsconfig.json file.

```bash
python3 scripts/tsconfig_validator.py lint tsconfig.json
python3 scripts/tsconfig_validator.py lint tsconfig.json --strict --format json
```

### `strict <file>`
Check strictness-related options and suggest enabling strict mode.

```bash
python3 scripts/tsconfig_validator.py strict tsconfig.json
```

### `compat <file>`
Check target/module compatibility issues.

```bash
python3 scripts/tsconfig_validator.py compat tsconfig.json
```

### `validate <file>`
Structural validation — valid keys, types, JSON syntax.

```bash
python3 scripts/tsconfig_validator.py validate tsconfig.json
```

## Options

- `--format text|json|markdown` — Output format (default: text)
- `--strict` — Exit 1 on warnings too (not just errors)

## Rules (22)

| # | Rule | Category | Severity |
|---|------|----------|----------|
| 1 | invalid-json | structure | error |
| 2 | unknown-compiler-option | structure | warning |
| 3 | empty-config | structure | warning |
| 4 | missing-include | structure | info |
| 5 | conflicting-include-exclude | structure | warning |
| 6 | strict-not-enabled | strictness | warning |
| 7 | no-implicit-any | strictness | warning |
| 8 | strict-null-checks | strictness | warning |
| 9 | no-unchecked-indexed | strictness | info |
| 10 | no-unused-locals | strictness | info |
| 11 | no-unused-params | strictness | info |
| 12 | outdated-target | compat | warning |
| 13 | module-target-mismatch | compat | warning |
| 14 | jsx-without-react | compat | warning |
| 15 | node-module-resolution | compat | info |
| 16 | es-interop | compat | warning |
| 17 | missing-outdir | best-practices | info |
| 18 | missing-rootdir | best-practices | info |
| 19 | skip-lib-check | best-practices | info |
| 20 | source-map-in-prod | best-practices | info |
| 21 | incremental-not-enabled | best-practices | info |
| 22 | paths-without-baseurl | best-practices | error |

## Exit Codes

- `0` — No issues (or only info-level)
- `1` — Errors or warnings found (with `--strict`)
