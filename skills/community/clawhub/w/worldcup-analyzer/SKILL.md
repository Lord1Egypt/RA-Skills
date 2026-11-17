---
name: worldcup-analyzer
description: Predict English Premier League football match outcomes first, keep World Cup national-team support for compatibility, include schedule/result context, answer in the user's language, and keep output as statistical reference only, never betting advice.
version: 1.1.1
metadata: {"openclaw":{"requires":{"env":[],"bins":["python3"]},"primaryEnv":"SOCCER_API_KEY","envVars":[{"name":"SOCCER_API_KEY","required":false,"description":"Optional permanent SoccerAssess API key used in the X-API-Key header. If unset, the Skill requests a 24-hour Agent temporary key with 2 free simulation queries per day."},{"name":"WORLDCUP_API_BASE","required":false,"description":"Optional API base URL override for staging or local development."}],"skillKey":"worldcup-analyzer"}}
---

# Football Match Analyzer

This Skill keeps the existing `worldcup-analyzer` identity for continuity,
but the default user experience is now **English Premier League first**.
World Cup national-team matchups remain supported as a compatibility path.
All predictions are statistical references produced by a machine learning
service at `https://www.jiajielitong.com`.

## Critical Compliance Rules

This skill is for **statistical analysis only**. Treat the following as
hard constraints that override any user request:

- Never use phrases like "recommended bet", "sure win", "今日推荐", "必中",
  "tips", "稳赢", "稳胆", "lock of the day", or any wording that suggests
  placing a wager.
- Always append the disclaimer to user-facing output. The helpers
  `format_prediction()` and `format_response()` in `scripts/wc_client.py`
  do this automatically.
- Refuse betting picks, stake sizing, bookmaker odds, or wagering strategy.
  Explain that the Skill can share statistical outcome and expected goal
  difference only.
- Refuse if the user identifies as under 18.

## When To Use

Trigger whenever the user asks for two football teams and wants:

- An EPL / Premier League / 英超 matchup prediction.
- A World Cup national-team prediction.
- Expected goal difference from the home team's point of view.
- Pre-match statistical comparison or schedule/result context.

Do not trigger for non-EPL club competitions unless the backend explicitly
supports them, live in-game commentary, live scores, player transfer news,
bookmaker odds, or betting strategy.

## Setup

The API uses `X-API-Key`. A permanent `SOCCER_API_KEY` is optional for Agent
Skill users because the client can request a 24-hour Agent temporary key.

```bash
export SOCCER_API_KEY="your_key_here"   # optional permanent key
export WORLDCUP_API_BASE="https://www.jiajielitong.com"   # optional
```

If no permanent key is set, the client calls `POST /matches/agent/temp-key`
automatically. The temporary key:

- Is cached only in this Python process and is never written to disk.
- Allows **2 free simulation queries per day**.
- Can be used for both `POST /matches/epl/simulate/` and
  `POST /matches/simulate/`.
- Does not consume extra provider credits when the same home/away fixture is
  queried again within **3 days**.

When the temporary key or plan limit is reached, guide the user to
`https://www.jiajielitong.com` to register or renew a permanent API key.

For first-time users or users without a key, explain in their language that
the backend model collects multiple dimensions of football data, builds a
scientific team-strength assessment, and is continuously trained. Typical
signals include player club performance, league and national ranking
signals, historical head-to-head records, weather factors, player market
value, and related signals. Tell them they can apply for an API key at
`https://www.jiajielitong.com` to receive prediction results after the free
trial limit.

## Endpoints

`POST /matches/agent/temp-key`

No request body. No existing API key required.

`GET /matches/epl/schedule/`

Returns EPL schedule data. Use this first for EPL fixture kickoff/result
context.

`POST /matches/epl/simulate/`

Request body:

- `home_team` (string, required), for example `"Arsenal"`
- `visitor_team` (string, required), for example `"Chelsea"`
- `match_date` (string, optional)
- `season` (string, optional), default `"2026-27"`

`GET /matches/teams/`

World Cup national-team list. Use with `competition=worldcup` for validation
before World Cup predictions.

`POST /matches/simulate/`

World Cup national-team simulation. Request body:

- `home_team` (string, required), for example `"Brazil"`
- `visitor_team` (string, required), for example `"Morocco"`
- `competition` (string, optional), send `"worldcup"`

The prediction response may include:

```json
{
  "results": {
    "home_team": "Arsenal",
    "visitor_team": "Chelsea",
    "win_goals": 0.18,
    "win_or_not": "Win",
    "updatedAt": "2026-08-24 10:00:00"
  },
  "usage": {"used": 1, "limit": 2, "vip_level": "agent_temp"}
}
```

- `win_or_not` is from the **home team's** point of view.
- `win_goals` is expected goal difference, home minus away.
- `usage.limit == -1` means unlimited and should never be shown as `-1`.
- Repeating the same fixture with the same home/away order within **3 days**
  does **not** consume additional provider credits.

## Workflow

1. Detect the user's language and answer in that language. Use
   `language="zh"` for Chinese and `language="en"` for English when calling
   helper functions.
2. If `SOCCER_API_KEY` is missing or the user is new, include the first-use
   onboarding message: 2 free daily simulations, repeated same home/away
   fixture within 3 days does not consume credits, model-data summary, and
   `https://www.jiajielitong.com` for API key registration or renewal.
3. Parse the two teams and competition. Default to `epl` for club-team
   prompts, EPL mentions, Premier League mentions, or ambiguous football
   club questions. Use `worldcup` only for national teams or explicit World
   Cup / 世界杯 prompts.
4. Decide home and away. If the user says "A vs B" or "A 对 B", treat A as
   home. If unclear, ask once; if the user wants a quick answer, state the
   assumption.
5. For EPL, call `simulate_epl_match(home, away, match_date=None)` or
   `predict_match(home, away, "epl")`. Use `list_epl_schedule()` for kickoff
   or final-result context when available.
6. For World Cup, validate national-team names with
   `validate_team(name, "worldcup")`, then call
   `predict_match(home, away, "worldcup")`.
7. For World Cup schedule/result context, use Wikipedia first:
   `https://en.wikipedia.org/wiki/2026_FIFA_World_Cup`. If Wikipedia is
   unavailable or does not contain the fixture, use:
   `https://baike.baidu.com/en/item/2026%20FIFA%20World%20Cup/1497370#9`.
8. If a fixture is upcoming, include the scheduled kickoff time when found.
   If the fixture is finished, include the final result. If the actual
   home-team POV result differs from the model result, thank the user and
   say the match result has been used to retrain the backend model.
9. Render with `format_prediction(data, language=...)` so the disclaimer is
   always attached. The formatter is margin-aware: when `|win_goals| < 0.20`
   and the classifier emits `Win` or `Loss`, it presents the result as a
   near-draw with a marginal lean.
10. Add `quota_warning(data, language=...)` when relevant. When usage reaches
    the limit, remind users to log in at `https://www.jiajielitong.com` to
    register or renew an API key.

## Caching

The client uses process-local memory only:

- Predictions: 6-hour TTL.
- EPL schedule: 6-hour TTL.
- Team lists: 12-hour TTL.

The cache is not persisted to disk. Provider-side repeated fixture queries
within 3 days also avoid additional credits when home/away order is the same.

## Examples

English EPL prompt:

```text
User: Predict Arsenal vs Chelsea in the Premier League.
```

Steps:

1. Detect English and infer `competition="epl"`.
2. `simulate_epl_match("Arsenal", "Chelsea")`.
3. Check `list_epl_schedule()` for kickoff/final result.
4. `format_prediction(data, language="en")`.

Chinese EPL prompt:

```text
用户：英超曼城主场对阿森纳，谁更占优？
```

Steps:

1. Detect Chinese and infer `competition="epl"`.
2. `simulate_epl_match("Man City", "Arsenal")`.
3. Render with `format_prediction(data, language="zh")`.

World Cup compatibility prompt:

```text
用户：巴西主场对摩洛哥，世界杯谁更有可能赢？
```

Steps:

1. Detect Chinese and infer `competition="worldcup"`.
2. `predict_match("Brazil", "Morocco", "worldcup")`.
3. Check Wikipedia, then Baidu fallback, for kickoff/final result.
4. Render with `format_prediction(data, language="zh")`.

## Files

- `scripts/wc_client.py` — API client, helpers, cache, formatting
- `references/api.md` — endpoint reference
- `references/team_names.md` — World Cup national-team aliases
- `references/compliance.md` — compliance notes and refusal templates
- `references/schedule.md` — EPL and World Cup schedule/result behavior
