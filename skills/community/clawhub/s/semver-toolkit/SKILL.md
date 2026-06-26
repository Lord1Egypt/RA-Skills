---
name: semver-toolkit
description: Semantic Versioning (SemVer 2.0.0) toolkit for parsing, validating, comparing, bumping, and sorting version strings. Use when working with software versions, release management, version bumps, or checking if version strings conform to semver spec.
---

# SemVer Toolkit

Parse, validate, compare, bump, and sort semantic version strings per the SemVer 2.0.0 spec.

## Quick Start

```bash
# Parse a version into components
python3 scripts/semver_toolkit.py parse 1.2.3-beta.1+build.42

# Validate versions
python3 scripts/semver_toolkit.py validate 1.0.0 v2.1 not-a-version

# Bump version
python3 scripts/semver_toolkit.py bump 1.2.3 minor
python3 scripts/semver_toolkit.py bump 1.2.3 major --pre rc

# Compare two versions
python3 scripts/semver_toolkit.py compare 1.2.3 2.0.0

# Sort versions (ascending)
python3 scripts/semver_toolkit.py sort 3.0.0 1.0.0-alpha 1.0.0 2.1.0

# Sort descending, JSON output
python3 scripts/semver_toolkit.py sort 3.0.0 1.0.0 2.1.0 -r -f json
```

## Commands

| Command | Description |
|---------|-------------|
| `parse VERSION` | Break version into major, minor, patch, prerelease, build |
| `validate VERSION...` | Check if versions are valid semver |
| `bump VERSION PART` | Bump major/minor/patch/prerelease (optional `--pre TAG`) |
| `compare A B` | Show which version is greater/less/equal |
| `sort VERSION...` | Sort versions in semver order (`-r` for descending) |

## Notes

- Accepts optional `v` prefix (e.g. `v1.2.3`)
- Prerelease precedence follows SemVer spec (numeric < alpha, no prerelease > prerelease)
- Python 3 stdlib only — no external dependencies
- Use `-f json` on any command for machine-readable output
