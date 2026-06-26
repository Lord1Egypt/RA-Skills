---
name: skill-analyst
description: >
  Analyze and evaluate OpenClaw skills before installing or publishing.
  Compare against existing or ClawHub skills, check feature overlap,
  perform security review, and provide clear install/publish recommendations.
  Requires `clawhub` CLI to be available.
  Triggers: "analyze skill-name", "evaluate installing/publishing skill",
  "is this skill worth installing", "can I publish this", "skill comparison".
---

# Skill Analyst

Help you analyze, compare, and vet skills before installing or publishing.

## Prerequisites

- `clawhub` CLI required
- `skill-vetter` optional (for security review)

## Workflow: Install Evaluation

### Step 1: Search the Target

Search ClawHub for similar skills:

```bash
clawhub search "<skill-name>"
clawhub inspect "<best-match>"
```

Get: name, author, version, summary, license, last updated.

### Step 2: Check Installed Skills

Scan `~/.openclaw/skills/` for SKILL.md files, or use `clawhub list`.

### Step 3: Find Overlap

Compare target against installed skills:
- Search by functionality keywords or use case
- Rate overlap: HIGH / MEDIUM / LOW / NONE
- Note key differences

### Step 4: Security Check (optional)

If `skill-vetter` is installed, run security review. Otherwise mark "security check skipped".

### Step 5: Generate Report

```markdown
## 🔍 Analysis Report: Install <skill-name>

### Overview
| Field | Value |
|-------|-------|
| Name | ... |
| Author | ... |
| Version | ... |
| License | ... |
| Last Updated | ... |

### Overlap with Installed Skills
- skill-a: MEDIUM — Similar use case, different approach
- skill-b: NONE — Unrelated

### Unique Value
- Feature X (no installed skill covers this)

### Risks
- Requires Z API key

### Verdict
✅ Recommended / ⚠️ Consider / ❌ Not recommended
```

## Workflow: Publish Evaluation

### Step 1: Read Local Skill

Read SKILL.md from workspace or skills directory. Extract name, description, features, file list.

### Step 2: Search Competitors

Use 2-3 different keywords:

```bash
clawhub search "<skill-name>"
clawhub search "<keywords from description>"
```

### Step 3: Analyze Competitors

For each relevant result:

```bash
clawhub inspect "<competitor>"
```

Compare: feature coverage, maturity, update frequency, uniqueness.

### Step 4: Generate Report

```markdown
## 🔍 Analysis Report: Publish <skill-name>

### Your Skill
| Field | Value |
|-------|-------|
| Name | ... |
| Files | ... |
| Description | ... |

### ClawHub Competitors
| Skill | Author | Version | Overlap | Updated |
|-------|--------|---------|---------|---------|
| ... | ... | ... | HIGH/MED/LOW | ... |

### Your Advantages
- Key differentiators

### Suggestions
- Consider adding X before publishing

### Verdict
✅ Ready to publish / ⚠️ Optimize first / ❌ Reconsider
```

## Output Rules

- Always use tables for structured comparison
- Keep analysis concise and actionable
- End with a clear verdict
- Follow the report templates above
