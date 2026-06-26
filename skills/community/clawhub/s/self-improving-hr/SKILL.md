---
name: self-improving-hr
description: "Captures policy gaps, compliance risks, recruiting process issues, onboarding friction, retention signals, candidate experience problems, and offboarding gaps to enable continuous HR improvement. Use when: (1) A compliance deadline is missed or approaching, (2) A candidate drops off during the recruiting pipeline, (3) A new hire leaves within 90 days, (4) A policy gap is discovered, (5) An exit interview reveals a recurring theme, (6) A benefits enrollment error occurs, (7) An I-9 or employment verification issue is found."
---

# Self-Improving HR Skill

Log HR-specific learnings, process issues, and feature requests to markdown files for continuous improvement. Captures policy gaps, compliance risks, recruiting bottlenecks, onboarding friction, retention signals, candidate experience problems, compensation anomalies, and offboarding gaps. Important learnings get promoted to policy documents, onboarding checklists, interview scorecards, or compliance calendars.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# HR Learnings\n\nPolicy gaps, compliance risks, recruiting insights, onboarding friction, retention signals, and offboarding gaps captured during HR operations.\n\n**Categories**: policy_gap | compliance_risk | process_inefficiency | candidate_experience | retention_signal | onboarding_friction\n**Areas**: recruiting | onboarding | compensation | compliance | performance | offboarding | dei\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/HR_PROCESS_ISSUES.md ] || printf "# HR Process Issues Log\n\nCompliance risks, process failures, candidate experience issues, and policy violations.\n\n---\n" > .learnings/HR_PROCESS_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nHR tools, automation capabilities, and process improvement requests.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

**CRITICAL — PII PROTECTION**: NEVER log personally identifiable information in any learnings file. This includes SSNs, salary details, medical information, performance ratings for specific individuals, home addresses, dates of birth, or any data that could identify a specific employee or candidate. Always anonymize examples. Use role titles, department names, or anonymized identifiers (e.g., "Employee A", "Candidate #12") instead of real names.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Compliance audit finding discovered | Log to `.learnings/HR_PROCESS_ISSUES.md` with compliance_risk |
| Candidate drops off at pipeline stage | Log to `.learnings/LEARNINGS.md` with category `candidate_experience` |
| New hire leaves within 90 days | Log to `.learnings/LEARNINGS.md` with category `retention_signal` |
| Policy gap found (missing or outdated) | Log to `.learnings/LEARNINGS.md` with category `policy_gap` |
| Exit interview reveals recurring theme | Log to `.learnings/LEARNINGS.md` with category `retention_signal` |
| Benefits enrollment error | Log to `.learnings/HR_PROCESS_ISSUES.md` with process_inefficiency |
| I-9 verification issue | Log to `.learnings/HR_PROCESS_ISSUES.md` with compliance_risk |
| Onboarding step causing delays | Log to `.learnings/LEARNINGS.md` with category `onboarding_friction` |
| Offer rejection spike | Log to `.learnings/LEARNINGS.md` with category `candidate_experience` |
| Recurring issue across multiple entries | Link with `**See Also**`, consider priority bump |
| Broadly applicable HR insight | Promote to policy document, checklist, or compliance calendar |
| Process improvement idea | Log to `.learnings/FEATURE_REQUESTS.md` |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-hr
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-hr.git ~/.openclaw/skills/self-improving-hr
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
    ├── HR_PROCESS_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — policy gaps, onboarding friction, retention signals, candidate experience, process inefficiencies
- `HR_PROCESS_ISSUES.md` — compliance risks, I-9 issues, benefits errors, policy violations, discrimination claims
- `FEATURE_REQUESTS.md` — HR automation, compliance tools, recruiting pipeline improvements

### Promotion Targets

When HR learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Onboarding patterns | Onboarding checklists | "IT setup must be completed 2 days before start date" |
| Interview insights | Interview scorecards | "Structured behavioral questions reduce bias by 40%" |
| Compliance findings | Compliance calendars | "I-9 re-verification due dates for visa holders" |
| Policy gaps | Policy documents | "Remote work policy for international contractors" |
| Recruiting patterns | Recruiting playbooks | "Offer acceptance improves 15% with 48-hour deadline" |
| Workflow improvements | `AGENTS.md` | "Run compliance check before generating offer letter" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-hr
openclaw hooks enable self-improving-hr
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

#### Self-Improving HR Workflow

When HR process issues, compliance gaps, or people-operations patterns are discovered:
1. Log to `.learnings/HR_PROCESS_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Policy documents — compliance rules, employment policies, handbook updates
   - Onboarding checklists — step-by-step new hire processes
   - Interview scorecards — structured evaluation criteria
   - Compliance calendars — deadline tracking and regulatory reminders

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: recruiting | onboarding | compensation | compliance | performance | offboarding | dei

### Summary
One-line description of the HR insight or pattern

### Details
Full context: what was discovered, why it matters for the organization,
what the correct process or policy should be. Include anonymized data points.

### Impact
- **Affected population**: e.g., "all remote employees", "engineering new hires"
- **Risk level**: compliance, financial, retention, reputational
- **Estimated scope**: number of employees or candidates affected

### Suggested Action
Specific policy update, process change, or compliance remediation step

### Metadata
- Source: audit | exit_interview | hris_report | candidate_feedback | manager_report | benefits_system
- Jurisdiction: federal | state_CA | state_NY | multi_state | international (if applicable)
- Regulation: FMLA | ADA | EEOC | FLSA | COBRA | HIPAA | WARN | state_specific (if applicable)
- Related Files: path/to/policy.md
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: policy_gap.remote_work | compliance_risk.i9_expiry (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `policy_gap` | Missing or outdated policy, handbook section not covering a scenario |
| `compliance_risk` | Regulatory deadline missed, audit finding, legal exposure |
| `process_inefficiency` | HR workflow taking too long, manual step that should be automated |
| `candidate_experience` | Recruiting pipeline friction, offer process delays, poor communication |
| `retention_signal` | Early attrition, exit interview theme, engagement survey pattern |
| `onboarding_friction` | New hire setup delays, missing documentation, unclear first-week plan |

### HR Process Issue Entry [HRP-YYYYMMDD-XXX]

Append to `.learnings/HR_PROCESS_ISSUES.md`:

```markdown
## [HRP-YYYYMMDD-XXX] issue_type_or_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: recruiting | onboarding | compensation | compliance | performance | offboarding | dei

### Summary
Brief description of the HR process issue

### Issue Details
What went wrong or was found. Include anonymized specifics:
timeline, affected group size, business impact.
NEVER include names, SSNs, salary figures, or medical details.

### Root Cause
What process gap, system failure, or policy omission caused this.

### Remediation
Specific steps to resolve this issue and prevent recurrence.

### Compliance Impact
- **Regulation**: FMLA | ADA | EEOC | FLSA | COBRA | HIPAA | WARN | N/A
- **Exposure**: fine amount range, lawsuit risk, audit failure
- **Deadline**: remediation deadline if applicable
- **Audit trail**: what documentation is required

### Context
- Trigger: audit | complaint | hris_alert | manager_escalation | exit_interview | benefits_error
- Jurisdiction: federal | state | local | international
- Department: affected department(s)
- Headcount impact: number of employees affected

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/policy.md
- See Also: HRP-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: recruiting | onboarding | compensation | compliance | performance | offboarding | dei

### Requested Capability
What HR tool, automation, or process improvement is needed

### User Context
Why it's needed, what HR workflow it improves, what risk it mitigates

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: HRIS integration, compliance automation, workflow tool,
reporting dashboard, calendar integration

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_process

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `HRP` (HR process issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `HRP-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Approved By**: [role title, not name — e.g., "VP People Operations"]
- **Notes**: Updated employee handbook section 4.3 / Added to compliance calendar
```

Other status values:
- `in_progress` — Actively being remediated
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to policy document, checklist, or compliance calendar
- `promoted_to_skill` — Extracted as a reusable skill

## Detection Triggers

Automatically log when you encounter:

**Recruiting Pipeline Issues** (→ learning with candidate_experience):
- Offer acceptance rate drops below target
- Time-to-fill exceeding SLA for a role family
- Candidate drop-off spike at a specific pipeline stage
- Offer letter generation or approval delays

**Retention Signals** (→ learning with retention_signal):
- New hire leaves within first 90 days
- Multiple departures from the same team within a quarter
- Exit interview themes recurring across departments
- Engagement survey scores declining in a business unit

**Compliance Deadlines** (→ HR process issue with compliance_risk):
- I-9 re-verification deadline approaching or missed
- FMLA leave tracking errors or ADA accommodation past deadline
- EEO-1 or VETS-4212 filing deadline approaching
- COBRA notification timelines missed

**Benefits and Compensation** (→ HR process issue with process_inefficiency):
- Benefits enrollment errors during open enrollment
- Payroll discrepancy reported
- Compensation band misalignment discovered
- 401(k) contribution errors or match calculation issues

**Onboarding Issues** (→ learning with onboarding_friction):
- IT equipment or access provisioning taking more than 1 business day
- Missing or outdated onboarding documentation
- Background check delays blocking start dates
- Required training not completed within compliance window

**Offboarding Gaps** (→ learning with process_inefficiency):
- System access not revoked on termination date
- Final paycheck or PTO payout delayed
- COBRA notification not sent within 14-day window

## Priority Guidelines

| Priority | When to Use | HR Examples |
|----------|-------------|-------------|
| `critical` | Compliance violation, discrimination claim, active legal exposure | EEOC complaint filed, I-9 audit failure, wage theft allegation, harassment report, WARN Act violation |
| `high` | Retention crisis, significant policy gap, regulatory deadline imminent | 3+ departures from one team, missing state-required policy, EEO-1 deadline in <30 days, ADA accommodation overdue |
| `medium` | Process improvement, onboarding issue, moderate compliance gap | Onboarding takes too long, offer letter template outdated, benefits enrollment friction, interview scorecard missing |
| `low` | Documentation update, minor process tweak, cosmetic policy edit | Handbook formatting, job description template refresh, org chart update, minor workflow optimization |

## Area Tags

Use to filter learnings by HR domain:

| Area | Scope |
|------|-------|
| `recruiting` | Job postings, sourcing, screening, interviews, offers, candidate communication |
| `onboarding` | Pre-boarding, first day, orientation, training, 30-60-90 day milestones |
| `compensation` | Salary bands, equity, bonuses, pay equity analysis, total rewards |
| `compliance` | Employment law, regulatory filings, audits, I-9, FMLA, ADA, EEOC, OSHA |
| `performance` | Reviews, PIPs, goal setting, calibration, promotion criteria |
| `offboarding` | Resignations, terminations, exit interviews, knowledge transfer, final pay |
| `dei` | Diversity metrics, inclusion initiatives, ERGs, bias training, pay equity |

## PII Protection Rules

These rules are non-negotiable and apply to every entry in every file:

1. **NEVER log names** — use "Employee A", "Candidate #12", "Hiring Manager in Engineering"
2. **NEVER log SSNs, tax IDs, or government identifiers**
3. **NEVER log specific salary figures** — use band levels ("Band L5", "above midpoint")
4. **NEVER log medical information** — reference only the accommodation type, not the condition
5. **NEVER log performance ratings for identifiable individuals**
6. **ALWAYS use department/role/level for context** instead of identifying details
7. **ALWAYS redact** before logging — if in doubt, leave it out
8. **Aggregate data is acceptable** — "3 of 12 new hires in Q1", "engineering attrition at 18%"

## Promoting to Permanent HR Standards

When a learning is broadly applicable (not a one-off incident), promote it to permanent organizational standards.

### When to Promote

- Same compliance gap found in consecutive audits
- Onboarding friction reported by 3+ new hires
- Exit interview theme appears across 2+ departments
- Policy gap affects 10+ employees or creates legal exposure

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Policy documents | Employment policies, handbooks, leave policies, remote work guidelines |
| Onboarding checklists | Pre-boarding tasks, day-one setup, 30-60-90 day milestones |
| Interview scorecards | Structured evaluation criteria, competency rubrics, bias mitigation |
| Compliance calendars | Filing deadlines, re-verification dates, posting requirements |
| `AGENTS.md` | Automated HR workflows, compliance checks before actions |
| Recruiting playbooks | Sourcing strategies, offer negotiation frameworks, pipeline stage criteria |

### How to Promote

1. **Distill** the learning into an actionable policy update, checklist item, or calendar entry
2. **Get approval** — HR policy changes typically require VP/CHRO sign-off
3. **Add** to appropriate target (policy doc, checklist, compliance calendar)
4. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: onboarding checklist` (or `policy document`, `compliance calendar`, `interview scorecard`)

### Promotion Examples

**Learning** (verbose):
> New hires in engineering consistently report that IT equipment is not ready on day one.
> Average setup time is 5 business days. 4 of the last 8 hires had no laptop on start date.

**As onboarding checklist item** (concise):
```markdown
## IT Equipment Provisioning
- [ ] Laptop ordered and configured 5 business days before start date
- [ ] Software licenses activated 2 business days before start date
- [ ] Building access badge prepared 1 business day before start date
```

**Learning** (verbose):
> I-9 re-verification deadline for visa holders was missed for 3 employees.

**As compliance calendar entry** (actionable):
```markdown
## I-9 Re-Verification Tracking
- Set HRIS alert 90 days before work authorization expiry
- Escalate to immigration counsel at 30 days if no renewal documentation
- Complete Section 3 of I-9 on or before expiry date
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: HRP-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Missing policy, broken process, HRIS gap, or training need

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before annual compliance audits
- After each open enrollment period
- At quarter-end (compensation, headcount reviews)
- When turnover spikes in any department

### Quick Status Check
```bash
grep -h "Status\*\*: pending" .learnings/*.md | wc -l
grep -B5 "Priority\*\*: high" .learnings/HR_PROCESS_ISSUES.md | grep "^## \["
grep -l "Area\*\*: compliance" .learnings/*.md
grep -B2 "retention_signal" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve remediated compliance issues
- Promote recurring patterns to policy documents
- Link related entries across files

## Simplify & Harden Feed

Ingest recurring HR patterns from `simplify-and-harden` into policy documents or compliance calendars.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ departments, within 90-day window.
Targets: policy documents, onboarding checklists, compliance calendars, `AGENTS.md`.

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
        "command": "./skills/self-improving-hr/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects an HR-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-hr/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-hr/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for compliance keywords, violation indicators, and HR process failures.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate HR learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on compliance terms, violations, HR process errors |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When an HR learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same process issue in 2+ audit cycles or departments |
| **Verified** | Status is `resolved` with confirmed remediation |
| **Non-obvious** | Required actual investigation or legal research |
| **Broadly applicable** | Not location-specific; useful across business units |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-hr/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-hr/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with HR-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session and confirm it is PII-free

### Extraction Detection Triggers

Use conversation signals ("This compliance issue keeps coming up", "Save this onboarding process as a skill") and entry signals (multiple `See Also`, high-priority resolved items, recurring `compliance_risk`/`policy_gap`) to identify extraction candidates.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Best Practices

1. **Log immediately** — compliance details and process observations fade fast
2. **Anonymize always** — never include names, SSNs, salaries, or medical info
3. **Specify jurisdiction** — federal vs. state vs. local matters enormously
4. **Note the regulation** — cite FMLA, ADA, EEOC, etc. by name
5. **Follow chain of approval** — HR policy changes need sign-off before implementation
6. **Check multiple jurisdictions** — a compliant federal policy may violate state law
7. **Review before audits** — check `.learnings/` for open compliance items

## Gitignore Options

**Keep learnings local** (per-user, recommended for HR due to sensitivity):
```gitignore
.learnings/
```

**Track learnings in repo** (team-wide, only for anonymized operational patterns):
Don't add to .gitignore — learnings become shared knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

**Recommendation**: For HR data, default to `.learnings/` local and untracked.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/hr/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: hr
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (hr)
Only trigger this skill automatically for HR signals such as:
- `policy violation|onboarding|offboarding|performance review`
- `payroll issue|retention risk|compliance training|workforce planning`
- explicit HR intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/hr/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
