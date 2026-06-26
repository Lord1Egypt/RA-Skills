# AGENTS.md — openclaw-uninstall

## Overview

Community-maintained uninstall skill for OpenClaw. Scripts: `install.sh`, `schedule-uninstall.sh`, `uninstall-oneshot.sh`, `verify-clean.sh`.

## E2E Tests

Tests simulate the flow: install → schedule (dry-run) → uninstall validation → verify-clean. Uses mocks to avoid real ClawHub API, launchd, and destructive uninstall.

### Run tests

```bash
./tests/run-e2e.sh
```

### Full lifecycle (install → gateway run → uninstall)

```bash
./tests/run-lifecycle.sh
```

Runs: install openclaw → start gateway in background → uninstall-oneshot. Use after machine reboot or to verify the full flow.

### Test coverage

| Test | What it verifies |
|------|------------------|
| install.sh | clawhub stub installs SKILL.md + scripts to workdir |
| schedule-uninstall --dry-run | Arg parsing, CMD contains --notify-im, --no-backup, --preserve-state |
| uninstall-oneshot --dry-run | STATE_DIR validation passes, no destructive ops |
| verify-clean (clean env) | Reports "Fully cleaned" when no residue |
| verify-clean (with residue) | Reports "Residue found" when state dir exists |

### Mocks and dry-run

- **clawhub stub** (`tests/helpers/clawhub-stub.sh`): Mimics `clawhub star` and `clawhub install`; copies SKILL.md and scripts to workdir. Use via `PATH="tests/helpers:$PATH"` with a symlink named `clawhub`.
- **schedule-uninstall --dry-run**: Prints `DRY_RUN_CMD:` and exits without scheduling.
- **uninstall-oneshot --dry-run**: Validates `OPENCLAW_STATE_DIR` and exits before any destructive steps (gateway stop, rm, npm remove, etc.).

### Adding tests

1. Add a new `run_test "description" ' ... '` block in `tests/run-e2e.sh`.
2. Use temp dirs (`mktemp -d`) and clean up with `rm -rf`.
3. For verify-clean: set `HOME` and `OPENCLAW_STATE_DIR` to control residue detection.
4. Avoid `grep -q "--flag"` — use `grep -q "flag"` so grep does not treat `--flag` as its own option.

## Script options

- **schedule-uninstall**: `--notify-email`, `--notify-ntfy`, `--notify-im`, `--no-backup`, `--preserve-state`, `--all-profiles`, `--dry-run`
- **uninstall-oneshot**: `--notify-email`, `--notify-ntfy`, `--notify-im`, `--no-backup`, `--preserve-state`, `--all-profiles`, `--dry-run`

## CI (future)

When E2E tests are stable, add a job to `.github/workflows/` and register in `.workflows.yml`.
