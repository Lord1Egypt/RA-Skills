# SPEC.md — weread-reading-recommender

## 1. Objective
Provide a local-first skill for WeRead-based book recommendation. The skill should help answer prompts such as:

- 结合我的微信读书记录，我最近想系统学 AI Agent，推荐几本书
- 根据我的微信读书历史，推荐下一本最值得读的书
- 分析我的阅读偏好，再给我 3 本稳妥推荐和 2 本探索推荐

## 2. Inputs
### 2.1 Local cookie input for export script
Supported sources:
- `--cookie "..."`
- `--cookie-file /path/to/weread.cookie`
- env var `WEREAD_COOKIE` (default)
- custom env var via `--env-var`

### 2.2 Raw export file
Default example path:
- `data/weread-raw.json`

### 2.3 Normalized file
Default example path:
- `data/weread-normalized.json`

### 2.4 Recommendation prompt
Optional natural-language goal supplied by the user.

## 3. Export Script Requirements
File:
- `scripts/export_weread.py`

### CLI
```bash
python3 scripts/export_weread.py --out data/weread-raw.json
python3 scripts/export_weread.py --cookie-file ~/.config/weread.cookie --out data/weread-raw.json
python3 scripts/export_weread.py --include-book-info --detail-limit 50 --out data/weread-raw.json
```

### Required behavior
- Read cookie locally
- Call WeRead bookshelf endpoint
- Call WeRead notebook endpoint
- Optionally call per-book info endpoint
- Write JSON output without cookie contents
- Print a short summary to stdout

### Required output fields
Top-level fields:
- `exported_at`
- `source`
- `summary`
- `shelf_sync`
- `notebook`
- `book_info` (optional)
- `warnings` (optional)

## 4. Normalization Script Requirements
File:
- `scripts/normalize_weread.py`

### CLI
```bash
python3 scripts/normalize_weread.py --input data/weread-raw.json --output data/weread-normalized.json
```

### Required behavior
- Read raw export JSON
- Build per-book normalized records
- Compute reading status buckets
- Compute engagement score
- Compute top categories / lists
- Produce recommendation-friendly summary sections

### Normalized top-level fields
- `generated_at`
- `source_file`
- `summary`
- `profile_inputs`
- `llm_hints`
- `books`

### Required per-book normalized fields
- `book_id`
- `title`
- `author`
- `translator`
- `categories`
- `book_lists`
- `status` (`finished` | `reading` | `unread`)
- `is_finished`
- `progress`
- `reading_time_seconds`
- `last_read_at`
- `note_count`
- `bookmark_count`
- `review_count`
- `interaction_count`
- `engagement_score`
- `is_imported`
- `is_paid`
- `public_rating` (if available)
- `intro` (if available)

## 5. Skill Behavior Requirements
File:
- `SKILL.md`

### Trigger scope
Use when the user asks to:
- export local WeRead records
- normalize WeRead data
- analyze reading history
- recommend books from WeRead history

### Skill workflow
1. If normalized file is missing, help the user export + normalize first.
2. Read normalized JSON.
3. Extract strongest books, categories, recency, unfinished momentum, interaction patterns.
4. If the user has a current goal/question, prioritize that.
5. Produce recommendations with explanations.

### Output format expectations
Suggested reply sections:
- 阅读画像 / Reading profile
- 推荐结果 / Recommendations
- 为什么适合现在 / Why now
- 可选：暂缓推荐 / Skip for now

Each recommendation should ideally explain:
- why it matches the user's current goal
- which past books it resembles
- what new value it adds
- whether it is a safe pick or an exploration pick

## 6. Security Requirements
- Never store cookie in exported JSON
- Never hardcode cookie in code or assets
- Never suggest third-party cookie sync as the default path
- Keep export local-first

## 7. Deferred Items
- highlight / note text analysis
- duplicate edition detection
- external candidate retrieval
- automatic refresh jobs
- packaging / installation
