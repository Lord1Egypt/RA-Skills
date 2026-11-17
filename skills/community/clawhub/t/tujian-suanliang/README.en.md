# Civil/Structural Quantity Takeoff (Tujian)

> tujian-suanliang (tujian-suanliang) v0.9.44 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
Produces fast concrete volume and rebar estimate bands from structural drawings, with standard size/grades checks and norm/figure metadata. Reports per floor or pour zone (including post-cast first-pour vs closed-band accounting) for material planning.

## When to use it
Use for civil/structural rough takeoff and material planning from DWG/DXF. It now owns the former cad-file-reader beam/slab/column/wall, staircase, opening, precast, structural-model and concrete-ledger pipelines.

## Quick start
```bash
bash scripts/cad_quantity.sh --scan scan.json --format all --out out
python3 scripts/run_qty.sh <drawing.dwg>
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3.10+; requires cad-file-reader base (auto-installed and checksum-verified); openpyxl for spreadsheets.

## Privacy
Local only; drawing bytes never leave the machine.

## Boundaries / limitations
Estimate bands with review flags, not a replacement for design review, settlement, or formal pricing.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
