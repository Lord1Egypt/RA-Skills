# Shengwang Token Server

Server-side Token generation using the AgoraDynamicKey library.

## Overview

Agora uses **AccessToken2** (HMAC-SHA256) for channel authentication.
- Requires `SHENGWANG_APP_ID` + `SHENGWANG_APP_CERTIFICATE` (server-side only)
- Uses the open-source [AgoraDynamicKey](https://github.com/AgoraIO/Tools) library
- NEVER expose `APP_CERTIFICATE` to clients

## Workflow

### Step 1: Confirm Credentials

Need `SHENGWANG_APP_ID` and `SHENGWANG_APP_CERTIFICATE` from [Shengwang Console](https://console.shengwang.cn/).
Missing? → [general/credentials-and-auth.md](../general/credentials-and-auth.md)

### Step 2: Get AgoraDynamicKey

All language implementations live in one repo: `https://github.com/AgoraIO/Tools`

> ⚠️ **DO NOT** use `agora-token-builder`, `agora-token`, or any third-party token package from PyPI / npm / Maven.
> These are unofficial, outdated, and may generate incompatible tokens (v1 instead of v2).
> The ONLY supported source is the official [AgoraDynamicKey](https://github.com/AgoraIO/Tools) repo below.

Clone the repo:

```bash
git clone --depth 1 https://github.com/AgoraIO/Tools.git
```

After download, find your language under `Tools/DynamicKey/AgoraDynamicKey/<language>/src/`:

| Language | Source path | Builder file |
|----------|------------|--------------|
| Go | `go/src/rtctokenbuilder2/` | `RtcTokenBuilder2.go` |
| Java | `java/src/main/java/io/agora/media/` | `RtcTokenBuilder2.java` |
| Python3 | `python3/src/` | `RtcTokenBuilder2.py` |
| Node.js | `nodejs/src/` | `RtcTokenBuilder2.js` |
| PHP | `php/src/` | `RtcTokenBuilder2.php` |
| C++ | `cpp/src/` | `RtcTokenBuilder2.h` |

> Go projects: copy `rtctokenbuilder2` source files into your project. The Tools repo is not a standalone Go module.

### Step 3: Implement Token Endpoint

Create a `GET /api/agora/token` endpoint.

**Request parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `channelName` | string | Yes | — | RTC channel name. `""` for wildcard (any channel). |
| `uid` | integer | No | `0` | User ID. `0` = wildcard (any user). |
| `role` | string | No | `publisher` | `publisher` (send+receive) or `subscriber` (receive only) |
| `expireSeconds` | integer | No | `3600` | Token validity in seconds. Max: 86400 (24h). |

**Environment variables:**

```bash
SHENGWANG_APP_ID=your_app_id
SHENGWANG_APP_CERTIFICATE=your_app_certificate
```

**Response:** Plain text token string.

| Status | Meaning |
|--------|---------|
| 200 | Token generated |
| 400 | Missing `channelName` |
| 500 | Generation failed |

**Example:**

```bash
curl "http://localhost:8080/api/agora/token?channelName=test&uid=12345&role=publisher&expireSeconds=3600"
```

### Step 4: Environment Setup

- Local: add to `.env`
- Production: configure in deployment environment
- NEVER commit `SHENGWANG_APP_CERTIFICATE` to version control

---

## Token Generation API

### Core Method

```
BuildTokenWithUid(appId, appCertificate, channelName, uid, role, tokenExpire, privilegeExpire)
```

- `role`: `RolePublisher` (send+receive) or `RoleSubscriber` (receive only)
- `tokenExpire` and `privilegeExpire`: seconds — set both to the same value for standard use

### Token Types by Product

| Product | Builder class | Method |
|---------|--------------|--------|
| RTC (channel join) | `RtcTokenBuilder2` | `BuildTokenWithUid` |
| RTM (messaging) | `RtmTokenBuilder2` | `BuildToken` |
| Chat | `ChatTokenBuilder2` | `BuildUserToken` |

This reference focuses on RTC tokens (most common). RTM and Chat use the same library, different builder class.

### Wildcard Tokens

- `uid = 0` → works for any UID
- `channelName = ""` → works for any channel
- Both wildcard → single token for any user in any channel (use with caution)

### Fine-grained Tokens (BuildTokenWithUidAndPrivilege)

Set separate expiry per privilege: `joinChannel`, `pubAudio`, `pubVideo`, `pubDataStream`.
Use for co-host scenarios where publish permissions differ per user.

---

## Token Expiry Handling

| Client SDK Callback | When | Action |
|---------------------|------|--------|
| `onTokenPrivilegeWillExpire` | 30s before expiry | Fetch new token, call `renewToken()` |
| `onRequestToken` | Token expired | Fetch new token, call `renewToken()` |

For multi-channel (`joinChannelEx`): use `updateChannelMediaOptionsEx` to update token.

### ConvoAI Token Renewal

When using token with ConvoAI `/join`:
- Generate token for `channelName` = the RTC channel the agent joins
- `uid` = the agent's UID (match `agent_rtc_uid`, or `0` for auto-assign)
- If token expires mid-session → `POST /agents/{agentId}/update` with new token

---

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `APP_CERTIFICATE` empty | Env var not set | Check `.env`. If App Certificate not enabled in Console, token is not needed — use empty string. |
| Token returns empty string | Wrong library version or params | Verify AgoraDynamicKey uses AccessToken2. Check `channelName` is not nil. |
| `BuildTokenWithUid` not found | Wrong import path | Must use `rtctokenbuilder2` (v2), not v1. Check language-specific path in table above. |
| Client `ERR_INVALID_TOKEN` | Token mismatch | Verify: same `channelName`, same `uid`, not expired, correct `APP_CERTIFICATE`. |
| Download fails | Network or URL issue | Clone manually from https://github.com/AgoraIO/Tools. |

Never fall back to hardcoded tokens or skip authentication. Report the error and guide the user to fix the root cause.

---

Official docs: https://doc.shengwang.cn/doc/rtc/android/basic-features/token-authentication
