# Repo Layout

## Main project files

- `README.md`
  - User-facing introduction and usage.
- `pyproject.toml`
  - Package metadata and console entrypoints.
- `setup.py`
  - Compatibility shim for older pip/setuptools environments.
- `.github/workflows/ci.yml`
  - GitHub Actions test workflow.

## Code

- `src/workspace_doctor/core.py`
  - Core checks, report generation, and safe workspace-local fixes.
- `src/workspace_doctor/cli.py`
  - Main CLI entrypoint for the doctor.
- `src/workspace_doctor/fix_openclaw_config.py`
  - External config patcher for the `codex-cli` backend.

## Wrappers

- `scripts/workspace_doctor.py`
  - Runs the packaged CLI from a repo checkout.
- `scripts/fix_openclaw_codex_config.py`
  - Runs the external config fixer from a repo checkout.

## Tests

- `tests/test_core.py`
  - Core doctor behavior.
- `tests/test_fix_openclaw_config.py`
  - External config patching behavior.
