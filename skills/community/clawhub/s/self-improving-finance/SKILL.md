---
name: self-improving-finance
description: "Captures reconciliation errors, forecast variances, control weaknesses, regulatory gaps, valuation errors, and cash flow anomalies to enable continuous finance operations improvement. Use when: (1) A reconciliation break is identified, (2) Budget vs. actual variance exceeds 10%, (3) A SOX control test fails, (4) A close task misses its deadline, (5) An intercompany imbalance is discovered, (6) An unusual journal entry is flagged by audit, (7) AR aging spikes past 90 days."
---

# Self-Improving Finance Skill

Log finance-specific learnings, operational issues, and feature requests to markdown files for continuous improvement. Captures reconciliation errors, forecast variances, control weaknesses, regulatory gaps, valuation errors, and cash flow anomalies. Important learnings get promoted to close checklists, reconciliation procedures, control matrices, tax calendars, forecast models, or audit response templates.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Finance Learnings\n\nReconciliation errors, control weaknesses, forecast variances, regulatory gaps, valuation errors, and cash flow anomalies captured during finance operations.\n\n**Categories**: reconciliation_error | forecast_variance | control_weakness | regulatory_gap | valuation_error | cash_flow_anomaly\n**Areas**: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/FINANCE_ISSUES.md ] || printf "# Finance Issues Log\n\nReconciliation breaks, control failures, forecast misses, regulatory findings, and cash flow anomalies.\n\n---\n" > .learnings/FINANCE_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nFinance tools, automation capabilities, and process improvements requested during finance operations.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

> **IMPORTANT — Data Sensitivity**: NEVER log actual account numbers, bank routing numbers, specific financial figures for real entities, audit findings with client names, taxpayer identification numbers, or any personally identifiable financial information. Always abstract and anonymize. Use placeholders like "Entity A", "$X.XM", "Account XXXX-1234", or percentage-based descriptions. Financial data is highly regulated under SOX, GDPR, PCI-DSS, and other frameworks. Treat all logged content as if it could be read by an external auditor.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Reconciliation break identified | Log to `.learnings/FINANCE_ISSUES.md` with reconciliation details |
| Budget vs. actual variance >10% | Log to `.learnings/FINANCE_ISSUES.md` with variance analysis |
| SOX control test fails | Log to `.learnings/FINANCE_ISSUES.md` with control failure details |
| Late close item discovered | Log to `.learnings/FINANCE_ISSUES.md` with deadline impact |
| Intercompany imbalance found | Log to `.learnings/FINANCE_ISSUES.md` with entity mismatch |
| Unusual journal entry flagged by audit | Log to `.learnings/FINANCE_ISSUES.md` with JE anomaly |
| AR aging past 90 days | Log to `.learnings/FINANCE_ISSUES.md` with aging bucket analysis |
| Control weakness identified | Log to `.learnings/LEARNINGS.md` with category `control_weakness` |
| Regulatory gap discovered | Log to `.learnings/LEARNINGS.md` with category `regulatory_gap` |
| Valuation model error | Log to `.learnings/LEARNINGS.md` with category `valuation_error` |
| Cash flow anomaly detected | Log to `.learnings/LEARNINGS.md` with category `cash_flow_anomaly` |
| Forecast methodology improvement | Log to `.learnings/LEARNINGS.md` with category `forecast_variance` |
| Recurring reconciliation pattern | Link with `**See Also**`, consider priority bump |
| Broadly applicable procedure | Promote to close checklist, control matrix, or reconciliation procedure |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-finance
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-finance.git ~/.openclaw/skills/self-improving-finance
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
    ├── FINANCE_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — reconciliation errors, control weaknesses, forecast variances, regulatory gaps, valuation errors, cash flow anomalies
- `FINANCE_ISSUES.md` — reconciliation breaks, control failures, regulatory findings, close delays
- `FEATURE_REQUESTS.md` — finance tools, automation, reporting capabilities

### Promotion Targets

When finance learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Close procedures | Close checklists | "Verify intercompany eliminations before consolidation" |
| Reconciliation patterns | Reconciliation procedures | "Three-way match for AP: PO, receipt, invoice" |
| Control gaps | Control matrices | "Journal entries >$X require dual approval" |
| Tax compliance | Tax calendars | "Embedded lease review before ASC 842 filing" |
| Forecast improvements | Forecast models | "Weight pipeline deals by stage probability" |
| Audit findings | Audit response templates | "Standard response for revenue recognition inquiries" |
| Workflow patterns | `AGENTS.md` | "Run trial balance before close meeting" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-finance
openclaw hooks enable self-improving-finance
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

#### Self-Improving Finance Workflow

When finance issues or patterns are discovered:
1. Log to `.learnings/FINANCE_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Close checklists — month-end and quarter-end close procedures
   - Reconciliation procedures — step-by-step account reconciliation guides
   - Control matrices — SOX controls, approval workflows, segregation of duties
   - Tax calendars — filing deadlines, compliance milestones
   - Forecast models — revenue and expense projection methodologies
   - Audit response templates — standard responses for common audit inquiries

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable

### Summary
One-line description of the finance insight

### Details
Full context: what reconciliation error, control gap, or valuation issue was found,
why it matters for financial accuracy, and what the correct procedure or treatment is.
Include anonymized figures and account references.

### Correct Treatment

**Before (incorrect):**
Description of the incorrect accounting treatment, reconciliation approach,
or control procedure. Use anonymized examples only.

**After (correct):**
Description of the correct treatment, procedure, or control.

### Suggested Action
Specific process change, control enhancement, or procedure update to adopt.
Reference applicable standards (ASC, IFRS, SOX section) where relevant.

### Metadata
- Source: reconciliation | close_review | audit_finding | variance_analysis | control_test | regulatory_update
- Framework: US_GAAP | IFRS | SOX | local_GAAP
- Related Accounts: anonymized account references
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: reconciliation.fx_conversion | control.approval_bypass (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `reconciliation_error` | Account balance discrepancy, bank rec break, intercompany mismatch |
| `forecast_variance` | Budget vs. actual deviation, revenue miss, expense overrun |
| `control_weakness` | Missing approval, segregation of duties gap, access control issue |
| `regulatory_gap` | Non-compliance with accounting standard, missed regulatory requirement |
| `valuation_error` | Incorrect fair value, wrong depreciation method, impairment oversight |
| `cash_flow_anomaly` | Unexpected cash movement, timing difference, liquidity event |

### Finance Issue Entry [FIN-YYYYMMDD-XXX]

Append to `.learnings/FINANCE_ISSUES.md`:

```markdown
## [FIN-YYYYMMDD-XXX] issue_type

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable

### Summary
Brief description of the finance issue (anonymized)

### Issue Details
What was found during reconciliation, close, audit, or analysis.
Include anonymized amounts, account references, and entity names.
NEVER include real account numbers, bank details, or client names.

### Root Cause
What process gap, system error, or procedural failure caused this issue.

### Impact
- Financial statement impact (material / immaterial, estimated range)
- Regulatory exposure (SOX deficiency classification if applicable)
- Operational impact (close delay, restatement risk, cash flow effect)

### Remediation
Steps taken or recommended to resolve the issue and prevent recurrence.
Reference control framework requirements where applicable.

### Context
- Trigger: reconciliation | close_review | audit | variance_analysis | control_test | aging_review
- Period: fiscal quarter or month affected
- Entity: anonymized entity reference
- System: ERP, GL, or sub-ledger involved

### Metadata
- Materiality: material | immaterial | pending_assessment
- Related Accounts: anonymized references
- See Also: FIN-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable

### Requested Capability
What finance tool, automation, or process improvement is needed

### User Context
Why it's needed, what workflow it improves, what risk it mitigates

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: ERP configuration, report template, reconciliation script,
control automation, or process redesign

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_process

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `FIN` (finance issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `FIN-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is resolved, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Reference**: adjusting JE #1234 or control remediation ticket
- **Notes**: Updated reconciliation procedure / added control step / revised forecast model
```

Other status values:
- `in_progress` — Actively being remediated or investigated
- `wont_fix` — Determined immaterial or accepted risk (add reason in Resolution notes)
- `promoted` — Elevated to close checklist, control matrix, or reconciliation procedure
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**Reconciliation Breaks** (→ finance issue with reconciliation trigger):
- Account balance discrepancy of any amount (reconciliation difference >$0)
- Bank reconciliation unreconciled items
- Intercompany balance mismatch between entities
- Sub-ledger to general ledger variance

**Budget & Forecast Variances** (→ finance issue with variance_analysis trigger):
- Budget vs. actual variance exceeding 10% on any line item
- Revenue forecast miss by more than one standard deviation
- Capital expenditure overrun vs. approved budget

**Control Failures** (→ finance issue with control_test trigger):
- SOX control test failure (key control or compensating control)
- Journal entry exceeding materiality threshold without dual approval
- Segregation of duties violation detected
- Access control exception (unauthorized GL posting)

**Close Process Issues** (→ finance issue with close_review trigger):
- Close task past its deadline
- Pending adjusting entries at close cutoff
- Unresolved reconciling items carried forward

**Audit Flags** (→ finance issue with audit trigger):
- Unusual journal entry flagged (round amounts, off-hours posting, above threshold)
- Revenue recognition timing question
- Related-party transaction without proper disclosure

**Receivables & Payables** (→ finance issue with aging_review trigger):
- AR aging spike past 90 days (concentration or volume)
- Duplicate payment detected in AP
- Vendor invoice without purchase order match

**Regulatory & Standards** (→ learning with regulatory_gap category):
- New accounting standard not yet implemented (ASC, IFRS updates)
- Tax law change affecting current period
- Transfer pricing documentation gap

## Priority Guidelines

| Priority | When to Use | Finance Examples |
|----------|-------------|-----------------|
| `critical` | Material misstatement risk, regulatory penalty exposure | Restatement required, SEC comment letter, material weakness in ICFR |
| `high` | SOX control failure, reconciliation break, cash flow crisis | Key control deficiency, unreconciled bank balance >materiality, covenant breach risk |
| `medium` | Forecast variance, process improvement, non-critical control gap | Q3 revenue 15% below forecast, manual workaround in close process, compensating control relied upon |
| `low` | Documentation update, minor procedure enhancement | Reconciliation template needs update, naming convention for GL accounts, archive policy for supporting schedules |

## Area Tags

Use to filter learnings by finance domain:

| Area | Scope |
|------|-------|
| `accounting` | General ledger, journal entries, chart of accounts, period close, consolidation |
| `treasury` | Cash management, bank relationships, debt/investment, FX exposure, liquidity |
| `tax` | Income tax provision, sales/use tax, transfer pricing, tax compliance filings |
| `audit` | Internal audit, external audit support, SOX testing, control documentation |
| `budgeting` | Annual budget, rolling forecasts, variance analysis, capital planning |
| `reporting` | Financial statements, management reporting, regulatory filings, board packages |
| `accounts_payable` | Vendor invoices, payment processing, three-way match, 1099 reporting |
| `accounts_receivable` | Customer invoicing, collections, credit memos, aging analysis, bad debt |

## Promoting to Permanent Finance Procedures

When a learning is broadly applicable (not a one-off adjustment), promote it to permanent finance standards.

### When to Promote

- Reconciliation issue recurs across multiple periods or entities
- Control gap is found in 2+ process areas
- Regulatory interpretation applies to all entities under the same framework
- Close procedure improvement saves measurable time

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Close checklists | Period-end tasks, cutoff procedures, sign-off requirements |
| Reconciliation procedures | Step-by-step account rec guides, tolerance thresholds, escalation paths |
| Control matrices | SOX key controls, compensating controls, control owners, test procedures |
| Tax calendars | Filing deadlines, estimated payment dates, compliance milestones |
| Forecast models | Revenue drivers, expense assumptions, sensitivity parameters |
| Audit response templates | Standard responses for common audit inquiries and requests |
| `AGENTS.md` | Automated finance workflows, pre-close checks |

### How to Promote

1. **Distill** the learning into a concise procedure, control step, or checklist item
2. **Add** to appropriate target (close checklist entry, control matrix row, reconciliation step)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: close checklist` (or `control matrix`, `reconciliation procedure`, `tax calendar`, `forecast model`, `audit response template`)

### Promotion Examples

**Learning** (verbose):
> Found FX conversion for P&L items using spot rate at transaction date instead of
> average rate for the period. This affected three subsidiaries and caused a $X.XM
> translation variance that required a top-side adjustment at consolidation.

**As close checklist item** (concise):
> ☐ Verify FX rates applied to P&L items use weighted-average rate for the period,
>   not spot rate. Cross-check against rate table published by treasury.

**Learning** (verbose):
> Journal entries under $10K were bypassing the approval workflow due to a threshold
> misconfiguration in the ERP. This was discovered during SOX testing when 47 entries
> in Q2 had no approver stamp.

**As control matrix entry** (actionable):
> | Control ID | Description | Owner | Frequency | Evidence |
> |------------|-------------|-------|-----------|----------|
> | JE-001 | All journal entries require dual approval regardless of amount | Controller | Per occurrence | Approver signature in ERP workflow |

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: FIN-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring finance issues often indicate:
   - Missing close checklist step (→ add to close checklist)
   - Incomplete control design (→ update control matrix)
   - System configuration gap (→ ERP configuration change request)
   - Training gap (→ add to onboarding documentation)

## Periodic Review

Review `.learnings/` at natural breakpoints in the finance calendar:

### When to Review
- Before each month-end close or after completing a close cycle
- When the same reconciliation issue recurs
- During quarterly SOX testing or before annual audit fieldwork

### Quick Status Check
```bash
# Count pending finance issues
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority finance issues
grep -B5 "Priority\*\*: high" .learnings/FINANCE_ISSUES.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: treasury" .learnings/*.md

# Find all control weaknesses
grep -B2 "control_weakness" .learnings/LEARNINGS.md | grep "^## \["

# Find all reconciliation errors
grep -B2 "reconciliation_error" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve remediated finance issues
- Promote recurring patterns to close checklists or control matrices
- Link related entries across files
- Extract reusable procedures as skills

## Simplify & Harden Feed

Ingest recurring finance patterns from `simplify-and-harden` into close checklists or control matrices.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ periods or entities, within 90-day window.
Targets: close checklists, reconciliation procedures, control matrices, `AGENTS.md`.

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
        "command": "./skills/self-improving-finance/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a finance-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-finance/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-finance/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for reconciliation issues, variances, and control failures.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate finance learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on reconciliation breaks, variances, control test output |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a finance learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same reconciliation or control issue in 2+ periods or entities |
| **Verified** | Status is `resolved` with confirmed remediation |
| **Non-obvious** | Required investigation beyond standard procedures |
| **Broadly applicable** | Not entity-specific; useful across the finance organization |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-finance/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-finance/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with finance-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

**In conversation**: "This reconciliation keeps breaking", "Save this close procedure as a skill", "We hit this same control gap last quarter", "Every entity has this intercompany issue".

**In entries**: Multiple `See Also` links, high priority + resolved, `control_weakness` or `reconciliation_error` with broad applicability, same `Pattern-Key` across entities.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Finance Best Practices

1. **Reconcile daily** — do not wait until close to identify breaks
2. **Four-eyes principle** — every journal entry, payment, and adjustment requires a second reviewer
3. **Segregation of duties** — the person who initiates a transaction must not be the person who approves it
4. **Maintain audit trail** — every adjustment must have supporting documentation and a clear rationale
5. **Close on schedule** — late close items compound; escalate at the first sign of delay
6. **Track materiality thresholds** — know the quantitative thresholds for your entity and apply them consistently
7. **Anonymize all logged data** — never record real account numbers, bank details, or client-identifying information
8. **Log immediately** — context around reconciliation breaks and control failures fades fast
9. **Reference applicable standards** — cite ASC, IFRS, SOX section, or internal policy numbers
10. **Promote aggressively** — if the same issue appears in two periods, it deserves a checklist item or control update

## Gitignore Options

Add `.learnings/` to `.gitignore` for local-only; omit for org-wide sharing; or ignore `*.md` but keep `.gitkeep` for a hybrid approach.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/finance/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: finance
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (finance)
Only trigger this skill automatically for finance signals such as:
- `reconciliation|journal entry|close process|variance|materiality`
- `sox control|audit evidence|cash flow|forecast miss`
- explicit finance intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/finance/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
