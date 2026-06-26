# Data Schema

## Raw export (`weread-raw.json`)

Top-level shape:

```json
{
  "exported_at": "2026-03-19T16:00:00Z",
  "source": "weread-local-cookie",
  "summary": {
    "total_books": 123,
    "finished_books": 40,
    "reading_books": 12,
    "unread_books": 71,
    "notebook_books": 18
  },
  "shelf_sync": { "...": "raw WeRead response" },
  "notebook": { "...": "raw WeRead response" },
  "book_info": {
    "book_id": { "...": "raw per-book info" }
  }
}
```

Notes:
- `shelf_sync` is intentionally close to the original response for debugging and future expansion.
- `book_info` is optional because fetching details for every book can be slow.

## Normalized export (`weread-normalized.json`)

Top-level shape:

```json
{
  "generated_at": "2026-03-19T16:05:00Z",
  "source_file": "data/weread-raw.json",
  "summary": {
    "total_books": 123,
    "status_counts": {
      "finished": 40,
      "reading": 12,
      "unread": 71
    },
    "top_categories": [
      {"name": "商业", "books": 10, "weighted_score": 421.0}
    ]
  },
  "profile_inputs": {
    "highest_engagement_books": [],
    "recent_books": [],
    "unfinished_books_with_momentum": []
  },
  "llm_hints": [],
  "books": []
}
```

## Engagement score
The normalizer computes a heuristic `engagement_score` in the range `0..100` from:
- reading progress
- finished state
- interaction count (notes/bookmarks/reviews)
- reading time
- recency

This score is not a universal truth; it is a ranking hint for recommendation reasoning.

## Status definition
- `finished`: `finishReading == 1`
- `reading`: not finished and `progress > 0`
- `unread`: not finished and no measurable progress
