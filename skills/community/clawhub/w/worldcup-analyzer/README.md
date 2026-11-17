# worldcup-analyzer

[![ClawHub](https://img.shields.io/badge/ClawHub-worldcup--analyzer-blue)](https://clawhub.ai/datatrevor/worldcup-analyzer)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![License](https://img.shields.io/badge/license-MIT--0-lightgrey)

Mira/Claude-Code Skill for football match prediction using the remote
machine learning API at `https://www.jiajielitong.com`. The project keeps
the original `worldcup-analyzer` name for published-user continuity, but
the default experience is now **English Premier League first**. World Cup
national-team matchups remain supported.

Statistical analysis only. **Not betting advice.**

## Layout

```text
worldcup-analyzer/
├── SKILL.md
├── README.md
├── skill-card.md
├── requirements.txt
├── scripts/
│   └── wc_client.py
├── references/
│   ├── api.md
│   ├── team_names.md
│   ├── compliance.md
│   └── schedule.md
└── evals/
    ├── evals.json
    └── run_evals.py
```

## Quick Start

```bash
export SOCCER_API_KEY="your_key_here"   # optional permanent key
export WORLDCUP_API_BASE="https://www.jiajielitong.com"   # optional default
pip install -r requirements.txt
python3 evals/run_evals.py
```

No permanent key? Agent Skill users can still try the simulation API. The
client automatically requests a 24-hour temporary key from
`POST /matches/agent/temp-key`. It includes 2 free simulation queries per
day. Repeating the exact same home/away fixture within 3 days does not
consume additional credits. When the temp-key limit is reached, register or
renew a permanent API key at `https://www.jiajielitong.com`.

## Client Helpers

| Function | Purpose |
|---|---|
| `request_agent_temp_key()` | Requests a 24-hour Agent temporary key; cached in process only. |
| `simulate_epl_match(home, away, match_date=None, season="2026-27")` | EPL outcome + expected goal diff via `/matches/epl/simulate/`. |
| `list_epl_schedule()` | EPL schedule payload via `/matches/epl/schedule/`. |
| `list_epl_teams()` | EPL team names inferred from the schedule payload. |
| `predict_match(home, away, competition="epl")` | Compatibility wrapper. Defaults to EPL; pass `"worldcup"` for national-team World Cup matchups. |
| `list_teams(competition="epl")` | EPL teams by default; World Cup national teams when `competition="worldcup"`. |
| `validate_team(name, competition="epl")` | `(True, canonical)` or `(False, fuzzy_suggestion)`. |
| `format_prediction(data, language="en")` | Margin-aware renderer with mandatory disclaimer. Flags near-draws when `|win_goals| < 0.20`. |
| `first_use_message(language="zh")` | First-use onboarding text with free-trial, repeat-credit, model-data, and API-key guidance. |
| `quota_warning(data, language="zh")` | Warns near/at finite quota limits and points users to `https://www.jiajielitong.com`. |
| `cache_clear()` | Resets process-local cache. |

## Demo

ClawHub page: `https://clawhub.ai/datatrevor/worldcup-analyzer`

English EPL prompt:

```text
User: Predict Arsenal vs Chelsea in the Premier League.
```

Example output:

```text
**Arsenal vs Chelsea** (modeled projection)

- Outcome from Arsenal's POV: Win
- Expected goal difference (home - away): +0.18
- Interpretation: model projects a near-draw; marginal lean toward Arsenal
- Schedule: kickoff time is included when available; final result is shown for completed fixtures

Statistical reference only. Not betting advice. 18+.
```

Chinese EPL prompt:

```text
用户：英超曼城主场对阿森纳，谁更占优？
```

Example output:

```text
**Man City vs Arsenal**（模型预测）

- 从 Man City 视角看的赛果：Win
- 预期净胜球（主队 - 客队）：+0.21
- 解读：模型偏向主场的 Man City
- 赛程：若赛程接口已公布，将附上开赛时间；若比赛已结束，将附上最终赛果

仅供统计参考，不构成投注建议。18+。
```

World Cup compatibility prompt:

```text
用户：巴西主场对摩洛哥，世界杯谁更有可能赢？
```

World Cup fixtures still use Wikipedia first and Baidu Baike as fallback
for kickoff/final-result context.

## Compliance

- No phrases like `recommended bet`, `sure win`, `lock`, `tips`, `稳赢`, `推荐`.
- Disclaimer is automatic and must not be stripped.
- Refuse betting picks, stake sizing, bookmaker odds, and under-18 use.

See `references/compliance.md` for full text and refusal templates.

## Changelog

### 1.1.1

Republished EPL-first version to refresh the ClawHub latest tag and update
the marketplace listing to the current EPL-first description.

### 1.1.0

English: Added EPL-first support through `/matches/epl/simulate/` and
`/matches/epl/schedule/`, while preserving World Cup national-team support
under the existing Skill name and repository. Updated onboarding,
temporary-key credit messaging, schedule handling, and marketplace copy.

中文：新增英超优先支持，调用 `/matches/epl/simulate/` 做比赛预测，并通过
`/matches/epl/schedule/` 获取赛程上下文；同时保留世界杯国家队预测能力，沿用
现有 Skill 名称和仓库，避免用户重新认识一个新项目。本版本同步强化首次使用提示、
临时 key 免费额度说明、3 天内重复查询不扣 credits 的提示，以及发布页文案。

### 1.0.3

English: World Cup-focused prediction flow with bilingual formatting,
near-draw handling at `|win_goals| < 0.20`, automatic Agent temporary keys,
and Wikipedia/Baidu schedule fallback.

中文：以世界杯预测为主，支持中英文输出、`|win_goals| < 0.20` 的近似平局展示、
Agent 临时 key 自动申请，以及 Wikipedia/Baidu 赛程降级查询。
