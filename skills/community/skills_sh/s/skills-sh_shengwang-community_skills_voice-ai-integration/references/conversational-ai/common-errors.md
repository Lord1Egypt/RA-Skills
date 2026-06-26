# Common Errors & Diagnosis

## Diagnosis Flow

```
Got an error?
    │
    ├─ HTTP 400 → Check field types (agent_rtc_uid string? remote_rtc_uids array?)
    ├─ HTTP 403 → ConvoAI not enabled, or wrong credentials
    ├─ HTTP 404 → Agent not found / already stopped
    ├─ HTTP 409 → Duplicate agent name → use new unique name or existing agent_id
    ├─ HTTP 422 → Quota exceeded → request increase in Console
    ├─ HTTP 502/503/504 → Retry with exponential backoff
    └─ Agent FAILED state → Check LLM/TTS connectivity, then recreate agent
```

---

## Error Reference

### 400 — Invalid Request

Most common causes:

| Symptom | Fix |
|---------|-----|
| `agent_rtc_uid` type error | Must be string `"0"`, not int `0` |
| `remote_rtc_uids` type error | Must be array `["*"]`, not string `"*"` |
| `channel not found` | RTC channel must exist before agent joins — have a user join first, or pre-create |
| Missing `tts` field | Required when using standard text LLM |
| `enable_string_uid` conflict | Cannot mix int and string UIDs in the same channel |

### 403 — Forbidden

1. ConvoAI service not enabled → Shengwang Console → enable ConvoAI for your project
2. Wrong `SHENGWANG_CUSTOMER_KEY` or `SHENGWANG_CUSTOMER_SECRET` → regenerate in Console
3. `SHENGWANG_APP_ID` in URL doesn't match the credentials project

### 404 — Agent Not Found

- Agent was never successfully created (check `/join` response)
- Agent already stopped or destroyed
- Wrong `agentId` in URL path (note: `/join` returns `agent_id` in body, use that as path param)

### 409 — Conflict (Duplicate Name)

Agent with same `name` already exists in this project.

**Fix options:**
1. Extract `agent_id` from the 409 error response body and reuse it
2. Generate a new unique name: `agent_{uuid[:8]}` and retry

```json
// 409 error body — extract agent_id if present
{
  "detail": "create agent failed, code: 409, msg: task conflict",
  "reason": "TaskConflict"
}
```

### 422 — Quota Exceeded

Concurrent agent limit reached. Options:
1. Stop idle agents via `POST /agents/{agentId}/leave`
2. Request quota increase in Shengwang Console

### 502 / 503 / 504 — Gateway / Timeout

Transient server-side errors. Always retry:

```python
import time

def create_agent_with_retry(payload, max_retries=3):
    for attempt in range(max_retries):
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code in (200, 201):
            return resp.json()
        if resp.status_code in (503, 504):
            time.sleep(2 ** attempt)  # 1s, 2s, 4s
            continue
        resp.raise_for_status()
    raise Exception("Max retries exceeded")
```

---

## Agent FAILED State

When `GET /agents/{agentId}` returns `"status": "FAILED"`:

1. Check `message` field — it contains the exit reason
2. Common causes:
   - LLM endpoint unreachable or returned error
   - TTS vendor API key invalid or quota exceeded
   - ASR vendor connectivity issue
3. Fix the underlying cause, then call `POST /agents/{agentId}/leave` to clean up
4. Create a new agent with `POST /join`

---

## Agent Not Responding to Voice

Agent is RUNNING but not responding to user speech:

1. Confirm user is in the **same RTC channel** as the agent
2. Confirm `remote_rtc_uids` includes the user's UID (or is `["*"]`)
3. Check ASR language matches user's spoken language
4. Check `idle_timeout` — if too short, agent may have stopped
5. Check LLM endpoint is reachable from Shengwang's servers (not localhost)

---

## Additional Error Lookup

For errors not covered here, fetch the relevant endpoint doc URL from
[convoai-restapi/index.mdx](convoai-restapi/index.mdx) for response schemas, or search
`references/docs.txt` for broader doc lookup:

```
1. Search docs.txt for relevant doc URL
2. Fetch the URL to get full doc content
```
