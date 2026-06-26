# Skill Evolver Task

**Record and track improvement opportunities for skills.**

## When to Use

Use this template when:
- A skill error or unexpected behavior was observed
- A user suggests an improvement
- During routine skill audit/review
- After analyzing session logs for patterns

## Task Metadata

| Field | Value |
|-------|-------|
| **Skill Name** | [Name of skill to improve] |
| **Task ID** | EV-[YYYYMMDD]-[NN] |
| **Created** | {{date}} |
| **Priority** | 🔴 High / 🟡 Medium / 🟢 Low |
| **Status** | 📝 Open / 🔄 In Progress / ✅ Resolved / ❌ Won't Fix |

## Observation / Trigger

**What happened:**
[Describe the event that triggered this improvement opportunity]

**Context:**
- Session: [session ID or date]
- User: [if applicable]
- Related logs: [file paths or snippets]

## Analysis

### Current State
[How the skill currently works]

### Problem/Gap
[What's wrong or missing]

### Root Cause (if known)
[Why this happens]

## Proposed Improvement

### Option 1: [Title]
- **Description:** [What to change]
- **Rationale:** [Why this helps]
- **Risk:** [Potential downsides]
- **Effort:** [Low/Medium/High]

### Option 2: [Title] (if applicable)
- **Description:**
- **Rationale:**
- **Risk:**
- **Effort:**

## Decision

**Chosen approach:** [Which option to implement]

**Rationale:** [Why this option was selected]

**Requires user confirmation:** Yes / No (explain why)

## Implementation

### Diff Preview
```markdown
[Before / After blocks or summary of changes]
```

### Files Modified
- [ ] `SKILL.md`
- [ ] `scripts/[name]`
- [ ] `templates/[name]`
- [ ] Other: `[specify]`

### Validation
- [ ] `python scripts/validate_skill.py [skill_dir]` passes
- [ ] Examples updated
- [ ] Safety rules still enforced

## Verification

**Tested with:**
- [Example scenario 1]
- [Example scenario 2]

**Results:**
[Did it fix the issue? Any side effects?]

## Documentation

- [ ] Session notes updated
- [ ] LEARNINGS.md entry added (if broadly applicable)
- [ ] CHANGELOG updated (if versioned skill)

---

## Quick Template (for rapid logging)

**Skill:** [name]
**Issue:** [one-liner]
**Fix:** [one-liner]
**Confirmed:** [y/n]
**Applied:** [date]
