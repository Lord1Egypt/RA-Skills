# Combined Pattern Template

Use this template when the skill needs more than one pattern. The most common combinations are documented below.

---

## Inversion → Generator

The most common combination. Interview first, then generate structured output.

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill does. Mention both the interview and the structured output.}}
---

# {{Skill Name}}

{{Brief explanation. This skill interviews you to understand requirements, then generates structured output.}}

## Phase 1: Interview (Inversion)

{{Follow the Inversion template for Phases 1-3}}

**HARD GATE: Do NOT begin generating until the user confirms the summary.**

## Phase 2: Generate (Generator)

Load template from `assets/{{output-template}}.md`.
Load style guide from `references/{{style-guide}}.md`.

Fill every section using the information gathered in Phase 1.

{{Follow the Generator template for Steps 2-4}}
```

---

## Pipeline + Reviewer

Multi-step work with quality gates.

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill does. Mention the sequential process and quality review.}}
---

# {{Skill Name}}

{{Brief explanation. This skill executes work in ordered steps with a quality review before final output.}}

## Step 1: {{Step Name}}
{{Follow Pipeline template}}

## Step 2: {{Step Name}}
{{Follow Pipeline template}}

## Step 3: Review (Reviewer)

Load checklist from `references/{{checklist}}.md`.

Review the output from Steps 1-2 against the checklist.
Present findings to user before finalizing.

{{Follow Reviewer template for Steps 2-4}}

## Step 4: Finalize
Apply fixes from review, produce final output.
```

---

## Inversion → Pipeline

Gather requirements, then execute in stages.

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill does. Mention requirements gathering and staged execution.}}
---

# {{Skill Name}}

{{Brief explanation. This skill gathers requirements through interview, then executes in ordered stages.}}

## Phase 1: Requirements (Inversion)

{{Follow Inversion template for Phases 1-3}}

**HARD GATE: Do NOT begin execution until the user confirms.**

## Phase 2: Execute (Pipeline)

### Step 1: {{Step Name}}
{{Follow Pipeline template — use info from Phase 1}}

### Step 2: {{Step Name}}
{{Follow Pipeline template}}

### Step 3: {{Step Name}}
{{Follow Pipeline template}}
```
