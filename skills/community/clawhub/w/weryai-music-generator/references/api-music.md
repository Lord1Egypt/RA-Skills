# Music API Reference

Use this reference when you need the exact WeryAI music request and response rules without bloating `SKILL.md`.

## Endpoint

- `POST /v1/generation/music/generate`

This endpoint submits an asynchronous music generation task and returns a task ID.

## Required Rules

- `type` is required
- At least one of `description` or `styles` must be present
- `type` must be one of:
  - `VOCAL_SONG`
  - `ONLY_MUSIC`

## CLI Defaults

- Default `type`: `VOCAL_SONG`
- Default timbre in `VOCAL_SONG`: `male` (`gender: m`)
- Default `genre`, `emotion`, and `instrument`: unset unless the user or agent explicitly adds them

The CLI also accepts higher-level helper fields and normalizes them before submission:

- `genre`
- `emotion`
- `instrument`
- `timbre`

These are converted into the API's `styles` and `gender` fields.

## Request Fields

| Field | Type | Notes |
| --- | --- | --- |
| `type` | string | Required. `VOCAL_SONG` or `ONLY_MUSIC` |
| `description` | string | Optional only if `styles` exists. Main generation prompt |
| `lyrics` | string | Optional for `VOCAL_SONG`. Omit for `ONLY_MUSIC` |
| `reference_audio` | string | Optional public audio URL used for style guidance |
| `audio_name` | string | Optional in the upstream API. This CLI requires it when `reference_audio` is present |
| `gender` | string | Optional. `m` or `f`. Use only with `VOCAL_SONG` |
| `styles` | object | Optional only if `description` exists. Key-value map of style enums to prompt text |
| `webhook_url` | string | Optional callback URL |
| `caller_id` | integer | Optional business association ID |

## Style Keys

### Genre

- `POP`
- `ROCK`
- `RAP`
- `ELECTRONIC`
- `RNB`
- `JAZZ`
- `FOLK`
- `CLASSIC`
- `WORLD`

### Emotion

- `HAPPY`
- `RELAXED`
- `WARM`
- `ROMANTIC`
- `TOUCHING`
- `SAD`
- `LONELY`
- `DEPRESSED`
- `TENSE`
- `EXCITED`
- `EPIC`
- `MYSTERIOUS`

### Instrument

- `PIANO`
- `GUITAR`
- `BASS`
- `DRUMS`
- `STRINGS`
- `WIND`
- `SYNTHESIZER`
- `ELECTRONIC_SOUND`
- `FOLK_INSTRUMENT`
- `MIXED_ORCHESTRATION`

## User-facing Option Aliases

These are useful when the skill collects options in a more UI-like format:

| Helper field | Accepted examples | Normalized API field |
| --- | --- | --- |
| `genre` | `POP`, `流行`, `ROCK`, `摇滚` | `styles` |
| `emotion` | `HAPPY`, `开心`, `WARM`, `温暖` | `styles` |
| `instrument` | `PIANO`, `钢琴`, `STRINGS`, `弦乐` | `styles` |
| `timbre` | `male`, `female`, `男声`, `女声` | `gender` |

## Response Fields

The submit endpoint returns a standard envelope plus a task ID:

```json
{
  "status": 0,
  "desc": "success",
  "message": "success",
  "data": {
    "task_id": "task_abc123",
    "task_status": "WAITING"
  }
}
```

When polling task status, relevant fields include:

| Field | Meaning |
| --- | --- |
| `task_id` | Unique task ID |
| `task_status` | `WAITING`, `PROCESSING`, `SUCCEED`, or `FAILED` |
| `audios` | Result audio URLs |
| `lyrics` | Generated lyrics for vocal songs |
| `cover_url` | Generated cover image URL |
| `msg` | Error message when the task fails |

## CLI-specific Validation Policy

The CLI intentionally adds a few stricter rules to reduce ambiguous or hard-to-debug requests:

- Reject `lyrics` when `type` is `ONLY_MUSIC`
- Reject `gender` when `type` is `ONLY_MUSIC`
- Require public `http` or `https` URLs for `reference_audio` and `webhook_url`
- Require `audio_name` whenever `reference_audio` is provided

## Polling Behavior

- `submit` sends one request and returns immediately
- `wait` sends the same submit request, then polls `/v1/generation/<taskId>/status`
- `status` only polls the existing task and does not consume credits

## Re-run Semantics

- Re-running `submit` creates a new paid task
- Re-running `wait` also creates a new paid task before polling
- Re-running `status` is safe and idempotent for the same task ID
