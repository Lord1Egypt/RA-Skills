---
name: self-improving-business
description: "Captures business administration issues, policy gaps, KPI misalignment, decision delays, handoff failures, and stakeholder misalignment to improve operational decision quality. Use when: (1) approval or execution bottlenecks appear, (2) KPI definitions conflict across teams, (3) process governance is inconsistent, (4) SLA commitments are missed or trending late, (5) budget variance requires triage, (6) vendor or cross-team handoff breaks, (7) policy documentation drifts from actual practice."
---

# Self-Improving Business Skill

Log business administration learnings, operational issues, and governance improvements to markdown files for continuous improvement. This skill focuses on business administration operations, cross-functional coordination, process governance, KPI tracking, execution risk, policy consistency, stakeholder communication, and operational decision quality.

## CRITICAL: Safety Posture (Reminder-Only)

This skill is documentation and reminder only.

It does **not** execute or authorize:

- spending approvals
- vendor commitments
- payroll actions
- legal actions
- procurement commitments
- policy sign-offs
- executive approvals

Use this skill to capture structured findings and recommendations. Human owners remain responsible for all high-impact business decisions.

**Always require explicit human approval for high-impact decisions**, including:

- budget reallocations
- vendor selection or termination
- policy exceptions
- operating model changes
- governance escalations
- staffing or compensation effects

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Business Learnings\n\nBusiness administration learnings across process, governance, KPI tracking, and decision quality.\n\n**Categories**: process_breakdown | policy_gap | kpi_misalignment | decision_latency | handoff_failure | stakeholder_misalignment | documentation_drift | compliance_oversight\n**Areas**: planning | execution | governance | reporting | operations | budgeting | procurement | vendor_management | risk_management | communication\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/BUSINESS_ISSUES.md ] || printf "# Business Issues Log\n\nOperational execution issues, policy inconsistencies, KPI risks, and governance concerns.\n\n---\n" > .learnings/BUSINESS_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Business Operations Feature Requests\n\nBusiness administration automation and process-improvement requests.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not treat this skill as an approval engine. It is a structured learning and reminder system only.

If you want automatic reminders, use the opt-in workflow in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Missed SLA in operational workflow | Log to `.learnings/BUSINESS_ISSUES.md` with `decision_latency` or `process_breakdown` |
| KPI value disputed due to conflicting definitions | Log to `.learnings/LEARNINGS.md` with `kpi_misalignment` |
| Policy exists but team did not follow it | Log to `.learnings/BUSINESS_ISSUES.md` with `policy_gap` |
| Handoff failed between departments | Log to `.learnings/BUSINESS_ISSUES.md` with `handoff_failure` |
| Stakeholder expectations diverge from execution plan | Log to `.learnings/LEARNINGS.md` with `stakeholder_misalignment` |
| Dashboard differs from source-of-truth report | Log to `.learnings/LEARNINGS.md` with `documentation_drift` |
| Compliance or audit requirement missed in workflow | Log to `.learnings/BUSINESS_ISSUES.md` with `compliance_oversight` |
| Similar entry already exists | Add `**See Also**`, increase recurrence metadata |
| Reusable operating guidance emerges | Promote to playbook/checklist/KPI registry/RACI/cadence artifact |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-business
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-business.git ~/.openclaw/skills/self-improving-business
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` - reusable business learnings and governance improvements
- `BUSINESS_ISSUES.md` - execution problems, policy misses, and risk items
- `FEATURE_REQUESTS.md` - requested capabilities for administration workflows

### Promotion Targets

When business patterns are broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Repeatable cross-team process | Process playbooks | "Procurement intake triage in 2 business days" |
| Governance controls and checks | Governance checklists | "Quarterly policy attestation for budget owners" |
| KPI definition clarity | KPI definition registry | "On-time delivery = committed date at order acceptance" |
| Ownership ambiguity resolution | RACI matrix updates | "Vendor SLA exceptions accountable by Operations Director" |
| Execution rhythm improvements | Operating cadences | "Weekly risk triage + monthly KPI review forum" |
| Agent collaboration pattern | `AGENTS.md` | "Route budgeting conflicts to governance triage agent" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-business
openclaw hooks enable self-improving-business
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above.

### Agent file reminder

Add a short note in `AGENTS.md` or `CLAUDE.md` to log LRN/BUS/FEAT entries and keep this workflow reminder-only with human approval for high-impact decisions.

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: planning | execution | governance | reporting | operations | budgeting | procurement | vendor_management | risk_management | communication

### Summary
One-line description of the business learning

### Details
Context of the finding: what happened, which teams were involved, where the process,
policy, KPI definition, or communication failed, and what improved outcome is expected.

### Recommended Action
Specific process correction, governance control, KPI definition update, or cadence change.
Reminder-only: this does not execute approvals.

### Metadata
- Source: meeting_review | retrospective | dashboard_audit | vendor_sync | finance_review | incident_postmortem
- Stakeholders: operations | finance | procurement | legal | hr | product | sales
- Related Files: path/to/process.md, path/to/report.csv
- Tags: tag1, tag2
- See Also: LRN-20260413-001
- Pattern-Key: ops.handoff_failure | kpi.definition_mismatch (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2026-04-13 (optional)
- Last-Seen: 2026-04-13 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `process_breakdown` | A repeatable business process fails due to missing or weak controls |
| `policy_gap` | Existing policy is absent, unclear, or not operationalized |
| `kpi_misalignment` | KPI meaning, source, or target differs across functions |
| `decision_latency` | Decision gates are consistently delayed and impact execution |
| `handoff_failure` | Work transfer between teams causes errors or delays |
| `stakeholder_misalignment` | Stakeholders disagree on goals, scope, or priorities |
| `documentation_drift` | Documentation diverges from actual process or system behavior |
| `compliance_oversight` | Internal or external compliance expectations are not met |

### Business Issue Entry [BUS-YYYYMMDD-XXX]

Append to `.learnings/BUSINESS_ISSUES.md`:

```markdown
## [BUS-YYYYMMDD-XXX] issue_type

**Logged**: ISO-8601 timestamp
**Priority**: critical | high | medium | low
**Status**: pending
**Area**: planning | execution | governance | reporting | operations | budgeting | procurement | vendor_management | risk_management | communication
**Severity**: critical | high | medium | low

### Summary
Brief description of the business issue

### Issue Details
What happened, why it matters, where dependencies broke, and what operational risk emerged.
Keep this as a documented finding and recommendation; this skill does not execute decisions.

### Impact Assessment
- Affected functions and owners
- KPI or SLA impact estimate
- Cost or budget impact range
- Governance or compliance implication

### Recommended Action
- Immediate containment steps
- Owner + escalation path
- Long-term process hardening
- Human approval required for any high-impact decisions

### Timeline
- **Identified**: ISO-8601
- **Escalated**: ISO-8601 (if applicable)
- **Resolved**: ISO-8601 (if applicable)

### Metadata
- Trigger: sla_miss | approval_delay | raci_conflict | kpi_variance | budget_alert | handoff_block | policy_missing | audit_finding | dependency_blocked
- Stakeholders: operations | finance | procurement | vendor_management | compliance | leadership
- Related Files: path/to/doc
- See Also: BUS-20260413-001

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: planning | execution | governance | reporting | operations | budgeting | procurement | vendor_management | risk_management | communication

### Requested Capability
What business administration capability is needed

### Business Justification
Why it improves speed, quality, policy consistency, or risk reduction

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: workflow automation, dashboard guardrails, dependency tracker,
handoff checklist, policy linting, governance workflow reminders.

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_feature
- Benefit: cycle_time | decision_quality | risk_reduction | policy_consistency

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `BUS` (business issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (for example `001`, `A7B`)

Examples: `LRN-20260413-001`, `BUS-20260413-A3F`, `FEAT-20260413-002`

## Resolving Entries

When an issue is resolved, update the entry:

1. Change `**Status**: pending` to `**Status**: resolved`
2. Add a resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2026-04-13T09:00:00Z
- **Action Taken**: Brief description of process or governance fix
- **Artifact Updated**: Playbook/checklist/KPI registry/RACI/cadence reference
- **Verified By**: operations review | finance review | governance committee | internal audit
```

Other status values:
- `in_progress` - actively being remediated
- `wont_fix` - risk accepted with documented rationale and human approver
- `promoted` - elevated to permanent business operating artifacts
- `promoted_to_skill` - extracted as reusable skill

## Detection Triggers

Automatically log when you encounter:

**Execution Signals** (learning or business issue):
- missed SLA on committed deliverable
- overdue approval at decision gate
- repeated dependency blocked status
- handoff without complete acceptance criteria

**Governance Signals** (learning or business issue):
- policy exists but team follows outdated practice
- control owner unknown or contested
- RACI accountability conflict between teams
- governance board receives contradictory status reports

**KPI Signals** (learning):
- KPI definition mismatch across dashboards
- variance unexplained beyond tolerance band
- lagging metrics reported as leading indicators

**Budget and Procurement Signals** (business issue):
- budget overrun warning without mitigation owner
- purchase request bypasses policy threshold
- vendor onboarding stalled at approval handoff

**Compliance and Documentation Signals** (learning):
- audit issue reveals missing process evidence
- runbook differs from actual operational behavior
- required approval record missing for material decision

## Priority Guidelines

| Priority | When to Use | Business Examples |
|----------|-------------|-------------------|
| `critical` | Material operational disruption, uncontrolled budget risk, or compliance exposure | Payroll-impacting process outage, major procurement exception without approval trail |
| `high` | SLA misses, delayed governance decisions, or significant KPI variance | Missed month-end close dependency, recurring approval bottleneck |
| `medium` | Important process hardening or definition alignment work | KPI glossary mismatch, outdated handoff checklist |
| `low` | Documentation cleanup and minor process optimization | Naming consistency updates, low-risk reporting cleanup |

## Area Tags

Use these areas to classify learnings:

| Area | Scope |
|------|-------|
| `planning` | planning cycles, prioritization, resource alignment |
| `execution` | task flow, dependency management, delivery completion |
| `governance` | approvals, controls, operating model oversight |
| `reporting` | KPI reporting quality, cadence, dashboard trust |
| `operations` | day-to-day process reliability and service delivery |
| `budgeting` | budget planning, variance review, spend controls |
| `procurement` | purchasing controls, approvals, sourcing process |
| `vendor_management` | vendor onboarding, SLA adherence, performance reviews |
| `risk_management` | risk identification, escalation, mitigation tracking |
| `communication` | cross-functional alignment, decision clarity, status clarity |

## Promoting to Permanent Business Standards

When a learning is broadly applicable, promote it to business administration standards.

### When to Promote

- the same process breakdown recurs across teams
- policy gap repeatedly creates execution risk
- KPI definition issue causes repeated reporting conflicts
- decision latency appears in multiple planning or governance cycles
- handoff failures recur with shared root causes

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Process playbooks | documented steps, guardrails, exception routing |
| Governance checklists | decision controls, evidence requirements, escalation criteria |
| KPI definition registry | metric owners, formulas, data sources, review cadence |
| RACI matrix updates | role clarity for accountable/responsible/consulted/informed |
| Operating cadences | recurring forums, review rituals, frequency and owners |
| `CLAUDE.md` | agent operating conventions for business context |
| `AGENTS.md` | cross-agent routing and workflow orchestration |

### How to Promote

1. Distill the finding into concise and reusable operational guidance
2. Add it to the correct target artifact
3. Update original entry:
   - set `**Status**: promoted`
   - add `**Promoted**: process_playbook` (or other target)
4. confirm human owner for adoption and enforcement

### Promotion Examples

**Learning to governance checklist:**
> Overdue approvals repeatedly blocked procurement. Added checklist rule: "Any approval older than 48h triggers escalation to backup approver."

**Learning to KPI registry:**
> Revenue-at-risk definition mismatched between sales and finance. Registered canonical formula and source system for both teams.

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. Search first: `rg "keyword" .learnings/`
2. Link entries with `**See Also**`
3. Increment recurrence fields
4. Raise priority if impact is increasing
5. Trigger systemic fix proposal when recurrence exceeds threshold

Recurring business patterns usually indicate one or more root causes:
- missing process control
- weak policy communication
- unclear ownership model
- inconsistent KPI definition
- brittle cross-team handoff protocol
- insufficient governance cadence

## Simplify/Harden Feed

Keep incoming signals easy to process, and harden the learning feed against noise.

### Simplify Rules

- prefer one clear issue statement per entry
- include only evidence needed for a decision
- use standard categories and area tags
- avoid duplicating the same incident in multiple files
- route uncertain items to `pending` with explicit open questions

### Harden Rules

- require source attribution in metadata
- require owner and next action for `high` and `critical`
- require explicit approval note for `wont_fix`
- require recurrence tracking for repeated issues
- require status updates before review meetings

## Periodic Review

Review `.learnings/` at operational checkpoints.

### When to Review

- before weekly operating review
- before monthly business review
- before quarterly planning cycle
- before budget review forums
- after major incident retrospectives
- before governance committee decisions

### Quick Status Check

```bash
rg "Status\\*\\*: pending" .learnings/*.md | wc -l
rg "Priority\\*\\*: critical|Priority\\*\\*: high" .learnings/*.md
rg "Area\\*\\*: budgeting|Area\\*\\*: procurement" .learnings/*.md
rg "Category\\*\\*:|\\] process_breakdown|\\] decision_latency" .learnings/*.md
```

### Review Actions

- close resolved entries and capture verification evidence
- merge duplicates and strengthen canonical entries
- promote proven patterns to permanent artifacts
- add or adjust operating cadence for recurring issues

## Hook Integration

Enable automatic reminders through hooks. This is opt-in.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-business/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a business-administration reminder after each prompt.

### Advanced Setup (With Pattern Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-business/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-business/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want command output pattern reminders.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | reminds to evaluate business learnings |
| `scripts/error-detector.sh` | PostToolUse (Bash) | triggers on high-signal business patterns |

See `references/hooks-setup.md` for details.

## Automatic Skill Extraction

When a learning becomes stable and reusable, extract it into a dedicated skill.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| recurring | same pattern appears in multiple teams or cycles |
| verified | status is resolved with validated operational improvement |
| non-obvious | required cross-functional reasoning or governance design |
| broadly applicable | useful outside a single incident |
| user-flagged | user requests conversion into a reusable skill |

### Extraction Workflow

1. identify candidate entry
2. run helper:
   ```bash
   ./skills/self-improving-business/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-business/scripts/extract-skill.sh skill-name
   ```
3. customize generated `SKILL.md`
4. update source entry status to `promoted_to_skill`
5. verify no transactional instructions were embedded

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | hooks | automatic via scripts |
| Codex CLI | hooks | automatic via scripts |
| GitHub Copilot | manual guidance | manual review |
| OpenClaw | workspace injection + hooks | session reminders |

Regardless of agent, apply this workflow when you:

1. coordinate cross-functional delivery with dependencies
2. track KPI quality and reporting consistency
3. manage policy-governed approvals and exceptions
4. monitor budget, procurement, and vendor execution
5. document risk controls and escalation outcomes
6. resolve stakeholder alignment and communication gaps

## Business Administration Best Practices

1. keep ownership explicit and visible in each entry
2. separate signal from symptom using root-cause notes
3. normalize KPI definitions before target discussions
4. document decision deadlines and escalation rules
5. review RACI regularly for contested responsibilities
6. harden handoffs with acceptance criteria and evidence
7. tie governance controls to actual operating cadences
8. use consistent tags for reporting and searchability
9. require human approval for high-impact decisions
10. avoid turning reminders into hidden execution commands

## Gitignore Options

Keep learnings local when entries include sensitive business context:

```gitignore
.learnings/
```

Hybrid option (track structure, ignore contents):

```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

Track learnings in-repo only when content is sanitized and approved for sharing.

## Final Reminder

This skill is a structured memory and improvement mechanism. It does not approve, execute, sign, spend, commit, or authorize business actions. Use it to improve clarity and decision quality, and require human approval for high-impact outcomes.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/business/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: business
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (business)
Only trigger this skill automatically for business signals such as:
- `kpi|revenue|margin|strategy|roadmap`
- `pricing|forecast|market shift|business case`
- explicit business intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/business/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
