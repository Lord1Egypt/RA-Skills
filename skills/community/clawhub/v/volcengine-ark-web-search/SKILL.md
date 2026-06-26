---
name: volcengine-ark-web-search
description: Use when you need fresh web results through Volcengine ARK Responses API, especially for today's news, recent updates, fact checks, topic monitoring, or Chinese-language search workflows powered by ARK_API_KEY.
metadata:
  openclaw:
    requires:
      env:
        - ARK_API_KEY
      anyBins:
        - python3
    primaryEnv: ARK_API_KEY
    homepage: "https://www.volcengine.com/docs/82379/1783703?lang=zh"
---

# Volcengine Ark Web Search

## Overview

Use this skill when the task needs up-to-date public web information and the runtime should go through Volcengine ARK Responses API instead of the model's built-in browsing. The bundled script wraps ARK `responses` with the `web_search` tool, defaults to Chinese-friendly output, and is suitable for repeatable automation or local agent workflows.

Default markdown output is stabilized into three sections:

- title
- summary
- sources

## When to Use

- The user asks for today's news, recent updates, current public coverage, or live fact checks.
- You want fresh web results but must route them through Volcengine ARK with `ARK_API_KEY`.
- You need a reusable local command that can be shared in scripts, cron jobs, or other skills.
- The answer should prefer Chinese output, explicit dates, and source links.
- You need to compare or verify public web information before answering.

## When Not to Use

- `ARK_API_KEY` is missing.
- The task is static and does not need current web information.
- You need browser automation, authenticated sessions, or site-specific interaction rather than search.
- A different provider is mandatory.

## Quick Start

1. Confirm `ARK_API_KEY` is set.
2. Run the bundled script.
3. Summarize the returned answer with explicit dates and source links.

Basic usage:

```bash
python3 scripts/ark_web_search.py "What are today's AI news headlines?"
```

Chinese query:

```bash
python3 scripts/ark_web_search.py "今天有什么热点新闻"
```

Custom model:

```bash
python3 scripts/ark_web_search.py "OpenAI latest announcements" \
  --model doubao-seed-1-6-250615
```

Structured JSON output:

```bash
python3 scripts/ark_web_search.py "latest semiconductor policy news" \
  --format json
```

Longer timeout with quick retries:

```bash
python3 scripts/ark_web_search.py "OpenAI latest news" \
  --timeout 90 \
  --retries 2
```

Dry run without network:

```bash
python3 scripts/ark_web_search.py "today's EV market news" \
  --dry-run
```

## Core Workflow

1. Rewrite the user request into a direct search question when needed. Prefer explicit entities, topics, and time windows.
2. Use the default system prompt unless the task requires raw passthrough behavior.
3. Run `scripts/ark_web_search.py`.
4. If the script returns enough signal, summarize in Chinese unless the user asked for another language.
5. For relative-time prompts such as "today" or "recently", write absolute dates in the final answer.

## Output Requirements

- Prefer concise summaries with links.
- Default markdown output should be stable and easy to scan: title, summary, then sources.
- Preserve uncertainty when the search result is thin or conflicting.
- If sources are present, include them.
- Convert relative date language into explicit dates whenever possible.
- If the API result is insufficient, say so instead of inventing facts.

## Files

- `scripts/ark_web_search.py`: ARK Responses API runner with `web_search`, dry-run support, streaming support, and source extraction.
- `references/ark-responses-api.md`: Notes on request shape, model drift, tool naming drift, and maintenance references.

## Maintenance Notes

- Prefer overriding the model with `--model` or `ARK_MODEL`. ARK model availability changes over time.
- `--timeout` is per attempt. Use `--retries` for quick retry behavior on transient failures.
- Some ARK environments reject `search_context_size` with HTTP `400`. This script now retries automatically without that field if the server reports it as unsupported.
- The default system prompt asks the model to return summary body only. Title and source sections are added by the script to keep output stable.
- The Volcengine docs have shown both `web_search` and `web_search_preview` historically. This skill defaults to `web_search` and should only change if official docs for the target environment require it.
- If response parsing breaks after an upstream API change, update the normalization logic in `scripts/ark_web_search.py` and keep `references/ark-responses-api.md` in sync.
