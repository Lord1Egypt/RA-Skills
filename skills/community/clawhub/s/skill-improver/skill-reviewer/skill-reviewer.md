---
name: skill-reviewer
description: "Use this skill when the user says 'review this skill', 'check SKILL.md', 'optimize this skill', 'help me review a skill', 'diagnose this skill', or similar requests to audit or improve a OpenClaw SKILL.md file."
version: 1.0.0
author: OpenClaw
---

# Skill Reviewer

## STATIC

Review criteria are defined in `.openclaw/skills/skill-standard/SKILL-STANDARD.md` (v1.0.0). **Load it only when grade is C or D.**

**Grade Rating:**
- A (excellent) / B (passing) — SKILL.md meets standard. **Do NOT load skill-standard.**
- C (needs improvement) / D (failing) — Issues found. **Load skill-standard to fix.**

**Reviewer Principles:**
- Act as a professional editor, not a cold-hearted quality inspector
- Point out problems and provide specific improvement suggestions
- Distinguish between "non-compliant" and "could be better"

## DYNAMIC
# Target Skill to Review: {$TARGET_SKILL}

## Execution Flow

### [Step 1: Locate File]

1. User provided a path → Read file content
2. User pasted content directly → Parse the content
3. Neither available → Ask for path

### [Step 2: Apply Review Criteria]

Apply the six dimensions without loading skill-standard (criteria are self-contained):

1. Metadata (Layer 1) — name + description
2. Lean body (Layer 2) — < 500 lines
3. STATIC section — identity + tool specs + safety constraints
4. Dynamic section — use of !command or {$VAR} (suggested)
5. Execution flow — branches + [Prepare/Execute/Verify/Report]
6. Output specification — success + failure JSON

**Only if grade is C or D:** Load skill-standard/SKILL-STANDARD.md to get remediation guide.

### [Step 3: Output Result]

**Output Format:**

```markdown
## Skill Review Report

**Skill:** `<name>`
**Grade:** `[A/B/C/D]`
**Issues:** `<N>`
**Warnings:** `<W>`

---

### Dimension Scores

| Dimension | Status | Notes |
|-----------|--------|-------|
| description | pass/warn/fail | <assessment> |
| Three-layer structure | pass/warn/fail | <assessment> |
| STATIC section | pass/warn/fail | <assessment> |
| Execution flow | pass/warn/fail | <assessment> |
| Output specification | pass/warn/fail | <assessment> |

---

### Issue List

1. **<Issue Title>** (<dimension>)
   - Problem: <specific description>
   - Suggestion: <modification plan>

---

### Next Step

**If Grade A or B:** No action needed. SKILL.md meets standard.

**If Grade C or D:** Load skill-standard to apply fixes.
```

### [Step 4: Provide Optimized Version]

Only for grade C or D, provide the optimized SKILL.md:

```
### Optimized SKILL.md

```markdown
<Full optimized content>
```
```

### [Step 5: Backup]

Remind user to backup original before applying fixes.

---

## Output Specification

```json
// Success
{ "action": "review", "result": "success", "skill": "<name>", "grade": "A/B/C/D", "issues": N, "warnings": W }

// Failure
{ "action": "review", "result": "failed", "error": { "code": "PARSE_ERROR", "message": "Cannot parse SKILL.md structure" } }
```

---

## Error Patterns

| Error Code | Meaning | Handling |
|------------|---------|----------|
| PARSE_ERROR | Cannot parse YAML frontmatter or Markdown | Return original, ask user to confirm |
| FILE_NOT_FOUND | Path does not exist | Ask if user wants to paste content |
| EMPTY_CONTENT | File is empty | Return error |

---

_Version history: v1.0.0 (initial release)_
