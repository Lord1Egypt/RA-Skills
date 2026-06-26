---
name: runbook-automator
description: Convert manual incident runbooks into automated, executable playbooks. Parse existing runbooks, generate scripts for each step, add health checks, rollback procedures, and notification hooks.
---

# Runbook Automator

Transform manual runbooks into automated, executable playbooks. Parse existing documentation, generate step-by-step scripts with health checks, decision points, rollback procedures, and notification hooks — so incidents get resolved faster with less human intervention.

Use when: "automate this runbook", "convert runbook to script", "make this playbook executable", "incident automation", "turn this wiki page into a script", or when building on-call automation.

## Commands

### 1. `convert` — Parse Runbook and Generate Automation

#### Step 1: Identify Runbook Format

Read the input runbook (markdown, Confluence wiki, Google Doc, plain text) and extract:
- **Title and scope** — what incident does this address
- **Prerequisites** — access, tools, permissions needed
- **Steps** — ordered actions (distinguish manual vs automatable)
- **Decision points** — if/then branches
- **Verification steps** — how to confirm each step worked
- **Rollback steps** — how to undo if things go wrong
- **Escalation criteria** — when to page someone

#### Step 2: Classify Each Step

For each step in the runbook, classify as:

| Type | Example | Automation |
|------|---------|------------|
| **Command** | "Run `kubectl rollout restart`" | Direct script execution |
| **Check** | "Verify pods are running" | Script with assertion |
| **Decision** | "If error rate > 5%, proceed to step 4" | Conditional branch |
| **Manual** | "Call the database team" | Notification + pause |
| **Observation** | "Watch the dashboard for 10 minutes" | Timed wait + metric check |

#### Step 3: Generate Executable Playbook

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================
# Automated Runbook: [Title]
# Generated from: [source document]
# Last updated: [date]
# ============================================

SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
PAGERDUTY_KEY="${PAGERDUTY_KEY:-}"
DRY_RUN="${DRY_RUN:-false}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
notify() {
  log "NOTIFY: $1"
  if [[ -n "$SLACK_WEBHOOK" ]]; then
    curl -s -X POST "$SLACK_WEBHOOK" -H 'Content-Type: application/json' \
      -d "{\"text\": \"🔧 Runbook: $1\"}" > /dev/null
  fi
}
fail() { notify "❌ FAILED at step $1: $2"; exit 1; }

# --- Step 1: [Name] ---
step_1() {
  log "Step 1: [description]"
  if [[ "$DRY_RUN" == "true" ]]; then
    log "DRY RUN: would execute [command]"
    return 0
  fi
  # [actual command]
  [command] || fail 1 "[error description]"
  # Verify
  [verification command] || fail 1 "Verification failed"
  log "Step 1: ✅ Complete"
}

# --- Step 2: [Decision Point] ---
step_2() {
  log "Step 2: Checking [condition]"
  local metric
  metric=$([check command])
  if (( $(echo "$metric > 5" | bc -l) )); then
    log "Threshold exceeded ($metric > 5) — escalating"
    step_2a  # escalation path
  else
    log "Within bounds ($metric <= 5) — continuing"
    step_3
  fi
}

# --- Rollback ---
rollback() {
  notify "🔄 Rolling back..."
  log "Rollback: [undo commands]"
  [rollback command 1]
  [rollback command 2]
  notify "Rollback complete"
}

trap 'rollback' ERR

# --- Execute ---
notify "Starting runbook: [Title]"
step_1
step_2
# ... remaining steps
notify "✅ Runbook complete"
```

### 2. `analyze` — Audit Existing Runbooks for Gaps

Read all runbooks in a directory and flag:

```bash
# Find runbook-like documents
find . -maxdepth 3 \( -name "*.md" -o -name "*.txt" -o -name "*.adoc" \) | \
  xargs grep -li "runbook\|playbook\|incident\|on-call\|troubleshoot" 2>/dev/null
```

For each runbook, check:
- **Missing rollback steps** — what happens if step 3 fails?
- **No verification** — steps that say "do X" but never check if X worked
- **Stale commands** — references to deprecated tools, old hostnames, removed services
- **Missing decision criteria** — "if it's bad, escalate" (how bad? what metric?)
- **No estimated time** — SLA-critical runbooks need time bounds per step
- **Missing prerequisites** — assumed access or tools not listed

Output a coverage report:
```markdown
# Runbook Audit Report

| Runbook | Steps | Automated | Rollback | Verified | Gaps |
|---------|-------|-----------|----------|----------|------|
| DB Failover | 8 | 3/8 (38%) | ✅ | 5/8 | Stale hostname in step 4 |
| API Scale-Up | 5 | 5/5 (100%) | ❌ Missing | 4/5 | No rollback procedure |
| Cache Flush | 3 | 2/3 (67%) | ✅ | 3/3 | Step 2 references removed tool |
```

### 3. `test` — Dry-Run a Generated Playbook

Execute the generated script with `DRY_RUN=true`:
- Validate all commands exist in PATH
- Check prerequisite access (can reach hosts, have credentials)
- Verify notification hooks work (send test message)
- Estimate execution time based on sleep/wait steps
- Flag any steps that would require manual intervention

### 4. `template` — Generate Runbook Template

Given an incident type (database, network, application, security), generate a structured template with:
- Standard sections (scope, impact, prerequisites, steps, rollback, escalation)
- Common steps for that incident type pre-filled
- Placeholder verification commands
- Notification hooks
- Post-incident review checklist
