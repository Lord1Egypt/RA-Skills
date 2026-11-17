# Landscape Quantity Takeoff (Plants & Pavement)

> yuanlin-suanliang (yuanlin-suanliang) v0.4.40 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
Based on cad-file-reader landscape candidates, classifies plants by Chinese/English legend, parses plant-table design baselines, computes pavement area by closed regions, and outputs a budget draft and material-plan draft with usage boundaries, confidence tiers (P0-P3) and evidence coordinates.

## When to use it
Use for landscape/trees/paving rough takeoff from landscape DWG/DXF or landscape-geometry JSON.

## Quick start
```bash
bash scripts/yuanlin_qty.sh --landscape landscape.json --out-dir out
bash scripts/yuanlin_qty.sh --scan scan.json --plant-library 本地库.csv --out-dir out
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3.8+; requires cad-file-reader landscape candidates; optional local plant-name reference libraries (JSON/CSV/XLSX).

## Privacy
Local only; drawing bytes never leave the machine.

## Boundaries / limitations
Budget candidates only, not a replacement for design review, setting-out, tree counting, completed-amount measurement, reconciliation, settlement or formal quotation.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
