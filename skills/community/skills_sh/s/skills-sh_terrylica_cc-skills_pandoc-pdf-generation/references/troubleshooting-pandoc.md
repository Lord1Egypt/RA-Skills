**Skill**: [Pandoc PDF Generation](../SKILL.md)

### Issue: Everything numbered under "1.x"

**Cause:** Document title is a level-1 heading (`# Title`)

**Solution:** Move title to YAML front matter

```yaml
---
title: Document Title
---
## First Section    ← Now correctly Section 1, not 1.1
```

### Issue: Tables breaking across pages

**Solution:** Add compact spacing in LaTeX preamble (see "LaTeX Customization" above)

### Issue: ToC too detailed

**Solution:** Reduce `--toc-depth` from 3 to 2

### Issue: Multi-digit subsection numbers overlap with titles in ToC

**Problem:** Section numbers like "2.5.10", "2.5.11" overlap with section titles in Table of Contents

**Cause:** Default LaTeX allocates only 2.3em for subsection numbers, insufficient for multi-digit numbers

**Solution:** Add to LaTeX preamble using `tocloft` package

```latex
\usepackage{tocloft}
\setlength{\cftsecnumwidth}{2.5em}      % Section numbers (1, 2, 3)
\setlength{\cftsubsecnumwidth}{3.5em}   % Subsection numbers (2.1, 2.5.10)
\setlength{\cftsubsubsecnumwidth}{4.5em} % Subsubsection numbers (2.5.10.1)
```

**Result:** Proper spacing for all subsection number lengths

### Issue: Footnotes not appearing in References section

**Expected behavior:** Pandoc footnotes appear at bottom of each page (LaTeX standard)

**For consolidated references:** Use `--citeproc` with bibliography file instead of footnote syntax

### Issue: Font not found

**Common problem:** XeLaTeX requires system fonts

**Solution:** List available fonts:

```bash
fc-list | grep -i "dejavu"
```

**Or use standard LaTeX fonts:**

```bash
-V mainfont="Latin Modern Roman"
```

### Issue: Bullet Lists Rendering as Inline Text (CRITICAL)

**Problem:** Bullet lists appear as inline text with dashes instead of proper bullets (•)

**Bad Rendering:**

```
Multi-layer validation frameworks: - HTTP/API layer validation - Schema validation - Sanity checks...
```

**Expected Rendering:**

```
Multi-layer validation frameworks:
• HTTP/API layer validation
• Schema validation
• Sanity checks
```

**Root Cause:** LaTeX's default justified text alignment breaks Pandoc-generated bullet list structures.

LaTeX's justification algorithm tries to make every line the same width by:

1. Adding/removing inter-word spaces
2. Hyphenating words
3. Sometimes **reflowing line breaks** in ways that break Pandoc's list structures

When a list appears after a paragraph ending with a colon (common pattern), the justification algorithm may:

- Merge list items onto previous lines
- Convert bullet markers (`-`) into inline dashes
- Collapse vertical list structure into horizontal flow

**Solution:** Always include `\raggedright` in LaTeX preamble

The canonical build script includes this automatically:

```latex
% Use ragged-right (left-aligned) instead of justified text
% Justified text can create awkward spacing and break list structures
\raggedright
```

**Location:** `./assets/table-spacing-template.tex` (lines 89-90, relative to skill directory)

**Verification:**

Automated check for broken bullets (expect 0 matches):

```bash
pdftotext output.pdf - | grep -E '^\w.*: -'
```

Manual visual inspection:

- Open PDF in viewer
- Scan sections with bullet lists
- Verify bullets (•) appear, not inline dashes

**Prevention:**

1. ✅ Always invoke the skill: `Skill(doc-tools:pandoc-pdf-generation)`
2. ❌ Never create ad-hoc `pandoc` commands without LaTeX preamble
3. ✅ Verify all PDFs before presenting to users

**Why This Matters:** This issue only surfaces in production with certain text patterns. Ad-hoc Pandoc commands without proper LaTeX configuration will miss this critical requirement.

**Reference:** See [Core Principles](./core-principles.md) for universal development patterns learned from this failure.

### Issue: Code Blocks/Diagrams Breaking Across Pages

**Problem:** ASCII diagrams or code blocks split between two pages, making them unreadable.

**Root Cause:** LaTeX treats code blocks as normal content flow without page break protection.

**Solution:** The canonical LaTeX preamble now includes fancyvrb with samepage:

```latex
\usepackage{fancyvrb}
\fvset{samepage=true}

\BeforeBeginEnvironment{Shaded}{\begin{samepage}}
\AfterEndEnvironment{Shaded}{\end{samepage}}
```

**For very tall diagrams** that exceed page height, add `\newpage` in markdown BEFORE the code block.

**Prevention:**

1. Always use the canonical build script (includes page break protection)
2. For tall diagrams, add `\newpage` before the section
3. Visually inspect PDF before presenting to users

### Issue: Double Section Numbering ("1. 1. Title")

**Problem:** Section headings display as "1. 1. Introduction" instead of "1. Introduction"

**Root Cause:** Manual numbering in markdown combined with `--number-sections` flag.

**Bad:** `# 1. Introduction` with `--number-sections`

**Good:** `# Introduction` with `--number-sections`

**Solution:** NEVER manually number markdown headings. Let `--number-sections` handle it.

**Prevention:**

1. Never manually number headings in markdown
2. Always use `--number-sections` flag for numbered output
3. Verify section numbering before finalizing

### Issue: ASCII Diagram Misalignment

**Problem:** ASCII box diagrams have misaligned edges, broken arrows, or inconsistent spacing.

**Root Cause:** Manually typed ASCII art instead of using graph-easy tool.

**Solution:** ALWAYS use the `itp:graph-easy` skill for ASCII diagrams:

```bash
# General diagrams
Skill(itp:graph-easy)

# ADR architecture diagrams
Skill(itp:adr-graph-easy-architect)
```

**Also:** Keep annotations OUTSIDE code blocks. Don't add inline comments inside diagrams - they break alignment. Place descriptive text in regular markdown paragraphs before or after the diagram.

**Prevention:**

1. Never manually type ASCII diagrams
2. Always use graph-easy skills
3. Never add inline comments inside diagram code blocks

### Issue: Unwanted Double-Sided Printing

**Problem:** Printer outputs double-sided when single-sided is needed.

**Solution:** Use `-o Duplex=None` with lpr:

```bash
# One-sided (simplex)
lpr -P "PRINTER_NAME" -o Duplex=None output.pdf

# Two-sided (duplex) - long edge binding
lpr -P "PRINTER_NAME" -o Duplex=DuplexNoTumble output.pdf

# Two-sided (duplex) - short edge binding (landscape)
lpr -P "PRINTER_NAME" -o Duplex=DuplexTumble output.pdf
```

**Find printer name:**

```bash
lpstat -p -d
```

**Note:** Some systems have default duplex settings in `~/.lpoptions` that may override command-line options.
