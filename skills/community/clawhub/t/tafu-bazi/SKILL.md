---
name: tafu_bazi
description: Use Tafu's paid API for deterministic BaZi chart calculation, thematic readings, synastry, and soul-song generation when users ask for Chinese astrology analysis based on birth data.
homepage: https://tafu.me/developers
user-invocable: true
metadata: {"openclaw":{"emoji":"☯️","skillKey":"tafu_bazi","os":["darwin","linux"],"requires":{"bins":["sh","curl"],"env":["TAFU_API_KEY"]},"primaryEnv":"TAFU_API_KEY"}}
---

# Tafu BaZi

Use this skill when the user asks for:

- 八字 / BaZi 排盘
- 主题解读，例如性格底色、事业财富、感情、健康、年度运势
- 双人合盘 / compatibility / synastry
- 灵魂歌曲

Tafu is the source of truth for all chart math and paid analysis. Do not improvise the actual BaZi chart or paid reading if the API is available.

## Preconditions

- The host should inject `TAFU_API_KEY` from `skills.entries.tafu_bazi.apiKey`.
- Optional override: `skills.entries.tafu_bazi.env.TAFU_API_BASE_URL`.
- If the key is missing, stop and tell the user to create a key at `https://tafu.me/developers`, then configure `skills.entries.tafu_bazi.apiKey`.

Use `{baseDir}/scripts/tafu_api.sh` for every API call. It reads:

- `TAFU_API_KEY`
- `TAFU_API_BASE_URL` if present
- otherwise defaults to `https://api.tafu.me/api/v1`

If you need concrete payload examples, read `{baseDir}/references/examples.md`.

## Input Rules

- Collect the user's language and reply in that language.
- Ask for missing required birth fields before calling paid endpoints.
- For best accuracy, collect:
  - date
  - time
  - gender
  - birthplace or current city-level location
  - calendar type when the user gives a lunar date
- If the birth minute is unknown, ask once. If the user still does not know, call out the assumption before using `00`.
- If the user gives a lunar date and the month could be leap, use `GET /bazi/leap-month/:year` before confirming `isLeapMonth`.
- If the user gives a free-form location and it looks ambiguous, use `GET /bazi/coordinates?location=...` first.

## API Workflow

### 1. Deterministic charting

For raw chart calculation, call:

- `POST /bazi/calculate`

Use the normalized JSON payload expected by the API. Prefer these keys:

- `gender`
- `calendarType`
- `birthYear`
- `birthMonth`
- `birthDay`
- `birthHour`
- `birthMinute`
- `isLeapMonth`
- `location`

### 2. Paid thematic reading

For a single-person reading, call:

- `POST /reading`

Payload:

- `birthData`
- `theme`

Valid `theme` values:

- `life_color`
- `relationship`
- `career_wealth`
- `health`
- `life_lesson`
- `yearly_fortune`

### 3. Soul song

For soul-song generation, call:

- `POST /soul-song`

Payload:

- `birthData`

### 4. Synastry

For two-person compatibility, call:

- `POST /synastry`

Payload:

- `subjectA`
- `subjectB`

### 5. Polling async tasks

`/reading`, `/soul-song`, and `/synastry` may return an already completed result or an async task.

If the response includes a `result`, use it immediately.

If the response includes `taskId` and `status`:

1. Poll `GET /tasks/<taskId>`
2. Wait about 5 seconds between polls
3. Poll up to 12 times, or stop earlier if status becomes `completed` or `failed`
4. If it is still pending after the polling window, tell the user the task is still running and include the `taskId`

## Output Rules

- Preserve the API result as the factual source.
- You may add a short top summary, but do not discard or rewrite away important structured output.
- Surface `creditsUsed` and `creditsRemaining` when returned.
- If the API returns `viewUrl`, include it.
- On `402` or `INSUFFICIENT_CREDITS`, tell the user to recharge Credits at `https://tafu.me/developers/billing`.
- On `401` or `INVALID_API_KEY`, tell the user to rotate or reconfigure the API key.
- On input validation errors, ask for the missing or invalid field instead of guessing.
- If the API fails, do not fall back to a hallucinated BaZi reading.

## Execution Notes

- Keep secrets out of the chat transcript.
- Use temporary JSON files for complex payloads instead of long inline shell escaping.
- Only call paid endpoints after the user has clearly asked for that capability.
