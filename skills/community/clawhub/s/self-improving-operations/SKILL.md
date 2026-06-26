---
name: self-improving-operations
description: "Captures process bottlenecks, incident patterns, capacity issues, automation gaps, SLA breaches, and toil accumulation to enable continuous operations improvement. Use when: (1) An incident repeats within 30 days, (2) MTTR exceeds target thresholds, (3) A manual step exists in an automated pipeline, (4) Alert fatigue indicates noisy monitoring, (5) Change failure rate spikes, (6) Toil exceeds 50% of on-call time."
---

# Self-Improving Operations Skill

Log operations-specific learnings, incident patterns, and feature requests to markdown files for continuous improvement. Captures process bottlenecks, incident patterns, capacity issues, automation gaps, SLA breaches, and toil accumulation. Important learnings get promoted to runbooks, incident postmortems, automation backlog items, capacity models, on-call handoff checklists, or SLO definitions.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Operations Learnings\n\nProcess bottlenecks, incident patterns, capacity insights, automation gaps, and toil patterns captured during operations work.\n\n**Categories**: process_bottleneck | incident_pattern | capacity_issue | automation_gap | sla_breach | toil_accumulation\n**Areas**: incident_management | change_management | capacity_planning | automation | monitoring | runbooks | on_call\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/OPERATIONS_ISSUES.md ] || printf "# Operations Issues Log\n\nIncidents, outages, SLA breaches, capacity problems, and automation failures.\n\n---\n" > .learnings/OPERATIONS_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nOperations tooling, automation, monitoring, and process improvement requests.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log secrets, credentials, internal IP addresses, or customer data. Prefer redacted excerpts over raw log output. Mask hostnames, account IDs, and PII in all entries.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Same incident repeats within 30 days | Log to `.learnings/OPERATIONS_ISSUES.md` with `incident_pattern` |
| MTTR exceeds target (>4h for P1) | Log to `.learnings/OPERATIONS_ISSUES.md` with root cause analysis |
| Manual step in automated pipeline (>30min) | Log to `.learnings/LEARNINGS.md` with `automation_gap` |
| Alert fatigue (>50 alerts/day same monitor) | Log to `.learnings/LEARNINGS.md` with `monitoring` area |
| Change failure rate spikes (>15%) | Log to `.learnings/LEARNINGS.md` with `change_management` area |
| Toil exceeds 50% of on-call hours | Log to `.learnings/LEARNINGS.md` with `toil_accumulation` |
| Deployment rollback required | Log to `.learnings/OPERATIONS_ISSUES.md` with rollback details |
| Capacity utilization exceeds 85% | Log to `.learnings/OPERATIONS_ISSUES.md` with `capacity_issue` |
| Recurring pattern (3+ occurrences) | Link with `**See Also**`, consider priority bump |
| Broadly applicable operational insight | Promote to runbook, postmortem, or SLO definition |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-operations
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-operations.git ~/.openclaw/skills/self-improving-operations
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows, delegation patterns
├── SOUL.md            # Behavioral guidelines, personality, principles
├── TOOLS.md           # Tool capabilities, integration gotchas
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── OPERATIONS_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — process bottlenecks, incident patterns, automation gaps, toil patterns
- `OPERATIONS_ISSUES.md` — incidents, outages, SLA breaches, capacity problems
- `FEATURE_REQUESTS.md` — operations tools, monitoring, automation capabilities

### Promotion Targets

When operations learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Incident response steps | Runbook | "Database connection pool exhaustion recovery" |
| Root cause findings | Incident postmortem | "Monthly batch job causes OOM in worker pods" |
| Automation candidates | Automation backlog | "Certificate renewal should be fully automated" |
| Resource projections | Capacity model | "Storage grows 15% monthly, need expansion by Q3" |
| Shift handoff gaps | On-call handoff checklist | "Always verify cron job status at shift start" |
| Reliability targets | SLO definition | "API P99 latency must stay below 500ms" |
| Workflow patterns | `AGENTS.md` | "Run pre-deploy checklist before production pushes" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-operations
openclaw hooks enable self-improving-operations
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above.

### Add reference to agent files

Add to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`:

#### Self-Improving Operations Workflow

When operational issues or patterns are discovered:
1. Log to `.learnings/OPERATIONS_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Runbooks — step-by-step incident response procedures
   - Postmortems — blameless root cause analysis documents
   - Automation backlog — toil reduction and automation candidates
   - Capacity models — resource forecasting and scaling plans
   - SLO definitions — reliability targets with error budgets

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: incident_management | change_management | capacity_planning | automation | monitoring | runbooks | on_call

### Summary
One-line description of the operational insight

### Details
Full context: what operational pattern was found, why it matters for reliability,
what the correct process or automation should be. Include relevant metrics.

### Impact
- **Blast Radius**: systems, users, or revenue affected
- **Duration**: how long the issue persisted
- **Error Budget Consumed**: percentage of SLO budget spent

### Metrics
- MTTR: time to resolve
- MTTD: time to detect
- Frequency: how often this occurs
- Toil Hours: manual effort spent per occurrence

### Suggested Action
Specific runbook entry, automation script, SLO threshold, or process change to adopt

### Metadata
- Source: incident | monitoring | capacity_review | change_audit | on_call_handoff | postmortem
- Environment: production | staging | development
- Service: service-name
- Related Alerts: alert-name or monitor-id
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: incident_pattern.connection_pool | automation_gap.cert_renewal (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `process_bottleneck` | Manual step, approval queue, or handoff slows delivery |
| `incident_pattern` | Same or similar incident recurring across time windows |
| `capacity_issue` | Resource exhaustion, scaling limit, or growth projection gap |
| `automation_gap` | Manual task that should be automated (toil candidate) |
| `sla_breach` | SLI/SLO threshold exceeded, error budget exhausted |
| `toil_accumulation` | Repetitive manual work consuming on-call or engineering time |

### Operations Issue Entry [OPS-YYYYMMDD-XXX]

Append to `.learnings/OPERATIONS_ISSUES.md`:

```markdown
## [OPS-YYYYMMDD-XXX] incident_or_issue_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Severity**: P1 | P2 | P3 | P4
**Area**: incident_management | change_management | capacity_planning | automation | monitoring | runbooks | on_call

### Summary
Brief description of the operational issue

### Timeline
| Time (UTC) | Event |
|------------|-------|
| HH:MM | Issue detected / Incident declared / Root cause identified / Mitigated / Restored |

### Impact
- **Users Affected**: count or percentage
- **Duration**: total downtime or degradation window
- **SLO Impact**: error budget consumed (e.g., "consumed 40% of monthly budget")

### Root Cause
What in the system caused this issue. Reference dashboards or logs (redacted).

### Mitigation
Steps taken to restore service (commands, config changes, scaling actions)

### Prevention
How to avoid this in the future (automation, alert, architecture change, runbook update)

### Action Items
- [ ] Action item 1 (owner, deadline)

### Metadata
- Trigger: alert | user_report | monitoring | deployment | capacity_breach
- Environment: production | staging
- Services Affected: service-a, service-b
- Related Incidents: OPS-20250110-001 (if recurring)
- DORA Metrics Impact: deployment_frequency | lead_time | change_failure_rate | mttr

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: incident_management | change_management | capacity_planning | automation | monitoring | runbooks | on_call

### Requested Capability
What operations tool, automation, or capability is needed

### User Context
Why it's needed, what toil it eliminates, estimated hours saved per week

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: script, pipeline stage, monitoring rule, runbook automation, K8s operator

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_capability

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `OPS` (operations issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `OPS-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is resolved, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Postmortem**: link or document reference
- **Notes**: Added runbook / updated SLO / automated remediation / added alert
```

Other status values:
- `in_progress` — Actively being investigated or mitigated
- `wont_fix` — Accepted risk (add reason and risk assessment in Resolution notes)
- `promoted` — Elevated to runbook, postmortem, capacity model, or SLO definition
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**Incident Recurrence** (→ operations issue with incident_pattern):
- Same service incident within 30-day window
- Same alert firing 3+ times in a week
- Same root cause across different services

**MTTR Exceeding Targets** (→ operations issue with severity context):
- P1: MTTR > 4 hours | P2: MTTR > 8 hours | P3: MTTR > 24 hours
- Any incident where MTTD exceeds 30 minutes

**Manual Pipeline Steps** (→ learning with automation_gap):
- Manual approval step taking > 30 minutes
- Copy-paste commands from wiki during deployments
- Manual rollback procedure without automated safeguards

**Alert Fatigue** (→ learning with monitoring area):
- > 50 alerts/day from the same monitor
- Alert acknowledged but no action taken (false positive pattern)

**Change Failure Rate** (→ learning with change_management area):
- Change failure rate > 15% over rolling 7-day window
- Failed deployment requiring rollback

**Toil Accumulation** (→ learning with toil_accumulation):
- On-call engineer spending > 50% of shift on repetitive manual tasks
- Same manual remediation applied 3+ times in a month
- Certificate, credential, or secret rotation done manually

**Capacity Thresholds** (→ operations issue with capacity_issue):
- CPU > 85% sustained > 15 min, memory > 90%, disk > 85%
- Connection pool > 80% during peak hours
- Queue depth growing with consumers not keeping up

**Deployment Issues** (→ operations issue with context):
- Deployment rollback initiated
- Canary showing error rate increase or post-deploy regression

## Priority Guidelines

| Priority | When to Use | Operations Examples |
|----------|-------------|---------------------|
| `critical` | Production outage, data loss, security breach | Full service outage, data corruption, cascading failure, error budget exhausted |
| `high` | SLA breach, recurring incident, capacity limit approaching | P99 latency exceeding SLO, same incident 3rd time in 30 days, disk at 90% |
| `medium` | Automation opportunity, process bottleneck, alert tuning | Manual runbook step taking 30 min, noisy alert needing threshold adjustment |
| `low` | Documentation update, minor toil reduction, process clarification | Runbook missing verification step, on-call handoff checklist incomplete |

## Area Tags

Use to filter learnings by operations domain:

| Area | Scope |
|------|-------|
| `incident_management` | Incident detection, response, communication, resolution, and postmortem |
| `change_management` | Deployment processes, config changes, database migrations, feature flags |
| `capacity_planning` | Resource utilization, scaling strategy, growth forecasting, cost optimization |
| `automation` | Pipeline automation, runbook automation, self-healing, auto-remediation |
| `monitoring` | Alert configuration, SLI collection, dashboards, observability, log analysis |
| `runbooks` | Step-by-step procedures, troubleshooting guides, recovery playbooks |
| `on_call` | Rotation management, escalation policies, handoff procedures, fatigue management |

## SRE Concepts Reference

### SLI / SLO / SLA Hierarchy

| Concept | Definition | Example |
|---------|------------|---------|
| **SLI** (Service Level Indicator) | Quantitative measure of service behavior | Request latency P99, error rate, throughput |
| **SLO** (Service Level Objective) | Target value for an SLI, set internally | "P99 latency < 500ms over 30-day window" |
| **SLA** (Service Level Agreement) | Contractual commitment with consequences | "99.9% uptime or service credits apply" |

Define SLOs before SLAs. SLOs should be stricter than SLAs to provide a buffer.

### Error Budgets

The acceptable amount of unreliability derived from SLOs:
- **100% - SLO = Error Budget** (e.g., 99.9% SLO → 0.1% error budget → ~43 minutes/month)
- When budget is healthy: ship features, take calculated risks
- When budget is low: freeze risky changes, focus on reliability
- When budget is exhausted: halt all non-critical deployments, prioritize stability

### Toil Definition

Work that is manual, repetitive, automatable, tactical, devoid of enduring value, and scales linearly with service growth. Target: toil below 50% of on-call time.

### DORA Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| **Deployment Frequency** | On-demand (multiple/day) | Weekly to monthly | Monthly to biannually | Fewer than biannually |
| **Lead Time for Changes** | < 1 hour | 1 day – 1 week | 1 week – 1 month | 1 – 6 months |
| **Change Failure Rate** | 0–15% | 16–30% | 31–45% | 46–60% |
| **MTTR** | < 1 hour | < 1 day | < 1 week | 1 week – 1 month |

Use DORA metrics to measure improvement over time. Log deviations as operations issues.

## Promoting to Permanent Operations Standards

When a learning is broadly applicable (not a one-off incident), promote it to permanent operational standards.

### When to Promote

- Incident pattern recurs across multiple services or time windows
- Same manual remediation applied 3+ times in a month
- Process bottleneck impacts deployment velocity across teams

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Runbooks | Step-by-step incident response and recovery procedures |
| Incident postmortems | Blameless root cause analysis with action items |
| Automation backlog | Toil candidates ranked by effort saved per automation |
| Capacity models | Resource growth projections with scaling triggers |
| On-call handoff checklists | Shift-start verification items and known issues |
| SLO definitions | Service reliability targets with error budget policies |
| `AGENTS.md` | Automated operational workflows, pre-deploy checks |

### How to Promote

1. **Distill** the learning into an actionable runbook, model, or definition
2. **Add** to appropriate target (runbook entry, postmortem template, SLO doc)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: runbook` (or `postmortem`, `automation backlog`, `capacity model`, `SLO definition`)

### Promotion Examples

**Learning → Runbook:**
> DB connection pool exhaustion during monthly batch ETL. Pool size 50, batch opens 40+ connections.

Promoted to runbook: Check pool utilization (`SELECT count(*) FROM pg_stat_activity`), scale down batch concurrency (`kubectl patch job/monthly-etl -p '{"spec":{"parallelism":2}}'`), permanent fix with PgBouncer and separate connection pools.

**Learning → Automation backlog:**
> On-call spent 12 hours across 4 shifts manually renewing TLS certs for 15 services.

Promoted to automation backlog: cert-manager with Let's Encrypt, 2 days to implement, saves 45 hours/year of toil, eliminates certificate expiry incidents.

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: OPS-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring operations issues often indicate:
   - Missing automation (→ add to automation backlog)
   - Missing runbook (→ create runbook entry)
   - Incorrect SLO threshold (→ review and adjust SLO)
   - Architectural limitation (→ capacity model or architecture review)
   - Missing alert (→ add monitoring rule)

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- After an incident is resolved (during postmortem)
- Before on-call shift handoff
- After completing a deployment or change
- During quarterly SLO review
- When error budget is running low

### Quick Status Check
```bash
grep -h "Status\*\*: pending" .learnings/*.md | wc -l
grep -B5 "Severity\*\*: P1\|Severity\*\*: P2" .learnings/OPERATIONS_ISSUES.md | grep "^## \["
grep -B2 "automation_gap\|toil_accumulation" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve fixed operations issues with postmortem links
- Promote recurring patterns to runbooks
- Update capacity models and adjust SLO thresholds

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in**.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-operations/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects an operations-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-operations/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-operations/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for operational errors like outages, capacity breaches, deployment failures, and SLO violations.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate operational learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on incidents, outages, capacity alerts, deployment failures |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When an operations learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same incident pattern in 2+ services or environments |
| **Verified** | Status is `resolved` with confirmed root cause and working fix |
| **Non-obvious** | Required investigation beyond checking dashboards |
| **Broadly applicable** | Not specific to one service; useful across infrastructure |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-operations/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-operations/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with operations-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

Use conversation signals ("This incident keeps happening", "Save this runbook as a skill") and entry signals (multiple `See Also`, high-priority resolved items, recurring `Pattern-Key`) to identify extraction candidates.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Best Practices

1. **Conduct blameless postmortems** — focus on systemic causes, not individual blame
2. **Automate toil aggressively** — if you do it manually 3 times, automate it
3. **Define SLOs before SLAs** — internal targets should be stricter than customer commitments
4. **Maintain runbooks** — keep them current, test them during game days, include verification steps
5. **Track error budgets** — use them to balance feature velocity and reliability work
6. **Rotate on-call fairly** — equitable distribution, adequate rest, compensatory time off
7. **Rehearse incident response** — run tabletop exercises and chaos engineering experiments
8. **Log immediately** — incident context fades fast after resolution
9. **Include timelines** — timestamps are critical for postmortems and pattern detection
10. **Measure DORA metrics** — track deployment frequency, lead time, change failure rate, and MTTR
11. **Review before on-call shifts** — check `.learnings/` for known issues and recent patterns

## Gitignore Options

**Keep local** (per-team): add `.learnings/` to `.gitignore`.
**Track in repo** (org-wide): don't add to `.gitignore`.
**Hybrid**: ignore `*.md` entries, keep `.gitkeep`.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/operations/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: operations
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (operations)
Only trigger this skill automatically for operations signals such as:
- `incident|on-call|runbook|slo breach|error budget`
- `mttr|postmortem|rollback|service degradation`
- explicit operations intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/operations/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
