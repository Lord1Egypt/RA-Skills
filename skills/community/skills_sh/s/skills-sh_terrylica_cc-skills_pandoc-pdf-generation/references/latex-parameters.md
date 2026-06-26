**Skill**: [Pandoc PDF Generation](../SKILL.md)

# LaTeX Parameters Reference for Pandoc

## Table of Contents

- [Document Class and Layout](#document-class-and-layout)
  - [Document Class](#document-class)
  - [Page Geometry](#page-geometry)
- [Typography](#typography)
  - [Fonts](#fonts)
  - [Spacing](#spacing)
- [Headers and Footers](#headers-and-footers)
- [Table of Contents](#table-of-contents)
- [Section Numbering](#section-numbering)
- [Colors](#colors)
- [Tables](#tables)
  - [Default Table Parameters (in LaTeX preamble)](#default-table-parameters-in-latex-preamble)
- [Page Breaks](#page-breaks)
- [Code Highlighting](#code-highlighting)
- [Bibliography and Citations](#bibliography-and-citations)
- [Hyphenation and Language](#hyphenation-and-language)
- [Advanced LaTeX Customization](#advanced-latex-customization)
  - [Custom Preamble File](#custom-preamble-file)
  - [Include LaTeX Inline](#include-latex-inline)
- [Common Combinations](#common-combinations)
  - [Academic Paper](#academic-paper)
  - [Technical Manual](#technical-manual)
  - [Business Report](#business-report)
- [Troubleshooting](#troubleshooting)
  - [Font Not Found](#font-not-found)
  - [Package Not Found](#package-not-found)
  - [Page Break Issues](#page-break-issues)
  - [Section Numbering Starting at 0](#section-numbering-starting-at-0)
- [Resources](#resources)
- [LaTeX Customization](#latex-customization)
  - [Custom LaTeX Preamble](#custom-latex-preamble)
  - [Common LaTeX Variables](#common-latex-variables)
  - [Table Spacing Troubleshooting](#table-spacing-troubleshooting)
  - [Reducing Table Font Size](#reducing-table-font-size)
- [Production Build Script Pattern](#production-build-script-pattern)
  - [Example: build-pdf.sh](#example-build-pdfsh)
- [Common Patterns and Solutions](#common-patterns-and-solutions)

Comprehensive guide to LaTeX variables and customizations available through Pandoc's `-V` flag and custom preambles.

## Document Class and Layout

### Document Class

```bash
-V documentclass=article    # Standard document (default)
-V documentclass=report     # Longer documents with chapters
-V documentclass=book       # Books with front/back matter
-V documentclass=memoir     # Flexible book class
```

### Page Geometry

**Single margin:**

```bash
-V geometry:margin=1in      # All margins 1 inch
```

**Individual margins:**

```bash
-V geometry:top=1in
-V geometry:bottom=1in
-V geometry:left=1.5in
-V geometry:right=1.5in
```

**Page orientation:**

```bash
-V geometry:landscape       # Landscape mode
-V geometry:portrait        # Portrait mode (default)
```

**Paper size:**

```bash
-V geometry:a4paper         # A4 (210 × 297 mm)
-V geometry:letterpaper     # US Letter (8.5 × 11 in) [default]
-V geometry:a3paper         # A3 (297 × 420 mm)
```

## Typography

### Fonts

**Main document font:**

```bash
-V mainfont="DejaVu Sans"
-V mainfont="Times New Roman"
-V mainfont="Latin Modern Roman"  # LaTeX default
```

**Monospace font (code blocks):**

```bash
-V monofont="DejaVu Sans Mono"
-V monofont="Courier New"
-V monofont="Fira Code"
```

**Sans-serif font:**

```bash
-V sansfont="Arial"
-V sansfont="Helvetica"
```

**Font size:**

```bash
-V fontsize=10pt
-V fontsize=11pt
-V fontsize=12pt
-V fontsize=14pt
```

### Spacing

**Line spacing:**

```bash
-V linestretch=1.0      # Single spacing
-V linestretch=1.5      # 1.5 spacing
-V linestretch=2.0      # Double spacing
```

**Paragraph spacing:**

```bash
-V parskip=half         # Half line between paragraphs
-V parskip=full         # Full line between paragraphs
```

**Paragraph indentation:**

```bash
-V indent=true          # Indent first line (default)
-V indent=false         # No indentation
```

## Headers and Footers

### Page numbering:\*\*

```bash
-V pagestyle=plain      # Page numbers at bottom center (default)
-V pagestyle=empty      # No headers/footers
-V pagestyle=headings   # Chapter/section in header
```

### Custom headers:\*\*

```bash
-V header-includes='\\usepackage{fancyhdr}\\pagestyle{fancy}\\fancyhead[L]{Left Header}\\fancyhead[R]{Right Header}'
```

## Table of Contents

**ToC title:**

```bash
-V toc-title="Table of Contents"
-V toc-title="Contents"
```

**ToC depth (via command line):**

```bash
--toc-depth=2           # Include h2, h3
--toc-depth=3           # Include h2, h3, h4
--toc-depth=4           # Include all heading levels
```

**ToC number spacing (fix overlapping multi-digit numbers):**

```latex
% Add to LaTeX preamble to fix subsection numbers like "2.5.10" overlapping titles
\usepackage{tocloft}
\setlength{\cftsecnumwidth}{2.5em}      % Section numbers (1, 2, 3)
\setlength{\cftsubsecnumwidth}{3.5em}   % Subsection numbers (2.1, 2.5.10)
\setlength{\cftsubsubsecnumwidth}{4.5em} % Subsubsection numbers (2.5.10.1)
```

**Default widths (often too small):**

- `\cftsecnumwidth`: 1.5em
- `\cftsubsecnumwidth`: 2.3em (causes overlap with multi-digit subsections)
- `\cftsubsubsecnumwidth`: 3.2em

## Section Numbering

**Control section depth:**

```bash
-V secnumdepth=2        # Number up to subsections
-V secnumdepth=3        # Number up to subsubsections (default)
-V secnumdepth=0        # No section numbering
```

## Colors

**Link colors:**

```bash
-V linkcolor=blue
-V urlcolor=blue
-V citecolor=blue
```

**Named colors:** black, blue, brown, cyan, darkgray, gray, green, lightgray, lime, magenta, olive, orange, pink, purple, red, teal, violet, white, yellow

## Tables

### Default Table Parameters (in LaTeX preamble)

**Row spacing:**

```latex
\renewcommand{\arraystretch}{1.2}    % 1.0 = tight, 1.5 = loose
```

**Cell padding:**

```latex
\setlength{\extrarowheight}{4pt}     % Top padding in cells
```

**Column spacing:**

```latex
\setlength{\tabcolsep}{8pt}          % Space between columns
```

**Table breaking:**

```latex
\LTchunksize=50                      % Rows processed before page break
```

## Page Breaks

**Penalties (higher = less likely to break):**

```latex
\widowpenalty=10000        % Orphaned line at top of page
\clubpenalty=10000         % Orphaned line at bottom of page
\brokenpenalty=10000       % Hyphenated word across pages
```

## Code Highlighting

**Syntax highlighting theme:**

```bash
--highlight-style=pygments
--highlight-style=tango
--highlight-style=espresso
--highlight-style=zenburn
--highlight-style=kate
--highlight-style=monochrome
```

**Custom highlight theme:**

```bash
--highlight-style=custom.theme
```

Generate theme file:

```bash
pandoc --print-highlight-style=pygments > custom.theme
```

## Bibliography and Citations

**Citation style:**

```bash
--csl=chicago-author-date.csl
--csl=apa.csl
--csl=mla.csl
```

**Bibliography file:**

```bash
--bibliography=references.bib
--bibliography=refs1.bib --bibliography=refs2.bib
```

**Bibliography title:**

```bash
-V reference-section-title="References"
-V reference-section-title="Bibliography"
```

## Hyphenation and Language

**Language:**

```bash
-V lang=en-US           # American English (default)
-V lang=en-GB           # British English
-V lang=de-DE           # German
-V lang=fr-FR           # French
```

**Hyphenation:**

```bash
-V hyphenate=true       # Allow hyphenation (default)
-V hyphenate=false      # Disable hyphenation
```

## Advanced LaTeX Customization

### Custom Preamble File

Create `.tex` file with LaTeX commands:

**example-preamble.tex:**

```latex
% Custom packages
\usepackage{booktabs}       % Professional tables
\usepackage{longtable}      % Multi-page tables
\usepackage{graphicx}       % Enhanced graphics
\usepackage{xcolor}         % Extended colors

% Custom commands
\newcommand{\mycommand}[1]{\textbf{#1}}

% Custom spacing
\setlength{\parskip}{1em}
\setlength{\parindent}{0em}
```

**Usage:**

```bash
pandoc document.md -o document.pdf -H example-preamble.tex
```

### Include LaTeX Inline

For simple customizations:

```bash
-V header-includes='\\usepackage{booktabs}'
-V header-includes='\\renewcommand{\\arraystretch}{1.2}'
```

## Common Combinations

### Academic Paper

```bash
pandoc paper.md -o paper.pdf \
  --pdf-engine=xelatex \
  --number-sections \
  --citeproc \
  --bibliography=refs.bib \
  --csl=apa.csl \
  -V fontsize=12pt \
  -V linestretch=2 \
  -V geometry:margin=1in
```

### Technical Manual

```bash
pandoc manual.md -o manual.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --highlight-style=tango \
  -V mainfont="DejaVu Sans" \
  -V monofont="Fira Code" \
  -V fontsize=11pt
```

### Business Report

```bash
pandoc report.md -o report.pdf \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  -V geometry:landscape \
  -V geometry:margin=1in \
  -V mainfont="Calibri" \
  -H table-spacing.tex
```

## Troubleshooting

### Font Not Found

**Problem:** `Font 'Arial' not found`

**Solution:**

```bash
# List available fonts
fc-list | grep -i arial

# Use system-available font
-V mainfont="Helvetica"

# Or use LaTeX default
-V mainfont="Latin Modern Roman"
```

### Package Not Found

**Problem:** `LaTeX Error: File 'package.sty' not found`

**Solution:**

```bash
# Install missing LaTeX package (macOS)
sudo tlmgr install package-name

# Or install full MacTeX distribution
brew install --cask mactex
```

### Page Break Issues

**Problem:** Tables or figures breaking awkwardly

**Solution:**

```latex
% Add to preamble (-H file.tex)
\usepackage{needspace}
\widowpenalty=10000
\clubpenalty=10000
```

### Section Numbering Starting at 0

**Problem:** Sections numbered 0.1, 0.2 instead of 1, 2

**Solution:** Use YAML front matter for title instead of `# Title` heading

## Resources

- [Pandoc Manual - Variables](https://pandoc.org/MANUAL.html#variables)
- [LaTeX geometry package](https://ctan.org/pkg/geometry)
- [LaTeX font catalog](https://tug.org/FontCatalogue/)
- [CSL style repository](https://www.zotero.org/styles)

## LaTeX Customization

### Custom LaTeX Preamble

Create a `.tex` file with LaTeX commands for fine-grained control:

**table-spacing.tex:**

```latex
% Compact table spacing to prevent page breaks
\renewcommand{\arraystretch}{1.0}      % Row spacing (default: 1.0)
\setlength{\extrarowheight}{2pt}       % Cell padding (default: 0pt)
\setlength{\tabcolsep}{6pt}            % Column spacing (default: 6pt)

% Discourage awkward table page breaks
\usepackage{needspace}
\LTchunksize=100                        % Process more rows before page break
\widowpenalty=10000                     % Discourage orphaned lines
\clubpenalty=10000
```

**Use in build:**

```bash
pandoc document.md -o document.pdf -H table-spacing.tex
```

### Common LaTeX Variables

Set LaTeX variables with `-V` flag:

```bash
-V geometry:margin=1in              # Page margins
-V geometry:landscape               # Landscape orientation
-V mainfont="DejaVu Sans"           # Font family
-V fontsize=11pt                    # Font size
-V linestretch=1.5                  # Line spacing
-V documentclass=article            # Document class
```

### Table Spacing Troubleshooting

**Problem:** Tables breaking across pages awkwardly

**Solution 1: Compact spacing (reduces table height 20-25%)**

```latex
\renewcommand{\arraystretch}{1.0}      % Was 1.2
\setlength{\extrarowheight}{2pt}       % Was 4pt
\setlength{\tabcolsep}{6pt}            % Was 10pt
```

**Solution 2: Increase page break penalties**

```latex
\usepackage{needspace}
\LTchunksize=100
\widowpenalty=10000
\clubpenalty=10000
```

**Trade-off:** Denser tables vs. better page break behavior. Very long tables will still break (correct behavior for readability).

### Reducing Table Font Size

**Problem:** Tables with many columns or dense content need to fit better on pages

**Idiomatic Solution: Automatic font reduction for all tables**

```latex
% Add to LaTeX preamble (e.g., table-spacing.tex)
\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\small}
```

**How it works:**

- Uses `etoolbox` package's `\AtBeginEnvironment` hook
- Automatically applies to all Pandoc-generated tables (Pandoc uses `longtable` environment)
- No markdown changes required - applies globally to all tables
- Captions remain at normal size for visual hierarchy

**Font size options (from largest to smallest):**

- `\small` (~90% of normal) - Subtle reduction, recommended default
- `\footnotesize` (~80% of normal) - Moderate reduction
- `\scriptsize` (~70% of normal) - Significant reduction
- `\tiny` (~50% of normal) - Very small, use sparingly

**To also reduce caption size:**

```latex
\usepackage[font=small]{caption}
```

**Benefits:**

- Better space efficiency without markdown modifications
- More content fits per page (especially wide tables)
- Maintains readability while improving density
- Idiomatic LaTeX pattern, widely used in academic publishing

## Production Build Script Pattern

### Example: build-pdf.sh

```bash
#!/bin/bash
# Build PDF with professional formatting
# Usage: ./build-pdf.sh

set -e  # Exit on error

echo "Generating PDF with ToC and automatic numbering..."

pandoc DOCUMENT.md \
  -o DOCUMENT.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --citeproc \
  --bibliography=references.bib \
  -V mainfont="DejaVu Sans" \
  -V geometry:margin=1in \
  -V toc-title="Table of Contents" \
  -H table-spacing.tex

echo "✅ PDF generated: DOCUMENT.pdf"
ls -lh DOCUMENT.pdf
pdfinfo DOCUMENT.pdf | grep Pages
```

**Make executable:**

```bash
chmod +x build-pdf.sh
```

**Run:**

```bash
./build-pdf.sh
```

## Common Patterns and Solutions
