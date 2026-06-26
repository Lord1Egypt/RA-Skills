# Vocabulary Anti-Forgetting

Spaced-repetition tool based on the Ebbinghaus forgetting curve. Picks 10 words daily from a 2087-word vocabulary bank, displays them for study, and schedules future reviews at increasing intervals.

## Quick Start

```bash
python vocabulary-anti-forgetting/review.py
```

## Usage

```bash
# Daily review (10 words)
python vocabulary-anti-forgetting/review.py

# Custom word count
python vocabulary-anti-forgetting/review.py --count 5

# View progress stats
python vocabulary-anti-forgetting/review.py --stats
```

## How It Works

Each word progresses through 8 levels with increasing review intervals:

| Level | Interval | Status |
|-------|----------|--------|
| 0 | New word | new |
| 1 | 1 day | learning |
| 2 | 2 days | learning |
| 3 | 4 days | reviewing |
| 4 | 7 days | reviewing |
| 5 | 15 days | reviewing |
| 6 | 30 days | mastered |
| 7 | 60 days | mastered |

Each session:
1. Selects words that are due for review (most overdue first)
2. Fills remaining slots with new words from the bank
3. Displays all words at once for study
4. Automatically advances each word's level and schedules the next review

## Files

| File | Description |
|------|-------------|
| `review.py` | Main CLI script (Python 3.9+, no external dependencies) |
| `asset/vocabulary_bank.md` | Master word list (2087 entries with Chinese translations) |
| `SKILL.md` | AI agent skill definition for OpenClaw |

## Data Storage

Review progress is stored at `<workspace>/memory/review_log.md`. The script resolves this by going up two levels from the skill folder (past the `skills/` directory) to the workspace root. This works across different OpenClaw workspace instances.

For example, if the skill is installed at:
```
/root/.openclaw/workspace/gaby-english-coach/skills/vocabulary-anti-forgetting/
```
Then the review log is at:
```
/root/.openclaw/workspace/gaby-english-coach/memory/review_log.md
```

This is outside the skill folder so upgrades won't overwrite your progress.

For local testing, override the path with an environment variable:

```bash
REVIEW_MEMORY_DIR=./vocabulary-anti-forgetting python3 vocabulary-anti-forgetting/review.py
```
