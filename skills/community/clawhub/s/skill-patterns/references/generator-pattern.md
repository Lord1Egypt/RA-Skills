# Pattern 2: Generator

## Core Purpose

Force **structurally consistent** output, solving the "every generation has different format" problem.

## Use Cases

- Technical report/document generation
- API documentation
- Project scaffolding
- Standardized emails/announcements
- Commit Message generation

## Directory Structure

```
skills/report-generator/
├── SKILL.md
├── references/
│   └── style-guide.md      # Style guide (tone/format)
└── assets/
    └── report-template.md  # Output template
```

## SKILL.md Template

```markdown
---
name: report-generator
description: Generate structured technical reports. Activates when users request to write, create, or draft reports, summaries, or analysis documents.
metadata:
  pattern: generator
  output-format: markdown
  trigger-phrases: [write report, generate document, create summary, draft a report, write a summary]
---

You are a technical report generator. **Strictly follow these steps**:

## Step 1: Load Style Guide
Load `references/style-guide.md` to get tone and format conventions.

## Step 2: Load Template
Load `assets/report-template.md` to get required output structure.

## Step 3: Collect Missing Information
Ask user for following information (if not provided):
- Topic or core content
- Key findings or data points
- Target audience (technical/management/general)
- Expected length (brief/detailed)

## Step 4: Fill Template
Fill each field of template per style guide rules.
**Prohibit** omitting any sections in template.

## Step 5: Output
Return complete Markdown document.

## Output Requirements
- Use Markdown format
- All section headers match template
- Reference tone conventions from style guide
- If data exists, present with tables or lists
```

## assets/report-template.md Template

```markdown
# {{title}}

## Executive Summary
{{Core conclusions within 200 words}}

## Background
{{Problem background/context}}

## Methodology
{{Analysis methods/tools/data sources}}

## Key Findings
{{List 3-5 core findings as bullet points}}

## Detailed Analysis
{{In-depth analysis, can be split into subsections}}

## Recommendations & Next Steps
{{Actionable recommendations}}

## Appendix
{{Supplementary materials/reference links}}

---
*Generated: {{date}}*
*Author: {{generator}}*
```

## references/style-guide.md Template

```markdown
# Technical Report Style Guide

## Tone Conventions
- **Technical audience**: Professional, precise, may include terminology
- **Management audience**: Conclusions first, avoid technical details, emphasize ROI
- **General audience**: Accessible, use analogies, explain terminology

## Format Conventions
- Headers use Sentence case (only first letter capitalized)
- Code blocks must specify language
- Tables must have headers
- Use > format for quotes

## Prohibited Content
- Avoid vague words like "might", "perhaps"
- Don't use first person (I/we)
- Don't add unverified data

## Length Control
- Executive summary: ≤200 words
- Key findings: 3-5 items, each ≤50 words
- Detailed analysis: adjust per topic, but each section ≤800 words
```

## Variant: Interactive Generation

```markdown
## Step 3 (Interactive Version): Step-by-Step Confirmation

After filling each section, show to user and ask:
"Does this section meet your expectations? Need any adjustments?"

Continue to next section after user confirms.
```

## Pros & Cons

| Pros | Cons |
|-----|------|
| Highly consistent output | Templates rigid, low flexibility |
| Newcomers can generate professional content | Need to maintain template library |
| Easy to automate acceptance | High template design cost |

## Pattern Combinations

### Generator + Inversion

Use Inversion pattern to collect requirements first, then use Generator to fill template:

```markdown
## Phase 1: Requirements Gathering (Inversion)
Ask 5 questions to understand user needs

## Phase 2: Generate Report (Generator)
Fill template with collected information
```

### Generator + Reviewer

Auto self-check after generation:

```markdown
## Step 6: Quality Check
Load `references/quality-checklist.md` for self-check:
- [ ] All sections complete
- [ ] No spelling errors
- [ ] Data has source citations

If issues found, fix and re-output.
```

---

## Checklist

- [ ] `assets/` directory has complete templates
- [ ] `references/` directory has style guide
- [ ] SKILL.md specifies step sequence
- [ ] Has missing information handling logic (ask user)
- [ ] Output format is clear (Markdown/JSON/etc.)
