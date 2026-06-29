---
name: tencentdb-databaseclaw
description: "This skill should be used when an AI agent or automated system needs to send messages to a TencentDB DatabaseClaw instance and receive streaming responses. It provides a verified Python client (scripts/chat.py) and complete TC3-HMAC-SHA256 signing reference for the CreateChatCompletion SSE API. Trigger on keywords: DatabaseClaw, DBClaw, clawins-, TDAI chat, agent-to-agent database query."
---

# TencentDB-DatabaseClaw

Send messages to a DatabaseClaw instance via the `CreateChatCompletion` SSE API and receive streaming Agent responses.

## When to Use

- An AI agent needs to invoke DatabaseClaw for SQL execution, inspection, or data analysis
- Building an AI workflow that integrates DatabaseClaw as a tool (LangChain / CrewAI / custom)
- Verifying a DatabaseClaw instance is healthy by sending a test message
- Cross-product function-calling where DBClaw acts as a backend tool

**Not for**: instance lifecycle management (isolate/restart/offline) — user must operate in the [DatabaseClaw Console](https://console.cloud.tencent.com/tdai/claw/instance).

> **API Scope**: This skill ONLY uses `CreateChatCompletion` (SSE chat) and `CreateClawSession` (create session for console visibility). No other APIs are supported.

---

## Critical Facts (Must-Know Before Starting)

| Fact | Value |
|------|-------|
| SSE streaming host | `tdai.ai.tencentcloudapi.com` |
| Non-streaming host (list/describe) | `tdai.tencentcloudapi.com` |
| Service name (for TC3 signing) | `tdai` |
| API version | `2025-07-17` |
| Action (chat) | `CreateChatCompletion` |
| Action (session) | `CreateClawSession` (non-streaming host) |
| Required body fields | `InstanceId`, `InputContent` |
| Optional body fields | `ChatId` (pass SessionKey here to link with console session list) |
| Forbidden body fields | `AppId`, `Uin`, `OwnerUin`, `IdempotencyKey` (identity derived from AK/SK) |
| Instance requirement | Status must be `running` |
| SSE end marker | `data: [DONE]` |
| Response wrapper | Frames may be wrapped in `{"Response": {...}}` — unwrap before parsing |
| Heartbeat interval | 20 seconds (ignore these frames) |
| Recommended timeout | **120s** (covers 99% cases); complex multi-region scans may take 60-90s |
| Timeout guidance | Simple Q&A: 2-5s; single query: 5-15s; multi-region scan: 30-90s |

> **Domain split is the #1 pitfall**: `CreateChatCompletion` MUST hit `tdai.ai.tencentcloudapi.com`. Using `tdai.tencentcloudapi.com` returns `InternalError`.

---

## Workflow

### Step 0: Ensure Instance is Running

Before using this skill, the target DatabaseClaw instance **must** be in `running` status. If the instance is not running (API returns an error like "实例状态异常"), guide the user to:

1. Open the [DatabaseClaw Console](https://console.cloud.tencent.com/tdai/claw/instance)
2. Locate the target instance and ensure it is in "运行中" status
3. If the instance is stopped/isolated, click "重启" or "解除隔离" in the console

> **Important**: This skill only uses the `CreateChatCompletion` API (and optionally `CreateClawSession`). Instance lifecycle operations (restart/isolate/offline) are NOT supported via this skill — the user must operate them in the console.

### Step 1: Session Creation (Default Behavior)

By default, `chat.py` automatically calls `CreateClawSession` (on `tdai.tencentcloudapi.com`) to get a `SessionKey` before sending the message. This makes the conversation visible in the console's session list page (会话列表).

```bash
# Default: session is created automatically
python3 scripts/chat.py --instance-id $INSTANCE_ID --secret-id $SECRET_ID --secret-key $SECRET_KEY \
  --message "hello"
```

To skip session creation (conversation won't appear in console list):

```bash
python3 scripts/chat.py --instance-id $INSTANCE_ID --secret-id $SECRET_ID --secret-key $SECRET_KEY \
  --no-session --message "hello"
```

### Step 2: Send Message (Programmatic)

Use `scripts/chat.py` — two output modes:

- **Default (clean)**: Only final Agent response on stdout. Ideal for piping into other tools or Agent integrations.
- **`--verbose` / `-v`**: Shows tool calls, reasoning, and connection info on stderr. Ideal for debugging and development.

```bash
# Clean mode (default) — only final answer on stdout
python3 scripts/chat.py \
  --instance-id $INSTANCE_ID \
  --secret-id $SECRET_ID \
  --secret-key $SECRET_KEY \
  --message "查询近7天慢查询 TOP 10"
```

Omit `--message` for interactive multi-turn mode.

Verbose mode (show tool calls and intermediate steps on stderr):

```bash
python3 scripts/chat.py -v \
  --instance-id $INSTANCE_ID \
  --secret-id $SECRET_ID --secret-key $SECRET_KEY \
  --message "查询ap-shanghai的MySQL实例"
```

For internal dev gateway (no signing needed):

```bash
python3 scripts/chat.py \
  --internal \
  --instance-id $INSTANCE_ID \
  --message "SELECT 1"
```

### Step 3: Parse SSE Stream

The response is a standard SSE stream (`data: {json}\n\n`). Key event types:

| Event Object | Meaning | Action |
|-------------|---------|--------|
| (first frame, has `ChatId`) | Connection established | Store `ChatId` for multi-turn |
| `claw.tool_call` | Agent calling a tool | Display progress (optional) |
| `claw.tool_result` | Tool execution complete | Display result (optional) |
| `claw.partial` / `chat.chunk` | Text chunk | Append to output buffer |
| `claw.final` / `FinishReason=stop` | Stream complete | Close connection |
| `heartbeat` | Keep-alive (every 20s) | Ignore |
| `"Error"` key in Response | API error | Log and abort |
| `data: [DONE]` | Hard stream end | Close connection |

Concatenate all `Delta.Content` values to form the complete Agent response.

### Step 4: Integrate into Agent Framework

For Python integration with proper TC3 signing, see `references/python-integration.md`. The reference includes:
- Verified `tc3_sign()` function
- HTTP headers format
- SSE stream parsing example
- Error diagnosis table

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `InternalError` | Wrong host (used `tdai.tencentcloudapi.com`) | Switch to `tdai.ai.tencentcloudapi.com` |
| `UnknownParameter` | Body contains `AppId`/`Uin`/`OwnerUin` | Remove them; identity is from AK/SK |
| `MissingParameter` (InputContent) | Missing required field | Add `InputContent` to body |
| `AuthFailure.SignatureExpire` | Timestamp drift | Use `int(time.time())`, never `datetime.utcnow()` |
| `InvalidAuthorization` | Wrong credential_scope | Must be `YYYY-MM-DD/tdai/tc3_request` |
| Instance error in SSE | Instance not running | Go to [DatabaseClaw Console](https://console.cloud.tencent.com/tdai/claw/instance) and ensure instance is in "运行中" status |
| Connection timeout | Instance stuck | Restart instance via console, retry |

---

## TC3 Signing Checklist

When implementing TC3 signing manually (not using `scripts/chat.py`):

1. Timestamp: `int(time.time())` — never `datetime.utcnow()` (macOS timezone drift)
2. SignedHeaders must include: `content-type;host;x-tc-timestamp` (alphabetical)
3. credential_scope: `{date}/tdai/tc3_request` (service name = `tdai`)
4. Host in canonical_headers: `tdai.ai.tencentcloudapi.com` (the SSE host)
5. HTTP headers must include: `X-TC-Action`, `X-TC-Version`, `X-TC-Region`, `X-TC-Timestamp`, `Authorization`
6. Accept header: `text/event-stream`

Full signing implementation: `references/python-integration.md`

---

## Files

| Path | Purpose |
|------|--------|
| `scripts/chat.py` | Standalone CLI client — single message or interactive mode, zero external deps beyond stdlib |
| `references/python-integration.md` | Complete TC3 signing code, HTTP headers, SSE parsing, error diagnosis |
