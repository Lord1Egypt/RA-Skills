---
name: resume-parsing
description: Parses PDF/DOCX resumes (CV, 简历) into structured JSON Resume standard data using the pdfmuse deterministic extraction engine. Handles English and Chinese resumes and whole folders in batch, extracting contacts, work history, education, skills, and projects with source traceability. Use when the user wants to parse/extract/structure a resume or CV, convert a resume PDF to JSON, build a candidate table from resumes, or process a folder of resumes for recruiting/screening/ATS workflows.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
---

# Resume parsing

Turn resume PDFs/DOCX into clean JSON Resume standard data. Works for English and
Chinese resumes, single files or whole folders.

## How it works — division of labor

Extraction is split so nothing gets hallucinated:

- **`scripts/extract.py` (deterministic)** runs pdfmuse to produce clean
  reading-order Markdown plus a sidecar of regex-mined facts (emails, phones,
  URLs, social profiles, column count, parser warnings). No guessing.
- **You (semantic)** read that Markdown and map it onto the JSON Resume schema —
  deciding what is a company vs a title, normalizing dates, grouping bullets.
- **`scripts/validate.py`** checks your output against the standard.

Requirements are auto-handled: `extract.py` installs `pdfmuse` on first run, so
the user never sets anything up. Only `python3` (already present) is needed.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Extract: run extract.py on the input(s)
- [ ] 2. Read each .extract.md + .extract.json
- [ ] 3. Map to JSON Resume (see reference/schema.md) → <name>.json
- [ ] 4. Validate: run validate.py; fix errors; repeat until [ OK ]
- [ ] 5. Write <name>.md human summary; for batch, build index.csv
```

### Step 1 — Extract

```bash
python scripts/extract.py RESUME.pdf --out resume_parsed          # single
python scripts/extract.py ./resumes/ --out resume_parsed          # folder (recursive)
python scripts/extract.py "resumes/*.pdf" --out resume_parsed     # glob
```

Writes `<stem>.extract.md` (body) and `<stem>.extract.json` (contacts, columns,
warnings) per file, and prints a manifest. Read the manifest: a `columns: 2` or
any `warnings` entry means the reading order may be scrambled — cross-check that
resume's timeline against the source, and if it looks interleaved, render pages
to images to read the layout visually before mapping.

### Step 2–3 — Map to JSON Resume

Read `reference/schema.md` for the full field list and mapping rules, and
`examples.md` for worked English + Chinese examples. Core rules:

- **Never invent** — omit unknown fields and whole empty sections; no `"N/A"`.
- **Dates → ISO** — `2020年3月`/`Mar 2020` → `2020-03`; current role = `startDate`
  with no `endDate`.
- **Contacts from the sidecar** — use its regex-mined email/phone/profiles, not
  prose re-reads.
- **Keep the original language** for values; section keys stay English.
- **Fields the standard lacks** (birth date, gender, job objective, expected
  salary…) go in the fixed extension namespaces `x_personal` / `x_objective` —
  see `reference/schema.md` for the exact sub-field names; don't invent keys.
- **Traceability** — add an `x_parse` block with `source`, `columns`, `warnings`,
  `confidence`. Parser data goes in `x_parse`, never in standard `meta`.

Write each candidate to `<name>.json`.

### Step 4 — Validate (feedback loop)

```bash
python scripts/validate.py resume_parsed/*.json
```

`[warn]` = non-standard field (fix unless intentional under `x_`); `[FAIL]` =
type or date error you must fix. Re-run until every file is `[ OK ]`.

### Step 5 — Human outputs

- `<name>.md`: a one-page summary (name, headline, contacts → work timeline →
  skills → education) for quick reading.
- **Batch only** — `index.csv`: one row per candidate with columns
  `name, label, years, current_company, top_skills, email, phone, source,
  warnings`. This is the scannable roster (and maps cleanly onto a spreadsheet /
  多维表格 later).

## Output summary

- Primary: `<name>.json` — valid JSON Resume (standard 13 sections) + `x_parse`.
- Companion: `<name>.md` — human summary.
- Batch: `index.csv` — candidate roster.

## Reference files

- `reference/schema.md` — full JSON Resume field reference + mapping rules.
- `examples.md` — English and Chinese input→output examples.
- `scripts/extract.py` — deterministic extraction (run it).
- `scripts/validate.py` — schema validator (run it).
