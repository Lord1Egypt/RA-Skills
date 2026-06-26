# AGENTS — Multi-tool project entry (Cursor, Claude Code, OpenClaw, Codex)

This file is the **canonical** agent instructions hub. Root stubs (`AGENTS.md`, `CLAUDE.md`) point here so IDEs and CLIs stay aligned.

## Repository contract

| Rule | Detail |
|------|--------|
| Docs & SQL | All `.md` and `.sql` live under **`/setup`** (see `setup/tools/check_structure.py`). Exceptions at repo root: `SKILL.md`, `AGENTS.md`, `CLAUDE.md` only. |
| Package | Importable code: `tai_alpha/`; thin CLIs: `scripts/`. |
| Persistence | Default SQLite: `tai_alpha_output/tai_alpha.db` or `TAI_ALPHA_DB_PATH`. |
| Python env | Prefer **conda** env **`llm_base`** for local runs (per project standards). |

## OpenClaw / marketplace skill

- **Skill manifest:** root [`SKILL.md`](../../../SKILL.md) — YAML frontmatter `name` + `description` (required for registries).
- **Mirror:** [`SKILL.md`](SKILL.md) in this folder (same content policy).
- **Install:** `pip install -e ".[dev]"` from repo root; entry points `tai-alpha-*` in `pyproject.toml`.
- **Do not** duplicate large upstream skills (e.g. full UZI YAML); link and attribute instead.

## Cursor

- **Project rules:** [`.cursor/rules/tai-alpha-stock.mdc`](../../../.cursor/rules/tai-alpha-stock.mdc) (`alwaysApply` conventions).
- **User flows:** [USERFLOW.md](../../USERFLOW.md), [AGENT_GUIDE.md](AGENT_GUIDE.md).

## Claude Code

- **Project file:** root [`CLAUDE.md`](../../../CLAUDE.md) (stub → this doc).
- Use this hub + [`AGENT_GUIDE.md`](AGENT_GUIDE.md) for orchestration, SQLite, personas.

## Core commands

```bash
pip install -e ".[dev]"
python scripts/analyze.py AAPL --no-report
pytest tests/unit tests/integration -v
python setup/tools/check_structure.py
```

## Doc map

| Topic | Path |
|-------|------|
| Index | [README.md](../../README.md) |
| Module layout | [MODULE_STRUCTURE.md](../../MODULE_STRUCTURE.md) |
| Personas / i18n | [../guides/PERSONA_ECOSYSTEM_GUIDE.md](../guides/PERSONA_ECOSYSTEM_GUIDE.md), [../guides/CHINESE_AUDIENCE_GUIDE.md](../guides/CHINESE_AUDIENCE_GUIDE.md) |
| Disclaimer | [../guides/DISCLAIMER_AND_LIMITATIONS.md](../guides/DISCLAIMER_AND_LIMITATIONS.md) |
| SQLite | [../database/SQLITE.md](../database/SQLITE.md) |

## Safety

- Production DB / RLS: do not overwrite without explicit approval.
- `.env` may exist but is gitignored; never commit secrets.
