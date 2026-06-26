# Commands

## Primary commands

- `python3 scripts/workspace_doctor.py`
  - Run the doctor in human-readable mode.
- `python3 scripts/workspace_doctor.py --json`
  - Emit JSON output for automation.
- `python3 scripts/workspace_doctor.py --fix`
  - Apply safe workspace-local fixes before reporting.

## External config commands

- `python3 scripts/fix_openclaw_codex_config.py --check`
  - Return `ok` or `needs-change`.
- `python3 scripts/fix_openclaw_codex_config.py`
  - Patch the live OpenClaw config and create a timestamped backup first.
- `python3 scripts/fix_openclaw_codex_config.py --stdout`
  - Print the patched JSON without writing it.

## Boundaries

- `workspace_doctor.py --fix` only touches files inside the workspace.
- `fix_openclaw_codex_config.py` is the tool for `~/.openclaw/openclaw.json`.
- If sandbox permissions block writes outside the workspace, say so explicitly and do not claim the live config was fixed.
