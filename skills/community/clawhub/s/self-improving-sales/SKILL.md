---
name: self-improving-sales
description: "Captures pipeline leaks, objection patterns, pricing errors, forecast misses, competitor shifts, and deal velocity drops to enable continuous sales improvement. Use when: (1) A deal slips past stage thresholds, (2) An objection recurs across multiple deals, (3) A pricing mistake is discovered, (4) Forecast accuracy falls below target, (5) A deal is lost to a competitor, (6) Discount escalations exceed policy, (7) A win/loss pattern emerges."
---

# Self-Improving Sales Skill

Log sales-specific learnings, deal issues, and feature requests to markdown files for continuous improvement. Captures pipeline leaks, objection patterns, pricing errors, forecast misses, competitor shifts, and deal velocity drops. Important learnings get promoted to battle cards, objection handling scripts, pricing playbooks, or qualification frameworks (MEDDIC/BANT).

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Sales Learnings\n\nObjection patterns, competitor intelligence, pipeline insights, qualification gaps, and deal execution lessons captured during sales operations.\n\n**Categories**: pipeline_leak | objection_pattern | pricing_error | forecast_miss | competitor_shift | deal_velocity_drop\n**Areas**: prospecting | qualification | discovery | proposal | negotiation | closing | renewal\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/DEAL_ISSUES.md ] || printf "# Deal Issues Log\n\nLost deals, pipeline leaks, pricing errors, forecast misses, and deal execution failures.\n\n---\n" > .learnings/DEAL_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nSales tools, CRM automation, competitive intelligence, and pipeline management capabilities requested during sales operations.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log customer PII, exact contract values, or confidential deal terms. Use deal size ranges (e.g., "$100K-$250K") and anonymize company names when sharing externally.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Deal stuck in same stage >30 days | Log to `.learnings/DEAL_ISSUES.md` with pipeline_leak category |
| Objection you couldn't handle | Log to `.learnings/LEARNINGS.md` with category `objection_pattern` |
| Pricing mistake discovered | Log to `.learnings/DEAL_ISSUES.md` with pricing_error category |
| Forecast missed by >20% | Log to `.learnings/DEAL_ISSUES.md` with forecast_miss category |
| Lost deal to competitor | Log to `.learnings/LEARNINGS.md` with category `competitor_shift` |
| Discount over threshold requested | Log to `.learnings/DEAL_ISSUES.md` with pricing_error category |
| Recurring objection across deals | Link with `**See Also**`, consider priority bump |
| Broadly applicable insight | Promote to battle card, objection handler, or pricing playbook |
| Qualification gap identified | Promote to MEDDIC/BANT framework update |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-sales
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-sales.git ~/.openclaw/skills/self-improving-sales
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
    ├── DEAL_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — objection patterns, competitor intelligence, pipeline insights, deal velocity
- `DEAL_ISSUES.md` — pipeline leaks, lost deals, pricing errors, forecast misses
- `FEATURE_REQUESTS.md` — CRM automation, competitive intelligence tools, pipeline analytics

### Promotion Targets

When sales learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Objection patterns | Objection handling scripts | "When prospect says 'too expensive', reframe to ROI" |
| Competitor intelligence | Battle cards | "Competitor X launched free tier — counter with migration cost" |
| Qualification gaps | MEDDIC/BANT frameworks | "Always identify economic buyer before demo" |
| Pricing patterns | Pricing playbooks | "Never discount >15% without VP approval and multi-year commit" |
| Win/loss patterns | Deal review templates | "Deals without champion identified by Stage 3 close at 12%" |
| Process improvements | `AGENTS.md` | "Update CRM within 24 hours of every meeting" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-sales
openclaw hooks enable self-improving-sales
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

#### Self-Improving Sales Workflow

When sales issues or patterns are discovered:
1. Log to `.learnings/DEAL_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Battle cards — competitive positioning and differentiation
   - Objection handling scripts — proven responses to common objections
   - Pricing playbooks — discount policies, packaging, and negotiation guardrails
   - Qualification frameworks — MEDDIC/BANT checklists and stage gate criteria

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: prospecting | qualification | discovery | proposal | negotiation | closing | renewal

### Summary
One-line description of the sales insight

### Details
Full context: what happened in the deal, why the outcome occurred, what the
correct approach or response is. Include specific objection language, competitor
positioning, or deal dynamics.

### Deal Context

**Objection / Situation:**
> Exact quote or paraphrase of the objection, competitor claim, or deal blocker

**Response Used:**
> What was said or done in response

**Outcome:**
Won | Lost | Stalled | Pushed — and why

### Suggested Action
Specific change to pitch, process, pricing, or qualification criteria

### Metadata
- Source: call_transcript | deal_review | win_loss_analysis | pipeline_review | competitor_intel | forecast_review
- Deal Size: $50K-$100K | $100K-$250K | $250K-$500K | $500K+ (use ranges)
- Segment: SMB | mid_market | enterprise | strategic
- Industry: technology | financial_services | healthcare | manufacturing | retail | other
- Related Deals: DEAL-YYYYMMDD-XXX (if linked to a deal issue)
- Tags: tag1, tag2
- See Also: LRN-20250410-001 (if related to existing entry)
- Pattern-Key: objection.budget_freeze | competitor.free_tier (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `pipeline_leak` | Deals consistently falling out at a specific stage |
| `objection_pattern` | Same objection surfacing across multiple deals |
| `pricing_error` | Quoting wrong price, unapproved discount, packaging mistake |
| `forecast_miss` | Predicted close date or amount significantly off actual |
| `competitor_shift` | Competitor launches feature, changes pricing, or wins pattern |
| `deal_velocity_drop` | Deals taking longer than historical average to progress |

### Deal Issue Entry [DEAL-YYYYMMDD-XXX]

Append to `.learnings/DEAL_ISSUES.md`:

```markdown
## [DEAL-YYYYMMDD-XXX] issue_type

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: prospecting | qualification | discovery | proposal | negotiation | closing | renewal

### Summary
Brief description of the deal issue

### Deal Details
- **Stage**: Stage where the issue occurred
- **Deal Size**: $100K-$250K (use ranges)
- **Days in Stage**: Number of days stuck or time to loss
- **Segment**: SMB | mid_market | enterprise | strategic

### What Happened
Narrative of what went wrong: missed signals, process breakdown, competitive
loss, pricing confusion, or forecast error.

### Root Cause
Why the deal was lost, stalled, or mispriced. Distinguish symptom from cause.

### Impact
- Revenue impact (range)
- Pipeline coverage impact
- Forecast accuracy impact

### Prevention
How to avoid this issue in future deals: qualification criteria, process gate,
pricing checklist, competitive preparation

### Metadata
- Trigger: pipeline_review | deal_review | win_loss_analysis | forecast_review | CRM_audit
- Competitor: competitor name (if applicable)
- Loss Reason: no_budget | no_decision | lost_to_competitor | timing | product_gap | price
- Related Files: path/to/deal_review.md
- See Also: DEAL-20250110-001 (if recurring pattern)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: prospecting | qualification | discovery | proposal | negotiation | closing | renewal

### Requested Capability
What sales tool, automation, or capability is needed

### User Context
Why it's needed, what workflow it improves, what revenue impact it could have

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: CRM workflow, Slack integration, dashboard, alert system

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_feature

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `DEAL` (deal issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `DEAL-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is addressed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Action Taken**: Updated battle card / revised pricing playbook / added qualification gate
- **Notes**: Rolled out to team in weekly sales meeting, updated CRM stage criteria
```

Other status values:
- `in_progress` — Actively being addressed or tested in live deals
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to battle card, objection script, or pricing playbook
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**Pipeline Stalls** (→ deal issue with pipeline_leak):
- Deal in same stage for >30 days
- Multiple deals stalling at the same stage
- Conversion rate drop between stages
- Deals pushed from one quarter to next

**Objection Patterns** (→ learning with objection_pattern):
- Same objection heard in 3+ deals within a quarter
- Objection that consistently leads to no-decision outcomes
- New objection not covered by existing battle cards
- Objection specific to a segment or industry vertical

**Pricing Issues** (→ deal issue with pricing_error):
- Discount >20% requested by prospect
- Quoting a deprecated or incorrect pricing tier
- Competitor undercut by >30% on similar deal
- Custom pricing requested outside standard packaging

**Forecast Misses** (→ deal issue with forecast_miss):
- Quarterly forecast accuracy below 80%
- Deal close date pushed more than twice
- Commit deal lost or pushed to next quarter
- Upside deal that was actually a commit

**Competitive Intelligence** (→ learning with competitor_shift):
- Competitor mentioned in 3+ call transcripts in a month
- Competitor launches new product, feature, or pricing tier
- Prospect received competitive quote or evaluation
- Win rate drops against specific competitor

**Deal Velocity** (→ learning with deal_velocity_drop):
- Average deal cycle lengthening quarter over quarter
- Specific stage taking 2x historical average
- Deals requiring more meetings to close
- Longer legal/procurement review cycles

## Priority Guidelines

| Priority | When to Use | Sales Examples |
|----------|-------------|----------------|
| `critical` | Deal >$500K at risk, data integrity issue, compliance violation | Enterprise deal at risk of loss, CRM data corruption, contract pricing error affecting multiple deals |
| `high` | Recurring objection pattern, forecast miss >20%, competitive threat | Same objection losing 3+ deals, quarterly forecast off by 25%, competitor winning all deals in a segment |
| `medium` | Pipeline hygiene, process improvement, single deal coaching | Deals not advancing past discovery, reps not updating CRM, proposal template outdated |
| `low` | Documentation, minor CRM fix, process tweak | Field label change, report format update, email template refresh |

## Area Tags

Use to filter learnings by sales stage:

| Area | Scope |
|------|-------|
| `prospecting` | Lead generation, outbound sequences, ICP targeting, SDR handoff |
| `qualification` | MEDDIC/BANT scoring, stage gate criteria, champion identification |
| `discovery` | Pain identification, business case building, stakeholder mapping |
| `proposal` | Pricing, packaging, SOW creation, legal review, procurement |
| `negotiation` | Discount requests, contract terms, multi-year commits, procurement |
| `closing` | Final approval, signature, procurement, legal, security review |
| `renewal` | Expansion, upsell, churn prevention, customer success handoff |

## Promoting to Permanent Sales Assets

When a learning is broadly applicable (not a one-off deal quirk), promote it to permanent team assets.

### When to Promote

- Objection recurs across 3+ deals in a quarter
- Competitive intelligence applies to an entire segment
- Pricing insight affects multiple deal sizes or verticals
- Qualification gap leads to predictable deal failures
- Win/loss pattern is statistically significant (10+ deals)

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Battle cards | Competitive positioning, differentiation, trap-setting questions |
| Objection handling scripts | Proven responses with context, follow-up questions, proof points |
| Pricing playbooks | Discount guardrails, packaging options, negotiation tactics |
| MEDDIC/BANT frameworks | Qualification checklists, stage gate criteria, champion tests |
| Deal review templates | Win/loss analysis structure, pipeline review agendas |
| `AGENTS.md` | Automated CRM workflows, deal scoring rules |

### How to Promote

1. **Distill** the learning into a concise, actionable asset
2. **Add** to appropriate target (battle card entry, objection script, playbook rule)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: battle card` (or `objection script`, `pricing playbook`, `MEDDIC framework`)

### Promotion Examples

**Learning** (verbose):
> Prospect said "We already have a vendor for this." We had no differentiation
> message ready. Lost the deal because we couldn't articulate unique value vs.
> incumbent. This happened in 4 deals this quarter against Vendor X.

**As battle card** (concise):
```markdown
## Objection: "We already have a vendor"

**Response Framework:**
1. Acknowledge: "That makes sense — most companies in your space do."
2. Probe: "How well is it handling [specific pain point]?"
3. Differentiate: "Where we're different is [unique capability] which means [business outcome]."
4. Proof: "Company Y switched from [vendor] and saw [metric improvement]."

**Trap-Setting Questions:**
- "How much time does your team spend on [task our product automates]?"
- "What happens when [scenario our product handles better]?"
```

**Learning** (verbose):
> Deals without an identified champion by Stage 3 close at only 12% vs. 48%
> for deals with a champion. We need a hard gate requiring champion
> identification before advancing to proposal.

**As MEDDIC framework update** (actionable):
```markdown
## Stage Gate: Discovery → Proposal

**Required before advancing:**
- [ ] Champion identified (name, title, access level)
- [ ] Champion has confirmed the problem exists
- [ ] Champion has agreed to introduce economic buyer
- [ ] Decision criteria documented from champion conversation

**Block advancement if:** No champion identified after 3 discovery calls.
Recommend: Re-qualify or move to nurture.
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: DEAL-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring sales issues often indicate:
   - Missing qualification criteria (→ update MEDDIC/BANT framework)
   - Competitive gap (→ create or update battle card)
   - Pricing misalignment (→ revise pricing playbook)
   - Process breakdown (→ add CRM stage gate or automation)

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before starting a new deal in the same segment or against the same competitor
- After completing quarterly business review (QBR)
- When the same objection or loss reason appears again
- Weekly during pipeline review meetings
- After each win/loss analysis

### Quick Status Check
```bash
# Count pending sales issues
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority deal issues
grep -B5 "Priority\*\*: high" .learnings/DEAL_ISSUES.md | grep "^## \["

# Find learnings for a specific sales stage
grep -l "Area\*\*: negotiation" .learnings/*.md

# Find all competitor-related learnings
grep -B2 "competitor_shift" .learnings/LEARNINGS.md | grep "^## \["

# List objection patterns
grep -B2 "objection_pattern" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve addressed deal issues
- Promote recurring objections to battle cards
- Link related entries across files
- Extract reusable qualification criteria as framework updates
- Update forecast model based on historical miss patterns

## Simplify & Harden Feed

Ingest recurring sales patterns from `simplify-and-harden` into playbooks or frameworks.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ deals or segments, within 90-day window.
Targets: battle cards, objection scripts, pricing playbooks, MEDDIC/BANT frameworks, `AGENTS.md`.

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in**.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{"matcher": "", "hooks": [{"type": "command", "command": "./skills/self-improving-sales/scripts/activator.sh"}]}],
    "PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "./skills/self-improving-sales/scripts/error-detector.sh"}]}]
  }
}
```

The `UserPromptSubmit` hook injects a sales-focused reminder (~50-100 tokens). The `PostToolUse` hook detects deal-related signals (lost deals, churn, competitor mentions, forecast misses). Use only `UserPromptSubmit` for lower overhead.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate sales learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on deal issues, competitor mentions, pipeline signals |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a sales learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same objection or deal pattern in 3+ deals or segments |
| **Verified** | Status is `resolved` with proven response or process fix |
| **Non-obvious** | Required actual deal experience or loss to discover |
| **Broadly applicable** | Not deal-specific; useful across segments or verticals |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-sales/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-sales/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with sales-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

**In conversation**: "This objection keeps coming up", "Save this competitive intel as a skill", "I keep losing deals at this stage", "Every enterprise deal has this procurement issue".

**In entries**: Multiple `See Also` links, high priority + resolved, `objection_pattern` or `competitor_shift` with broad applicability, same `Pattern-Key` across deals or segments.

## Sales-Specific Best Practices

1. **Qualify early** — disqualify faster to focus pipeline on winnable deals
2. **Document objections immediately** — exact wording matters for battle cards
3. **Update CRM same day** — stale data poisons forecasts and pipeline reviews
4. **Track competitor intel in real time** — pricing changes and feature launches decay fast
5. **Review win/loss quarterly** — patterns only emerge with enough data points
6. **Log the objection, not just the outcome** — "we lost" is less useful than "they said X"
7. **Anonymize appropriately** — use deal size ranges and avoid customer PII in shared logs
8. **Distinguish decision-maker objections from user objections** — different responses required
9. **Record what you tried** — failed responses are as valuable as successful ones
10. **Promote aggressively** — if an objection appears in 3 deals, it deserves a battle card

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Gitignore Options

**Keep learnings local** (per-rep):
```gitignore
.learnings/
```

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared team knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/sales/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: sales
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (sales)
Only trigger this skill automatically for sales signals such as:
- `pipeline|opportunity|objection|close-lost|win rate`
- `quota|forecast|deal stage|discovery call|proposal`
- explicit sales intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/sales/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
