# Study Buddy - Data Format

## Deck Schema

```json
{
  "name": "Biology Exam",
  "cards": [
    {
      "id": 1,
      "q": "What is mitosis?",
      "a": "Cell division producing two identical daughter cells",
      "interval": 7,
      "ease": 2.6,
      "repetitions": 3,
      "next_review": "2026-03-26T10:00:00",
      "created_at": "2026-03-19T10:00:00"
    }
  ],
  "next_id": 2,
  "created_at": "2026-03-19T10:00:00",
  "updated_at": "2026-03-19T10:00:00"
}
```

## Card Fields

| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique card ID within deck |
| q | string | Question text |
| a | string | Answer text |
| interval | int | Days until next review |
| ease | float | SM-2 ease factor (1.3-3.0, default 2.5) |
| repetitions | int | Consecutive correct answers |
| next_review | ISO datetime | When the card is next due |
| created_at | ISO datetime | When the card was created |

## SM-2 Algorithm

Interval progression for consecutive correct answers:
- Rep 1: 1 day
- Rep 2: 3 days
- Rep 3+: previous_interval * ease_factor

Ease adjustments:
- correct: ease + 0.1
- partial: ease - 0.15
- missed: ease - 0.2, reset to rep 0, interval 1 day

Minimum ease: 1.3

## Storage Location

`~/.openclaw/study-buddy/decks/<deck_name>.json`

Deck names are normalized: lowercased, spaces replaced with underscores.
