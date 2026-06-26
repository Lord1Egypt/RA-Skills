---
name: self-improving-support
description: "Captures ticket resolution delays, misdiagnoses, escalation gaps, SLA breaches, knowledge gaps, and customer churn signals to enable continuous support improvement. Use when: (1) A ticket is resolved late or incorrectly, (2) An SLA breach occurs, (3) A customer reopens a ticket, (4) An escalation pathway fails, (5) A knowledge base search returns no results, (6) CSAT scores drop below threshold, (7) A churn signal is detected in customer communication."
---

# Self-Improving Support Skill

Log support-specific learnings, ticket issues, and feature requests to markdown files for continuous improvement. Captures resolution delays, misdiagnoses, escalation gaps, SLA breaches, knowledge base gaps, and customer churn signals. Important learnings get promoted to KB articles, troubleshooting trees, escalation matrices, or canned responses.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Support Learnings\n\nResolution delays, misdiagnoses, escalation gaps, SLA breaches, knowledge gaps, and churn signals captured during support operations.\n\n**Categories**: resolution_delay | misdiagnosis | escalation_gap | knowledge_gap | sla_breach | customer_churn_signal\n**Areas**: triage | diagnosis | resolution | follow_up | documentation | escalation\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/TICKET_ISSUES.md ] || printf "# Ticket Issues Log\n\nRecurring ticket problems, resolution failures, SLA breaches, and escalation breakdowns.\n\n---\n" > .learnings/TICKET_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nSupport tooling, automation, and workflow improvement requests.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log customer PII, account credentials, or internal auth tokens. Use ticket IDs and anonymised references. Prefer short summaries over verbatim customer messages.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Repeat ticket from same customer | Log to `.learnings/TICKET_ISSUES.md` with resolution_delay or misdiagnosis |
| CSAT score drops below threshold | Log to `.learnings/LEARNINGS.md` with category `customer_churn_signal` |
| SLA breach on any priority ticket | Log to `.learnings/TICKET_ISSUES.md` with sla_breach details |
| Misdiagnosis leads to wrong fix | Log to `.learnings/TICKET_ISSUES.md` with misdiagnosis root cause |
| KB search returns no results | Log to `.learnings/LEARNINGS.md` with category `knowledge_gap` |
| Escalation to engineering fails | Log to `.learnings/LEARNINGS.md` with category `escalation_gap` |
| Customer uses churn language | Log to `.learnings/LEARNINGS.md` with category `customer_churn_signal` |
| Recurring ticket pattern (3+) | Link with `**See Also**`, consider priority bump |
| Broadly applicable resolution | Promote to KB article, troubleshooting tree, or canned response |
| Reusable triage workflow | Promote to escalation matrix or runbook |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-support
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-support.git ~/.openclaw/skills/self-improving-support
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
    ├── TICKET_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — resolution delays, escalation gaps, knowledge gaps, churn signals
- `TICKET_ISSUES.md` — misdiagnoses, SLA breaches, escalation failures, repeat tickets
- `FEATURE_REQUESTS.md` — support tooling, automation, workflow improvements

### Promotion Targets

When support learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Diagnostic pattern | KB article | "DNS resolution failures always check /etc/resolv.conf first" |
| Triage workflow | Troubleshooting tree | "Login failure decision tree: SSO vs local vs MFA" |
| Escalation insight | Escalation matrix | "Database deadlocks → DBA on-call, not general engineering" |
| Common resolution | Canned response template | "Password reset steps for enterprise SSO customers" |
| Support tone pattern | `SOUL.md` | "Acknowledge frustration before offering solutions" |
| Triage automation | `AGENTS.md` | "Auto-categorize tickets by keyword before human triage" |
| Tool configuration | `TOOLS.md` | "Zendesk macro for bulk SLA extension on outage tickets" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-support
openclaw hooks enable self-improving-support
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

#### Self-Improving Support Workflow

When support issues or patterns are discovered:
1. Log to `.learnings/TICKET_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - KB articles — customer-facing resolution guides
   - Troubleshooting trees — step-by-step diagnosis flows
   - Escalation matrices — routing rules for engineering teams
   - Canned responses — pre-approved reply templates

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: triage | diagnosis | resolution | follow_up | documentation | escalation

### Summary
One-line description of the support insight

### Details
Full context: what support situation occurred, why the outcome was suboptimal,
what the correct triage, diagnosis, or resolution approach is.
Include ticket timeline and relevant customer interaction summary (anonymised).

### Resolution Steps

**What happened:**
Brief timeline of the support interaction and outcome.

**What should have happened:**
The correct workflow or diagnosis path.

### Suggested Action
Specific KB article, escalation rule, or process change to adopt

### Metadata
- Source: repeat_ticket | csat_drop | sla_timer | ticket_reopen | escalation_failure | kb_search_miss
- Channel: email | chat | phone | portal | api
- Product Area: billing | auth | api | dashboard | integrations | infrastructure
- Customer Tier: free | starter | professional | enterprise
- Related Tickets: TKT-12345, TKT-12346
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: misdiagnosis.dns_vs_ssl | escalation.wrong_team (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `resolution_delay` | Ticket took significantly longer than SLA target to resolve |
| `misdiagnosis` | Initial diagnosis was incorrect, leading to wasted time or wrong fix |
| `escalation_gap` | Escalation path was unclear, went to wrong team, or was delayed |
| `knowledge_gap` | No KB article existed for a common issue; agent had to research from scratch |
| `sla_breach` | SLA commitment was violated (first response, resolution, or update cadence) |
| `customer_churn_signal` | Customer expressed frustration, cancellation intent, or dissatisfaction |

### Ticket Issue Entry [TKT-YYYYMMDD-XXX]

Append to `.learnings/TICKET_ISSUES.md`:

```markdown
## [TKT-YYYYMMDD-XXX] issue_type_or_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: triage | diagnosis | resolution | follow_up | documentation | escalation

### Summary
Brief description of the ticket issue

### Ticket Timeline
| Time | Event |
|------|-------|
| T+0h | Ticket opened by customer |
| T+Xh | First response sent |
| T+Xh | Diagnosis attempted |
| T+Xh | Escalation / resolution |
| T+Xh | Ticket closed or reopened |

### Root Cause
What in the support process caused the issue. Was it a misdiagnosis,
wrong escalation path, missing KB article, or SLA timer oversight?

### Correct Approach
What the agent should have done — the right triage, diagnosis, and
resolution path for this type of ticket.

### Customer Impact
- SLA Status: met | breached (first_response | resolution | update)
- CSAT Impact: none | minor | significant
- Reopened: yes | no
- Escalated: yes (to whom) | no

### Prevention
How to prevent this ticket issue from recurring (KB update, escalation
rule change, training material, canned response).

### Context
- Trigger: repeat_ticket | csat_drop | sla_breach | ticket_reopen | escalation_failure
- Channel: email | chat | phone | portal
- Product Area: billing | auth | api | dashboard | integrations | infrastructure
- Customer Tier: free | starter | professional | enterprise

### Metadata
- Related Tickets: TKT-12345
- Related Files: path/to/runbook.md
- See Also: TKT-20250110-001 (if recurring pattern)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: triage | diagnosis | resolution | follow_up | documentation | escalation

### Requested Capability
What support tool, automation, or workflow improvement is needed

### User Context
Why it's needed, what support workflow it improves, what ticket pattern it addresses

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: Zendesk macro, Intercom workflow, Slack bot, KB template,
escalation rule, auto-categorizer, SLA monitor, CSAT survey trigger

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_workflow

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `TKT` (ticket issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `TKT-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is addressed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Action Taken**: Updated KB article / revised escalation matrix / created canned response
- **Notes**: Added troubleshooting tree for DNS resolution failures
```

Other status values:
- `in_progress` — Actively being investigated or remediated
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to KB article, troubleshooting tree, or escalation matrix
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**Repeat Ticket Patterns** (→ ticket issue with repeat_ticket trigger):
- Same customer opens ticket for same issue within 30 days
- Multiple customers report identical symptoms in same week
- Ticket references a previous ticket number
- Customer says "I already contacted you about this"

**Negative Sentiment in Customer Messages** (→ learning with customer_churn_signal):
- Explicit frustration: "This is unacceptable", "I've been waiting for days"
- Cancellation language: "cancel my subscription", "looking for alternatives"
- Escalation demand: "Let me speak to a manager", "This needs to be escalated"
- Disappointment: "I expected better", "This used to work fine"

**SLA Timer Approaching** (→ ticket issue with sla_breach trigger):
- First response SLA at 80% elapsed time
- Resolution SLA at 70% elapsed time
- Update cadence SLA missed (no update in promised interval)
- P1/P2 ticket without engineer assignment within threshold

**Ticket Reopened** (→ ticket issue with ticket_reopen trigger):
- Customer reopens within 7 days of closure
- Auto-reopen from monitoring alert on same issue
- Customer replies "This didn't fix my problem"
- Same error recurs in customer's system logs

**CSAT Below Threshold** (→ learning with customer_churn_signal):
- Individual ticket CSAT ≤ 2/5
- Rolling 7-day CSAT average drops below target
- Customer leaves negative free-text feedback
- NPS detractor response from support interaction

**Knowledge Base Search Failures** (→ learning with knowledge_gap):
- Agent searches KB and finds no relevant article
- Customer self-service search returns zero results
- Agent creates ticket for issue that should have a KB article
- Multiple agents ask the same question in internal channels

## Priority Guidelines

| Priority | When to Use | Support Examples |
|----------|-------------|-----------------|
| `critical` | Data loss, service outage affecting customer, security incident | Production outage for enterprise customer, data breach notification, payment processing failure |
| `high` | SLA breach, repeated misdiagnosis, customer churn risk | P1 SLA violated, same misdiagnosis on 3 tickets, enterprise customer threatens cancellation |
| `medium` | Knowledge gap, process improvement, escalation refinement | Missing KB article for common issue, unclear escalation path, triage category missing |
| `low` | Documentation update, canned response refinement, minor process tweak | Typo in KB article, canned response tone adjustment, tag taxonomy cleanup |

## Area Tags

Use to filter learnings by support domain:

| Area | Scope |
|------|-------|
| `triage` | Initial ticket classification, priority assignment, routing, auto-categorization |
| `diagnosis` | Root cause analysis, symptom-to-cause mapping, diagnostic questioning |
| `resolution` | Fix implementation, workaround delivery, solution verification |
| `follow_up` | Post-resolution check-in, CSAT survey, ticket closure, reopening prevention |
| `documentation` | KB articles, internal runbooks, troubleshooting trees, canned responses |
| `escalation` | Routing to engineering, manager involvement, cross-team handoffs, war rooms |

## Promoting to Permanent Support Standards

When a learning is broadly applicable (not a one-off ticket), promote it to permanent support resources.

### When to Promote

- Same ticket issue recurs across multiple customers or channels
- Misdiagnosis pattern found in 3+ resolved tickets
- Knowledge gap affects multiple agents independently
- Resolution workflow would save significant handle time if documented

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| KB article | Customer-facing resolution guides, FAQ entries, how-to documents |
| Troubleshooting tree | Decision-flow diagrams for diagnosis (symptom → cause → fix) |
| Escalation matrix | Team routing rules, on-call contacts, severity-based escalation paths |
| Canned response | Pre-approved reply templates for common scenarios |
| Internal runbook | Step-by-step procedures for agents handling specific issue types |
| `SOUL.md` | Support tone and communication patterns, empathy guidelines |
| `AGENTS.md` | Automated triage workflows, ticket routing rules |

### How to Promote

1. **Distill** the learning into a concise KB article, triage rule, or response template
2. **Add** to appropriate target (KB, escalation matrix, canned response library)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: KB article` (or `troubleshooting tree`, `escalation matrix`, `canned response`)

### Promotion Examples

**Learning → KB article**:
> Three agents misdiagnosed "502 Bad Gateway" as server-side when the root cause was
> customer's WAF blocking our API callbacks.

Promoted to: KB article "502 Bad Gateway on API Callbacks" with symptom, common
misdiagnosis, actual cause (customer WAF/firewall), and IP whitelist resolution steps.

**Learning → Escalation rule**:
> Enterprise customer escalated to VP after three P2 tickets for the same SSO issue.
> Each time a different agent started from scratch with no linked history.

Promoted to: Escalation matrix rule — on 3rd ticket for same issue category from
enterprise customer, auto-assign previous agent, link history, notify account manager.

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: TKT-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring support issues often indicate:
   - Missing KB article (→ write and publish)
   - Unclear escalation path (→ update escalation matrix)
   - Product defect (→ file engineering ticket with linked support tickets)
   - Training gap (→ create internal training material)

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before starting a shift or taking over a ticket queue
- After a major incident or outage
- When the same ticket category spikes
- Weekly during support retrospectives

### Quick Status Check
```bash
grep -h "Status\*\*: pending" .learnings/*.md | wc -l
grep -B5 "Priority\*\*: high" .learnings/TICKET_ISSUES.md | grep "^## \["
grep -B2 "sla_breach" .learnings/TICKET_ISSUES.md | grep "^## \["
grep -B2 "knowledge_gap" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve addressed ticket issues
- Promote recurring patterns to KB articles
- Link related entries across files
- Extract reusable resolutions as canned responses or troubleshooting trees

## Simplify & Harden Feed

Ingest recurring support patterns from `simplify-and-harden` into KB articles or escalation rules.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen across 2+ customers or channels, within 30-day window.
Targets: KB articles, troubleshooting trees, escalation matrices, canned responses, `SOUL.md` / `AGENTS.md`.

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
        "command": "./skills/self-improving-support/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a support-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Issue Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-support/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-support/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for SLA breaches, escalation failures, and customer dissatisfaction signals.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate support learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on SLA warnings, escalation gaps, churn signals |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a support learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same ticket pattern across 3+ customers or channels |
| **Verified** | Status is `resolved` with confirmed resolution and prevention steps |
| **Non-obvious** | Required actual investigation or escalation to discover |
| **Broadly applicable** | Not customer-specific; useful across products or support tiers |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-support/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-support/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with support-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

**In conversation**: "This keeps happening to customers", "Save this resolution as a skill", "Every agent struggles with this", "We need a runbook for this".

**In entries**: Multiple `See Also` links, high priority + resolved, `knowledge_gap` or `misdiagnosis` with broad applicability, same `Pattern-Key` across customer tiers.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Best Practices

1. **Acknowledge first, diagnose second** — validate the customer's experience before troubleshooting
2. **Diagnose before acting** — confirm root cause before applying a fix; misdiagnosis wastes everyone's time
3. **Always follow up** — check back after resolution to confirm the fix holds and customer is satisfied
4. **Document every resolution** — if you had to research it, future agents will too; write the KB article
5. **Log immediately** — context fades fast; capture the ticket issue while details are fresh
6. **Anonymise customer data** — use ticket IDs and product areas, never names or account details
7. **Link related tickets** — patterns only emerge when individual tickets are connected
8. **Escalate with context** — include what you already tried, what you ruled out, and what you suspect
9. **Promote aggressively** — if the same issue appears three times, it needs a KB article or automation
10. **Review before shift** — check `.learnings/` for recent patterns in your ticket queue

## Gitignore Options

**Keep learnings local** (per-agent):
```gitignore
.learnings/
```

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/support/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: support
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (support)
Only trigger this skill automatically for support signals such as:
- `ticket|sla breach|escalation|incident update|resolution note`
- `repeat issue|handoff|kb gap|customer impact`
- explicit support intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/support/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
