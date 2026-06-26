---
name: swarm-layer
description: "OpenClaw Swarm Layer: spec-driven workflow orchestration with ACP-first execution, supervised autopilot control plane, manual fallback, persistent sessions, review gates, automatic retry, parallel dispatch, reject-retry workflows, ACP concurrency protection, harness patterns, cross-session continuity, and operator reporting. Covers setup, operation, diagnosis, and reporting."
---

# OpenClaw Swarm Layer

Turn workflow specifications into executable task graphs. Dispatch tasks through manual fallback or ACP automation. Supervise execution through an optional autopilot control plane. Track execution via persistent sessions with reuse and thread binding. Gate completion with review approval. Auto-retry on failure. Generate reports to local disk and Obsidian.

Current release baseline: `openclaw-swarm-layer@0.5.12`, validated on OpenClaw local mini `2026.6.5` with startup tool contracts, plugin doctor checks, conservative ACP failure mapping, artifact-acceptance smoke (positive note-producing task plus negative missing-artifact task on a live ACP backend), unique-bridge-session smoke, parallel admission checks, and the full unit/e2e regression suite.

## What It Does

- **Spec-driven planning** — Write a Markdown spec with goals and phased tasks → generates a dependency-ordered task graph, including explicit `[parallel]` phase barriers
- **Multi-runner execution** — Manual (operator-driven safe fallback) and ACP (default-capable automation path)
- **Session management** — Persistent sessions with binding-key reuse, thread-bound follow-up, and steering messages
- **Review gates** — Tasks require explicit approve/reject; structured quality rubrics for weighted multi-dimension scoring
- **Sprint contracts** — Negotiated verifiable acceptance criteria per task with automated evaluator injection (GAN-inspired pattern)
- **Artifact acceptance** — Optional `expectedArtifacts` (absolute paths or globs) per task; a completed ACP run with missing artifacts is downgraded to `failed` with `failure.source: "artifact-validation"` instead of reaching `done`
- **Cross-session continuity** — Progress summary synthesis, bootstrap startup sequence, harness assumption tracking
- **Protective guardrails** — Task field immutability guard, session budget control (duration + retries)
- **Automatic retry** — Configurable per-task retry policy with dead letter tracking for exhausted tasks
- **Concurrency protection** — ACP session concurrency limits with queued task scheduling (FIFO)
- **Reject-retry workflow** — Review rejections return tasks to ready for re-run; configurable retry limits
- **Parallel dispatch** — `--parallel N` and `--all-ready` batch dispatch with concurrency-aware queued-task drain
- **Autopilot control plane** — Supervised `status/start/pause/resume/stop/tick` flows with lease-backed decisions, optional watcher-driven ticks, and degraded-mode holds
- **Operator reports** — Status snapshots, run logs, review logs, spec archives, completion summaries → local + Obsidian sync

## What It Does NOT Do

- Not a distributed multi-node orchestrator — single machine, single project
- Not a CI/CD pipeline — no git push, PR creation, or deployment automation
- Not an autonomous PR factory — operator stays in the loop for review decisions

## Install

Three installation paths:

**ClawHub** (skill only):
```bash
openclaw skills install swarm-layer
```

**ClawHub package** (full plugin):
```bash
openclaw plugins install clawhub:openclaw-swarm-layer
```

**npm** (full plugin):
```bash
npm install openclaw-swarm-layer
openclaw plugins install -l node_modules/openclaw-swarm-layer
```

**GitHub** (source):
```bash
git clone https://github.com/xucheng/openclaw-swarm-layer.git
cd openclaw-swarm-layer && npm install && npm run build
openclaw plugins install -l /path/to/openclaw-swarm-layer
```

After install, verify: `openclaw plugins info openclaw-swarm-layer` should show `Status: loaded`.

## End-to-End Example

```bash
# 1. Initialize
openclaw swarm init --project <TEMP_DIR>/my-project

# 2. Write a spec
cat > <TEMP_DIR>/my-project/SPEC.md << 'EOF'
# Feature Build
## Goals
- Implement and test the new feature
## Phases
### Implement
- Write the core logic
### Test
- Run unit tests
EOF

# 3. Plan
openclaw swarm plan --project <TEMP_DIR>/my-project --spec <TEMP_DIR>/my-project/SPEC.md
# → specId: feature-build, taskCount: 2

# 4. Execute first task
openclaw swarm run --project <TEMP_DIR>/my-project --runner acp
# → action: dispatched, runId: implement-task-1-run-...

# 5. Poll until complete
openclaw swarm session status --project <TEMP_DIR>/my-project --run <runId>
# → status: completed

# 6. Approve
openclaw swarm review --project <TEMP_DIR>/my-project --task <taskId> --approve
# → status: done

# 7. Execute next task, repeat steps 4-6

# 8. View report
openclaw swarm report --project <TEMP_DIR>/my-project
```

## Links

- **GitHub**: https://github.com/xucheng/openclaw-swarm-layer
- **npm**: https://www.npmjs.com/package/openclaw-swarm-layer
- **Docs**: https://github.com/xucheng/openclaw-swarm-layer/tree/main/docs
- **Issues**: https://github.com/xucheng/openclaw-swarm-layer/issues
- **ClawHub**: https://clawhub.ai/skills/swarm-layer

---

## Module Router

Determine which module to use based on what the user needs:

| User Intent | Module | Key Commands |
|------------|--------|-------------|
| Install, configure, initialize | [Setup](#setup) | `plugins install`, `doctor`, `init` |
| Plan, execute, review, session ops | [Operate](#operate) | `plan`, `run`, `review`, `session *` |
| Supervised automation control | [Operate](#operate) | `autopilot status/start/pause/resume/stop/tick` |
| Something broken, stuck, or failing | [Diagnose](#diagnose) | `doctor`, `session status/cancel/cleanup` |
| Check progress, read reports | [Report](#report) | `status`, `report`, `session list/inspect` |

When unsure, start with `openclaw swarm status --project .` to assess the situation.

---

# Setup

## When to Use
First-time install, ACP configuration, project initialization, or config troubleshooting.

## Flow

### 1. Prerequisites
```bash
node --version     # >= 22
openclaw --version # >= 2026.3.22
```

The `0.5.12` release was smoke-tested on OpenClaw local mini `2026.6.5` with a Daily Papers-style live ACP workload.

### 2. Install Plugin
```bash
openclaw plugins install clawhub:openclaw-swarm-layer   # Published package
openclaw plugins install -l /path/to/openclaw-swarm-layer
openclaw plugins info openclaw-swarm-layer   # Should show Status: loaded
```

### 3. Configure ACP Public Path
```json
{
  "plugins": { "entries": { "openclaw-swarm-layer": { "config": {
    "defaultRunner": "auto",
    "acp": {
      "enabled": true,
      "defaultAgentId": "codex",
      "allowedAgents": ["codex"],
      "defaultMode": "run",
      "defaultRuntimeMode": "auto"
    }
  }}}}
}
```

### 4. Verify
```bash
openclaw swarm doctor --json
# severity should be "healthy" or "warning", not "blocked"
```

### 5. Initialize Project
```bash
openclaw swarm init --project .
```

### 6. Optional: Obsidian Sync + Journal
```json
{
  "obsidianRoot": "/path/to/vault/reports",
  "journal": {
    "enableRunLog": true,
    "enableReviewLog": true,
    "enableSpecArchive": true,
    "enableCompletionSummary": true
  }
}
```

### Setup Troubleshooting
- **Plugin not loading** → `openclaw plugins info openclaw-swarm-layer`
- **ACP unavailable** → `openclaw swarm doctor --json`, confirm public ACP export readiness and runner resolution
- **ACP stuck in read-only** → set `acp.defaultRuntimeMode` to `auto` for Codex-backed workflow tasks
- **Legacy bridge config warning** → remove `bridge.acpFallbackEnabled` after confirming ACP public path is ready

---

# Operate

## When to Use
Plan and execute workflows, manage sessions, complete review cycles.

## Core Loop

```
Write Spec → Plan → Status → Run → Poll Session → Review → Repeat
```

### Write a Spec
```markdown
# My Workflow
## Goals
- What to achieve
## Phases
### Phase 1
- Task A
- Task B
```

### Plan → Run → Review
```bash
openclaw swarm plan --project . --spec SPEC.md      # Import and generate tasks
openclaw swarm status --project . --sync              # Sync active runs, then see what's ready
openclaw swarm run --project . --sync-active --dry-run # Preview after active-run sync
openclaw swarm run --project . --sync-active --runner acp # Execute (acp/manual)
openclaw swarm run --project . --sync-active --parallel 3 # Dispatch up to 3 ready/queued tasks
openclaw swarm run --project . --sync-active --all-ready # Fill all available concurrency slots
openclaw swarm session status --project . --run <id>  # Poll until complete
openclaw swarm review --project . --task <id> --approve
openclaw swarm review --project . --task <id> --reject --retry-now  # Reject and force retry
```

### Autopilot Control Plane
```bash
openclaw swarm autopilot status --project .           # Health + last decision
openclaw swarm autopilot start --project .            # Start supervised loop
openclaw swarm autopilot pause --project . --reason "operator review"
openclaw swarm autopilot resume --project .
openclaw swarm autopilot tick --project . --dry-run   # Inspect next actions without mutating state
openclaw swarm autopilot stop --project . --mode graceful
```

Use autopilot when you want the workflow to keep progressing under policy control instead of manually calling `run`, `session status`, and recovery commands one by one.

Optional watcher mode:

```json
{
  "autopilot": {
    "enabled": true,
    "watcherMode": "hybrid",
    "watcher": {
      "debounceMs": 100,
      "safetyTickMs": 300000,
      "library": "auto"
    }
  }
}
```

Use `watcherMode: "polling"` as the rollback path.

### Runner Selection
| Runner | Use When |
|--------|----------|
| `manual` | Safe explicit fallback when ACP automation is unavailable or not desired |
| `acp` | Default-capable automation path through the public ACP control-plane |

### Session Operations
```bash
session list --project .                                    # List all
session inspect --project . --session <id>                  # Details
session follow-up --project . --session <id> --task <desc>  # Inject task
session steer --project . --session <id> --message <text>   # Redirect
session cancel --project . --run <id>                       # Abort
session cleanup --project . --stale-minutes 60              # Clean orphans
```

### Session Policies
| Policy | Behavior |
|--------|----------|
| `none` | New session each run (default) |
| `create_persistent` | Creates reusable persistent session |
| `reuse_if_available` | Reuse idle persistent session if match found |
| `require_existing` | Fail if no matching session exists |

### Harness Enhancement (GAN-Inspired Patterns)

Enable advanced harness features for long-running agent orchestration:

```json
{
  "enforceTaskImmutability": true,
  "bootstrap": { "enabled": true },
  "evaluator": { "enabled": true, "autoInjectAfter": ["coding"] }
}
```

**Sprint Contracts** — Add `Acceptance Criteria` to your spec. `plan` auto-generates a `SprintContract` with verifiable criteria attached to coding tasks.

**Evaluator Injection** — When `evaluator.enabled`, each coding task gets an auto-injected `-eval` task that validates the contract. Dependency chains adjust automatically:
```
coding-task → coding-task-eval → next-task
```

**Quality Rubrics** — Replace binary approve/reject with 4-dimension weighted scoring:
- functionality (0.3) / correctness (0.3) / design (0.2) / craft (0.2)
- Weighted total >= 6.0 → approve; < 6.0 → reject

**Cross-Session Progress** — `progress.json` auto-updated after each `run` and `review`. Bootstrap sequence loads progress on startup: verify env → load progress → select task → verify baseline.

**Task Immutability** — When `enforceTaskImmutability` is enabled, agents cannot mutate task definitions (title, deps, runner, etc.). Only `status`, `review.status`, and `contract.criteria[].passes` are mutable.

**Session Budget** — Set `runner.budget.maxDurationSeconds` and `runner.budget.maxRetries` per task. Exceeded budgets annotate `[BUDGET EXCEEDED]` on run records.

**Assumption Tracking** — `WorkflowState.assumptions` tracks model capability, environment, tooling, and workflow structure assumptions with validation lifecycle.

### Conversational Patterns
| User Says | Do This |
|-----------|---------|
| "start a new workflow" | Help write spec → `plan` → `status` |
| "run the next task" | `status` → dry-run → `run` |
| "what's happening?" | `status` → `session status` for running tasks |
| "approve everything" | List review queue → approve each |
| "enable harness mode" | Add evaluator + immutability + bootstrap config |
| "something is stuck" | → [Diagnose](#diagnose) module |

---

# Diagnose

## When to Use
Tasks stuck, ACP readiness failures, sessions not updating, dead letters, orphans.

## Diagnostic Flow

```
1. openclaw swarm doctor --json      → Check ACP readiness and bridge-exit health
2. openclaw swarm status --project . → Find abnormal tasks/sessions
3. Investigate specific issue (see below)
```

### Doctor Severity
| Severity | Meaning | Action |
|----------|---------|--------|
| `healthy` | All good | None |
| `warning` | Works but risky | Address warnings when convenient |
| `blocked` | Cannot execute | Follow `remediation` immediately |

### Issue Resolution

**Legacy bridge compatibility warning:**
- `doctor --json` → check `warnings` / `remediation`
- Common: remove stale `bridge.acpFallbackEnabled`, or clean up old `versionAllow`/`openclawRoot` metadata

**Stuck running task:**
```bash
swarm session status --project . --run <runId>   # Check if session died
swarm session cancel --project . --run <runId>   # Force cancel if hung
```

**Dead letter task** (retries exhausted):
- `swarm status` → find `dead_letter` tasks
- Fix root cause → manually reset task to `ready`

**Orphaned sessions** (stale active):
```bash
swarm session cleanup --project . --stale-minutes 60
```

**Version drift** (after OpenClaw upgrade):
```bash
swarm doctor --json
# Remove stale bridge metadata if present → rerun doctor → verify runner resolution
```

---

# Report

## When to Use
Check progress, generate reports, understand session inventory.

## Quick Check
```bash
openclaw swarm status --project .  # Structured summary
openclaw swarm report --project .  # Full Markdown report
```

## Report Sections
| Section | Content |
|---------|---------|
| **Attention** | Items needing action: review / blocked / running / dead_letter |
| **Tasks** | All tasks with current status |
| **Review Queue** | Tasks awaiting approve/reject |
| **Highlights** | Notable terminal events (completed/failed/cancelled) |
| **Recommended Actions** | What to do next |
| **Recent Runs** | Last 5 runs |
| **Sessions** | Last 5 sessions with state |
| **Session Reuse Candidates** | Which tasks can reuse which sessions |

## Report Files
| File | Trigger | Mode |
|------|---------|------|
| `swarm-report.md` | Every operation | Overwrite |
| `run-log.md` | `swarm run` | Append |
| `review-log.md` | `swarm review` | Append |
| `specs/<specId>.md` | `swarm plan` | Create once |
| `completion-summary.md` | All tasks done | Overwrite |

Local: `<project>/.openclaw/swarm/reports/` (always)
Obsidian: `<obsidianRoot>/<project>/` (optional async mirror)

## Conversational Patterns
| User Says | Do This |
|-----------|---------|
| "what's the status?" | `status` → summarize counts + attention |
| "show me the report" | `report` → read and present key sections |
| "what needs attention?" | `status` → focus on `attention` array |
| "how are sessions?" | `status` → show session counts + recent |

---

# Tools Reference

For AI tool calling. All tools accept `--json` for structured output.

| Tool | Parameters | Purpose |
|------|-----------|---------|
| `swarm_status` | `project`, `sync?` | Workflow status with optional active-run sync and attention items |
| `swarm_task_plan` | `project`, `spec` | Import spec, generate task graph |
| `swarm_run` | `project`, `task?`, `dryRun?`, `parallel?`, `allReady?`, `syncActive?` | Sync active runs when requested, then dispatch runnable or queued tasks |
| `swarm_review_gate` | `project`, `task`, `approve?`, `reject?`, `note?` | Approve/reject review (reject returns to ready by default) |
| `swarm_session_status` | `project`, `run` | Poll session status |
| `swarm_session_cancel` | `project`, `run`, `reason?` | Cancel session |
| `swarm_session_close` | `project`, `run`, `reason?` | Close session |
