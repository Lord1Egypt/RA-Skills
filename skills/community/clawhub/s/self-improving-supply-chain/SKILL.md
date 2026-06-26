---
name: self-improving-supply-chain
description: "Captures forecast errors, supplier risks, logistics delays, inventory mismatches, quality deviations, and demand signal shifts to enable continuous supply chain improvement. Use when: (1) A stockout or backorder event occurs, (2) A delivery SLA is missed, (3) Supplier lead time increases, (4) Quality rejection rate spikes, (5) Demand forecast vs. actual variance exceeds 15%, (6) Warehouse capacity threshold is breached, (7) A procurement or routing decision needs documentation."
---

# Self-Improving Supply Chain Skill

Log supply chain learnings, disruption patterns, and feature requests to markdown files for continuous improvement. Captures forecast errors, supplier risks, logistics delays, inventory mismatches, quality deviations, and demand signal shifts. Important learnings get promoted to supplier scorecards, safety stock policies, routing playbooks, demand planning models, or quality acceptance criteria.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Supply Chain Learnings\n\nForecast errors, supplier risks, logistics delays, inventory mismatches, quality deviations, and demand signal shifts captured during operations.\n\n**Categories**: forecast_error | supplier_risk | logistics_delay | inventory_mismatch | quality_deviation | demand_signal_shift\n**Areas**: procurement | inventory | logistics | manufacturing | quality | demand_planning | warehousing\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/SUPPLY_CHAIN_ISSUES.md ] || printf "# Supply Chain Issues Log\n\nStockouts, delivery delays, supplier failures, quality rejections, and capacity breaches.\n\n---\n" > .learnings/SUPPLY_CHAIN_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nSupply chain tools, automation capabilities, and operational improvements.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log proprietary supplier pricing, negotiated contract terms, or customer-identifiable order data. Prefer aggregated metrics and redacted summaries over raw PO numbers or customer names.
This skill is documentation-only: it does not execute purchases, place orders, trigger procurement transactions, or call external payment systems.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Stockout event detected | Log to `.learnings/SUPPLY_CHAIN_ISSUES.md` with category `inventory_mismatch` |
| Delivery late or SLA missed | Log to `.learnings/SUPPLY_CHAIN_ISSUES.md` with category `logistics_delay` |
| Supplier lead time increased | Log to `.learnings/LEARNINGS.md` with category `supplier_risk` |
| Quality rejection or defect spike | Log to `.learnings/SUPPLY_CHAIN_ISSUES.md` with category `quality_deviation` |
| Demand forecast off by >15% | Log to `.learnings/LEARNINGS.md` with category `forecast_error` |
| Warehouse at or above 90% capacity | Log to `.learnings/SUPPLY_CHAIN_ISSUES.md` with category `inventory_mismatch` |
| Demand spike from external signal | Log to `.learnings/LEARNINGS.md` with category `demand_signal_shift` |
| Recurring supply chain pattern | Link with `**See Also**`, consider priority bump |
| Broadly applicable pattern | Promote to scorecard, policy, playbook, or model |
| Reusable operational process | Promote to skill extraction |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-supply-chain
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-supply-chain.git ~/.openclaw/skills/self-improving-supply-chain
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
    ├── SUPPLY_CHAIN_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — forecast errors, supplier risks, demand signal shifts
- `SUPPLY_CHAIN_ISSUES.md` — stockouts, delays, quality problems, capacity breaches
- `FEATURE_REQUESTS.md` — supply chain tools, automation, operational capabilities

### Promotion Targets

When supply chain learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Supplier performance patterns | Supplier scorecards | "Require dual-source for components >$50K annual spend" |
| Inventory buffer patterns | Safety stock policies | "Ocean-freight SKUs carry 3 weeks safety stock" |
| Routing optimizations | Routing playbooks | "Divert to Nansha when Yantian queue >5 days" |
| Forecast accuracy patterns | Demand planning models | "Apply seasonal index for gift-category Q4 SKUs" |
| Quality failure patterns | Quality acceptance criteria | "100% inspection on first shipment from new suppliers" |
| Workflow patterns | `AGENTS.md` | "Run inventory reconciliation before reorder point calc" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-supply-chain
openclaw hooks enable self-improving-supply-chain
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

#### Self-Improving Supply Chain Workflow

When supply chain disruptions or patterns are discovered:
1. Log to `.learnings/SUPPLY_CHAIN_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Supplier scorecards — performance thresholds, risk tiers, qualification requirements
   - Safety stock policies — buffer calculations, service level targets, review cadence
   - Routing playbooks — contingency routes, mode-shift triggers, carrier selection
   - Demand planning models — seasonal indices, channel mix adjustments, event-driven overlays

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: procurement | inventory | logistics | manufacturing | quality | demand_planning | warehousing

### Summary
One-line description of the supply chain insight

### Details
Full context: what operational condition was observed, why it matters,
what the root cause is, and what the downstream impact was.
Include quantified metrics where possible (units, cost, days, fill rate).

### Impact
- Units affected: X
- Cost impact: $Y
- Duration: Z days
- Service level impact: from A% to B%

### Suggested Action
Specific policy change, process improvement, or operational adjustment to adopt

### Metadata
- Source: demand_forecast_review | supplier_communication | warehouse_audit | quality_inspection | order_management | logistics_tracking
- SKU/Component: identifier (if applicable)
- Supplier: name and code (if applicable)
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: forecast_error.seasonal_miss | supplier_risk.single_source (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `forecast_error` | Demand forecast deviates significantly from actuals (MAPE >15%) |
| `supplier_risk` | Supplier lead time increase, financial distress, capacity constraint, single-source exposure |
| `logistics_delay` | Shipment delay, port congestion, carrier failure, customs hold, routing inefficiency |
| `inventory_mismatch` | WMS vs physical count variance, stockout, overstock, expired inventory, capacity breach |
| `quality_deviation` | Defect rate spike, inspection failure, non-conformance, recall, specification drift |
| `demand_signal_shift` | Unexpected demand change from viral event, channel shift, competitor action, regulation |

### Supply Chain Issue Entry [SCM-YYYYMMDD-XXX]

Append to `.learnings/SUPPLY_CHAIN_ISSUES.md`:

```markdown
## [SCM-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: procurement | inventory | logistics | manufacturing | quality | demand_planning | warehousing

### Summary
Brief description of the supply chain disruption or issue

### Details
What happened, when, where in the supply chain, and what triggered it.

### Impact
- Units affected: X
- Cost impact: $Y (direct + indirect)
- Duration: Z days
- Customer impact: fill rate drop, delayed orders, SLA breach

### Mitigation Steps
1. Immediate containment action
2. Short-term workaround
3. Root cause investigation
4. Long-term corrective action

### Root Cause
What in the supply chain caused this issue. Include contributing factors.

### Context
- Trigger: stockout_event | delivery_sla_miss | supplier_lead_time_increase | quality_rejection_spike | forecast_variance | capacity_breach
- Carrier/Supplier: name and code
- Route/Lane: origin → destination
- SKU/Component: identifiers affected

### Metadata
- Reproducible: yes | no | seasonal | event_driven
- Related Files: path/to/file.ext
- See Also: SCM-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: procurement | inventory | logistics | manufacturing | quality | demand_planning | warehousing

### Requested Capability
What supply chain tool, automation, or capability is needed

### User Context
Why it's needed, what workflow it improves, what operational problem it solves

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: dashboard, integration, alert system, optimization model, workflow automation

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_system

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `SCM` (supply chain issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `SCM-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is resolved, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Corrective Action**: policy change / supplier qualification / routing update / safety stock adjustment
- **Notes**: Description of what was done and verification of effectiveness
```

Other status values:
- `in_progress` — Actively being investigated or mitigated
- `wont_fix` — Accepted risk or not actionable (add reason in Resolution notes)
- `promoted` — Elevated to scorecard, policy, playbook, or model
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**Inventory Below Safety Stock** (→ supply chain issue with inventory_mismatch):
- Available stock drops below reorder point
- Safety stock consumed with no inbound PO in transit
- Allocation conflict between customer orders
- WMS alerts for zero-available or negative-available

**Delivery Tracking Shows Delay** (→ supply chain issue with logistics_delay):
- Carrier tracking shows ETA pushed beyond original commitment
- Port congestion reports for origin or destination terminal
- Customs hold or inspection delay notification
- Mode conversion required (ocean → air) to meet deadline

**Supplier Communication Indicating Lead Time Change** (→ learning with supplier_risk):
- Supplier notifies of capacity reduction or allocation
- Lead time quoted on new PO exceeds historical average by >20%
- Supplier financial health downgrade (D&B, credit report)
- Force majeure notification from supplier

**Quality Inspection Failure Rate >2%** (→ supply chain issue with quality_deviation):
- Incoming quality inspection rejection rate exceeds 2% threshold
- Customer return rate for quality reasons exceeds 1%
- Supplier corrective action request (SCAR) issued
- Specification non-conformance on critical dimension

**Demand Forecast MAPE >15%** (→ learning with forecast_error):
- Monthly MAPE exceeds 15% at SKU-family level
- Bias consistently positive (underforecast) or negative (overforecast) for 3+ months
- New product launch demand significantly different from analogous forecast
- Promotional lift or cannibalization not captured in model

**Warehouse Utilization >90%** (→ supply chain issue with inventory_mismatch):
- DC utilization exceeds 90% of total capacity
- Receiving dock backlog exceeds 48 hours
- Put-away queue growing faster than processing rate
- Overflow to secondary or temporary storage required

## Priority Guidelines

| Priority | When to Use | Supply Chain Examples |
|----------|-------------|----------------------|
| `critical` | Production line stopped, customer order unfulfillable, safety/recall issue | Factory shut down waiting for parts, complete stockout on top-10 SKU, product recall initiated |
| `high` | Stockout imminent, supplier failure likely, major SLA breach | Safety stock below 3 days, sole-source supplier in financial distress, 50+ orders delayed |
| `medium` | Forecast accuracy degradation, routing inefficiency, quality trend | MAPE trending up over 3 months, suboptimal carrier selection, rejection rate at 1.5% |
| `low` | Process documentation, minor optimization, data cleanup | SOP update needed, rounding error in forecast, warehouse label format change |

## Area Tags

Use to filter learnings by supply chain domain:

| Area | Scope |
|------|-------|
| `procurement` | Supplier selection, PO management, contract negotiation, spend analysis, qualification |
| `inventory` | Safety stock, reorder points, cycle counting, ABC classification, obsolescence |
| `logistics` | Freight, routing, carrier management, customs, last-mile, mode selection |
| `manufacturing` | Production planning, BOM management, capacity, yield, changeover |
| `quality` | Inspection, SCAR, non-conformance, acceptance criteria, certification |
| `demand_planning` | Forecasting, seasonal decomposition, promotional planning, new product introduction |
| `warehousing` | Storage, picking, packing, receiving, put-away, layout, capacity |

## Promoting to Permanent Operational Standards

When a learning is broadly applicable (not a one-off event), promote it to permanent operational standards.

### When to Promote

- Same supplier issue recurs across multiple quarters
- Forecast error pattern appears for 3+ SKU families
- Logistics delay from same lane or carrier happens 3+ times
- Quality issue at same supplier or component recurs
- Inventory mismatch pattern found in 2+ distribution centers

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Supplier scorecards | Performance thresholds, risk tier definitions, qualification requirements |
| Safety stock policies | Buffer calculations by sourcing mode, service level targets, review cadence |
| Routing playbooks | Contingency routes, mode-shift triggers, carrier escalation matrix |
| Demand planning models | Seasonal indices, event overlays, channel mix assumptions |
| Quality acceptance criteria | Inspection sampling plans, reject thresholds, first-article requirements |
| `AGENTS.md` | Automated operational workflows, pre-reorder checks |

### How to Promote

1. **Distill** the learning into a concise rule or policy statement
2. **Add** to appropriate target (scorecard, policy, playbook, model)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: safety stock policy` (or `supplier scorecard`, `routing playbook`, `demand model`, `quality criteria`)

### Promotion Examples

**Learning** (verbose):
> Ocean-freight SKUs experience 10-21 day lead time variability. Existing 2-week
> safety stock insufficient — caused 4 stockouts in 6 months.

**As safety stock policy** (concise):
```markdown
## Ocean-Freight Safety Stock
- Buffer: 3 weeks of average weekly demand
- Review: quarterly against actual lead time data
- Trigger: adjust if lead time std dev changes >20%
```

**Learning** (verbose):
> Port congestion at Yantian added 14 days to 12 containers. Diverting to Nansha
> saved 7 days on 4 containers. West Coast routing avoided congestion entirely.

**As routing playbook** (actionable):
```markdown
## Yantian Congestion Response
1. Monitor Yantian vessel queue daily via CargoSmart
2. If berthing wait >5 days: divert new bookings to Nansha
3. If congestion >10 days: activate West Coast routing via Long Beach
4. Air-freight top 8 critical SKUs if customer SLA at risk
5. Notify customer service for affected order ETAs
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: SCM-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring supply chain issues often indicate:
   - Missing safety stock buffer (→ adjust policy)
   - Supplier concentration risk (→ qualification of alternate)
   - Forecast model gap (→ add decomposition or overlay)
   - Process gap (→ add SOP or checklist)

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before finalizing replenishment plans
- After month-end demand review
- When the same disruption type appears again
- Quarterly during S&OP planning cycle

### Quick Status Check
```bash
# Count pending supply chain issues
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority issues
grep -B5 "Priority\*\*: high" .learnings/SUPPLY_CHAIN_ISSUES.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: logistics" .learnings/*.md

# Find all supplier risk entries
grep -B2 "supplier_risk" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve mitigated issues
- Promote recurring patterns to policies and playbooks
- Link related entries across files
- Extract reusable processes as skills

## Simplify & Harden Feed

Ingest recurring supply chain patterns from `simplify-and-harden` into policies or playbooks.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ quarters or locations, within 12-month window.
Targets: supplier scorecards, safety stock policies, routing playbooks, demand models, `AGENTS.md`.

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
        "command": "./skills/self-improving-supply-chain/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a supply chain-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Disruption Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-supply-chain/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-supply-chain/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for stockouts, delays, shortages, defects, and other supply chain disruptions.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate supply chain learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on stockouts, delays, shortages, quality issues |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a supply chain learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same disruption pattern in 2+ quarters or locations |
| **Verified** | Status is `resolved` with effective corrective action |
| **Non-obvious** | Required investigation or cross-functional coordination |
| **Broadly applicable** | Not specific to one SKU or supplier; useful across categories |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-supply-chain/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-supply-chain/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with supply chain-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

**In conversation**: "This delay keeps happening", "Save this process as a skill", "Every quarter we hit this issue", "We need a standard playbook for this".

**In entries**: Multiple `See Also` links, high priority + resolved, `supplier_risk` or `logistics_delay` with broad applicability, same `Pattern-Key` across quarters or DCs.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Best Practices

1. **Log immediately** — operational context fades fast after disruption resolution
2. **Quantify impact** — always include units, cost, days, and service level metrics
3. **Specify the supply chain node** — supplier, DC, lane, or SKU family affected
4. **Track lead times weekly** — detect trends before they cause stockouts
5. **Validate forecasts monthly** — compare forecast vs. actual at SKU-family level using MAPE and bias
6. **Diversify suppliers** — no single-source for components with >$50K annual spend
7. **Maintain safety stock** — buffer by sourcing mode (ocean 3wk, air 1wk, domestic 1.5wk)
8. **Inspect at receiving** — verify quantity and quality before receipting into WMS
9. **Document routing decisions** — record why a lane or mode was chosen for future reference
10. **Promote aggressively** — if a pattern recurs across 2+ quarters, it deserves a policy

## Gitignore Options

**Keep learnings local** (per-team): add `.learnings/` to `.gitignore`.
**Track learnings in repo** (organization-wide): don't gitignore — learnings become shared operational knowledge.
**Hybrid**: gitignore `.learnings/*.md` but keep `.learnings/.gitkeep`.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/supply-chain/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: supply-chain
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (supply-chain)
Only trigger this skill automatically for supply-chain signals such as:
- `lead time|stockout|safety stock|supplier delay|fill rate`
- `forecast bias|otif|procurement|lane disruption|inventory`
- explicit supply-chain intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/supply-chain/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
