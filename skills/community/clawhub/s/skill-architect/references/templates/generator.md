# Generator Template

Use this template when the skill must produce output that follows a consistent structure every time.

---

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill generates AND when it should trigger. Emphasize the structured/consistent nature of the output.}}
---

# {{Skill Name}}

{{Brief explanation of what this skill generates and why consistency matters.}}

## Step 1: Load Style Guide

Read `references/{{style-guide}}.md` for tone, formatting, and content rules.

Key style points:
- {{Style point 1}}
- {{Style point 2}}

## Step 2: Load Output Template

Read `assets/{{output-template}}.md` for the output skeleton.

The template is authoritative — every section must appear in the output. Do not skip sections. Do not add sections not in the template.

## Step 3: Collect Variables

Before generating, confirm the following with the user (ask only for what's missing from context):
- {{Variable 1}} — {{why it's needed}}
- {{Variable 2}} — {{why it's needed}}
- {{Variable 3}} — {{why it's needed}}

## Step 4: Generate

Fill every section of the template using the collected variables and style guide.

### Quality Checks
Before presenting the output:
- [ ] Every template section is present
- [ ] Tone matches the style guide
- [ ] No placeholder text remains
- [ ] {{Domain-specific check}}
```
