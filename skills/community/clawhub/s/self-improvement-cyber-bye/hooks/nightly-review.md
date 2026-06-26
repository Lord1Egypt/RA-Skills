---
name: self-improvement-cyber-bye-nightly-review
description: Runs at 11 PM IST every night. Reviews all raw errors, attempts self-fixes, detects patterns, updates stats and soul. Permanent cron — never delete.
schedule: "30 17 * * *"
schedule_ist: "23:00 IST daily"
timezone: Asia/Kolkata
type: permanent
---

# Nightly Review Hook — 11 PM IST

## Step 1 — Inventory
Read all files in `errors/raw/`. If empty → skip to Step 7.

---

## Step 2 — Triage Each Error

```
hallucination   → can I state the correct fact confidently?   YES/NO
logic-error     → can I identify the correct reasoning?       YES/NO
code-bug        → can I write the corrected code?             YES/NO
skill-breach    → can I re-anchor to correct spec?            YES/NO
user-correction → depends on correction type                  YES/NO
judgment-error  → usually NO unless clear root cause
behavior-drift  → can I identify the spec violation?          YES/NO
tool-misuse     → can I identify correct usage?               YES/NO
memory-gap      → NO — context is gone
omission        → YES if can state what should have been done
```

---

## Step 3 — Self-Fix Attempt

For each YES:
1. Write fix entry to `fixes/<fix-slug>/entry.md`
2. Update error: `status: fixed`, `fix_entry: <fix-slug>`
3. Move error from `errors/raw/` → `errors/reviewed/`

Fix entry format:
```markdown
# <fix-slug>
## Meta
- Error slug: <original-slug>
- Fix type:   self-fix
- Created:    YYYY-MM-DD
## Original Error
[one-line summary]
## Correct Version
[actual correct fact / reasoning / code / behavior]
## Confidence
high | medium | low
## Lesson Learned
[one sentence]
## Behavioral Change
[specific change for future behavior]
```

Low confidence → escalate instead. One attempt only.

---

## Step 4 — Escalate Remaining

For each NOT self-fixable or failed fix:
1. Move to `errors/escalated/`
2. Update: `status: escalated`
3. Update memory index
4. Add to soul [UNRESOLVED ESCALATIONS]

---

## Step 5 — Pattern Detection

Scan all errors last 30 days. Group by error_type and context_area.
Any group with count >= 3 → write/update `patterns/entry.md`:

```markdown
# Pattern: <pattern-id>
## Meta
- Error type:  <type>
- Frequency:   N in 30 days
- First seen:  YYYY-MM-DD
- Last seen:   YYYY-MM-DD
- Status:      active
## Affected Errors
- <slug-1>, <slug-2>, <slug-3>
## Root Cause Assessment
[hypothesis]
## Proposed Behavioral Change
[specific actionable change]
```

Upsert soul [ACTIVE PATTERNS]. HIGH soul event for new pattern.

---

## Step 6 — Update STATS.md

```markdown
# Stats
*Updated: YYYY-MM-DD 23:00 IST*

## Totals
- Total captured:  N
- Self-fixed:      N (N%)
- Escalated:       N (N%)
- Promoted:        N
- Active patterns: N

## By Type
| Type | Count | Fixed | Escalated |
|---|---|---|---|

## 30-Day Trend
- Week 1-4: N errors, N% fix rate each
- Trend: improving | stable | worsening
```

---

## Step 7 — Write REVIEW_LOG.md Entry

```markdown
## YYYY-MM-DD 23:00 IST
- Raw reviewed: N | Self-fixed: N | Escalated: N | Patterns: N
- Notable: [one line or "nothing notable"]
```

---

## Step 8 — Update IMPROVEMENT_JOURNAL.md

If fixes made OR patterns resolved → append 2-4 sentence reflection.
If nothing → skip.

---

## Step 9 — Write Soul Session Log

```
YYYY-MM-DD | nightly-review | raw:N | fixed:N | escalated:N | patterns:N
```

---

## Step 10 — Morning Report Cron

If escalated errors exist AND no temp morning cron active:
→ Create `crons/active/temp-YYYY-MM-DD-10-00-escalation-report.md`
→ Add to soul [ACTIVE CRONS]
