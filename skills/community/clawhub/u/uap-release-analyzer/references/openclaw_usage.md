# OpenClaw Usage Notes

Default ClawHub install command:

```bash
clawhub --workdir ~/.openclaw/workspace --dir skills install uap-release-analyzer
```

Default installed path:

```text
~/.openclaw/workspace/skills/uap-release-analyzer/
```

Run the full pipeline:

```bash
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/run_all.py /path/to/release_root
```

Expected outputs under `/path/to/release_root`:

- `inventory.csv`
- `text/*.txt`
- `analytics/top_terms.csv`
- `analytics/terms_by_agency.csv`
- `analytics/entities.json`
- `analytics/per_file_digest.csv`
- `analytics/cross_doc.json`
- `REPORT.md`

Dependencies:

```bash
python3 -m pip install pdfplumber pypdf
```

If many PDFs are scanned images with no text layer, this skill intentionally reports them as OCR-needed instead of running long OCR automatically. Use an OCR workflow only as a follow-up when the user explicitly asks for it.
