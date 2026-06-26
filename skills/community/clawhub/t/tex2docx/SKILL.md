---
name: tex2docx
description: Convert LaTeX (.tex) academic papers to Word (.docx) with editable OMML equations, native Word tables, embedded figures, IEEE two-column format, and bibliography. Use when a user provides a .tex file and asks for a Word/DOCX version, or when converting academic LaTeX papers to editable Office format.
---

# tex2docx — LaTeX to Word Converter

## Requirements

- **pandoc** (system install): `winget install pandoc` or pandoc.org
- **Python packages**: `pip install python-docx lxml pypandoc_binary`

## Usage

```bash
python scripts/tex2docx.py input.tex [output.docx]
```

If `output.docx` is omitted, output is `input.docx` in the same directory.

## How It Works (Three Phases)

```
.tex ──→ [pandoc] ──→ OMML equations (13+ Word-editable formulas)
  │
  └──→ [Custom parser] ──→ Native Word tables ├──→ Final .docx
                           Embedded figures     │   (merged)
                           Formatted refs       │
                           IEEE layout & font  ┘
```

### Phase 1 — Pandoc
Runs pandoc via pypandoc. Input file must be in its own directory (with `figures/` subfolder if images exist). The script `chdir`s to the tex directory before running pandoc so image paths resolve correctly.

### Phase 2 — Custom LaTeX Parser
RegEx-based extraction of:
- **Tables**: `\begin{table}` → Word Table objects (full borders, centered, 8pt TNR)
- **Figures**: `\includegraphics{}` + `\caption{}` → PNG/PDF embeds with italic captions
- **References**: `\thebibliography` → formatted entries with hanging indent
- **Sections**: `\section{}`, `\subsection{}` → bold headings
- **Metadata**: `\title`, `author`, `\abstract`, `\IEEEkeywords`

### Phase 3 — Merge
OMML equation paragraphs from pandoc are inserted into the cleanly-built document. Body paragraphs get 0.25in first-line indent. All LaTeX commands (`\textbf`, `\toprule`, `\ref`, `\cite`, `\begin{itemize}`, etc.) are stripped from text content.

## Output Format

| Feature | Detail |
|---------|--------|
| Font | Times New Roman (10pt body, 9pt table/figure, 8pt refs) |
| Layout | A4, two-column IEEE conference style |
| Equations | OMML (double-click to edit in Word) |
| Tables | Native Word tables, all borders |
| Figures | PNG/PDF embedded with "Fig." captions |
| References | Hanging indent, `[bN]` format |
| First indent | 0.25in on body paragraphs |

## Verification

```bash
python scripts/verify.py output.docx
```

Reports paragraph/table/image/equation counts and checks for LaTeX residue.

## Chinese (ctex) Support

Fully supports Chinese LaTeX documents using the `ctex` package:
- Chinese section titles (引言, 方法, 实验, 结论等) are recognized
- `\section*{}` (star variant) is supported
- Chinese table headers preserved
- Chinese text in titles rendered via `w:eastAsia` font fallback
- `\title{...}` and `\author{...}` residue paragraphs are filtered

## Limitations

- **Inline math** (`$...$`) becomes plain text (italic), not OMML — only `\begin{equation}`, `\begin{align}`, and `\[...\]` become editable equations
- **No .bib support**: references must be in `\thebibliography{}` environment
- **PNG images preferred**: script tries PNG then PDF fallback
- **Pandoc path**: the system pandoc binary must be discoverable by pypandoc

## Script: `scripts/tex2docx.py`

Self-contained (660+ lines). Key internal functions:

| Function | Role |
|----------|------|
| `extract_tex()` | Parse all structural elements from .tex |
| `extract_omml()` | Pull OMML XML from pandoc output |
| `build_docx()` | Construct final document with all components |
| `clean()` | Strip LaTeX commands to plain text |
| `add_table()` | Build Word table with borders |
| `add_figure()` | Embed image + caption |
