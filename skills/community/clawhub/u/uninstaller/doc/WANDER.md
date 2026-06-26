# Wander Integration — CI Monitor

Use [Wander](https://github.com/ERerGB/wander) to monitor the Publish Skills workflow (ClawHub, ghcr.io, Sundial) without polling.

## Prerequisites

- `gh` CLI installed and authenticated
- Wander cloned (e.g. `~/code/wander` or sibling of this repo)
- macOS (for notifications)

## Quick usage

```bash
# 1. Push (triggers publish workflow)
git push

# 2. Monitor in background (from this repo)
./scripts/watch-publish.sh
```

You'll get a macOS notification when the workflow completes (success or failure).

## Pipeline context

The workflow has **3 parallel jobs**:

| Job | Domain | Common failure |
|-----|--------|----------------|
| verify-copilot-skill | GitHub Copilot | SKILL.md out of sync |
| publish-clawhub | ClawHub | CLAWHUB_TOKEN missing, clawhub patch |
| publish-sundial | Sundial | Skips if SUNDIAL_TOKEN unset |
| publish-ghcr | ghcr.io | skr Action, permissions |
| publish-skillcreator | SkillCreator | Skips if SKILLCREATOR_TOKEN unset |

Any job failure triggers a notification. Use the fix loop below.

## Modes

| Mode | Command | Use case |
|------|---------|----------|
| Foreground | `cd .. && wander/watch-workflow.sh publish.yml` (from wander) | Wait for result |
| Background | `./scripts/watch-publish.sh` | Continue working, notify when done |
| Detached | `./scripts/watch-publish-detached.sh` | Close terminal, log to `~/.wander_logs/` |

## Fix loop — when CI fails

1. **Get notification** — Wander shows failure with run ID (e.g. `#12345`).

2. **View failed logs**:
   ```bash
   gh run view <RUN_ID> --log-failed
   ```
   Or latest failed run:
   ```bash
   gh run list --workflow=publish.yml --limit 5
   gh run view <RUN_ID> --log-failed
   ```

3. **Identify failing job** — Logs show which job failed (publish-clawhub, publish-sundial, publish-ghcr).

4. **Fix and re-run**:
   - Fix code/config, commit, push → triggers new run
   - Or re-run without push: `gh run rerun <RUN_ID> --failed`

5. **Re-monitor**: `./scripts/watch-publish.sh` (if you triggered a new run)

## Common failures and fixes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| ClawHub: 401 / login failed | CLAWHUB_TOKEN missing or expired | Add/rotate token in repo Secrets |
| ClawHub: acceptLicenseTerms | clawhub bug (clawhub#660) | Patch step in workflow should fix; verify patch applied |
| Sundial: push failed | No token (expected) | Normal — job skips when SUNDIAL_TOKEN unset |
| ghcr: 403 / permission denied | packages: write | Ensure workflow has `packages: write` |
| ghcr: skr build error | SKILL.md structure | Check skr docs; ensure SKILL.md at repo root |

## Config

- **`.workflows.yml`** — Wander workflow config (check_window, expected_duration)
- **`WORKFLOW_REGISTRY_FILE`** — Set by `watch-publish.sh` to use project config

## Alias (optional)

```bash
alias watch-pub='cd /path/to/openclaw-uninstall && ./scripts/watch-publish.sh'
# Then: git push && watch-pub
```
