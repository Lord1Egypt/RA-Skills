---
name: unifuncs-deep-search
description: Use UniFuncs Deep Search API for fast, comprehensive information gathering. Use this skill when users ask for deep search, broad investigation, or in-depth topic coverage.
argument-hint: [query]
allowed-tools: Bash(python3:*)
---

# UniFuncs Deep Search Skill

Use this tool for deep search and deep investigation on a specific topic, producing a complete search report. It is suitable when the task requires multiple rounds of searching and reading, or when the user explicitly asks for deep search/deep digging. This is a relatively expensive operation and usually takes **1-5 minutes**. If the user has not clearly requested deep search for a topic, ask for confirmation before running it. If the intent is ambiguous, do brief goal clarification without over-questioning; execute as soon as the user gives a clear instruction.

## First-Time Setup

1. Go to <https://unifuncs.com/account> to get your API key.
2. Set the environment variable: `export UNIFUNCS_API_KEY="sk-your-api-key"`

## When to Use

You need deeper, broader, and more complete information than standard web search.
You want consolidated findings for complex or multi-part questions.
Typical deep-search completion time is about **1-5 minutes** depending on topic complexity.

## Usage Guidelines

The skills is split into 3 independent entries:

- `deep-search-report.py` - Synchronously gets the search report. Because it can take longer, set a sufficiently large timeout.
- `deep-search-create-task.py` - Asynchronously creates a search task and returns a task ID. Keep the task ID for later status/result queries to avoid creating duplicate tasks.
- `deep-search-query-task.py` - Queries task status and returns task result/report content.

### 1) Sync result: deep-search-report.py

```bash
python3 deep-search-report.py "query"
```

### 2) Async task creation: create_task

```bash
python3 deep-search-create-task.py "query"
```

This returns `task_id`.

### 3) Async task query: query_task

```bash
python3 deep-search-query-task.py "task_id"
```

## Options

```text
usage: deep-search-report.py [-h] [--model {s1,s2,s3}]
                             [--timeout TIMEOUT]
                             [--stream-file STREAM_FILE]
                             [--read-stream-file] [--language {zh,en}]
                             [--reference-style {link,character,hidden}]
                             [--max-depth MAX_DEPTH]
                             [--domain-scope DOMAIN_SCOPE]
                             [--domain-blacklist DOMAIN_BLACKLIST]
                             [--output-prompt OUTPUT_PROMPT]
                             [--important-urls IMPORTANT_URLS]
                             [--important-keywords IMPORTANT_KEYWORDS]
                             [--important-prompt IMPORTANT_PROMPT]
                             [--introduction INTRODUCTION]
                             [--push-to-share] [--set-public]
                             [--raw-response]
                             [query]

UniFuncs Deep Search client

positional arguments:
  query                 User query sent to Deep Search.

options:
  -h, --help            show this help message and exit
  --model {s1,s2,s3}    Model to use (default: s3).
  --timeout TIMEOUT     Max streaming wait time in seconds (default:
                        900).
  --stream-file STREAM_FILE
                        Path to persist/read stream chunks. If omitted,
                        temp file is auto-created when writable.
  --read-stream-file    Read and render already received content from
                        --stream-file, without calling API.
  --language {zh,en}    Output language.
  --reference-style {link,character,hidden}
                        Reference marker style.
  --max-depth MAX_DEPTH
                        Maximum research depth.
  --domain-scope DOMAIN_SCOPE
                        Comma-separated domain allowlist.
  --domain-blacklist DOMAIN_BLACKLIST
                        Comma-separated domain blocklist.
  --output-prompt OUTPUT_PROMPT
                        Custom output prompt template.
  --important-urls IMPORTANT_URLS
                        Comma-separated important URLs.
  --important-keywords IMPORTANT_KEYWORDS
                        Comma-separated important keywords.
  --important-prompt IMPORTANT_PROMPT
                        Important prompt content.
  --introduction INTRODUCTION
                        Researcher role/tone introduction.
  --push-to-share       Push result to share space.
  --set-public          Set result as public.
  --raw-response        Print full API response JSON instead of concise
                        text.
```
