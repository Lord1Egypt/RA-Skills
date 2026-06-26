---
name: vocabulary-anti-forgetting
version: 3.0.0
---

# Vocabulary Anti-Forgetting Skill

Use **spaced repetition** (based on the Ebbinghaus forgetting curve) to help the user memorize English phrases from the vocabulary bank.

## Trigger

Activate this skill when the user says any of: `复习`, `单词复习`, `review vocabulary`, `review words`.

## Files

| File | Purpose |
|---|---|
| `vocabulary-anti-forgetting/asset/vocabulary_bank.md` | Master list of 2087 English phrases with Chinese translations |
| `<workspace>/memory/review_log.md` | Tracks every word's review history, level, and next review date (stored in the workspace memory folder, outside skill folder to survive upgrades) |
| `vocabulary-anti-forgetting/review.py` | CLI script for non-interactive spaced-repetition review sessions |

## Spaced Repetition Algorithm

Each word has a **level** that determines when it should be reviewed next:

| Level | Interval | Status |
|---|---|---|
| 0 | New word, never reviewed | new |
| 1 | Review again in **1 day** | learning |
| 2 | Review again in **2 days** | learning |
| 3 | Review again in **4 days** | reviewing |
| 4 | Review again in **7 days** | reviewing |
| 5 | Review again in **15 days** | reviewing |
| 6 | Review again in **30 days** | mastered |
| 7 | Review again in **60 days** | mastered |

Each time a word is shown (studied), it counts as a correct review: level + 1, schedule next review per the interval table.

## Daily Review Session Flow (10 words)

When triggered, run the review script directly:

```bash
python vocabulary-anti-forgetting/review.py
```

This handles everything in one step: reads state, selects 10 words (due reviews first, then new words), displays them all at once, updates `review_log.md` with incremented levels and next review dates, and prints a session summary.

For custom word count: `python vocabulary-anti-forgetting/review.py --count 5`

Show the script output to the user as-is.

## review_log.md Format

The file uses a markdown table with these columns:

```markdown
| id | vocabulary | level | review_count | last_reviewed | next_review_date |
```

- `id`: matches the # column in `vocabulary_bank.md`
- `vocabulary`: the English word/phrase
- `level`: current spaced repetition level (0-7)
- `review_count`: total number of times reviewed
- `last_reviewed`: YYYY-MM-DD of last review
- `next_review_date`: YYYY-MM-DD when this word is next due

The file header also stores:
- `total_sessions`: running count of completed sessions
- `last_session_date`: date of the most recent session

## Important Rules

- NEVER skip the update to `review_log.md` — this is the memory of the system.
- The review log lives at `<workspace>/memory/review_log.md` (the skill folder's parent `memory/` directory), NOT in the skill folder. The script resolves this path automatically.
- If the user only wants a partial session (e.g., 5 words), that's fine — update only those words.
- If the user asks for stats (e.g., "复习统计"), read `review_log.md` and report: total words reviewed, mastered count, learning count, upcoming due words.
- The user can also run `python vocabulary-anti-forgetting/review.py` for a non-interactive session, or `python vocabulary-anti-forgetting/review.py --stats` for stats.
