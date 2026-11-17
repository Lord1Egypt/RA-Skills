---
name: xai-oauth-usage
description: Use when a Hermes Agent user asks to check xAI OAuth usage, remaining quota, or reset time without refreshing or modifying credentials.
version: 1.2.1
author: "proto0x.com"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [xAI, Grok, OAuth, usage, quota, billing, reset, 利用枠, リセット]
    category: utilities
    related_skills: []
---

# Hermes xAI Usage Checker

Use Hermes' canonical OAuth credential to check xAI weekly usage and reset time in read-only mode.
Do not modify credentials, reauthenticate, perform billing actions, or claim that the reported quota is model-specific.

## When to Use

- When a user asks for xAI OAuth or Grok usage, remaining quota, or reset time
- When `xai-oauth/grok-4.6` reports `billing` or quota exhaustion
- When deciding whether Hermes fallback behavior or `x_search` can be retested after the quota resets

## Prerequisites

- A valid `xai-oauth` credential in Hermes' canonical auth store
- `python3` and HTTPS access to `https://cli-chat-proxy.grok.com`
- User approval for a read-only OAuth request to the xAI Billing endpoint; ask first if approval has not been given

## How to Run

Run the script through Hermes' `terminal` tool with sanitized JSON output:

```text
terminal(command='python3 "${HERMES_SKILL_DIR}/scripts/check_xai_usage.py" --json', timeout=30)
```

For human-readable output, use the same `terminal` call without `--json`.
Human-readable output and stderr follow `HERMES_LANGUAGE`, then Hermes' `display.language`. Japanese settings produce Japanese output; every other value and configuration lookup failure produce English output. JSON keys and JSON error strings always remain in English.

Entry point: [`scripts/check_xai_usage.py`](scripts/check_xai_usage.py)

## Quick Reference

| Field | Meaning |
|---|---|
| `used_percent` | Current weekly usage percentage |
| `remaining_percent` | `100 - used_percent`, clamped at zero |
| `period_end_jst` | Billing API period end converted to JST |
| `remaining_seconds` | Seconds from execution time until the period ends |
| `product_usage` | Per-product usage returned by the Billing API |
| `source_host` | `cli-chat-proxy.grok.com` on success |

## Procedure

1. Confirm that the request is a read-only quota check and does not include credential changes or billing actions.
2. Run the `terminal` call in **How to Run** once. Do not redirect, log in, log out, refresh, reset, or top up.
3. If `status: ok`, report only usage, remaining quota, `period_end_jst`, approximate time remaining, and `product_usage`, using Hermes' display language.
4. If `remaining_percent` is zero and `remaining_seconds` is positive, treat the quota as not yet recovered.
5. If `status: error`, report only `error` and `http_status`. Do not automatically reauthenticate after a 401 or 403 response.
6. Never display, save, or include access tokens, refresh tokens, ID tokens, `auth.json` contents, or the raw API response in an answer.

Example report:

```text
xAI OAuth weekly quota is 100% used.
Reset: 2026-08-29 23:04 JST, approximately 29 hours 3 minutes remaining.
Breakdown: GrokBuild 100%.
```

## Pitfalls

- The `billing` period may represent a shared weekly quota. Do not claim it is a `Grok 4.6`-specific limit.
- Remaining time decreases while the command runs. Treat `period_end_jst` as authoritative and label remaining time as approximate.
- If Hermes still reports `billing` after the reset time, query once more instead of performing a blind reset.
- Prefer the API result even when no usage page is visible, but report the value as unverified if the request fails.
- The script rejects redirects. Do not replace this behavior with an implementation that sends the Authorization header to another host.

## Verification

In a source checkout, run the network-free regression tests from the skill directory:

```text
python3 -m unittest discover -s tests -v
```

For a skill installed through Hermes, run this network-free smoke test:

```text
terminal(command='python3 "${HERMES_SKILL_DIR}/scripts/check_xai_usage.py" --help', timeout=30)
```

Only with user approval, run the live request from **How to Run** and verify `status: ok`, the expected `source_host`, and the absence of token fields.

## 日本語での概要

HermesのxAI OAuth週間利用率・残量・リセット時刻を、認証情報を変更せず読み取り専用で確認するskillです。
通常表示とstderrはHermesが日本語設定なら日本語、それ以外は英語になります。JSONのキーとエラー文は英語固定です。
実行前にユーザーの承認を確認し、tokenや生のAPIレスポンスは表示・保存しません。
