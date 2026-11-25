# GitHub Actions adapter

Load only when GitHub Actions owns the requested terminal state.
Pin the actual run identity before launching; launch success is not workflow success.

## Prerequisites (GitHub Actions adapter path)

- `gh` CLI installed and authenticated
- `jq` installed; Python 3 for optional registry tooling/tests
- Wander checkout on disk: set `WANDER_HOME` explicitly; `~/code/wander` is an example install path
- macOS for notification center; Linux/headless: output-only mode still works

## Install (Wander / GHA adapter)

```bash
git clone https://github.com/ERerGB/wander.git ~/code/wander
cd ~/code/wander && chmod +x *.sh
```

Add to shell rc:

```bash
export WANDER_HOME="${WANDER_HOME:-$HOME/code/wander}"
export PATH="$WANDER_HOME:$PATH"
alias wf='watch-workflow.sh'
alias wfbg='watch-workflow-bg.sh'
alias wfdt='watch-workflow-detached.sh'
```

---

## Picking the right mode (GHA adapter)

| Mode | Script | Use case |
|------|--------|----------|
| Background | `watch-workflow-bg.sh` | **Default.** Keep working; get notified. |
| Detached | `watch-workflow-detached.sh` | Close terminal; logs to `~/.wander_logs/` |
| Foreground | `watch-workflow.sh` | Block session until done (rare) |

**Rule of thumb**: prefer background. Use detached for **> ~5 min** if the terminal may close.

---

## Workflow registry (`.workflows.yml`, GHA)

The optional registry records descriptive timing hints. Current monitors use `WANDER_MAX_POLLS` and `WANDER_POLL_SECONDS` for their finite wait budget; registry hints do not override it:

```yaml
workflows:
  - name: "ci.yml"
    description: "Lint + unit tests"
    check_window: 180      # grace window if already finished when we start
    expected_duration: 45  # typical runtime
    category: "smoke"

  - name: "build.yml"
    description: "Docker build + push"
    check_window: 600
    expected_duration: 180
    category: "build"

  - name: "deploy.yml"
    description: "Railway deploy"
    check_window: 900
    expected_duration: 300
    category: "deploy"
```

**`check_window`** is retained metadata from the earlier recent-run adapter; current exact-head discovery does not use it. It never establishes that a run belongs to this request. Match repository, workflow, event, branch and exact `headSha` (plus dispatch identity when available), then pin the `databaseId`. A matching recent timestamp alone is insufficient.

**Auto-generate** for a repo:

```bash
cd /path/to/repo
"$WANDER_HOME/scripts-registry.sh" scan-workflows --auto-scope
```

Default metadata `check_window`: 300s. Registry parsing supports the documented block/scalar subset, not YAML anchors or flow mappings. Scanning refuses existing output; choose a new path to review before replacement.

---

## Canonical usage patterns (GHA)

### After git push when CI is on GitHub Actions

```bash
git push origin main && "$WANDER_HOME/watch-workflow-bg.sh" ci.yml
```

### Project wrapper (recommended for teams)

```bash
# scripts/watch-ci.sh
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WANDER_DIR="${WANDER_HOME:-$(dirname "$REPO_ROOT")/wander}"
exec "$WANDER_DIR/watch-workflow-bg.sh" ci.yml "$@"
```

Then: `git push && ./scripts/watch-ci.sh`

### EAS when gated by GHA

If EAS is triggered from a GHA workflow (e.g. `eas-build.yml`):

```bash
git push origin feat/my-branch && "$WANDER_HOME/watch-workflow-bg.sh" eas-build.yml
```

If EAS is **only** CLI-triggered: monitor via **EAS/Expo**-native signals; optional team pattern is still to add a thin GHA `workflow_dispatch` wrapper if you want one uniform monitor.

### Manual workflow dispatch

```bash
# After an authorized dispatch, resolve and inspect its exact run ID/head first:
GH_REPO=owner/repo WANDER_RUN_ID="$RUN_ID" WANDER_HEAD_SHA="$HEAD_SHA" \
  "$WANDER_HOME/watch-workflow-bg.sh" deploy.yml main
```

---

## Edge cases (GHA adapter)

| Scenario | Behavior |
|----------|----------|
| Workflow finishes before monitor starts | A unique exact-head candidate can still be inspected |
| Run not appearing after ~30s | Wander waits, then exits with guidance |
| Wrong branch filter on workflow | No run found; report and stop |
| Multiple candidate runs | Stop and resolve event/dispatch identity; do not choose newest blindly |
| Very long workflow | Prefer detached; logs survive terminal close |

---

## When a task fails (GHA)

```bash
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID> --failed
```

For non-GHA tasks, use the **same meta rule**: pull **that platform's** primary failure surface (build log, deploy log, etc.).

---

## WANDER_HOME resolution

Set `$WANDER_HOME` to the maintained checkout. The project wrapper above uses a sibling only as its own explicit fallback; there is no universal runtime search order.

---


## Monitoring limits and tests

Foreground exits 0 only for verified remote success, 1 for a non-success/error, and 124 after its poll budget with the remote outcome still unknown. Background/detached exit 0 means launch only. Default budget is 120 polls at 10 seconds, excluding API latency; configure positive integers through `WANDER_MAX_POLLS` and `WANDER_POLL_SECONDS`. `nohup` survives terminal close, not computer shutdown/sleep. Detached logs can be directed to `WANDER_LOG_DIR`.

`./test-all-scripts.sh` runs shell syntax and synthetic offline fixtures. It does not dispatch, push, invoke models or send real notifications.
