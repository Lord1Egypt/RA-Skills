# ClawHub Publish

Publish and manage Claude Code skills on ClawHub (clawhub.ai).

## Features

- **Publish**: First-time publish with validation
- **Update**: Auto-bump version (major/minor/patch) with changelog
- **Check**: Validate skill format, CLI, and auth status
- **Dry-run**: Preview publish without actually doing it

## Quick Start

### 1. Check readiness

```
/clawhub-publish check /path/to/your-skill
```

### 2. Publish (first time)

```
/clawhub-publish publish /path/to/your-skill
```

### 3. Update version

```
/clawhub-publish update /path/to/your-skill --bump minor
```

## Commands

| Command | Description |
|---------|-------------|
| `/clawhub-publish status` | Check CLI, auth, and published skills |
| `/clawhub-publish check <path>` | Validate skill format |
| `/clawhub-publish publish <path>` | Publish new skill |
| `/clawhub-publish update <path>` | Update existing skill version |

## Auto-generated Changelog

When you don't provide a changelog, the skill will:
1. Try to read `CHANGELOG.md`
2. Fall back to recent git commits
3. Use a default message

## Version Bumping

- `--bump patch`: 1.0.0 → 1.0.1 (default)
- `--bump minor`: 1.0.0 → 1.1.0
- `--bump major`: 1.0.0 → 2.0.0

## Requirements

```bash
npm i -g clawhub
clawhub login
```
