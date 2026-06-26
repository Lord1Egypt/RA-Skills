---
name: psd-batch-export
description: Production PSD batch workflow for analyzing PSD text layers, mapping Excel/CSV data to editable layers, previewing, exporting editable PSD plus PNG batches, validating results, checking fonts/OCR dependencies, and using built-in PSD templates for tickets, certificates, invitations, badges, posters, daily cards, and recruitment assets. Use whenever the user mentions PSD, Photoshop templates, layer text replacement, batch image generation, Excel-driven design output, PSD analysis, print-ready PNG export, or OpenClaw/Claude/Codex skill packaging for PSD automation.
allowed-tools: [Read, Write, Edit, Bash]
---

# PSD Batch Export Skill

Use this skill for production PSD batch generation. Resolve all paths relative to the directory containing this `SKILL.md`; do not rely on machine-specific absolute paths.

## Preferred Entry Point

Use the unified CLI first:

```powershell
python scripts/psd_batch.py diagnose --json
python scripts/psd_batch.py analyze "template.psd" --data "data.xlsx" --json-out report.json
python scripts/psd_batch.py preview "template.psd" --data "data.xlsx" --out "out" --rows 3
python scripts/psd_batch.py export "template.psd" --data "data.xlsx" --out "out" --dpi 300 --verify-samples 3
python scripts/psd_batch.py verify "out" --samples 3
python scripts/psd_batch.py templates list
python scripts/psd_batch.py templates info morning
```

Built-in template IDs can be used instead of PSD paths: `morning`, `tech`, `doodle`.

## Workflow

1. Run `diagnose --json` before production work to check required Python packages, fonts, templates, optional OCR, and optional LLM configuration.
2. Run `analyze` with the PSD and optional Excel/CSV data source. Review `layers`, `mapping`, `capacity_risks`, `fonts`, `warnings`, and `errors`.
3. Run `preview` before full export. Check `out/dryrun_preview/` and the JSON report.
4. Run `export` to generate `out/psd/`, `out/png/`, and `out/verify_report/report.json`. Replacement text keeps the original PSD text-layer color; pass `--color R G B` only when the user explicitly requests a uniform override.
5. Run `verify` again when outputs are moved or inspected separately.

Use `--strict` for production batches where low-confidence column matches, capacity overflow, or missing fonts should stop the run before export.

## Stable Report Contract

All primary commands support `--json` and `--json-out <path>`. The report includes:

- `status`: `ok` or `error`
- `inputs`: PSD, data, output, or template inputs
- `layers`: detected PSD text layer details
- `mapping`: data-column to layer mapping with confidence
- `capacity_risks`: text fields likely to truncate
- `fonts`: available fonts and matching recommendations
- `outputs`: generated directories, files, and verification report paths
- `warnings`: non-fatal production risks
- `errors`: fatal failures
- `runtime_sec`: elapsed seconds

Exit codes are stable: `0` success, `1` input error, `2` dependency/PSD compatibility error, `3` export or verification failure, `4` unexpected error.

## Legacy Entrypoints

Older scripts are kept for compatibility:

```powershell
python scripts/batch_from_excel.py "data.xlsx" "template.psd" "out" --dry-run
python scripts/batch_from_excel.py "data.xlsx" "template.psd" "out"
python scripts/ai_designer.py --list
python scripts/color_tools.py --recommend ticket
python scripts/smart_layout.py --preset certificate
python scripts/psd_text_editor.py "in.psd" "out.psd" "图层名=新文本"
```

Prefer `scripts/psd_batch.py` for new workflows because it provides structured reports and stable exit codes.

## References

- `references/templates.json`: built-in PSD template catalog and editable fields.
- `references/runtime-compat.md`: Claude, Codex, OpenClaw, and ClawHub install/validation commands.

## Verification

Run these before publishing or sharing the skill:

```powershell
python -m compileall -q scripts
python -m pytest -q
python scripts/psd_batch.py diagnose --json
```

For Codex validation on Windows, run with UTF-8 mode:

```powershell
$env:PYTHONUTF8='1'; python C:\Users\26240\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

For OpenClaw validation, install the local skill and then check visibility:

```powershell
openclaw skills install . --global --force
openclaw skills check --json
```

Do not publish to ClawHub unless the user explicitly asks for a release.
