---
name: ref-manager
description: Use when the user wants to collect, extract, verify, and import bibliographic references into EndNote from web pages, PDF files, or a folder of PDFs, and to produce an Excel reconciliation sheet with APA citations. Trigger when the user mentions 文献、参考文献、导入 EndNote、EndNote 导入、APA 格式、APA 引用、整理文献、批量导入文献、文献对账、网页引用、PDF 文献提取、citation、reference manager、bibliography、RIS.
---

# Reference Manager

Turn web pages, PDFs, or a whole folder of PDFs into verified, APA-formatted references that can be imported into EndNote, plus an Excel reconciliation sheet.

## What This Skill Does

For every input source, the skill extracts bibliographic metadata, cross-checks it against Crossref (the authoritative DOI registry), corrects any wrong or missing fields, formats an APA 7th-edition citation, and writes three deliverables:

- `references.ris` — import into EndNote via File → Import → Reference Manager (RIS)
- `references.xml` — EndNote XML variant (richer field mapping)
- `文献对账表.xlsx` — Excel sheet comparing original inputs with the imported APA data

## Input Types

The user may provide any combination of:

1. Web page URLs (single or multiple)
2. PDF file paths
3. A folder path — every `.pdf` inside is scanned recursively
4. Raw APA text strings to parse and verify

## Core Workflow

1. Ask the user for their sources (URLs, PDF paths, folder, or raw APA text).
2. Run the pipeline script (see "Running the Pipeline" below).
3. Read the generated `refs.json` to see each record's verification status.
4. Report results to the user: how many corrected, how many already correct, how many need manual confirmation.
5. Present `references.ris`, `references.xml`, and the Excel sheet.
6. If any records are marked "待人工确认", list them and ask the user to supply the missing or uncertain fields, then re-run.

## Running the Pipeline

First ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python scripts/main.py \
  --urls "https://example.com/article" "https://example.com/page2" \
  --pdfs "/path/to/paper.pdf" \
  --folder "/path/to/papers" \
  --apa "Some raw APA string..." \
  --out "./ref-manager-output"
```

All flags are optional; provide at least one input type. The `--out` directory defaults to `./ref-manager-output`.

The script prints a per-record summary with a status flag for each reference.

## Verification and Correction

- **DOI present and resolved in Crossref** → fields are filled and corrected against Crossref; records marked `已修正` (corrected) or `原样正确` (already correct).
- **DOI present but not in Crossref** (common for Chinese literature) → marked `待人工确认` with a note; do NOT invent data.
- **No DOI found** → marked `待人工确认`; rely on the user to confirm.

Never fabricate authors, years, journals, or URLs. When a field is uncertain, mark it and ask.

## Output Structure

```text
ref-manager-output/
├── references.ris     # consolidated RIS for EndNote
├── references.xml     # consolidated EndNote XML
├── 文献对账表.xlsx      # reconciliation sheet
└── refs.json          # machine-readable intermediate
```

The Excel sheet has these columns (read `references/endnote-import-guide.md` for the full explanation):

- 原文信息：序号、来源类型、原文链接/文件名、原始提供的APA信息
- 导入信息：标题、作者、年份、期刊/来源、卷/期/页码、DOI、文献类型、APA引用（第7版）
- 核对结果：核对结果（已修正 / 原样正确 / 待人工确认）、修正说明/备注

## EndNote Import (Important Boundary)

The `.enl` library file is a closed proprietary format with no public API. This skill therefore produces RIS/XML files; the user imports them into EndNote with one action:

`File → Import → File` → select `references.ris` → Import Option `Reference Manager (RIS)` → Import.

See `references/endnote-import-guide.md` for step-by-step instructions.

## Reference Files

- Read `references/apa-7-rules.md` when formatting citations or when the user asks about APA rules or wants custom formatting.
- Read `references/crossref-api.md` when debugging extraction, adding new fields, or handling non-journal sources.
- Read `references/endnote-import-guide.md` when the user asks how to import or troubleshoots an EndNote import.
