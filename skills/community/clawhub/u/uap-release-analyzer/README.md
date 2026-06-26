# uap-release-analyzer

An OpenClaw-compatible skill adapted from a Claude Code / Claude.ai / Hermes skill that turns a folder of declassified UAP/UFO documents — war.gov "PURSUE" releases, FBI Vault tranches, NARA boxes, AARO publications — into a structured analytic report.

## What it does

Run it against a release directory, for example `~/Documents/UFO/release_01/`, and it produces:

- `inventory.csv` — one row per file: agency inferred from filename prefix, document type, page count, and size.
- `text/*.txt` — extracted text via pdfplumber, with empty files retained to flag scanned PDFs that need OCR.
- `analytics/`
  - `top_terms.csv`, `terms_by_agency.csv` — token frequencies.
  - `entities.json` — locations, agencies, phenomena vocabulary, year clusters, names appearing in 5+ files.
  - `per_file_digest.csv` — top terms / locations / redactions / short summary per file.
  - `cross_doc.json` — redaction patterns, agency totals, scanned-vs-text split.
- `REPORT.md` — standardized 11-section human-readable analytic writeup.

The scripts are idempotent and incremental: re-running on the same folder skips work that is already done where possible.

## Install from ClawHub / OpenClaw

```bash
clawhub --workdir ~/.openclaw/workspace --dir skills install uap-release-analyzer
```

Then load or invoke the skill in OpenClaw when analyzing a release folder. The default installed path is usually:

```text
~/.openclaw/workspace/skills/uap-release-analyzer/
```

## Python dependencies

```bash
python3 -m pip install -r ~/.openclaw/workspace/skills/uap-release-analyzer/requirements.txt
```

Equivalent direct install:

```bash
python3 -m pip install pdfplumber pypdf
```

## Usage

```bash
# One-shot: full pipeline
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/run_all.py ~/Documents/UFO/release_01/

# Or step-by-step
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/inventory.py    ~/Documents/UFO/release_01/
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/extract_text.py ~/Documents/UFO/release_01/
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/extract_text.py ~/Documents/UFO/release_01/ 0 25
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/analyze.py      ~/Documents/UFO/release_01/
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/build_report.py ~/Documents/UFO/release_01/
```

If your OpenClaw skills directory is customized, run the same scripts from that installed skill directory.

## Layout

```text
uap-release-analyzer/
├── SKILL.md
├── README.md
├── LICENSE.txt
├── ARTICLE.md
├── package.json
├── clawhub.json
├── requirements.txt
├── scripts/
│   ├── inventory.py
│   ├── extract_text.py
│   ├── analyze.py
│   ├── build_report.py
│   └── run_all.py
├── references/
│   ├── agency_vocab.md
│   ├── foia_codes.md
│   ├── openclaw_usage.md
│   └── war_gov_quirks.md
└── evals/evals.json
```

## Example dataset

The May 2026 war.gov "PURSUE" release this skill was tuned against is mirrored at `ckpxgfnksd-max/uap-release-01` on GitHub, using Git LFS.

```bash
git lfs install
git clone https://github.com/ckpxgfnksd-max/uap-release-01.git ~/Documents/UFO/release_01
python3 ~/.openclaw/workspace/skills/uap-release-analyzer/scripts/run_all.py ~/Documents/UFO/release_01
```

Video is not mirrored. For video material, use the source page at https://www.war.gov/UFO/ when available.

## Honest caveats

- Entity extraction is keyword-list + regex, not full NER. Year mentions are not necessarily incident dates.
- Scanned PDFs with no text layer produce 0-character `.txt` files by design. The analyzer reports them as OCR-needed instead of running multi-hour OCR automatically.
- The agency vocabulary is tuned to the May 2026 war.gov tranche. New filename prefixes should be added to `references/agency_vocab.md` and the `PREFIX_RULES` in `scripts/inventory.py` and `scripts/analyze.py`.

## License

MIT. See `LICENSE.txt`.
