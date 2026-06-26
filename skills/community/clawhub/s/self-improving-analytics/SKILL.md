---
name: self-improving-analytics
description: "Captures data quality issues, metric drift, pipeline failures, misleading visualizations, metric definition mismatches, and data freshness problems to enable continuous analytics improvement. Use when: (1) An ETL/ELT pipeline fails, (2) A metric value shows anomalous behavior, (3) Two teams define the same metric differently, (4) A dashboard shows wrong or misleading data, (5) A data freshness SLA is missed, (6) A schema change breaks downstream consumers."
---

# Self-Improving Analytics Skill

Log analytics-specific learnings, data issues, and feature requests to markdown files for continuous improvement. Captures data quality problems, metric drift, pipeline failures, misleading visualizations, metric definition mismatches, and data freshness breaches. Important learnings get promoted to data dictionaries, metric definitions, pipeline runbooks, dashboard standards, or data quality SLAs.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Analytics Learnings\n\nData quality patterns, metric drift insights, pipeline reliability findings, visualization best practices, and governance lessons.\n\n**Categories**: data_quality | metric_drift | pipeline_failure | visualization_mislead | definition_mismatch | freshness_issue\n**Areas**: ingestion | transformation | modeling | reporting | visualization | governance | data_catalog\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/DATA_ISSUES.md ] || printf "# Data Issues Log\n\nPipeline failures, data quality problems, metric anomalies, visualization errors, and schema drift.\n\n---\n" > .learnings/DATA_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nAnalytics tools, BI capabilities, data quality automation, and governance improvements.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log connection strings, database credentials, API keys, or PII. Prefer short summaries or redacted excerpts over raw query results or full table dumps.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| ETL/ELT pipeline fails | Log to `.learnings/DATA_ISSUES.md` with pipeline name and error |
| Metric value anomaly (spike/drop) | Log to `.learnings/DATA_ISSUES.md` with statistical context |
| Two teams define metric differently | Log to `.learnings/LEARNINGS.md` with category `definition_mismatch` |
| Dashboard shows wrong or misleading data | Log to `.learnings/LEARNINGS.md` with category `visualization_mislead` |
| Data freshness SLA missed | Log to `.learnings/DATA_ISSUES.md` with SLA threshold and actual delay |
| Schema change breaks downstream | Log to `.learnings/DATA_ISSUES.md` with schema diff details |
| NULL rate spike in key column | Log to `.learnings/DATA_ISSUES.md` with column and threshold |
| Metric silently drifts (calculation change) | Log to `.learnings/LEARNINGS.md` with category `metric_drift` |
| Recurring data quality pattern | Link with `**See Also**`, consider priority bump |
| Broadly applicable pattern | Promote to data dictionary, pipeline runbook, or dashboard standard |
| Reusable data quality check | Promote to data quality SLA or dbt test |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-analytics
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-analytics.git ~/.openclaw/skills/self-improving-analytics
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
    ├── DATA_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — metric drift, definition mismatches, visualization issues, data quality patterns
- `DATA_ISSUES.md` — pipeline failures, freshness breaches, schema drift, metric anomalies
- `FEATURE_REQUESTS.md` — analytics tools, BI capabilities, automation requests

### Promotion Targets

When analytics learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Metric definitions | Data dictionary | "Active user = login within 7 days with feature interaction" |
| Pipeline failure patterns | Pipeline runbooks | "DST partition handling: always use UTC-based keys" |
| Visualization standards | Dashboard style guide | "Absolute value charts must start Y-axis at zero" |
| Data quality rules | Data quality SLAs | "NULL rate in PK columns must be <0.01%" |
| Governance patterns | `AGENTS.md` | "New metrics require data dictionary entry before dashboard" |
| Tool configuration | `TOOLS.md` | "dbt source freshness checks required on all external sources" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-analytics
openclaw hooks enable self-improving-analytics
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

#### Self-Improving Analytics Workflow

When data issues or analytics patterns are discovered:
1. Log to `.learnings/DATA_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Data dictionaries — canonical metric definitions
   - Pipeline runbooks — failure recovery procedures
   - Dashboard standards — visualization conventions
   - Data quality SLAs — monitoring thresholds and alerts

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: ingestion | transformation | modeling | reporting | visualization | governance | data_catalog

### Summary
One-line description of the analytics insight

### Details
Full context: what data pattern was found, why it is problematic,
what the correct approach is. Include root cause analysis.

### SQL Example

**Before (problematic):**
\`\`\`sql
-- problematic query, pipeline config, or metric definition
\`\`\`

**After (correct):**
\`\`\`sql
-- corrected query, config, or definition
\`\`\`

### Suggested Action
Specific data dictionary update, pipeline fix, dashboard change, or governance rule to adopt

### Metadata
- Source: etl_failure | freshness_breach | metric_anomaly | definition_conflict | dashboard_review | reconciliation_failure | schema_drift
- Pipeline: Airflow DAG name, dbt model, Fivetran connector (if applicable)
- Warehouse: snowflake | bigquery | redshift | postgres | databricks
- Related Tables: schema.table_name
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: metric_drift.revenue_source | data_quality.null_spike (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `data_quality` | NULL spikes, duplicate records, invalid values, completeness issues |
| `metric_drift` | Metric calculation silently changed due to new data source, schema change, or logic update |
| `pipeline_failure` | ETL/ELT job failure, timeout, resource exhaustion, dependency issue |
| `visualization_mislead` | Chart axis, scale, aggregation, or color choice that misrepresents data |
| `definition_mismatch` | Same metric name with different definitions across teams or dashboards |
| `freshness_issue` | Data arriving later than SLA, stale dashboards, partition delays |

### Data Issue Entry [DAT-YYYYMMDD-XXX]

Append to `.learnings/DATA_ISSUES.md`:

```markdown
## [DAT-YYYYMMDD-XXX] issue_type_or_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: ingestion | transformation | modeling | reporting | visualization | governance | data_catalog

### Summary
Brief description of the data issue

### Error Output
\`\`\`
Actual error message, pipeline log, query error, or anomaly description (redacted/summarized)
\`\`\`

### Root Cause
What in the pipeline, data model, or source system caused this issue.
Include the problematic query or configuration.

### Fix
\`\`\`sql
-- corrected query, pipeline config, or data quality check
\`\`\`

### Prevention
How to avoid this issue in the future (data quality test, pipeline alert, schema validation, SLA monitor)

### Context
- Trigger: etl_failure | freshness_breach | metric_anomaly | null_spike | schema_drift | rendering_error
- Pipeline: Airflow DAG name, dbt model, Fivetran connector
- Warehouse: snowflake | bigquery | redshift | postgres | databricks
- Affected Tables: schema.table_name
- Downstream Impact: dashboards, reports, or teams affected

### Metadata
- Reproducible: yes | no | unknown
- Related Tables: schema.table_name
- See Also: DAT-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: ingestion | transformation | modeling | reporting | visualization | governance | data_catalog

### Requested Capability
What analytics tool, automation, or capability is needed

### User Context
Why it's needed, what workflow it improves, what data problem it solves

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: dbt macro, Airflow operator, data quality check, Looker feature, governance workflow

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_capability

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `DAT` (data issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `DAT-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Added data quality test / updated pipeline runbook / fixed metric definition
```

Other status values:
- `in_progress` — Actively being investigated or fixed
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to data dictionary, pipeline runbook, or dashboard standard
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**ETL/ELT Pipeline Failures** (→ data issue with etl_failure trigger):
- Airflow DAG task failure or retry exhaustion
- dbt model build error or test failure
- Fivetran/Stitch sync failure or schema change warning
- Spark/Databricks job timeout or OOM
- CDC replication lag exceeding threshold

**Data Freshness Breaches** (→ data issue with freshness_breach trigger):
- Source data >24h stale (no new rows for today's partition)
- dbt source freshness check failure (`warn_after`, `error_after`)
- Dashboard last-refresh timestamp exceeds SLA
- Downstream model depends on stale upstream

**Metric Value Anomalies** (→ data issue with metric_anomaly trigger):
- Metric value >3 standard deviations from 30-day rolling mean
- Day-over-day change exceeds historical maximum
- Metric drops to zero unexpectedly
- Revenue, user count, or conversion rate shows sudden discontinuity

**NULL Rate Spikes** (→ data issue with null_spike trigger):
- Key column NULL rate exceeds baseline by >1 percentage point
- Primary key contains NULLs (should never happen)
- Foreign key NULL rate spikes after source system change
- Required business fields (email, amount, status) contain unexpected NULLs

**Schema Changes** (→ data issue with schema_drift trigger):
- Column added, removed, or renamed in source system
- Data type changed (VARCHAR length, NUMERIC precision)
- Constraint added or removed (NOT NULL, UNIQUE, FK)
- Table renamed or moved to different schema

**Conflicting Definitions** (→ learning with definition_mismatch category):
- Same metric name in two dashboards with different values
- Team A and Team B disagree on metric logic
- Data dictionary entry contradicts actual implementation
- Looker explore definition differs from dbt model documentation

**Visualization Issues** (→ learning with visualization_mislead category):
- Y-axis not starting at zero for absolute value charts
- Dual Y-axis with mismatched scales
- Pie chart with too many slices (>6)
- Time series with inconsistent intervals
- Color coding that implies ranking where none exists

## Priority Guidelines

| Priority | When to Use | Analytics Examples |
|----------|-------------|-------------------|
| `critical` | Wrong data in executive dashboard or regulatory report | Revenue under-reported to board, compliance data incorrect, PII exposure in dashboard |
| `high` | Pipeline down, metric definition conflict, SLA breach | Airflow DAG failed for >4h, Marketing vs Product metric mismatch, daily report stale |
| `medium` | Data quality degradation, visualization improvement | NULL rate trending up, dashboard axis misleading, catalog entry outdated |
| `low` | Catalog update, documentation, minor improvement | Column description missing, unused dashboard cleanup, tag standardization |

## Area Tags

Use to filter learnings by analytics domain:

| Area | Scope |
|------|-------|
| `ingestion` | Data extraction, loading, CDC replication, API pulls, file imports |
| `transformation` | SQL transforms, dbt models, Spark jobs, data cleaning, deduplication |
| `modeling` | Dimensional modeling, entity relationships, slowly changing dimensions, grain |
| `reporting` | Scheduled reports, email digests, PDF generation, data exports |
| `visualization` | Dashboards, charts, Looker explores, Tableau workbooks, Metabase questions |
| `governance` | Metric definitions, data ownership, access control, PII classification |
| `data_catalog` | Column descriptions, table documentation, lineage, tagging, search |

## Promoting to Permanent Analytics Standards

When a learning is broadly applicable (not a one-off data fix), promote it to permanent standards.

### When to Promote

- Same metric definition conflict surfaces across 2+ teams
- Pipeline failure pattern recurs after different source system changes
- Visualization anti-pattern found in 3+ dashboards
- Data quality rule would have prevented multiple incidents
- Freshness monitoring gap caused repeated SLA breaches

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Data dictionary | Canonical metric definitions with owner, grain, and refresh cadence |
| Pipeline runbooks | Step-by-step recovery for known failure patterns |
| Dashboard standards | Visualization conventions (axis, colors, aggregation rules) |
| Data quality SLAs | Monitoring thresholds and alert configurations |
| `CLAUDE.md` | Project-specific analytics conventions for AI agents |
| `AGENTS.md` | Automated analytics workflows, data validation steps |

### How to Promote

1. **Distill** the learning into a concise definition, rule, or procedure
2. **Add** to appropriate target (data dictionary entry, runbook step, SLA threshold)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: data dictionary` (or `pipeline runbook`, `dashboard standard`, `data quality SLA`)

### Promotion Examples

**Learning → Data dictionary entry:**
> Marketing "active user" = 30-day login; Product = 7-day feature interaction → 420K vs 185K discrepancy.

Promoted as: `active_users_30d` (Marketing, login-based) and `active_users_7d` (Product, interaction-based) with governance note specifying which to use for board reports.

**Learning → Pipeline runbook:**
> Pipeline fails every DST transition — partition key uses local time, hour 2 doesn't exist.

Promoted as: "DST Partition Recovery" runbook — rerun with UTC key, verify no duplicates, migrate all partitions to UTC.

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: DAT-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring analytics issues often indicate:
   - Missing data quality test (→ add dbt test or Great Expectations suite)
   - Missing monitoring (→ add freshness check or anomaly detection)
   - Governance gap (→ add metric definition to data dictionary)
   - Pipeline design flaw (→ refactor ingestion or transformation logic)

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before building a new dashboard or metric
- After a pipeline incident is resolved
- When the same data quality issue appears again
- Before quarterly business reviews
- During data model refactoring

### Quick Status Check
```bash
# Count pending analytics issues
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority data issues
grep -B5 "Priority\*\*: high" .learnings/DATA_ISSUES.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: governance" .learnings/*.md

# Find all definition mismatches
grep -B2 "definition_mismatch" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve fixed data issues
- Promote recurring patterns to data dictionaries
- Link related entries across files
- Extract reusable data quality checks as skills

## Simplify & Harden Feed

Ingest recurring analytics patterns from `simplify-and-harden` into data quality rules or governance standards.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ pipelines/dashboards, within 30-day window.
Targets: data dictionary entries, pipeline runbooks, dashboard standards, `CLAUDE.md` / `AGENTS.md`.

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
        "command": "./skills/self-improving-analytics/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects an analytics-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-analytics/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-analytics/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for pipeline errors, query failures, and data quality issues.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate analytics learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on pipeline errors, query failures, data quality issues |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When an analytics learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same data issue in 2+ pipelines or warehouses |
| **Verified** | Status is `resolved` with working fix and data quality test |
| **Non-obvious** | Required actual investigation or cross-team coordination |
| **Broadly applicable** | Not project-specific; useful across data stacks |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-analytics/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-analytics/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with analytics-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

**In conversation**: "This pipeline keeps failing the same way", "Save this data quality check as a skill", "Every warehouse has this DST issue", "This metric definition problem happens everywhere".

**In entries**: Multiple `See Also` links, high priority + resolved, `definition_mismatch` or `pipeline_failure` with broad applicability, same `Pattern-Key` across projects.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Best Practices

1. **Define metrics before building** — agree on definitions in the data dictionary before creating dashboards
2. **Validate at ingestion** — catch data quality issues as early as possible in the pipeline
3. **Test transformations with known data** — use static test fixtures, not just production samples
4. **Document lineage** — every metric should trace back to source tables through explicit joins
5. **Alert on anomalies, not just failures** — a pipeline that succeeds but produces wrong data is worse than one that fails
6. **Use UTC everywhere** — local time in partitions, timestamps, or schedules causes DST and timezone bugs
7. **Version metric definitions** — treat metric logic changes like code changes with review and approval
8. **Separate facts from interpretation** — dashboards should present data; narrative belongs in annotations
9. **Review before building in same area** — check `.learnings/` for past issues with the same tables or metrics
10. **Reconcile against source of truth** — compare warehouse aggregates against GL, CRM, or billing system totals

## Gitignore Options

**Keep learnings local** (per-analyst): add `.learnings/` to `.gitignore`.

**Track learnings in repo** (team-wide): don't add to `.gitignore` — learnings become shared knowledge.

**Hybrid** (track templates, ignore entries): ignore `.learnings/*.md`, keep `.learnings/.gitkeep`.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/analytics/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: analytics
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (analytics)
Only trigger this skill automatically for analytics signals such as:
- `pipeline|etl|schema drift|metric mismatch|dashboard`
- `lineage|warehouse|bi|attribution|anomaly`
- explicit analytics intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/analytics/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
