# Pipeline Template

Use this template when the work has ordered steps that can't be skipped or reordered.

---

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill does AND when it should trigger. Emphasize the multi-step, sequential nature of the work.}}
---

# {{Skill Name}}

{{Brief explanation of what this skill does and why the sequential structure matters.}}

## Step 1: {{Step Name}}

**What:** {{What happens in this step}}
**Input:** {{What this step needs}}
**Output:** {{What this step produces}}

{{Detailed instructions for this step}}

**Gate:** {{What must be true before proceeding}}
Present to user: {{What to show the user for confirmation}}

---

## Step 2: {{Step Name}}

**What:** {{What happens in this step}}
**Input:** {{Output from Step 1}}
**Output:** {{What this step produces}}

Load `references/{{step-specific-reference}}.md` for this step.

{{Detailed instructions for this step}}

**Gate:** {{What must be true before proceeding}}
Present to user: {{What to show the user for confirmation}}

---

## Step 3: {{Step Name}}

**What:** {{What happens in this step}}
**Input:** {{Output from Step 2}}
**Output:** {{Final output}}

{{Detailed instructions for this step}}

**Gate:** {{Final quality check before delivering}}

---

## Error Handling

- If Step {{N}} fails: {{What to do — retry? report? abort?}}
- If user rejects at a gate: {{Go back to which step?}}
```
