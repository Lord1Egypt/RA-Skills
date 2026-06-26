---
name: wander-monitor
description: "Guides use of Wander to monitor GitHub Actions without polling. Use when the user pushes code and wants CI notifications, asks how to watch workflows, avoid refreshing the Actions page, or integrate Wander (smart-push, foreground/background/detached, wrappers, edge cases)."
---

# Wander — CI Workflow Monitor

**Don't watch. Wander.** CLI toolkit for monitoring GitHub Actions. No polling; optional macOS notifications when runs finish.

## Agent auto-trigger (mandatory)

**After every `git push` that triggers GitHub Actions, start Wander in background mode** unless the user opts out.

1. If `.workflows.yml` exists in the repo root: prefer a project wrapper (`scripts/watch-*.sh`) when present.
2. Otherwise: `"$WANDER_HOME/watch-workflow-bg.sh" <workflow.yml>` (or pass the workflow file the project uses).
3. Run in the background so the session stays responsive.
4. After ~8s, check terminal output and report initial status.

If there is no `.workflows.yml` but `.github/workflows/` exists, offer monitoring but do not auto-start without confirmation.

## When to use this skill

- User wants to monitor a workflow after `git push`
- User asks for notifications when CI completes
- User wants to avoid manually refreshing the Actions page
- Long-running E2E or publish pipelines (minutes)
- Project integrates CI monitoring (e.g. ClawHub publish)

## Prerequisites

- `gh` CLI installed and authenticated
- `jq` (used by scripts)
- Wander clone on disk; `WANDER_HOME` or default `~/code/wander`
- macOS for notification center integration

## Install (tool)

```bash
git clone https://github.com/ERerGB/wander.git ~/code/wander
cd ~/code/wander
chmod +x *.sh
```

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export WANDER_HOME="${WANDER_HOME:-$HOME/code/wander}"
export PATH="$WANDER_HOME:$PATH"
alias wf='watch-workflow.sh'
alias wfbg='watch-workflow-bg.sh'
alias wfdt='watch-workflow-detached.sh'
```

Or run `./scripts/install-personal.sh` from the Wander repo (see main README).

## Usage patterns

### Smart push (Wander repo or similar)

```bash
cd /path/to/wander
./smart-push.sh
```

Suggests smoke / e2e / skip from changed files, then push and monitor.

### Manual control (any repo)

```bash
git push
cd /path/to/target-repo
"$WANDER_HOME/watch-workflow-bg.sh" publish.yml
```

### Modes

| Mode | Script | Use case |
|------|--------|----------|
| Foreground | `watch-workflow.sh` | Block until result |
| Background | `watch-workflow-bg.sh` | Keep working; notify when done |
| Detached | `watch-workflow-detached.sh` | Close terminal; logs under `~/.wander_logs/` |

### Project wrapper (recommended)

```bash
#!/bin/bash
# scripts/watch-publish.sh
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WANDER_DIR="${WANDER_DIR:-$(dirname "$REPO_ROOT")/wander}"
cd "$REPO_ROOT"
exec "$WANDER_DIR/watch-workflow-bg.sh" publish.yml "$@"
```

Then: `git push && ./scripts/watch-publish.sh`

Examples elsewhere: `openclaw-uninstall` uses `./scripts/watch-publish.sh` and `watch-publish-detached.sh` when present.

## Workflow registry

For `check_window` / `expected_duration`, add `.workflows.yml` at project root or set `WORKFLOW_REGISTRY_FILE`:

```yaml
workflows:
  - name: "publish.yml"
    description: "Publish to ClawHub"
    check_window: 120
    expected_duration: 30
    category: "publish"
```

Default `check_window` is 300 seconds when a workflow is not listed.

## Edge cases

| Scenario | Behavior | Tip |
|----------|----------|-----|
| Workflow finishes in under ~30s | May show "already completed" + quick notify | `watch-workflow-bg.sh` detects recent completion |
| Push then monitor immediately | Run may not appear for 5–10s | Scripts wait up to ~30s for the run to show |
| Wrong branch | No workflow after wait window | Confirm workflow `on:` filters match current branch |
| No lockfile in repo | `setup-node` with `cache: npm` can fail | Remove `cache: npm` if there is no package lockfile |

## When CI fails

1. Note the run ID from output or notification.
2. View failed logs: `gh run view <RUN_ID> --log-failed`
3. Fix and `git push`, or `gh run rerun <RUN_ID> --failed`

## WANDER_HOME resolution

- Environment variable `WANDER_HOME` if set
- Sibling path: `$(dirname "$REPO_ROOT")/wander` (common in wrappers)
- Default: `~/code/wander`

## Reference

- [Wander README](https://github.com/ERerGB/wander)
- [EDGE_CASES.md](https://github.com/ERerGB/wander/blob/main/EDGE_CASES.md)
- [COFFEE_BREAK.md](https://github.com/ERerGB/wander/blob/main/COFFEE_BREAK.md)
