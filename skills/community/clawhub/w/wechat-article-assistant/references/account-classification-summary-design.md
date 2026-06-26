# Account Classification and Summary Design

## Goal

This document describes how to extend `wechat-article-assistant` so that:

1. Official accounts can be classified.
2. One class of accounts only syncs article lists.
3. Another class of accounts syncs article lists, then automatically fetches article details, aggregates all details, and produces a summary of core content.
4. Theme categories such as `AI`, `Politics`, `Economy` can be customized independently from the sync strategy.

## Current State

The current skill already supports:

- Maintaining a local `account` list.
- Syncing article metadata into `article`.
- Fetching a single article detail into `article_detail`.
- Running scheduled sync through `sync_config` and `sync_due`.

The current skill does **not** support:

- Account classification.
- Differentiating post-sync processing strategies by account.
- Batch detail fetching for an account.
- Account-level summary reports.
- Custom account theme tags.
- Provider-based LLM summarization.

## Core Design Principle

Do not use one field to represent two different business concepts.

There are actually two independent classification axes:

### 1. Processing strategy

This decides what the system does after sync:

- `sync_only`: only sync article list.
- `sync_and_detail`: sync article list, then fetch article details.
- `sync_detail_and_summary`: sync article list, fetch details, then generate summary.

### 2. Theme tags

This describes what the account is about:

- `AI`
- `Politics`
- `Economy`
- `Company`
- `Macro`
- any custom tag defined by the user

These two axes should be stored separately. For example:

- `机器之心`: strategy = `sync_detail_and_summary`, tags = `AI`
- `新华社`: strategy = `sync_only`, tags = `Politics`

## Recommended Minimal Data Model

To keep the first implementation simple, add a few strategy fields directly on `account`, and store theme tags in a separate table.

### 1. Extend `account`

Add the following columns to `account`:

- `processing_mode TEXT NOT NULL DEFAULT 'sync_only'`
- `auto_fetch_detail INTEGER NOT NULL DEFAULT 0`
- `auto_summarize INTEGER NOT NULL DEFAULT 0`
- `summary_scope TEXT NOT NULL DEFAULT 'new_articles'`
- `summary_enabled INTEGER NOT NULL DEFAULT 0`
- `summary_prompt TEXT NOT NULL DEFAULT ''`

Recommended meaning:

- `processing_mode`
  - canonical strategy enum, preferred for code branching
- `auto_fetch_detail`
  - explicit switch for automatic detail fetching
- `auto_summarize`
  - explicit switch for automatic summarization
- `summary_scope`
  - controls summary range
  - `new_articles`: summarize only newly synced articles
  - `recent_30`: summarize the latest 30 articles with details
  - `all_details`: summarize all fetched details for the account
- `summary_enabled`
  - summary feature master switch, useful for future rollout
- `summary_prompt`
  - optional per-account summary prompt customization

For the first version, you can keep `processing_mode` and derive the booleans from it. Example:

- `sync_only` -> `auto_fetch_detail=0`, `auto_summarize=0`
- `sync_and_detail` -> `auto_fetch_detail=1`, `auto_summarize=0`
- `sync_detail_and_summary` -> `auto_fetch_detail=1`, `auto_summarize=1`

### 2. Add theme tag tables

```sql
CREATE TABLE IF NOT EXISTS account_tag (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL DEFAULT '',
  color TEXT NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS account_tag_map (
  fakeid TEXT NOT NULL,
  tag_id INTEGER NOT NULL,
  created_at INTEGER NOT NULL,
  PRIMARY KEY (fakeid, tag_id)
);

CREATE INDEX IF NOT EXISTS idx_account_tag_map_fakeid ON account_tag_map(fakeid);
CREATE INDEX IF NOT EXISTS idx_account_tag_map_tag_id ON account_tag_map(tag_id);
```

Why not store tags as JSON on `account`:

- querying by tag is harder
- deduplication is harder
- tag management becomes messy
- later account filtering and reporting will be limited

### 3. Add summary result table

```sql
CREATE TABLE IF NOT EXISTS account_summary (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fakeid TEXT NOT NULL,
  scope TEXT NOT NULL DEFAULT 'new_articles',
  source_article_count INTEGER NOT NULL DEFAULT 0,
  source_article_ids_json TEXT NOT NULL DEFAULT '[]',
  title TEXT NOT NULL DEFAULT '',
  summary_markdown TEXT NOT NULL DEFAULT '',
  core_points_json TEXT NOT NULL DEFAULT '[]',
  topics_json TEXT NOT NULL DEFAULT '[]',
  provider TEXT NOT NULL DEFAULT '',
  model TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'success',
  error_message TEXT NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_account_summary_fakeid ON account_summary(fakeid);
CREATE INDEX IF NOT EXISTS idx_account_summary_created_at ON account_summary(created_at);
```

This table stores the final aggregated result for one summarization run.

### 4. Add processing task log table

```sql
CREATE TABLE IF NOT EXISTS processing_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fakeid TEXT NOT NULL,
  stage TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT '',
  message TEXT NOT NULL DEFAULT '',
  article_count INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL
);
```

Recommended stages:

- `sync`
- `detail_fetch`
- `summary`

This prevents `sync_log` from carrying responsibilities for all downstream processing stages.

## Migration Strategy

The current `database.py` only relies on `CREATE TABLE IF NOT EXISTS`, which is not enough for column evolution.

To support smooth upgrades, add a migration helper in `database.py`:

1. Ensure new tables with `CREATE TABLE IF NOT EXISTS`.
2. Check existing `account` columns via `PRAGMA table_info(account)`.
3. Run `ALTER TABLE account ADD COLUMN ...` for missing columns.
4. Backfill old rows:

```sql
UPDATE account
SET
  processing_mode = CASE
    WHEN enabled = 1 THEN 'sync_only'
    ELSE 'sync_only'
  END
WHERE processing_mode = '';
```

Recommended:

- keep migration idempotent
- do not rebuild the whole database
- do not break existing `app.db`

## Processing Flow

## Strategy Behavior

### Type A: sync only

Flow:

1. Sync article metadata.
2. Stop after `article` is updated.

Applicable to:

- accounts only used for monitoring updates
- high-volume accounts where full detail fetching is too expensive

### Type B: sync + detail + summary

Flow:

1. Sync article metadata.
2. Identify newly added articles.
3. Batch fetch article details.
4. Aggregate all fetched details into one corpus.
5. Generate summary result.
6. Save summary artifact and processing logs.

Applicable to:

- research accounts
- accounts used for topic tracking
- content sources that need downstream intelligence extraction

## Recommended Execution Chain

Current `sync_account()` only returns newly synced article metadata. Extend it so it can pass newly added article ids downstream.

Recommended orchestration:

1. `sync_service.sync_account()`
2. If account mode requires detail fetch:
   - call `article_service.fetch_account_details(...)`
3. If account mode requires summary:
   - call `summary_service.summarize_account(...)`

Pseudo flow:

```python
result = sync_account(db, fakeid)
if not result["success"]:
    return result

account = get_account(fakeid)
if account["processing_mode"] in {"sync_and_detail", "sync_detail_and_summary"}:
    detail_result = fetch_account_details(db, fakeid, article_ids=result["data"]["new_article_ids"])

if account["processing_mode"] == "sync_detail_and_summary":
    summarize_account(db, fakeid, article_ids=result["data"]["new_article_ids"])
```

## Needed Service Additions

## 1. `article_service.py`

Add batch detail helpers:

- `fetch_account_details(db, fakeid, article_ids=None, limit=None, force_refresh=False)`
- `list_article_details_by_fakeid(db, fakeid, limit=None)`
- `build_summary_corpus(db, fakeid, scope='new_articles', article_ids=None)`

`build_summary_corpus` should produce structured summary input like:

```json
{
  "fakeid": "...",
  "nickname": "...",
  "tags": ["AI", "Tooling"],
  "articles": [
    {
      "article_id": "...",
      "title": "...",
      "publish_time": 1234567890,
      "author_name": "...",
      "account_name": "...",
      "digest": "...",
      "text_content": "..."
    }
  ]
}
```

This is the correct boundary between data collection and summarization.

## 2. New `summary_service.py`

Create a new module instead of putting summary logic into `sync_service.py`.

Responsibilities:

- choose summary scope
- gather detail corpus
- call summary provider
- normalize summary output
- persist `account_summary`
- write `processing_log`

Recommended public functions:

- `summarize_account(db, fakeid, scope='new_articles', article_ids=None)`
- `list_account_summaries(db, fakeid, limit=20)`
- `get_latest_account_summary(db, fakeid)`

## 3. New `summary_provider.py`

Use an abstraction layer from the beginning.

Recommended interface:

```python
class SummaryProvider:
    def summarize_account(self, payload: dict) -> dict:
        ...
```

First version can support:

- `none`: do not call an LLM, only export corpus
- `openai_compatible`: call any OpenAI-compatible endpoint

Recommended environment variables:

- `WECHAT_SUMMARY_PROVIDER`
- `WECHAT_SUMMARY_MODEL`
- `WECHAT_SUMMARY_API_KEY`
- `WECHAT_SUMMARY_BASE_URL`

This keeps the skill reusable and avoids hard-coding a single vendor.

## 4. `account_service.py`

Extend account management:

- allow setting `processing_mode`
- allow setting summary options
- return theme tags on `list_accounts`
- add tag management helpers

Recommended new functions:

- `set_account_processing_mode(...)`
- `create_account_tag(...)`
- `delete_account_tag(...)`
- `assign_account_tag(...)`
- `unassign_account_tag(...)`
- `list_account_tags(...)`

## 5. `cli.py`

Add new commands.

### Account strategy

- `set-account-mode`
- `set-account-summary-options`

Example:

```bash
python scripts/wechat_article_assistant.py set-account-mode \
  --fakeid "..." \
  --processing-mode sync_detail_and_summary \
  --json
```

### Theme tags

- `create-tag`
- `list-tags`
- `delete-tag`
- `assign-tag`
- `unassign-tag`

Example:

```bash
python scripts/wechat_article_assistant.py create-tag --name AI --json
python scripts/wechat_article_assistant.py assign-tag --fakeid "..." --tag AI --json
```

### Detail batch

- `fetch-account-details`

Example:

```bash
python scripts/wechat_article_assistant.py fetch-account-details \
  --fakeid "..." \
  --limit 30 \
  --json
```

### Summary

- `summarize-account`
- `list-account-summaries`

Example:

```bash
python scripts/wechat_article_assistant.py summarize-account \
  --fakeid "..." \
  --scope all_details \
  --json
```

## Summary Prompt Recommendation

For account-level aggregation, the prompt should ask for structured output instead of one free-form paragraph.

Recommended summary output:

- `summary_markdown`
- `core_points`
- `topic_keywords`
- `content_map`
- `signals_to_watch`

Example shape:

```json
{
  "title": "AI 类公众号近期开源与应用趋势总结",
  "summary_markdown": "...",
  "core_points": [
    "模型落地从概念验证走向业务闭环",
    "智能体、知识库、工作流是高频主题"
  ],
  "topics": ["AI Agent", "RAG", "企业应用"],
  "signals_to_watch": [
    "更多文章开始比较模型成本和部署复杂度",
    "工具链整合成为共同话题"
  ]
}
```

## How to Interpret "Aggregate All Details"

There are two possible meanings:

### Option 1. Summarize newly synced articles only

Pros:

- faster
- cheaper
- fits daily automation

Cons:

- summary is incremental, not complete historical view

### Option 2. Summarize all detailed articles for the account

Pros:

- gives a full long-term profile

Cons:

- more expensive
- may exceed model context window

Recommended first implementation:

- default `summary_scope = new_articles`
- keep `all_details` as optional manual mode

For `all_details`, add chunking:

1. split articles into batches
2. summarize each batch
3. summarize the batch summaries again

## What "Account Detail" Should Mean Here

For this requirement, the practical meaning should be:

- fetch the full content of each article under the account
- not only keep article metadata

If later you also want profile-level information for the account itself, that can be a separate feature:

- account profile scrape
- account intro
- alias
- business/profile page info

This should not block the first implementation.

## Reporting Layer

When summary is generated, also export files under:

```text
downloads/reports/<fakeid>/
```

Recommended artifacts:

- `latest-summary.json`
- `latest-summary.md`
- timestamped historical summary files

This will make the skill easy to integrate into external automation.

## Recommended Implementation Order

### Phase 1: classification foundation

Modify:

- `scripts/schema.py`
- `scripts/database.py`
- `scripts/account_service.py`
- `scripts/cli.py`

Deliverables:

- processing mode stored on account
- custom tag CRUD
- list accounts returns mode + tags

### Phase 2: detail automation

Modify:

- `scripts/article_service.py`
- `scripts/sync_service.py`

Deliverables:

- account-level batch detail fetch
- automatic detail fetch after sync for selected accounts

### Phase 3: summary automation

Add:

- `scripts/summary_service.py`
- `scripts/summary_provider.py`

Modify:

- `scripts/sync_service.py`
- `scripts/cli.py`

Deliverables:

- automatic summary generation after sync
- summary history persistence

### Phase 4: reporting and refinements

Optional additions:

- filter accounts by tag
- batch summarize by tag
- export one report for all `AI` accounts
- support prompt templates by tag

## Concrete Recommendation For Your Requirement

For your specific use case, the best structure is:

### Account strategy classes

- `sync_only`
  - only sync article list
- `research`
  - sync article list
  - fetch article details automatically
  - summarize automatically

Implementation-wise, `research` can map to `processing_mode = sync_detail_and_summary`.

### Theme tags

Use independent tags such as:

- `AI`
- `Politics`
- `Economy`
- `Macro`
- `Company`

This combination is enough to express your business cleanly:

- `账号A`: mode = `sync_only`, tags = `Politics`
- `账号B`: mode = `sync_detail_and_summary`, tags = `AI`

## Files That Will Need Changes

Primary files:

- `scripts/schema.py`
- `scripts/database.py`
- `scripts/account_service.py`
- `scripts/article_service.py`
- `scripts/sync_service.py`
- `scripts/cli.py`

New files:

- `scripts/summary_service.py`
- `scripts/summary_provider.py`

## Final Recommendation

The safest and cleanest path is:

1. First implement `processing_mode + custom tags`.
2. Then implement automatic account-level detail fetching.
3. Finally connect summarization through a provider abstraction.

Do not start with a single generic "category" field.
It will quickly become ambiguous because "分类" in your scenario really includes both:

- business processing strategy
- content theme

Separating these two from the start will make the system much easier to extend.
