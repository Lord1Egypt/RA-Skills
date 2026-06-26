---
name: zsxq-fetch
description: Use this skill when the user wants OpenClaw to query synced Zhishi Xingqiu content, inspect recent posts, search downloaded documents, summarize updates, or answer questions grounded in the local ZSXQ database.
metadata: {"openclaw":{"requires":{"bins":["curl"]}}}
---

# ZSXQ Fetch

Use this skill to query the local OpenClaw ZSXQ database for summarization and grounded Q&A.

## When to use

- The user wants summaries of recent ZSXQ posts by time window or by group.
- The user asks questions that should be answered from synced ZSXQ posts or downloaded documents.
- The user wants to inspect downloaded attachments or search document text.
- The user wants to check sync status or manually trigger a sync.

## Preconditions

- The API server is running. Check with:

```bash
curl http://127.0.0.1:8000/health
```

If it is not running, start it from the project root:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server automatically syncs all subscribed groups in the background every hour (configurable via `SYNC_INTERVAL_SECONDS`).

## Core workflow

1. **Query the database directly** — do NOT sync before every request. Data is kept fresh by the background auto-sync.
2. Pull only the smallest relevant slice of data.
3. Use `/api/v1/topics`, `/api/v1/documents`, and `/api/v1/search_documents` to answer questions.
4. Summarize with explicit scope: group, time range, or topic.

## When to trigger a manual sync

Only trigger a manual sync if:
- The user explicitly asks for the "latest" or "most recent" content AND
- `/api/v1/sync_status` shows the last sync was more than 1 hour ago.

Otherwise, trust the database content.

## Useful endpoints

- Check sync status (always check this first for time-sensitive requests):

```bash
curl "http://127.0.0.1:8000/api/v1/sync_status"
```

- Trigger a manual sync (only if data is stale):

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/trigger_sync"
```

- Read recent topics:

```bash
curl "http://127.0.0.1:8000/api/v1/topics?group_id=GROUP_ID&limit=50&offset=0"
```

- List groups:

```bash
curl "http://127.0.0.1:8000/api/v1/groups/all"
```

- List downloaded documents:

```bash
curl "http://127.0.0.1:8000/api/v1/documents?group_id=GROUP_ID&limit=50"
```

- Search document text:

```bash
curl "http://127.0.0.1:8000/api/v1/search_documents?q=KEYWORD&group_id=GROUP_ID"
```

## Summarization pattern

- Pull recent topics for the requested group or across relevant groups.
- If documents may contain the answer, search them with keywords from the user question.
- Build the answer from retrieved records only. State when the answer is inferred from partial evidence.

## Output guidance

- For update summaries, group findings by topic or theme, not by raw post order.
- For question answering, cite the specific topic text or document match preview used.
- If the database has no relevant records, say so. Only recommend a manual sync if the last sync was more than 1 hour ago.
