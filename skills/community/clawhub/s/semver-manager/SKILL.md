---
name: semver-manager
description: Parse, validate, compare, sort, bump, and filter semantic versions (semver). Use when asked to check version compatibility, bump version numbers, sort releases, find latest matching version, or validate semver strings. Triggers on "semver", "version bump", "version compare", "semantic version", "version constraint", "caret range", "tilde range".
---

# Semver Manager

Parse, validate, compare, sort, bump, and filter semantic versions per the semver 2.0.0 spec.

## Validate

```bash
python3 scripts/semver.py validate 1.2.3 v2.0.0-beta.1 invalid
```

## Compare

```bash
python3 scripts/semver.py compare 1.2.3 2.0.0
```

## Sort

```bash
# Oldest first (default)
python3 scripts/semver.py sort 3.0.0 1.2.3 2.0.0-rc.1 2.0.0

# Newest first
python3 scripts/semver.py sort --reverse 3.0.0 1.2.3 2.0.0
```

## Bump

```bash
# Bump patch: 1.2.3 → 1.2.4
python3 scripts/semver.py bump 1.2.3 patch

# Bump minor: 1.2.3 → 1.3.0
python3 scripts/semver.py bump 1.2.3 minor

# Bump major: 1.2.3 → 2.0.0
python3 scripts/semver.py bump 1.2.3 major

# Bump with pre-release tag: 1.2.3 → 1.3.0-beta.0
python3 scripts/semver.py bump 1.2.3 minor --pre beta

# Bump pre-release: 1.3.0-beta.0 → 1.3.0-beta.1
python3 scripts/semver.py bump 1.3.0-beta.0 prerelease
```

## Filter by Constraint

```bash
# Caret (^): compatible versions
python3 scripts/semver.py filter "^1.2.0" 1.2.3 1.3.0 2.0.0 1.1.0

# Tilde (~): same minor
python3 scripts/semver.py filter "~1.2.0" 1.2.3 1.3.0 1.2.0

# Comparison operators
python3 scripts/semver.py filter ">=2.0.0" 1.9.9 2.0.0 2.1.0 3.0.0-alpha
```

## Find Latest

```bash
# Latest overall
python3 scripts/semver.py latest 1.2.3 2.0.0 1.9.0

# Latest matching constraint
python3 scripts/semver.py latest 1.2.3 2.0.0 1.9.0 --constraint "^1.0.0"
```

## Output Formats

```bash
python3 scripts/semver.py -f json validate 1.2.3
python3 scripts/semver.py -f markdown sort 3.0.0 1.2.3 2.0.0
```

## Supported Constraints

| Operator | Meaning | Example |
|----------|---------|---------|
| `^` | Compatible (same leftmost non-zero) | `^1.2.3` matches `1.x.x` |
| `~` | Same major.minor | `~1.2.0` matches `1.2.x` |
| `>=` | Greater or equal | `>=2.0.0` |
| `<=` | Less or equal | `<=3.0.0` |
| `>` | Greater than | `>1.0.0` |
| `<` | Less than | `<2.0.0` |
| `=` | Exact match | `=1.2.3` |
| `!=` | Not equal | `!=1.0.0` |
