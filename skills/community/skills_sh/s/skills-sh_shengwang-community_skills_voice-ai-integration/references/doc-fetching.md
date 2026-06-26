# Shengwang Doc Fetching Guide

## Overview

Shengwang docs are fetched via HTTP. The doc index (`references/docs.txt`) maps document names to fetchable URIs.

## Step 1: Ensure doc index exists

Check if `references/docs.txt` exists. If not, download it:
```bash
bash skills/voice-ai-integration/scripts/fetch-docs.sh
```

## Step 2: Find the document URI

Search `references/docs.txt` for keywords. Each entry follows this format:
```
- [doc-name](https://doc-mcp.shengwang.cn/doc-content-by-uri?uri=docs://default/...)
```

Extract the `docs://...` URI part for use in Step 3.

## Step 3: Fetch the document

Use the fetch script to get Markdown content:

```bash
bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start"
bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/rtc/javascript/get-started/quick-start"
```

For ConvoAI, do not start here by default. Inspect the matching sample repo, `agent-server-sdk` on the server side, and `agora-agent-client-toolkit` on the client side when possible first, then fetch REST docs only for missing schemas, vendor parameters, or unsupported operations.

The script handles the query parameter internally via curl, which works in environments
where web fetch tools cannot pass `?uri=...` query strings.

## URI Pattern

```
docs://default/{product}/{platform}/{path}
```

| Product | URI prefix |
|---------|-----------|
| ConvoAI | `docs://default/convoai/restful/...` |
| RTC | `docs://default/rtc/{platform}/...` |
| RTM | `docs://default/rtm2/{platform}/...` |
| Cloud Recording | `docs://default/cloud-recording/restful/...` |
| Token Auth | `docs://default/rtc/{platform}/basic-features/token-authentication` |

## When to fetch

Fetch for:
- API field details, request/response schemas
- Vendor configurations (TTS, ASR)
- Error codes and meanings
- Any content that may change with doc updates
- ConvoAI REST references only after sample/SDK inspection leaves a gap

Do NOT fetch for:
- Generation rules (field types, naming conventions) — stable, in skill files
- Auth patterns — stable, in [general/credentials-and-auth.md](general/credentials-and-auth.md)
- Workflow steps — stable, in skill files

## Fallback

If the fetch script fails, use the Shengwang doc site URL directly:
```
https://doc.shengwang.cn/doc/{product}/{platform}/{path}
```
