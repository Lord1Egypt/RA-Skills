**Skill**: [Pandoc PDF Generation](../SKILL.md)

## Common Patterns and Solutions

### Pattern 0: Markdown Best Practices for PDF Generation

#### Heading Numbering

**Never manually number headings - Pandoc handles this automatically**

❌ **Bad**:
```markdown
# 1. Executive Summary
## 1.1 Background
## 1.2 Key Findings
# 2. Analysis
## 2.1 Methodology
```

✅ **Good**:
```markdown
---
title: Strategic Analysis Report
---

# Executive Summary
## Background
## Key Findings
# Analysis
## Methodology
```

**Pandoc command**:
```bash
pandoc input.md -o output.pdf --number-sections
```

**Result**: Pandoc automatically numbers all sections as 1, 1.1, 1.2, 2, 2.1, etc.

**Why this matters**:
- Manual numbering creates "1. 1. Executive Summary" duplication
- Reorganizing sections requires manual renumbering (error-prone)
- `--number-sections` provides consistent, automatic numbering
- Section numbers update automatically when structure changes

**Applies to**: All markdown intended for PDF generation (technical docs, business proposals, reports, research papers)

---

### Pattern 1: Technical Documentation

**Use case:** API docs, user manuals, specifications

**Features needed:**
- Automatic section numbering
- Deep table of contents (level 3-4)
- Code syntax highlighting
- Monospace fonts for technical content

**Command:**
```bash
pandoc document.md \
  -o document.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=4 \
  --number-sections \
  --highlight-style=tango \
  -V mainfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono"
```

### Pattern 2: Academic Papers

**Use case:** Research papers, theses, dissertations

**Features needed:**
- Bibliography management
- Citation style control
- Academic formatting
- Abstract support

**YAML:**
```yaml
---
title: Research Paper Title
author: Author Name
date: 2025-11-04
abstract: |
  Research abstract here.
bibliography: references.bib
csl: apa.csl
---
```

**Command:**
```bash
pandoc paper.md \
  -o paper.pdf \
  --pdf-engine=xelatex \
  --citeproc \
  --number-sections \
  -V fontsize=12pt \
  -V linestretch=2
```

### Pattern 3: Business Proposals

**Use case:** Strategic proposals, executive reports

**Features needed:**
- Table of contents
- Section numbering
- Professional formatting
- Landscape orientation for wide tables

**Command:**
```bash
pandoc proposal.md \
  -o proposal.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  --number-sections \
  -V geometry:landscape \
  -V geometry:margin=1in \
  -V mainfont="DejaVu Sans" \
  -H table-spacing.tex
```

