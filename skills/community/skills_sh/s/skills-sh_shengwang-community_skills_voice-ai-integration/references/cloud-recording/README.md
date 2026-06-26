# Shengwang Cloud Recording

Server-side recording of RTC channel audio/video. Pure REST API, no client SDK.

## What It Does

- Records active RTC sessions to cloud storage (S3, Alibaba OSS, Azure Blob, etc.)
- Three modes: `individual` (per-user files), `mix` (single mixed file), `web` (web page recording)
- Depends on an active RTC channel with participants

## Recording Lifecycle

```
acquire → start → stop
            ↑
          query (optional)
```

- `acquire` returns a `resourceId` (valid 5 minutes — must call `start` quickly)
- `start` begins recording in the specified mode
- `query` checks recording status
- `stop` ends recording (always call to avoid billing)

## Auth

- HTTP Basic Auth: `SHENGWANG_CUSTOMER_KEY` + `SHENGWANG_CUSTOMER_SECRET`
- Cloud Recording service must be enabled in [Shengwang Console](https://console.shengwang.cn/)
- Credentials & auth → [general/credentials-and-auth.md](../general/credentials-and-auth.md)

## Quick Start Docs

Fetch docs using the doc fetching script (see [doc-fetching.md](../doc-fetching.md)):

| Topic | Command |
|-------|---------|
| Quick Start | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/cloud-recording/restful/get-started/quick-start"` |

## Key Errors

| Code | Meaning |
|------|---------|
| 403 | Cloud Recording not enabled in Console |
| 404 | Resource expired or invalid sid |
| 432 | Recording already in progress |
| 435 | No users in channel |

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/cloud-recording/restful/get-started/quick-start
