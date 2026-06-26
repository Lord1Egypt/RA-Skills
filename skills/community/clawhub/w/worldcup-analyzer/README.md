# worldcup-analyzer

[![ClawHub](https://img.shields.io/badge/ClawHub-worldcup--analyzer-blue)](https://clawhub.ai/datatrevor/worldcup-analyzer)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![License](https://img.shields.io/badge/license-MIT--0-lightgrey)

Mira/Claude-Code Skill for predicting outcomes of national-team football
matches using a remote machine learning API at
`https://www.jiajielitong.com`. Defaults to the 2026 FIFA World Cup;
`england-premium` is reserved for upcoming API support. Statistical
analysis only — **not** betting advice.

## Layout

```
worldcup-analyzer/
├── SKILL.md                  # Skill manifest + agent instructions
├── README.md                 # This file (human-facing)
├── skill-card.md             # ClawHub marketplace card
├── requirements.txt          # Python deps (httpx preferred, requests fallback)
├── scripts/
│   └── wc_client.py          # HTTP client, cache, formatter, validator
├── references/
│   ├── api.md                # Endpoint reference (/teams/, /predict/)
│   ├── team_names.md         # Canonical 48-team list + alias map
│   ├── compliance.md         # HK Cap. 148 refusal templates and rules
│   └── schedule.md           # World Cup schedule/result lookup behavior
└── evals/
    ├── evals.json            # Eval cases
    └── run_evals.py          # Local runner — hits the live API
```

## Quick start

```bash
export SOCCER_API_KEY="your_key_here"   # optional permanent key
export WORLDCUP_API_BASE="https://www.jiajielitong.com"   # optional; this is the default
pip install -r requirements.txt
python3 evals/run_evals.py
```

No permanent key? Agent Skill users can still try the prediction endpoint:
the client automatically requests a 24-hour Agent temporary key from
`POST /matches/agent/temp-key`. Each source IP can request one temp key per
UTC day, with 2 free prediction credits. Repeating the exact same home/away
fixture within 3 days does not consume additional credits. When the temp-key
limit is reached, register a permanent API key at `https://www.jiajielitong.com`.

## What the client gives you

| Function | Purpose |
|---|---|
| `request_agent_temp_key()` | Requests a 24-hour Agent temporary key with 2 free prediction credits per day; cached in process only. |
| `predict_match(home, away, competition="worldcup")` | Outcome + expected goal diff. Uses `SOCCER_API_KEY` when set, otherwise an Agent temporary key. 6h in-memory TTL cache. |
| `list_teams(competition="worldcup")` | Canonical team list from `GET /matches/teams/`. 12h TTL cache. |
| `validate_team(name, competition)` | `(True, canonical)` or `(False, fuzzy_suggestion)`. Cheap — uses cached team list. |
| `format_prediction(data)` | Margin-aware renderer with mandatory compliance disclaimer. Flags near-draws when `|win_goals| < 0.20`. |
| `format_response(body)` | Appends disclaimer to any custom string. |
| `format_prediction(data, language="zh")` | Optional Chinese rendering for Chinese user prompts. |
| `format_response(body, language="zh")` | Optional Chinese disclaimer. |
| `first_use_message(language="zh")` | First-use onboarding text that explains the 2-per-day free temp key, repeat-query credits behavior, and model-data summary. |
| `quota_warning(data, language="zh")` | Returns a short heads-up at ≥ 80% quota; points temp-key/plan-exhausted users to `https://www.jiajielitong.com` for a permanent key; `None` on unlimited (`limit == -1`) tier. |
| `canonicalize_team_name(name)` | Alias map only (no API call). |
| `cache_clear()` | Reset both predict + teams caches. |

Note: the provider does not count additional credits when the exact same
fixture is queried again with the same home/away order within 3 days.
Reversing home and away is a different fixture.

## Demo

ClawHub page: `https://clawhub.ai/datatrevor/worldcup-analyzer`

Chinese prompt:

```text
用户：巴西主场对摩洛哥，世界杯谁更有可能赢？
```

Example output:

```text
**Brazil vs Morocco**（模型预测）

- 从 Brazil 视角看的赛果：Win
- 预期净胜球（主队 - 客队）：+0.57
- 解读：模型偏向主场的 Brazil
- 赛程：若赛程页已公布，将附上开赛时间；若比赛已结束，将附上最终赛果

仅供统计参考，不构成投注建议。18+。
```

English prompt:

```text
User: Predict Brazil vs Morocco in the World Cup.
```

Example output:

```text
**Brazil vs Morocco** (modeled projection)

- Outcome from Brazil's POV: Win
- Expected goal difference (home - away): +0.57
- Interpretation: model favors Brazil at home
- Schedule: kickoff time is included when available; final result is shown for completed fixtures

Statistical reference only. Not betting advice. 18+.
```

## Compliance hard constraints

- No phrases like `recommended bet`, `sure win`, `lock`, `tips`, `稳赢`, `推荐`.
- Disclaimer is automatic and must not be stripped.
- Refuse betting picks, stake sizing, bookmaker odds, anyone identifying as under 18.

## Schedule/result behavior

After a World Cup prediction, check
`https://en.wikipedia.org/wiki/2026_FIFA_World_Cup` for the fixture. If the
page is unavailable or does not show the fixture, fall back to
`https://baike.baidu.com/en/item/2026%20FIFA%20World%20Cup/1497370#9`.
If the match is upcoming, include kickoff time. If it has finished, include
the final result; when the model's win/draw/loss differs from the actual
result, thank the user and say the result has been used to retrain the
backend model.

See `references/compliance.md` for full text + refusal templates.
