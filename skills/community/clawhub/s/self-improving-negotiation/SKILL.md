---
name: self-improving-negotiation
description: "Captures negotiation strategy failures, concession leaks, BATNA weakness, framing misses, objection handling gaps, escalation misalignment, anchor errors, and agreement quality risks for continuous improvement. Use when negotiations stall, concessions exceed guardrails, terms are ambiguous, or recurring bargaining patterns emerge."
---

# Self-Improving Negotiation Skill

Log negotiation learnings, negotiation issues, and feature requests to markdown files for continuous improvement. Capture preparation gaps, framing misses, concession leakage, weak BATNA posture, recurring objections, escalation mistakes, contract-term ambiguity, and agreement quality risk.

Promote validated patterns into:
- negotiation playbooks
- objection libraries
- concession guardrails
- BATNA checklists
- deal review templates

## Safety Posture

This skill is documentation and reminder guidance only.

It does **not**:
- auto-accept terms
- commit pricing
- execute legal/financial approvals
- finalize agreements

Always require explicit human approval for high-impact concessions and for final terms.

## First-Use Initialisation

Before logging, ensure `.learnings/` exists in project/workspace root. Create missing files only:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Negotiation Learnings\n\nNegotiation strategy insights, framing improvements, BATNA lessons, concession tactics, objection handling patterns, escalation learnings, and agreement quality improvements.\n\n**Categories**: concession_leak | batna_weakness | framing_miss | objection_handling_gap | escalation_misalignment | value_articulation_gap | anchor_error | agreement_risk\n**Areas**: preparation | discovery | framing | bargaining | concessions | closing | stakeholder_alignment | escalation | contract_terms | follow_up\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/NEGOTIATION_ISSUES.md ] || printf "# Negotiation Issues Log\n\nNegotiation failures, concession breakdowns, unresolved redlines, escalation misalignment, and agreement quality risks.\n\n---\n" > .learnings/NEGOTIATION_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nNegotiation tooling, preparation automation, objection support, BATNA planning, concession controls, and agreement-risk analysis capabilities.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Concession made without reciprocal value | Log `NEG` in `.learnings/NEGOTIATION_ISSUES.md` category `concession_leak` |
| BATNA undefined or weak | Log `NEG` category `batna_weakness` in `preparation` |
| Opening anchor failed or drifted | Log `LRN` category `anchor_error` |
| Same objection repeated across deals | Log `LRN` category `objection_handling_gap` |
| Escalation executed to wrong owner/timing | Log `NEG` category `escalation_misalignment` |
| Redline unresolved at close stage | Log `NEG` category `agreement_risk` |
| Value reframing improved movement | Log `LRN` category `value_articulation_gap` |
| Clause ambiguity discovered | Log `NEG` category `agreement_risk` in `contract_terms` |
| Workflow/tooling needed | Log `FEAT` in `.learnings/FEATURE_REQUESTS.md` |
| Pattern repeats 3+ times | Link entries and promote to permanent asset |

## OpenClaw Setup (Recommended)

OpenClaw supports workspace-based skill loading and hook reminders.

### Install

```bash
clawdhub install self-improving-negotiation
```

Manual clone:

```bash
git clone https://github.com/jose-compu/self-improving-negotiation.git ~/.openclaw/skills/self-improving-negotiation
```

### Workspace Structure

```text
~/.openclaw/workspace/
├── AGENTS.md
├── SOUL.md
├── TOOLS.md
├── MEMORY.md
├── memory/
│   └── YYYY-MM-DD.md
└── .learnings/
    ├── LEARNINGS.md
    ├── NEGOTIATION_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create learning files in OpenClaw workspace

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create:
- `LEARNINGS.md`
- `NEGOTIATION_ISSUES.md`
- `FEATURE_REQUESTS.md`

### Optional Hook

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-negotiation
openclaw hooks enable self-improving-negotiation
```

See `references/openclaw-integration.md`.

---

## Generic Setup (Other Agents)

For Claude Code, Codex CLI, Copilot, or other assistants:

```bash
mkdir -p .learnings
```

Create the same 3 files in `.learnings/`.

### Suggested instruction block

Add to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`:

When negotiation patterns are discovered:
1. Log to `.learnings/LEARNINGS.md`, `.learnings/NEGOTIATION_ISSUES.md`, or `.learnings/FEATURE_REQUESTS.md`
2. Review recurring items weekly
3. Promote reusable patterns to:
   - negotiation playbooks
   - objection libraries
   - concession guardrails
   - BATNA checklists
   - deal review templates

## Entry Types

- `LRN` = learning
- `NEG` = negotiation issue
- `FEAT` = feature request

## Logging Formats

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: preparation | discovery | framing | bargaining | concessions | closing | stakeholder_alignment | escalation | contract_terms | follow_up

### Summary
One-line negotiation learning.

### Details
What happened, why it mattered, and what to improve.

### Negotiation Context

**Trigger / Objection:**
> Quote or paraphrase

**Response Used:**
> Action, phrase, offer, or decision

**Outcome:**
advanced | stalled | rejected | escalated | closed

### Suggested Action
Concrete change to framing, concession strategy, BATNA prep, or escalation.

### Metadata
- Source: transcript_review | negotiation_debrief | legal_review | pricing_review | post_mortem
- Negotiation Type: procurement | renewal | enterprise_new_logo | partner | vendor | internal_budget
- Counterparty Role: procurement | legal | finance | exec | ops | technical
- Related Issues: NEG-YYYYMMDD-XXX
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX
- Pattern-Key: framing.anchor_drift (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: YYYY-MM-DD (optional)
- Last-Seen: YYYY-MM-DD (optional)

---
```

### Negotiation Issue Entry [NEG-YYYYMMDD-XXX]

Append to `.learnings/NEGOTIATION_ISSUES.md`:

```markdown
## [NEG-YYYYMMDD-XXX] issue_type

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: preparation | discovery | framing | bargaining | concessions | closing | stakeholder_alignment | escalation | contract_terms | follow_up

### Summary
Brief description of failure/risk.

### Context
- **Stage**: current stage
- **Counterparty**: role/team
- **Cycle Day**: days from first commercial exchange

### What Happened
Sequence of events and where the issue surfaced.

### Root Cause
Preparation gap, weak BATNA, framing miss, concession error, approval gap, or term ambiguity.

### Impact
- Margin/pricing impact range
- Timeline impact
- Business/legal risk impact

### Prevention
Guardrails, scripts, checklists, escalation path changes.

### Metadata
- Trigger: deadlock | repeated_objection | scope_creep | concession_exceeded_threshold | batna_not_defined | approval_missing | term_ambiguity | redline_unresolved
- Related Files: path/to/debrief.md
- See Also: NEG-YYYYMMDD-XXX

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: preparation | discovery | framing | bargaining | concessions | closing | stakeholder_alignment | escalation | contract_terms | follow_up

### Requested Capability
Tooling or workflow enhancement needed.

### User Context
Why this is needed and what friction it removes.

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
Practical implementation suggestion.

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## Categories

| Category | Use When |
|----------|----------|
| `concession_leak` | Concession granted without reciprocal value |
| `batna_weakness` | BATNA undefined, unrealistic, or not actionable |
| `framing_miss` | Value narrative fails to move negotiation |
| `objection_handling_gap` | Repeated objection lacks effective response |
| `escalation_misalignment` | Escalation timing/owner path is wrong |
| `value_articulation_gap` | Team cannot connect terms to measurable value |
| `anchor_error` | Anchor too weak/strong or abandoned prematurely |
| `agreement_risk` | Final terms contain ambiguity or unresolved risk |

## Area Tags

| Area | Scope |
|------|-------|
| `preparation` | BATNA setup, approval limits, stakeholder map |
| `discovery` | Interests, constraints, hidden blockers |
| `framing` | Value framing and anchor setup |
| `bargaining` | Offer-counteroffer strategy |
| `concessions` | Give-get discipline and thresholds |
| `closing` | Final package shaping and confirmation |
| `stakeholder_alignment` | Internal/external decision alignment |
| `escalation` | Escalation path and timing |
| `contract_terms` | Clauses, redlines, obligations, ambiguity |
| `follow_up` | Recaps, unresolved items, next-round prep |

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` | `NEG` | `FEAT`
- YYYYMMDD: date
- XXX: sequential (`001`) or random (`A7B`)

Examples:
- `LRN-20260413-001`
- `NEG-20260413-A3F`
- `FEAT-20260413-002`

## Resolve Workflow

When resolved:
1. Update `**Status**: pending` -> `**Status**: resolved`
2. Add resolution block:

```markdown
### Resolution
- **Resolved**: 2026-04-13T14:30:00Z
- **Action Taken**: Added concession guardrail and approval checklist
- **Notes**: Applied successfully in two subsequent negotiations
```

Additional statuses:
- `in_progress`
- `wont_fix`
- `promoted`
- `promoted_to_skill`

## Detection Triggers

Log when these appear:

### Deadlock
- No movement after 2+ rounds
- Repeated counters without new rationale
- Decision timeline slips with no clear blocker

### Repeated Objections
- Same objection in 3+ negotiations
- Existing response script fails repeatedly
- Objection appears across multiple stakeholder roles

### Scope Creep
- New obligations added after pricing alignment
- Added deliverables without compensating terms
- Late-stage requirement expansion

### Concession Exceeded Threshold
- Discount/term concession above approved band
- Multiple micro-concessions exceed policy combined
- Concession offered before reciprocal commitment

### BATNA Not Defined
- No walk-away threshold
- No fallback path
- BATNA not costed/timed

### Approval Missing
- Concession offered without required approval
- Decision made on verbal approval only
- Approval owner unclear late in cycle

### Term Ambiguity
- Clause supports conflicting interpretations
- Undefined SLA/penalty terms
- Renewal/termination trigger unclear

### Redline Unresolved
- Open legal comments at close stage
- Internal and external redline versions diverge
- "To be clarified later" language remains

## Priority Guidelines

| Priority | When to Use | Example |
|----------|-------------|---------|
| `critical` | High-impact unresolved risk or unauthorized concession | Liability term unresolved at close; major concession without approval |
| `high` | Recurring pattern with material impact | BATNA absent in enterprise cycles; repeated deadlocks |
| `medium` | Single-cycle issue with contained impact | One objection flow underperforming |
| `low` | Minor improvement or documentation cleanup | Non-critical wording updates |

## Promotion Targets

When patterns are validated and reusable, promote to:

| Target | What to Promote |
|--------|-----------------|
| Negotiation playbooks | End-to-end tactics across stages |
| Objection libraries | Reusable objection-response flows |
| Concession guardrails | Give-get rules and approval thresholds |
| BATNA checklists | Preflight criteria and walk-away readiness |
| Deal review templates | Structured post-negotiation reviews |

### Promotion Criteria

- Pattern recurs at least 3 times
- Countermeasure verified in real outcomes
- Useful across contexts (not one-off)
- Non-obvious and operationally important

### Promotion Workflow

1. Distill learning into concise asset.
2. Add asset to target repository/document.
3. Update source entry:
   - `**Status**: promoted`
   - `**Promoted**: negotiation_playbook` (or relevant target)

## Recurring Pattern Detection

Before creating a new entry:

1. Search existing patterns:
   ```bash
   rg "Pattern-Key|concession_leak|batna_weakness|anchor_error|agreement_risk" .learnings/
   ```
2. If related entry exists:
   - add `See Also`
   - increase `Recurrence-Count`
   - update `Last-Seen`
3. Raise priority if recurrence continues.
4. Identify systemic fix:
   - framing issue -> playbook update
   - objection issue -> objection library
   - concession issue -> guardrail policy
   - BATNA issue -> checklist hard gate
   - term issue -> contract review template

## Simplify/Harden Feed

When importing simplify-and-harden insights:

1. Use `Pattern-Key` as dedupe key.
2. Search for key:
   ```bash
   rg "Pattern-Key: <key>" .learnings/LEARNINGS.md
   ```
3. Existing key:
   - increment recurrence
   - update dates
   - link related entries
4. New key:
   - create `LRN` entry
   - set source to simplify-and-harden

Promotion threshold suggestion:
- recurrence >= 3
- appears in 2+ negotiation contexts
- appears within 90 days

## Periodic Review

### When to review

- Before high-stakes negotiation rounds
- After deadlock or failed escalation
- Weekly for active deals
- Monthly for pattern consolidation
- Before quarter-end closes

### Quick checks

```bash
# Pending entries
rg "Status\\*\\*: pending" .learnings/*.md | wc -l

# High and critical issues
rg -n "Priority\\*\\*: high|Priority\\*\\*: critical" .learnings/NEGOTIATION_ISSUES.md

# BATNA issues
rg -n "batna_weakness|BATNA" .learnings/*.md

# Concession leaks
rg -n "concession_leak|concession" .learnings/*.md

# Agreement risk
rg -n "agreement_risk|term_ambiguity|redline_unresolved" .learnings/NEGOTIATION_ISSUES.md
```

### Review actions

- Resolve addressed issues
- Promote validated patterns
- Merge duplicates with links
- Tighten concession thresholds
- Refresh BATNA checklist
- Update escalation matrix

## Best Practices

1. Define BATNA, reservation point, and walk-away before first offer.
2. Anchor on value and risk reduction, not only price.
3. Trade every concession for reciprocal value.
4. Avoid stacking concessions in one round.
5. Keep approval ownership explicit before offering exceptions.
6. Treat ambiguous terms as active risk.
7. Capture objection wording precisely for reuse.
8. Escalate with clear decision owner and deadline.
9. Log outcomes the same day while context is fresh.
10. Promote recurring patterns quickly.

## Hook Integration (Opt-In)

Use hooks to inject reminders and detect negotiation signals.

### Example configuration

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": "./skills/self-improving-negotiation/scripts/activator.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "./skills/self-improving-negotiation/scripts/error-detector.sh" }
        ]
      }
    ]
  }
}
```

Hook behavior is reminder-only; no execution of agreement or approval actions.

See `references/hooks-setup.md`.

## Automatic Skill Extraction

If a learning is stable and reusable, extract a new skill.

### Criteria

| Criterion | Requirement |
|-----------|-------------|
| Recurring | Appears in 3+ negotiations |
| Verified | Improvement proven in outcomes |
| Non-obvious | Practical experience required |
| Broad | Useful across contexts |
| Requested | User/team asked for standardization |

### Workflow

1. Select candidate `LRN` or `NEG`.
2. Run extraction helper:
   ```bash
   ./skills/self-improving-negotiation/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-negotiation/scripts/extract-skill.sh skill-name
   ```
3. Fill TODO placeholders.
4. Update source entry:
   - `**Status**: promoted_to_skill`
   - `**Skill-Path**: skills/<skill-name>`
5. Validate in fresh session.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hook scripts | Automatic |
| Codex CLI | Hook scripts | Automatic |
| GitHub Copilot | Instruction guidance | Manual |
| OpenClaw | Workspace + hooks | Automatic reminders |

Coordination rules:
- Use one canonical `.learnings/` folder
- Use stable IDs (`LRN`, `NEG`, `FEAT`)
- Add `See Also` cross-links and reviewer ownership before promotion

## Agreement Quality Gate

Before final recommendation, confirm:
- BATNA is still valid
- concessions are reciprocal
- approvals are documented
- redlines are resolved
- ambiguous clauses are removed

If any check fails, log `NEG` and pause final recommendation.

## Gitignore Options

```gitignore
.learnings/
```

```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

Shared team mode: do not ignore `.learnings/`.

## References

- `references/examples.md`
- `references/hooks-setup.md`
- `references/openclaw-integration.md`
- Clone URL: `https://github.com/jose-compu/self-improving-negotiation.git`
Skill, hooks, and scripts are reminder-only controls; they never approve concessions, accept terms, commit pricing, execute approvals, or finalize agreements. Human approval remains required for high-impact concessions and final terms.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/negotiation/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: negotiation
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (negotiation)
Only trigger this skill automatically for negotiation signals such as:
- `counteroffer|concession|anchor|walk-away|term sheet`
- `deal risk|stakeholder alignment|fallback option|BATNA`
- explicit negotiation intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/negotiation/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
