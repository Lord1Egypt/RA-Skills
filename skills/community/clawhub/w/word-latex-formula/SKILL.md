---
name: word-latex-formula
description: Convert manually typed formulas in Word documents (.doc, .docx, .wps) into editable Word equations while preserving layout through local Microsoft Word or LibreOffice conversion and direct OOXML edits. Use for academic manuscripts, staged formula review, local batch conversion, or optional AI-assisted formula classification.
---

# Word Formula Conversion

Use this skill when a user wants manually typed formula text in a Word document converted into editable Word equations while preserving the original document layout as much as possible.

## Resource Layout

The runnable project is bundled at `resources/latex_convert_project/`.

- Core CLI: `python3 -m latex_convert.cli`
- Web UI starter: `python scripts/start_web.py`
- Security notes: read `references/SECURITY_AND_PRIVACY.md` before enabling AI review or configuring any external model endpoint.
- Operational details: read `references/USAGE.md` when a user asks for installation, web UI, or advanced parameters.

## Default Workflow

1. Keep the source document unchanged.
2. Work from `resources/latex_convert_project/` unless the user provides another checkout path.
3. For `.doc` or `.wps`, use `--engine auto` by default. macOS and Windows try Microsoft Word first; if Word automation fails, the code falls back to LibreOffice. Linux uses LibreOffice.
4. For important manuscripts, prefer the staged pipeline: `scan`, review or decide, then `apply`.
5. Leave bibliography protection enabled unless the user explicitly says formulas appear inside the bibliography section.
6. Modify only OOXML formula targets. Do not rebuild the document with high-level document libraries.
7. Verify output by checking the JSON report and confirming Word math nodes exist.

## Common Commands

One-step local conversion:

```bash
cd resources/latex_convert_project
python3 -m latex_convert.cli convert input.docx -o output.docx --report report.json
```

Staged review:

```bash
cd resources/latex_convert_project
python3 -m latex_convert.cli scan input.docx --out candidates.json --review-doc candidates.docx
python3 -m latex_convert.cli decide candidates.json -o decisions.json --provider rule
python3 -m latex_convert.cli apply input.docx --decisions decisions.json -o output.docx --report apply_report.json
```

Optional AI-assisted decision:

```bash
cd resources/latex_convert_project
python3 -m latex_convert.cli decide candidates.json \
  -o ai_decisions.json \
  --provider ai \
  --api-key "$OPENAI_API_KEY" \
  --base-url "https://api.openai.com/v1" \
  --model "gpt-4.1-mini"
```

Quick Web UI:

```bash
cd resources/latex_convert_project
python scripts/start_web.py
```

Open `http://127.0.0.1:5173`.

## Data and Network Policy

Default rule-based conversion is local-only. It reads the user's document, invokes local Word or LibreOffice when needed, edits OOXML locally, and writes local output files.

External network requests occur only when the user explicitly chooses AI review, clicks AI conversion in the Web UI, or tests a configured AI model. In that mode, the tool sends only formula-candidate data needed for classification and LaTeX normalization to the user-provided `base_url`: candidate id, formula text, nearby context, local LaTeX draft, confidence/default action, and model metadata. The whole Word file is not uploaded by the built-in AI review path. API keys are read from user input or local environment files and are not bundled in this skill.

If an AI request times out or fails, the tool retries once by default and then falls back to local rule decisions, preserving task completion without requiring further external calls.

## Quality Checks

- Confirm the output `.docx` opens in Word.
- Confirm converted formulas are editable Word equations, not images.
- Check `formulas_converted`, `formulas_kept`, and `failed` in the report.
- Spot-check fractions, subscripts, superscripts, Greek letters, sums, and inequalities.
