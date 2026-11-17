# Sima Guang Perspective / Cognitive Advisory

> simaguang-perspective (simaguang-perspective) v0.4.7 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
A cognitive framework distilled from Sima Guang’s reasoning that helps analyze governance, people, decisions, history, strategy, psychology, law, investment, investigation, and high-productivity writing across scales. It is a perspective implant, not impersonation.

## When to use it
Use when you want historical/traditional cognitive structure applied to a management, decision, investment, or writing analysis.

## Quick start
```bash
bash scripts/generate_work_product.sh --type project-plan --output plan.md
bash scripts/prepare_input.sh --input input.txt --output prepared.md
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3.8+ standard library; optional Wikimedia fetch script for public celebrity images.

## Privacy
Local; no data is uploaded unless you run the documented fetch-celebrity network helper yourself.

## Boundaries / limitations
Provides perspective and structure; it does not substitute professional legal, medical, or business advice.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
