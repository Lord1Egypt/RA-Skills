# Markdown Structure for PDF Generation

Best practices for structuring Markdown documents that produce clean, professional landscape PDFs with Pandoc.

## Quick Pandoc Command (Standalone)

When you need to generate a PDF without relying on `build-pdf.sh`:

```bash
pandoc file.md -o file.pdf \
  --pdf-engine=xelatex \
  -V geometry:a4paper,landscape \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V mainfont="DejaVu Sans" \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  --toc --toc-depth=2 \
  --number-sections
```

**Key flags explained**:

| Flag                            | Purpose                               |
| ------------------------------- | ------------------------------------- |
| `--pdf-engine=xelatex`          | Required for Unicode and custom fonts |
| `-V geometry:a4paper,landscape` | Landscape orientation                 |
| `-V mainfont="DejaVu Sans"`     | Professional sans-serif font          |
| `--number-sections`             | Auto-number headings (1, 1.1, 1.1.1)  |
| `--toc --toc-depth=2`           | Table of contents with H1/H2          |
| `-V colorlinks=true`            | Clickable blue hyperlinks             |

---

## Heading Structure

### Never Manually Number Headings

**Wrong** - manual numbering breaks when sections are added/removed:

```markdown
# 1. Introduction

## 1.1 Background

## 1.2 Objectives

# 2. Methodology
```

**Correct** - let Pandoc number with `--number-sections`:

```markdown
# Introduction

## Background

## Objectives

# Methodology
```

### Heading Hierarchy

Use consistent heading levels for proper ToC structure:

```markdown
# Top-Level Section (H1)

## Subsection (H2)

### Sub-subsection (H3)

Content goes here. Avoid skipping levels (H1 → H3).
```

---

## Tables for Landscape Format

### Width Considerations

Landscape A4 provides ~25cm usable width. Design tables accordingly:

**Wide data tables** (ideal for landscape):

```markdown
| Project   | Duration | Commits | Releases | Cadence | Pattern        |
| --------- | -------- | ------- | -------- | ------- | -------------- |
| cc-skills | 9 days   | 167     | 64       | 7.1/day | Intense sprint |
| netstrata | 27 days  | 118     | 34       | 1.3/day | Responsive     |
```

**Narrow tables** - consider portrait or split into multiple tables.

### Table Best Practices

1. **Use pipe tables** - most portable Markdown table format
2. **Align columns** - use `:---` (left), `:---:` (center), `---:` (right)
3. **Keep headers short** - abbreviate if needed
4. **No merged cells** - Pandoc doesn't support them

---

## Links for Clickable PDFs

### External URLs

```markdown
**Profile**: [github.com/terrylica](https://github.com/terrylica)
```

With `-V colorlinks=true -V urlcolor=blue`, this renders as clickable blue text.

### Internal Cross-References

```markdown
See [Architecture Decision Records](#architecture-decision-records) below.
```

**Note**: Anchor IDs are auto-generated from heading text (lowercase, hyphens).

---

## ASCII Diagrams

### Always Use graph-easy Skill

**CRITICAL**: Never manually type ASCII diagrams. Always use the `itp:graph-easy` skill.

```bash
# General diagrams
Skill(itp:graph-easy)

# ADR architecture diagrams
Skill(itp:adr-graph-easy-architect)
```

**Why this matters:**

- Manual ASCII art has inconsistent character spacing
- graph-easy produces properly aligned boxart characters
- Output is reproducible and editable

### Keep Annotations Outside Code Blocks

**Wrong** - inline comments break diagram alignment:

Place annotations like "contains: file1, file2" inside the diagram code block.

**Correct** - annotations in regular markdown:

```markdown
**Contains**: file1, file2

[diagram code block here]
```

### Preventing Page Breaks in Diagrams

The canonical LaTeX preamble prevents code blocks from breaking across pages. For very tall diagrams that exceed page height, add `\newpage` before the section:

```markdown
\newpage

## Section with Tall Diagram
```

---

## Code Blocks

### Fenced Code with Language

````markdown
```bash
pandoc file.md -o file.pdf --pdf-engine=xelatex
```
````

````

Syntax highlighting works automatically with XeLaTeX.

### Inline Code

Use backticks for commands, filenames, and technical terms:

```markdown
Run `./build-pdf.sh` to generate the PDF.
````

---

## Lists

### Bullet Lists

```markdown
- First item
- Second item
  - Nested item
  - Another nested
- Third item
```

### Numbered Lists

```markdown
1. First step
2. Second step
3. Third step
```

**Tip**: Pandoc auto-renumbers, so you can use `1.` for all items during drafting.

---

## Horizontal Rules

Use `---` for section breaks (renders as thin line in PDF):

```markdown
## Section One

Content here.

---

## Section Two

More content.
```

---

## When to Use Landscape vs Portrait

### Use Landscape For

- Wide data tables (5+ columns)
- Comparison matrices
- Technical documentation with code blocks
- Dashboards and reports

### Use Portrait For

- Narrative documents (essays, letters)
- Simple documents with few tables
- Documents intended for printing

### Switching Orientation

If you need both in one document, use the `build-pdf.sh` script which defaults to landscape, or modify the geometry flag:

```bash
# Portrait
-V geometry:a4paper

# Landscape
-V geometry:a4paper,landscape
```

---

## Common Issues

### Table Overflow

If tables extend beyond page margins:

1. Reduce column count
2. Abbreviate headers
3. Split into multiple tables
4. Use landscape orientation

### ToC Number Overlap

If section numbers like "2.5.10" overlap with titles, the `table-spacing-template.tex` preamble fixes this automatically.

### Bullet Rendering

If bullets render as boxes or question marks, ensure you're using `mainfont="DejaVu Sans"` which has proper Unicode support.
