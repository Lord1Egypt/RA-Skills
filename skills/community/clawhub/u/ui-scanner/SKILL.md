---
name: ui-scanner
description: Crawl and analyze a website's visual design system from a given URL, identifying design style, color system, typography, component styles, and UI patterns. Output a structured design specification document for UI generation. Suitable for competitive design analysis, UI restoration, design system reverse engineering, style migration, and similar scenarios.
---

# UI Scanner — Website Design System Extraction

Automatically crawl a website URL and reverse-engineer its visual design system, outputting a structured design specification document.

## Workflow

```
URL input → page crawl → visual element classification → style extraction → structured output → write to file
```

## Routing Table

| Scenario | Reference File |
|----------|---------------|
| Quick start, minimal workflow | [quick-start.md](references/quick-start.md) |
| Output format, YAML template, field descriptions | [output-template.md](references/output-template.md) |
| Detailed explanation of 6 analysis dimensions | [analysis-dimensions.md](references/analysis-dimensions.md) |
| Extraction methods, CSS sources, inference rules | [extraction-methods.md](references/extraction-methods.md) |
| Common mistakes and anti-patterns | [anti-patterns.md](references/anti-patterns.md) |

## Output

Results are written to `{domain}_design.md` using standard YAML frontmatter + Markdown structure. See [output-template.md](references/output-template.md) for the complete template and field descriptions.
