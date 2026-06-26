# PSD Batch Export

Production PSD batch workflow for analyzing Photoshop text layers, mapping Excel/CSV data, generating editable PSD plus PNG batches, and verifying outputs.

[![ClawHub](https://img.shields.io/badge/ClawHub-v4.4-blue)](https://clawhub.com/luis1213899/psd-batch-export)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Quick Start

```powershell
python scripts/psd_batch.py diagnose --json
python scripts/psd_batch.py analyze "template.psd" --data "data.xlsx" --json-out report.json
python scripts/psd_batch.py preview "template.psd" --data "data.xlsx" --out "out" --rows 3
python scripts/psd_batch.py export "template.psd" --data "data.xlsx" --out "out" --dpi 300 --verify-samples 3 --json-out out/report.json
python scripts/psd_batch.py verify "out" --samples 3 --json
```

Built-in templates:

```powershell
python scripts/psd_batch.py templates list
python scripts/psd_batch.py templates info morning
python scripts/psd_batch.py export morning --data "data.xlsx" --out "out"
```

## What It Does

| Capability | Description |
| --- | --- |
| Layer analysis | Detects PSD text layers, text, font family, font size, fill color, bbox, and capacity risk. |
| Data mapping | Maps Excel/CSV columns to PSD layers with confidence labels and optional `--strict` failure mode. |
| Preview | Renders the first N rows to `out/dryrun_preview/` before full export. |
| Batch export | Writes editable PSD files to `out/psd/` and print-ready PNG files to `out/png/`; replacement text keeps each PSD layer color unless `--color` is provided. |
| Verification | Writes `out/verify_report/report.json` and optional OCR checks when Tesseract is configured. |
| Template catalog | Reads built-in template metadata from `references/templates.json`. |
| Runtime compatibility | Designed for Claude/ClawHub, Codex, and OpenClaw with one source folder. |

## Stable CLI

```powershell
python scripts/psd_batch.py diagnose --json
python scripts/psd_batch.py analyze <template.psd|template-id> [--data data.xlsx] [--sheet 0] [--json-out report.json]
python scripts/psd_batch.py preview <template.psd|template-id> --data data.xlsx --out out --rows 3 [--color R G B]
python scripts/psd_batch.py export <template.psd|template-id> --data data.xlsx --out out [--dpi 300] [--font font.ttf] [--color R G B] [--verify-samples 3] [--strict]
python scripts/psd_batch.py verify out [--samples 3] [--color R G B] [--ocr]
python scripts/psd_batch.py templates list
python scripts/psd_batch.py templates info <morning|tech|doodle>
```

Exit codes:

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | Input or argument error |
| 2 | Missing dependency or incompatible PSD |
| 3 | Export or verification failure |
| 4 | Unexpected failure |

## Legacy Scripts

These remain available for backward compatibility:

```powershell
python scripts/batch_from_excel.py "data.xlsx" "template.psd" "out"
python scripts/ai_designer.py --list
python scripts/color_tools.py --recommend ticket
python scripts/smart_layout.py --preset certificate
python scripts/render_psd_batch.py "psd_dir" "png_dir"
```

Use `scripts/psd_batch.py` for new work because it provides structured JSON reports and stable exit codes.

## Install

```powershell
pip install -r requirements.txt
```

Optional test dependencies:

```powershell
pip install -r requirements-dev.txt
```

Fonts can be placed in `fonts/`; the renderer also scans system font directories.

```powershell
python fonts/download_fonts.py --list
```

## Verification

```powershell
python -m compileall -q scripts
python -m pytest -q
python scripts/psd_batch.py diagnose --json
```

OpenClaw local install:

```powershell
openclaw skills install "C:\Users\26240\.claude\skills\psd-batch-export" --global --force
openclaw skills check --json
```

ClawHub publishing is intentionally manual. See `references/runtime-compat.md`.
