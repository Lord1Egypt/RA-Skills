# Test ClawHub CLI Skill

This is a test skill for validating clawhub CLI publish functionality.

## Features

- Tests the clawhub publish command
- Verifies CLI argument handling
- Validates tag and changelog parameters

## Usage

```bash
python test_script.py
```

## Testing

This skill is used to verify that the clawhub CLI correctly handles:
- `--name` parameter
- `--version` parameter (semver format)
- `--tags` parameter (comma-separated)
- `--changelog` parameter
