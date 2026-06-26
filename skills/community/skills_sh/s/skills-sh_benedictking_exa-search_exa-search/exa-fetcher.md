---
name: exa-fetcher
version: 1.0.0
author: BenedictKing
description: Independent subtask for executing Exa API calls (internal use)
allowed-tools:
  - Bash
context: fork
---

# Exa Fetcher Sub-skill

> Note: This is an internal sub-skill, invoked by the `exa-search` main skill through the Task tool.

## Purpose

Execute Exa API calls in an independent context with `context: fork`, avoiding carrying main conversation context, reducing token consumption.

## Received Parameters

Receives complete command through Task's `prompt`, using stdin for JSON:

```bash
cat <<'JSON' | node .claude/skills/exa-search/exa-api.js <search|contents|findsimilar|answer|research>
{ ...payload... }
JSON
```

## Output

Returns Exa API's JSON response as-is (pretty printed).
