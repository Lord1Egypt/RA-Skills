# Config

## groups.json

Example:

```json
{
  "groups": [
    {
      "name": "Core突击龙虾🦞",
      "enabled": true,
      "topics": ["AI", "创业", "商业认知", "社群运营"],
      "schedule": {
        "morning_question": "10:00",
        "afternoon_followup": "15:30",
        "evening_case": "20:30"
      }
    }
  ]
}
```

## Content pools

Stored under `assets/content/`:
- `questions.json`
- `followups.json`
- `cases.json`

Each item should include at least:
- `id`
- `topic`
- `text`

Cases may also include `title`.
