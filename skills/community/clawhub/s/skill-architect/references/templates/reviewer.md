# Reviewer Template

Use this template when the skill's primary job is to evaluate or audit something against a defined standard.

---

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill reviews/audits AND when it should trigger. Mention the domain and type of standards being applied.}}
---

# {{Skill Name}}

{{Brief explanation of what this skill reviews and what standards it applies.}}

## Step 1: Load Checklist

Read `references/{{checklist}}.md` for the review criteria.

The checklist defines what to check. This skill defines how to check it.

## Step 2: Read Before Critiquing

Read the full content being reviewed before making any assessments. Do not critique line-by-line on first pass — understand the whole first.

## Step 3: Apply Checklist

For each checklist item, assess the content and note any violations:

**Finding format:**
- **Severity:** Critical / Major / Minor
- **Rule:** Which checklist item was violated
- **Location:** Where in the content
- **Issue:** What's wrong
- **Fix:** How to resolve it

## Step 4: Present Findings

Structure the output as:

### Summary
{{1-2 sentence overall assessment}}

### Critical Findings
{{List critical issues — these must be fixed}}

### Major Findings
{{List major issues — should be fixed}}

### Minor Findings
{{List minor issues — nice to fix}}

### Recommendations
{{Optional suggestions that go beyond the checklist}}
```
