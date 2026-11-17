# Interior Decoration Quantity Takeoff & Material Plan

> zhuangshi-suanliang (zhuangshi-suanliang) v0.9.36 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
Generates decoration budget quantities and material plans from room type, building notes, architectural/structural drawings, room decoration tables, practice tables and node details. It imports cad-file-reader length/area candidates as review inputs; method mapping, opening deductions, loss, material ledger and BOQ quantities are computed by this skill.

## When to use it
Use for solid/interior (decoration) takeoff and material planning such as gypsum, finishes, waterproofing, tiles and ceilings.

## Quick start
```bash
bash scripts/decor_qty.sh --input 明细表.csv --out-dir out
bash scripts/decor_qty.sh --input 快速房间表.xlsx --out-dir out --level 一层
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3.10+; optional cad-file-reader for measurement candidates; openpyxl for XLSX output.

## Privacy
Local only; documents are never uploaded.

## Boundaries / limitations
Budget/material-plan estimates; contracts, local rules, enterprise quotas and current standards take precedence.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
