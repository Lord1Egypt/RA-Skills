---
name: wander
description: "Close the loop on long-running remote work: pick the right completion signal per platform (CI, EAS, deploy, releases), run monitoring in the background, notify on finish, and never treat trigger as success. Includes GitHub Actions via the Wander scripts when applicable."
---

# Wander — Remote async completion (meta) + GitHub Actions adapter

**Don't watch. Wander.** Philosophy: after you trigger something remote and slow, **completion should find you** — and the Agent must still **verify the outcome**, not assume it.

> **Meta vs implementation:** This skill defines a **portable best practice** for any long-running remote task. **Wander** (`watch-workflow-*.sh`) is the **reference adapter** when the source of truth is **GitHub Actions**. It is not the only valid monitor.

---

## Mental model (first principles)

Every remote async task has the same shape:

```
Trigger  →  Runs elsewhere  →  Terminal state (+ artifacts)
(Agent)     (cannot speed up)   (User + Agent both need this)
```

The Agent should:

1. **Trigger and move on** — do not burn chat turns hand-refreshing UIs.
2. **Attach a monitor** — something that surfaces **done + success/failure** without the user babysitting the tab.
3. **Close the cognitive loop** — when the monitor fires, the Agent reads the **actual result** and acts (ship next step, or diagnose).

**The loop is only complete when the Agent knows the terminal state** (and, for failures, has enough log/context to fix).

1. **Read the monitor output** (terminal log, JSON summary, dashboard link + status scrape — whatever the backend provides).
2. **Act on the result** — do not consider the task "done" until the terminal state is confirmed:
   - ✅ success → proceed (e.g. merge PR, deploy, tag)
   - ❌ failure / cancelled → surface failure, pull logs, propose fix
3. **Never assume success** — "monitor started" ≠ "job succeeded".

---

## Meta protocol — classifying the task before choosing a monitor

**Step A — Identify the system of record** (where does the authoritative status live?)

| Class | Examples | Typical system of record |
|-------|----------|---------------------------|
| Repo CI | lint, tests, build in PR | GitHub Actions, GitLab CI, Buildkite, Circle, … |
| Mobile cloud build | EAS / Xcode Cloud / … | Vendor build detail page, CLI status, webhook, or CI job that wraps the vendor |
| Deploy / PaaS | Fly, Railway, Vercel, k8s rollout | Provider CLI/API, deploy dashboard, or CI deploy job |
| Publish | npm, stores, artifact registries | Store/CI pipeline status, not "upload started" |

**Step B — Pick a completion channel** (lowest friction that preserves auditability)

1. **CI-as-facade** — If the team already gates quality on a CI run, monitoring that run is often best *even when* the heavy work is EAS/Railway/etc. (wrapper job or `workflow_dispatch`).
2. **Vendor-native CLI/API** — e.g. poll build ID until `finished` / `errored` when there is **no** CI wrapper and the vendor is authoritative.
3. **Dashboard + explicit handoff** — Acceptable when automation is impossible; still require a **named status** from the user or a single checked URL — not vibes.

**Step C — Run the monitor in the background** unless the user asked to block the session.

**Step D — After completion, fetch failure detail** from that same system of record (failed step logs, EAS error page, deploy logs).

Do **not** default to "must be GitHub Actions" at Step A. Default to: **whatever platform actually owns the terminal state** for *this* trigger.

---

## Reference adapter: GitHub Actions via Wander

When the authoritative run **is** a GitHub Actions workflow (push, `workflow_run`, `workflow_dispatch`, etc.), use the Wander scripts as the monitor:

```bash
# After Wander background process exits, check result:
gh run view <RUN_ID> --json conclusion -q .conclusion
# → "success" | "failure" | "cancelled" | "timed_out"

# If failure, fetch logs for Agent to diagnose:
gh run view <RUN_ID> --log-failed
```

**Task taxonomy** — examples (GHA column = when Wander adapter applies directly):

| Task type | Examples | Wander (GHA) |
|-----------|----------|----------------|
| CI test | lint, unit test, e2e | ✅ When workflow is on GHA |
| Build | Docker, web bundle | ✅ When workflow is on GHA |
| Mobile build | EAS iOS/Android | ⚠️ Often indirect: GHA wrapper *or* vendor CLI/dashboard |
| Deploy | Railway, Fly, Vercel | ✅/⚠️ CI job or provider-native |
| Release / publish | npm, store upload | ✅/⚠️ Same split as above |

For EAS invoked **only** via CLI with no GHA: Wander scripts do not apply — use **EAS/Expo** status (`eas build:list`, build URL, or project automation) per project docs.

**Engine note:** The [`wander` repo](https://github.com/ERerGB/wander) today implements **GitHub Actions** polling + notifications. Other backends belong here as **additional adapters** (future) or as **project-specific scripts** that follow the same meta protocol.

Scope details: [v1 scope: GitHub Actions today](https://github.com/ERerGB/wander/blob/main/README.md#v1-scope-github-actions-today).

---

## Agent auto-trigger — gate on task class, not on "always GHA"

**After triggering a long-running remote task**, attach monitoring **appropriate to that task's system of record** — unless the user opts out or the task is trivially short.

**If** the triggered work is clearly **GitHub Actions** (or is wrapped entirely in a GHA workflow the Agent just started):

1. Check `.workflows.yml` if present → pick workflow + timing.
2. If absent but `.github/workflows/` exists → identify the workflow (registry scan or ask), then start monitoring.
3. Use `watch-workflow-bg.sh <workflow.yml>` — background unless the user wants to block.
4. After ~8s, peek terminal output / run id and report initial status.
5. Tell the user: "Watching `<workflow>` on GitHub Actions; I'll notify when it finishes — you can keep working."
6. **Until terminal state is known:** check monitor output or `gh run view <RUN_ID> --json conclusion`. Do not declare success prematurely.
7. **On result:** success → next step; failure → `gh run view <RUN_ID> --log-failed` (or equivalent) and propose fix.

**If** the work is **not** GHA (raw EAS CLI, provider-only deploy, etc.):

- Do **not** force-fit `watch-workflow-bg.sh`.
- Use vendor CLI/API poll, project script, or agree with the user on the dashboard URL — still **background** where possible and still **verify terminal state** after.

If `.github/workflows/` does not exist: **do not** auto-start Wander; choose another monitor per Step A–B above.

---

## When to use this skill

- Any remote async task likely **> ~30s**
- User wants notification when "build / CI / deploy / release" finishes
- User is about to manually refresh a dashboard — offer a **structured** monitor instead
- Multi-step flows where the next step **depends** on pass/fail

## When NOT to use

- Task completes in **< ~10s** (wait inline)
- **Purely local** command with immediate exit code
- User explicitly wants **synchronous** blocking output in chat
- No path to **objective** terminal state (undefined trigger / unknown platform) — clarify first

---

## Prerequisites (GitHub Actions adapter path)

- `gh` CLI installed and authenticated
- `jq` installed
- Wander on disk: `WANDER_HOME` (default `~/code/wander`)
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

Each workflow has different timing. The registry tells the GHA adapter what to expect:

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

**`check_window`** = if the workflow already finished before monitoring starts, how far back we still accept the run as "ours". Often ~**6×** `expected_duration`.

**Auto-generate** for a repo:

```bash
cd /path/to/repo
"$WANDER_HOME/scripts-registry.sh" scan-workflows --auto-scope
```

Default `check_window` when unconfigured: 300s.

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
gh workflow run deploy.yml --ref main
"$WANDER_HOME/watch-workflow-bg.sh" deploy.yml main
```

---

## Edge cases (GHA adapter)

| Scenario | Behavior |
|----------|----------|
| Workflow finishes before monitor starts | `check_window` may catch it; notify quickly |
| Run not appearing after ~30s | Wander waits, then exits with guidance |
| Wrong branch filter on workflow | No run found; report and stop |
| Very short workflow | Often caught immediately via `check_window` |
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

1. `$WANDER_HOME` env var
2. Sibling of current repo: `$(dirname "$REPO_ROOT")/wander`
3. Default: `~/code/wander`

---

## Evolution: adapters beyond GitHub Actions

The **meta protocol** is stable. **Adapters** are replaceable:

- Today: Wander = GHA polling + desktop notify.
- Tomorrow: EAS CLI watcher, deploy webhooks → notify bridge, etc.

Until an adapter exists, prefer **CI-as-facade** or **vendor-native poll** — not silent assumption of success.

---

## Reference

- [Wander README](https://github.com/ERerGB/wander)
- [EDGE_CASES.md](https://github.com/ERerGB/wander/blob/main/EDGE_CASES.md)
- [COFFEE_BREAK.md](https://github.com/ERerGB/wander/blob/main/COFFEE_BREAK.md)
