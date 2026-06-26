# Skill Creator Assistant

A guided conversation-based tool that helps non-technical users create their own OpenClaw skills through a step-by-step questionnaire. No coding required.

## How It Works

1. User describes what they want the skill to do
2. Assistant asks 5-8 targeted questions
3. Assistant generates a complete, ready-to-use SKILL.md
4. Optionally: generates README, uploads to GitHub/ClawHub

## The Conversation Flow

### Step 1: Core Identity
- Skill name (what to call it)
- One-line description
- When/why someone would trigger this skill

### Step 2: Capabilities
- What exactly can this skill do? (checklist of 1-5 abilities)
- What input does it need from the user?
- What output does it produce?

### Step 3: Use Cases
- 1-2 concrete examples of when to use this skill
- Who is the target user?

### Step 4: Templates
Assistant recommends one of:
- **Research型** — data analysis, report generation
- **Creation型** — writing, design, content production
- **Collection型** — monitoring, search, intelligence gathering
- **Utility型** — file conversion, formatting, automation
- **Custom** — mixed or unique requirements

### Step 5: Output Format
- File format (markdown, docx, pdf, etc.)
- Any required structure/headings
- Naming conventions

### Step 6: Limitations
- What should it NOT do?
- Known constraints or dependencies
- Required packages/APIs

## Generated SKILL.md Structure

```markdown
# [Skill Name]

## Name
`skill-name`

## Description
[1-2 sentences]

## Capabilities
- [Capability 1]
- [Capability 2]

## Triggers
[When/why this skill activates]

## Workflow
[Step-by-step how the skill operates]

## Input Requirements
[What user must provide]

## Output
[What the skill delivers]

## Limitations
- [Limitation 1]
- [Limitation 2]

## Dependencies
[Any required tools/packages]
```

## Templates

The assistant has 5 built-in templates:

### Research Template
Focused on: data gathering, analysis, reporting
- Structured report format
- Source verification
- Citation tracking

### Creation Template
Focused on: writing, design, content
- Draft → refine → deliver workflow
- Format-aware output (HTML/DOCX/JSON)
- Iteration support

### Collection Template
Focused on: monitoring, search, alerts
- Periodic check workflow
- Threshold alerts
- Multi-source aggregation

### Utility Template
Focused on: conversion, processing, automation
- File format handling
- Batch processing
- Error handling

### Custom Template
Flexible structure based on user's specific needs

## Quality Checklist

Before finalizing, verify:
- [ ] Name is unique and descriptive
- [ ] Description is clear in 1-2 sentences
- [ ] All capabilities have concrete examples
- [ ] No circular logic or infinite loops
- [ ] Dependencies are available/installable
- [ ] File format is correct (.md)
- [ ] Ready for GitHub/ClawHub upload

## GitHub Upload

After generating the SKILL.md, offer to:
1. Create a GitHub repo
2. Generate a README.md
3. Upload both files
4. Provide the repo URL

## Limitations

- Cannot generate skills that require external paid APIs without user providing credentials
- Cannot test skills that need runtime environment (those must be tested manually)
- Complex multi-agent workflows require advanced technical understanding

