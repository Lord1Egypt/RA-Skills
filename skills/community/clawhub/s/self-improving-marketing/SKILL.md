---
name: self-improving-marketing
description: "Captures messaging misses, channel underperformance, audience drift, brand inconsistency, attribution gaps, and content decay to enable continuous marketing improvement. Use when: (1) CTR drops below threshold, (2) Conversion rate declines significantly, (3) Brand sentiment shifts negatively, (4) Organic traffic drops unexpectedly, (5) Email deliverability degrades, (6) UTM attribution breaks, (7) Campaign performance falls below benchmarks."
---

# Self-Improving Marketing Skill

Log marketing-specific learnings, campaign issues, and feature requests to markdown files for continuous improvement. Captures messaging misses, channel underperformance, audience drift, brand inconsistency, attribution gaps, and content decay. Important learnings get promoted to brand guidelines, content calendars, channel playbooks, audience personas, or attribution models.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Marketing Learnings\n\nMessaging misses, audience drift, brand inconsistency, content decay, and channel insights captured during marketing operations.\n\n**Categories**: messaging_miss | channel_underperformance | audience_drift | brand_inconsistency | attribution_gap | content_decay\n**Areas**: content | campaigns | seo | social | email | paid_media | analytics\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/CAMPAIGN_ISSUES.md ] || printf "# Campaign Issues Log\n\nCampaign failures, channel problems, messaging errors, and performance issues.\n\n---\n" > .learnings/CAMPAIGN_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nMarketing tools, automation capabilities, and analytics improvements.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log customer PII, API keys, ad account credentials, or internal revenue figures. Prefer aggregated metrics and redacted campaign identifiers over raw customer data.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| CTR drops >20% from baseline | Log to `.learnings/CAMPAIGN_ISSUES.md` with performance details |
| Conversion rate declines >15% | Log to `.learnings/CAMPAIGN_ISSUES.md` with funnel analysis |
| Brand guideline violation found | Log to `.learnings/LEARNINGS.md` with category `brand_inconsistency` |
| Organic traffic falls >25% | Log to `.learnings/LEARNINGS.md` with category `content_decay` |
| Email bounce rate spikes >5% | Log to `.learnings/CAMPAIGN_ISSUES.md` with deliverability details |
| UTM attribution breaks | Log to `.learnings/LEARNINGS.md` with category `attribution_gap` |
| Messaging misses target segment | Log to `.learnings/LEARNINGS.md` with category `messaging_miss` |
| Channel underperforms benchmark | Log to `.learnings/LEARNINGS.md` with category `channel_underperformance` |
| Audience persona no longer fits | Log to `.learnings/LEARNINGS.md` with category `audience_drift` |
| Social engagement declines | Log to `.learnings/CAMPAIGN_ISSUES.md` with engagement metrics |
| Recurring campaign pattern | Link with `**See Also**`, consider priority bump |
| Broadly applicable insight | Promote to brand guidelines, playbook, or persona doc |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-marketing
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-marketing.git ~/.openclaw/skills/self-improving-marketing
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
    ├── CAMPAIGN_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — messaging misses, audience drift, brand inconsistency, content decay, attribution gaps
- `CAMPAIGN_ISSUES.md` — campaign failures, channel problems, deliverability issues, performance drops
- `FEATURE_REQUESTS.md` — marketing tools, automation, analytics capabilities

### Promotion Targets

When marketing learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Messaging patterns | Brand guidelines | "Enterprise segment requires ROI-first messaging, not feature lists" |
| Channel insights | Channel playbooks | "LinkedIn carousel ads outperform single-image by 3x for B2B" |
| Audience shifts | Audience personas | "ICP shifted from SMB founders to mid-market VPs of Engineering" |
| Content patterns | Content calendar | "Publish comparison posts after competitor launches" |
| Attribution fixes | Attribution model | "Always use server-side UTM capture for redirect chains" |
| Email patterns | `TOOLS.md` | "Warm new sending domains for 14 days minimum" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-marketing
openclaw hooks enable self-improving-marketing
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

#### Self-Improving Marketing Workflow

When marketing issues or insights are discovered:
1. Log to `.learnings/CAMPAIGN_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Brand guidelines — messaging tone, positioning, and identity rules
   - Channel playbooks — per-channel strategy and benchmarks
   - Audience personas — updated ICP definitions and segment profiles
   - Content calendars — content type cadence and topic frameworks
   - Attribution models — tagging standards and measurement methodology

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: content | campaigns | seo | social | email | paid_media | analytics

### Summary
One-line description of the marketing insight

### Details
Full context: what happened in the campaign or channel, why the expected outcome
differed from actual, what the correct approach or messaging strategy should be.
Include relevant metrics (CTR, CVR, CPL, ROAS) with before/after comparison.

### Evidence

**Metrics before:**
- CTR: X.X%
- Conversion rate: X.X%
- CPL: $XX.XX

**Metrics after (or expected):**
- CTR: X.X%
- Conversion rate: X.X%
- CPL: $XX.XX

### Suggested Action
Specific campaign adjustment, messaging change, targeting update, or process improvement

### Metadata
- Source: analytics_dashboard | a_b_test | campaign_report | brand_audit | customer_feedback | attribution_tool
- Channel: google_ads | meta_ads | linkedin | email | organic_search | social | direct
- Segment: enterprise | mid_market | smb | consumer | all
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: messaging_miss.wrong_value_prop | audience_drift.icp_shift (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `messaging_miss` | Value proposition, copy, or positioning failed to resonate with target segment |
| `channel_underperformance` | Channel metrics (CTR, CPL, ROAS) fall significantly below benchmarks |
| `audience_drift` | Target audience behavior, demographics, or needs have shifted |
| `brand_inconsistency` | Messaging, visual identity, or tone deviates from brand guidelines |
| `attribution_gap` | Tracking breaks, UTM parameters lost, conversion path unclear |
| `content_decay` | Previously high-performing content loses traffic or engagement over time |

### Campaign Issue Entry [CMP-YYYYMMDD-XXX]

Append to `.learnings/CAMPAIGN_ISSUES.md`:

```markdown
## [CMP-YYYYMMDD-XXX] issue_description

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: content | campaigns | seo | social | email | paid_media | analytics

### Summary
Brief description of the campaign problem

### Performance Data
- Campaign: campaign name or ID (redacted if needed)
- Channel: google_ads | meta_ads | linkedin | email | organic_search
- Date Range: YYYY-MM-DD to YYYY-MM-DD
- Budget Spent: $X,XXX
- Key Metrics:
  - Impressions: XX,XXX
  - Clicks: X,XXX
  - CTR: X.X% (benchmark: X.X%)
  - Conversions: XXX
  - CVR: X.X% (benchmark: X.X%)
  - CPL: $XX.XX (benchmark: $XX.XX)
  - ROAS: X.Xx (benchmark: X.Xx)

### Root Cause
What in the campaign setup, targeting, creative, or messaging caused the issue.

### Fix Applied
What changes were made to address the problem.

### Prevention
How to avoid this issue in future campaigns (checklist item, review step, automation)

### Context
- Trigger: performance_alert | manual_review | a_b_test | customer_complaint | deliverability_report
- Campaign Type: lead_gen | brand_awareness | retargeting | nurture | product_launch | event_promotion
- Audience: target segment description

### Metadata
- Reproducible: yes | no | unknown
- Related Campaigns: campaign-name-or-id
- See Also: CMP-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: content | campaigns | seo | social | email | paid_media | analytics

### Requested Capability
What marketing tool, automation, or analytics capability is needed

### User Context
Why it's needed, what workflow it improves, what manual process it replaces

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: dashboard widget, automation rule, integration, report template, alert system

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_feature

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `CMP` (campaign issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `CMP-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Campaign/Initiative**: Q1 Product Launch v2
- **Notes**: Updated messaging to lead with ROI data instead of feature list
```

Other status values:
- `in_progress` — Actively being optimized or fixed
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to brand guidelines, playbook, or persona doc
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**CTR / Click Performance** (→ campaign issue or learning):
- CTR drops >20% from previous period or campaign benchmark
- Email open rate decline >15% week-over-week
- Landing page bounce rate exceeds 70%

**Conversion Performance** (→ campaign issue with performance data):
- Conversion rate declines >15% from baseline
- CPL exceeds benchmark by >50%
- ROAS drops below break-even threshold
- Funnel drop-off spikes at a specific stage

**Email Deliverability** (→ campaign issue with deliverability trigger):
- Bounce rate exceeds 5% (hard bounces)
- Spam complaint rate exceeds 0.1%
- Domain reputation score drops
- Unsubscribe rate spikes >2x normal

**Organic / SEO** (→ learning with content_decay or campaign issue):
- Organic traffic drops >25% month-over-month
- Top-ranking page loses position by 5+ spots
- Core Web Vitals fail threshold
- Featured snippet lost to competitor

**Social / Engagement** (→ learning with channel_underperformance):
- Engagement rate drops >30% from average
- Follower growth stalls or turns negative
- Comment sentiment shifts negative

**Brand / Messaging** (→ learning with brand_inconsistency or messaging_miss):
- Brand sentiment shifts negative in monitoring tools
- Customer feedback mentions confusion about positioning
- Internal teams use inconsistent value propositions

**Attribution / Tracking** (→ learning with attribution_gap):
- UTM parameters missing or malformed on campaign URLs
- Redirect chains strip tracking parameters
- Cross-domain tracking breaks between properties
- Multi-touch attribution model shows >30% unattributed conversions

## Priority Guidelines

| Priority | When to Use | Marketing Examples |
|----------|-------------|-------------------|
| `critical` | Brand crisis, major campaign failure with significant budget waste, data breach affecting customers | PR crisis from messaging mistake, $50K+ budget spent on broken tracking, sending PII in email blast |
| `high` | Significant CTR/conversion drops, deliverability issues affecting large audience, attribution fully broken | CPL 3x above benchmark for >1 week, bounce rate >10%, all UTMs stripped by new redirect |
| `medium` | Channel underperformance, content decay, gradual audience drift, minor brand inconsistency | Blog post lost 40% traffic after update, LinkedIn ads below median CTR, persona needs refresh |
| `low` | Minor copy improvements, process optimization, small tracking gaps, cosmetic brand issues | Subject line A/B test insight, minor UTM naming inconsistency, social post timing optimization |

## Area Tags

Use to filter learnings by marketing domain:

| Area | Scope |
|------|-------|
| `content` | Blog posts, landing pages, whitepapers, case studies, video content, webinars |
| `campaigns` | Campaign strategy, multi-channel orchestration, launch planning, promotions |
| `seo` | Organic search, keyword strategy, technical SEO, content optimization, link building |
| `social` | Social media strategy, community management, organic social, influencer partnerships |
| `email` | Email campaigns, nurture sequences, deliverability, list hygiene, segmentation |
| `paid_media` | PPC, display ads, social ads, programmatic, retargeting, budget allocation |
| `analytics` | Attribution, reporting, dashboards, A/B testing, conversion tracking, data quality |

## Promoting to Permanent Marketing Standards

When a learning is broadly applicable (not a one-off campaign fix), promote it to permanent marketing standards.

### When to Promote

- Messaging pattern proves effective across 3+ campaigns or segments
- Channel insight applies to all campaigns on that platform
- Audience shift is confirmed by multiple data sources over 2+ quarters
- Attribution fix prevents a class of tracking errors, not just one campaign
- Brand rule violation occurs in 3+ assets from different teams

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Brand guidelines | Messaging tone, positioning statements, visual identity rules, do/don't examples |
| Channel playbooks | Per-channel best practices, benchmarks, creative specs, targeting strategies |
| Audience personas | ICP definitions, segment profiles, buying triggers, objection handling |
| Content calendar | Content type cadence, topic frameworks, seasonal planning, repurposing rules |
| Attribution model | UTM taxonomy, tagging standards, measurement methodology, reporting templates |
| `TOOLS.md` | Marketing tool configurations, integration gotchas, API limits |
| `AGENTS.md` | Automated marketing workflows, review checkpoints |

### How to Promote

1. **Distill** the learning into a concise guideline, checklist item, or rule
2. **Add** to appropriate target (brand doc, playbook, persona profile)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: brand guidelines` (or `channel playbook`, `persona doc`, `content calendar`, `attribution model`)

### Promotion Examples

**Learning** (verbose):
> Product launch email sent to enterprise segment with SMB-focused messaging.
> Used "easy setup" and "affordable pricing" — enterprise buyers want ROI data,
> security compliance, and integration capabilities. Open rate 8% vs. 22% benchmark.

**As brand guideline** (concise):
```markdown
## Enterprise Messaging Rules
- Lead with ROI metrics and business impact, not ease-of-use
- Reference security certifications (SOC2, ISO 27001) in first fold
- Include integration ecosystem and API capabilities
- Avoid "affordable" or "cheap" — use "cost-effective" with TCO comparison
```

**Learning** (verbose):
> LinkedIn carousel ads outperform single-image for B2B. 12 campaigns, 3 months:
> 2.8x higher CTR, 1.9x lower CPL. Best with 5-7 slides, data-driven, strong hook.

**As channel playbook** (actionable):
```markdown
## LinkedIn Ad Creative Guidelines
- Default to carousel format for B2B educational content (5-7 slides)
- First slide: strong hook (question or bold stat)
- Benchmark CTR: 0.8-1.2% (carousel) vs. 0.3-0.5% (single image)
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: CMP-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring marketing issues often indicate:
   - Missing brand guideline (→ add to brand standards)
   - Outdated persona (→ refresh audience research)
   - Broken process (→ add to campaign checklist)
   - Attribution gap (→ fix tracking infrastructure)

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before launching a new campaign in the same channel
- After completing a campaign or content initiative
- When the same performance pattern appears again
- Monthly during active campaign periods
- Quarterly for audience persona and brand guideline updates

### Quick Status Check
```bash
# Count pending marketing issues
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority campaign issues
grep -B5 "Priority\*\*: high" .learnings/CAMPAIGN_ISSUES.md | grep "^## \["

# Find all messaging misses
grep -B2 "messaging_miss" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve fixed campaign issues
- Promote recurring patterns to brand guidelines or playbooks
- Link related entries across files
- Update attribution model with tracking fixes

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
        "command": "./skills/self-improving-marketing/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a marketing-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-marketing/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-marketing/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for campaign performance issues, deliverability problems, and tracking errors.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate marketing learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on campaign issues, deliverability errors, tracking problems |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a marketing learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same campaign pattern in 2+ channels or quarters |
| **Verified** | Status is `resolved` with proven fix and measured improvement |
| **Non-obvious** | Required actual analysis, testing, or investigation |
| **Broadly applicable** | Not campaign-specific; useful across segments or channels |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-marketing/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-marketing/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with marketing-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

Use conversation signals ("This campaign pattern keeps working", "Save this as a playbook") to identify extraction candidates.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Best Practices

1. **Log immediately** — campaign context and metrics fade fast after the moment passes
2. **Include before/after metrics** — quantify the impact with CTR, CVR, CPL, ROAS comparisons
3. **Specify the channel** — patterns differ between Google Ads, LinkedIn, email, organic
4. **A/B test before scaling** — never scale a campaign change based on gut feel alone
5. **Document creative rationale** — why a headline, image, or CTA was chosen for the segment
6. **Track attribution end-to-end** — verify UTMs survive redirects, link shorteners, and cross-domain hops
7. **Review personas quarterly** — audience needs and behaviors shift; validate with data
8. **Audit brand consistency monthly** — check all active assets against current brand guidelines
9. **Promote aggressively** — if a messaging pattern works across 3+ campaigns, codify it

## Gitignore Options

**Keep learnings local** (per-team):
```gitignore
.learnings/
```

**Track learnings in repo** (org-wide):
Don't add to .gitignore — learnings become shared marketing knowledge.

**Hybrid** (track templates, ignore entries): add `.learnings/*.md` and `!.learnings/.gitkeep` to `.gitignore`.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/marketing/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: marketing
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (marketing)
Only trigger this skill automatically for marketing signals such as:
- `campaign|ctr|conversion|attribution|creative test`
- `persona|positioning|channel mix|cac|roas`
- explicit marketing intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/marketing/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
