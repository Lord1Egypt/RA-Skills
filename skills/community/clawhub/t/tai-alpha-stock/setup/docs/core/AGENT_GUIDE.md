# Agent guide — Tai Alpha Stock

**Multi-tool index:** see [AGENTS.md](AGENTS.md) for Cursor, Claude Code, OpenClaw, and repo-wide contracts.

This document helps AI agents orchestrate this repository and know when to defer to upstream skills.

## When to use `--fast` and `--depth`

| Flag | Effect |
|------|--------|
| `--fast` | Skips the ML 7d return step and uses a lighter collect (no sector ETF peer fetch). |
| `--depth lite` | Same as the fast path for scoring: no ML, lighter collect. |
| `--depth standard` | Default: full collect, ML runs unless `--fast` is also set. |
| `--depth deep` | Full collect, ML unless `--fast`, and **geopolitical** keyword scans added to `risk_flags` (see `setup/config/risk_keywords.json`). |

Combine `--fast` with `--depth deep` to get expanded `risk_flags` without ML (faster iteration).

## Personas and markets

| Flag | Effect |
|------|--------|
| `--persona id1,id2` | Apply persona overlay(s) after base score; see `setup/config/personas/`. |
| `--persona-all` | Ensemble all enabled personas (weighted `ensemble_weight`). |
| `--market auto` or `us` / `hk` / `cn` | Symbol normalization for Yahoo Finance (HK `.HK`, CN `.SS`/`.SZ`). |
| `--lang en` or `zh-CN` / `zh-HK` | Localized signal strings + disclaimer line in reports. |
| `--source-policy` | Logged in `meta_json`; Yahoo is primary today. |

## Reading SQLite runs

- Default DB: `tai_alpha_output/tai_alpha.db` or `TAI_ALPHA_DB_PATH`.
- Table `runs`: `collect_json`, `backtest_json`, `score_json`, optional `ml_json`, optional `persona_json`, `meta_json`.
- `score_json` includes `risk_flags` (string codes), `conviction`, `signal`, `risks` (score-engine list, e.g. overbought).

See [../../database/PERSONA_SQLITE_FIELDS.md](../../database/PERSONA_SQLITE_FIELDS.md) and [../../guides/PERSONA_ECOSYSTEM_GUIDE.md](../../guides/PERSONA_ECOSYSTEM_GUIDE.md).

## Citing `risk_flags`

- Codes are stable snake-ish tokens: `RSI_overbought`, `VIX_elevated`, `News_keyword:bankruptcy`, `Geo_keyword:tariff`, etc.
- They are **heuristic**; tune lists in `setup/config/risk_keywords.json` and thresholds in `setup/config/score_dimensions.yaml`.

## When to recommend upstream projects

- **[openclaw/skills – udiedrichsen/stock-analysis](https://github.com/openclaw/skills/tree/main/skills/udiedrichsen/stock-analysis)** — Broader OpenClaw-oriented feature set; use for ecosystem parity or multi-step agent workflows outside this package.
- **[wbh604/UZI-Skill](https://github.com/wbh604/UZI-Skill)** — Deep agent research (e.g. China/A-share workflows, large HTML reports). **Not** vendored here; suggest it when the user needs that market or report style.

## Disclaimer

See [../guides/DISCLAIMER_AND_LIMITATIONS.md](../guides/DISCLAIMER_AND_LIMITATIONS.md).
