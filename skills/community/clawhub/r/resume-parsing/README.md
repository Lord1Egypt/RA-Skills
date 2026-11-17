# resume-parsing

A Claude Code / [ClawHub](https://clawhub.ai) skill that turns **PDF/DOCX resumes
into structured [JSON Resume](https://jsonresume.org) data** — for English and
Chinese resumes, single files or whole folders.

It is built on the deterministic PDF/DOCX parser
[**pdfmuse**](https://github.com/casperkwok/pdfmuse), so the "copy it down" parts
of a resume (text, emails, phones, URLs) are extracted exactly, with no
hallucination, and only the semantic mapping is left to the model.

## How it works

Extraction is split so nothing gets invented:

1. **`scripts/extract.py` (deterministic)** — runs pdfmuse to produce clean
   reading-order Markdown plus a JSON sidecar of regex-mined facts (emails,
   phones, URLs, social profiles, column count, parser warnings).
2. **The model (semantic)** — reads that Markdown and maps it onto the JSON
   Resume schema: company vs. title, ISO dates, bullets → highlights.
3. **`scripts/validate.py`** — checks the output against the standard (13
   sections) and the fixed `x_` extension namespaces.

`extract.py` auto-installs `pdfmuse` on first run, so there is **no manual
setup** — only `python3` (already present on macOS/Linux) is needed.

## Usage

In Claude Code, just point it at a resume: *"parse this resume"* /
*"解析这份简历"*. Or run the scripts directly:

```bash
# Single file, a folder (recursive), or a glob
python scripts/extract.py RESUME.pdf --out resume_parsed
python scripts/extract.py ./resumes/ --out resume_parsed
python scripts/extract.py "resumes/*.pdf" --out resume_parsed

# Validate the mapped JSON Resume output
python scripts/validate.py resume_parsed/*.json
```

## Output

- **`<name>.json`** — valid JSON Resume (standard 13 sections) plus fixed `x_`
  extensions for fields the standard lacks (`x_personal`, `x_objective`,
  `x_parse`). See [`reference/schema.md`](reference/schema.md).
- **`<name>.md`** — a one-page human-readable summary.
- **`index.csv`** (batch) — one row per candidate for quick scanning / import
  into a spreadsheet or database.

## Requirements

- `python3`
- [`pdfmuse`](https://pypi.org/project/pdfmuse/) (auto-installed; see
  `requirements.txt`)

## Credits

Extraction engine: [pdfmuse](https://github.com/casperkwok/pdfmuse). Schema:
[JSON Resume](https://jsonresume.org). Licensed under MIT.
