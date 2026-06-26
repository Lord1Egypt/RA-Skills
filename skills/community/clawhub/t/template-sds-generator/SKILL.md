---
name: template-sds-generator
version: "0.2.1"
description: Generate a deterministic, template-preserving 16-section SDS/MSDS package from 1 DOCX template, 1 prompt/rule file, and 1-3 source SDS/MSDS files, with DOCX/PDF output plus structured JSON, provenance CSV, and review checklist artifacts.
homepage: https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/template-sds-generator-skill
user-invocable: true
metadata: {"openclaw":{"emoji":"🧪","homepage":"https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/template-sds-generator-skill","os":["darwin","linux","win32"],"requires":{"anyBins":["python3","python","py"]},"skillKey":"template-sds-generator"}}
---

Use this skill when the user wants a traceable SDS/MSDS package that must preserve a supplied Word template.

Use `{baseDir}` to refer to this skill folder.

## Preconditions

- Before production use, replace the placeholder company block in `{baseDir}/config/fixed_company.yml` with the owning company's approved supplier information.
- The runtime needs Python 3.11+.
- OCR is optional. If scanned PDFs are expected, `tesseract` must be available on the host or in the sandbox/container runtime.
- PDF export requires `soffice` or `libreoffice` on the execution runtime.
- This package is self-bootstrapping at runtime: the Python launcher creates `.venv` and installs `requirements.lock` inside the skill folder on first use.
- ClawHub publishes text files only. The fallback base template `assets/templates/sds_base.docx` is generated locally on first use when it is missing.

## Canonical entrypoint

Prefer the bundled cross-platform Python launcher instead of shell-only wrappers:

```text
python3 {baseDir}/scripts/run_openclaw_skill.py --template-docx <template.docx> --prompt-file <rules.txt> --sources <source1> [<source2> <source3>] --outdir <target> --mode draft
```

Windows launcher variants:

```text
py {baseDir}\scripts\run_openclaw_skill.py --template-docx <template.docx> --prompt-file <rules.txt> --sources <source1> [<source2> <source3>] --outdir <target> --mode draft
python {baseDir}\scripts\run_openclaw_skill.py --template-docx <template.docx> --prompt-file <rules.txt> --sources <source1> [<source2> <source3>] --outdir <target> --mode draft
```

## Workflow

1. If the runtime looks incomplete, run:
   `python3 {baseDir}/scripts/runtime_doctor.py`
   On Windows use `py` or `python`.
2. Run the canonical entrypoint. The launcher creates or repairs `.venv`, installs `requirements.lock`, and generates a generic base template if `assets/templates/sds_base.docx` is missing.
3. Use `--enable-ocr` only when scanned PDFs are expected. If no OCR backend is available, the run fails clearly.
4. Return the generated files from `outputs/runs/.../final`.
5. When provenance or review details matter, inspect `outputs/runs/.../audit`.

## Output expectations

Primary deliverables:

- `final/sds_document.docx`
- `final/sds_document.pdf` when a PDF engine is available
- `final/structured_data.json`
- `final/field_source_map.csv`
- `final/review_checklist.md`

Audit outputs may also include:

- `audit/content_policy_report.json`
- `audit/ocr_audit.json`
- `audit/field_source_map.md`
- `run_manifest.json`

## Guardrails

- Preserve the supplied template layout. Do not clear the document body when the user provides a client template.
- Do not invent safety-critical values such as GHS classifications, UN numbers, packing groups, flash points, LD50 values, or regulatory identifiers.
- Treat `structured_data.json`, `field_source_map.csv`, and `review_checklist.md` as first-class deliverables alongside the DOCX/PDF.
