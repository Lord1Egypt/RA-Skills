---
name: upstage-studio
description: "Run document processing workflows using Upstage Document Agent API (v2) — both Studio-UI-configured agents (`agt_xxx`) and programmatically defined Agents/Configs via REST API. Handles file upload, agent/config creation, job execution, and result polling. Use when user asks to run an agent workflow, execute a Studio pipeline, create an agent or config via API, run a Document Agent job, or process documents through parse → classify → extract chains. Triggers on '에이전트 워크플로우 돌려줘', 'Studio 파이프라인 실행해줘', 'Document Agent API', 'config 생성해줘', 'create agent', 'run job'."
homepage: https://console.upstage.ai/studio
---

# Upstage Studio / Document Agent API

Run multi-step document processing workflows via the Upstage Document Agent API (v2). Two paths:

1. **Studio UI path** — visually configure a workflow at [console.upstage.ai/studio](https://console.upstage.ai/studio), then call the resulting Agent ID (`agt_xxx`) from your code.
2. **API-only path** — create Agents and Configs (workflows) programmatically via REST. See `references/agents-and-configs.md`.

Both paths execute the same way: upload a File → run a Job → poll for results.

## Quick Start (End-to-End, Studio UI Path)

```python
import os
import time
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["UPSTAGE_API_KEY"],
    base_url="https://api.upstage.ai/v2"
)

# 1. Upload file
file = client.files.create(
    file=open("document.pdf", "rb"),
    purpose="user_data"
)

# 2. Create workflow job
job = client.responses.create(
    model="agt_BxcRatEWzVYH2yRNtyWynn",  # Studio Agent ID
    input=[{
        "role": "user",
        "content": [{"type": "input_file", "file_id": file.id}]
    }],
    include=["all"]  # "all": all step results, "last": final step only
)

# 3. Poll until complete
while job.status in ("queued", "in_progress"):
    time.sleep(5)
    job = client.responses.retrieve(job.id, include=["all"])

# 4. Print results
if job.status == "completed":
    for step in job.output:
        print(f"\n=== {step.model} ===")
        for content in step.content:
            print(content.text)
else:
    print(f"Job failed: {job.status}")

# 5. Cleanup
client.files.delete(file.id)
```

**API Key**: Always use `os.environ["UPSTAGE_API_KEY"]`. Get your key at [console.upstage.ai/api-keys](https://console.upstage.ai/api-keys) (keys start with `up_`).

**Base URL**: `https://api.upstage.ai` (Document Agent endpoints live under `/v2`)

---

## Core Concepts

### Resource Hierarchy

```
Agent (execution unit)
 └─ Config (workflow definition: ordered Steps + conditional branching)
     └─ Job (execution instance)
         ├─ File (input document)
         └─ Results (per-step output)
```

| Concept | Description | ID Format |
|---------|-------------|-----------|
| **Agent** | Basic unit of workflow execution. Includes library metadata, publish state, thumbnail, copy stats, and like stats | `agt_xxx` |
| **Config** | Workflow attached to an Agent. Defines Steps as a DAG with conditional branching. Immutable once created — create a new Config to change steps | `cfg_xxx` or numeric index (`"1"`, `"2"`) |
| **Step** | Individual processing stage: `document-parse`, `information-extract`, `document-classify`, `instruct` | UUID |
| **Job** | Result of executing a Config. Status: `in_progress` → `completed` / `failed` | `job_xxx` |
| **File** | Uploaded document. Automatically converted to page images on upload | `file_xxx` |

### Basic Usage Flow

```
1. Upload file        POST /v2/files                 → get file_id
2. Create Agent       POST /v2/agents                → get agent_id   (skip if using Studio UI)
3. Define Config      POST /v2/agents/{id}/configs   → define workflow (skip if using Studio UI)
4. Run Job            POST /v2/responses             → execute pipeline
5. Get results        GET /v2/responses/{id}         → retrieve output
```

### Execution Modes

| Mode | Setting | Behavior |
|------|---------|----------|
| Synchronous | (default) | Waits until completion, returns JSON |
| Background | `background: true` | Returns Job ID immediately, poll for results |

Agents with `agt_` prefix automatically use `background: true`.

### Status Values

| Status | Description |
|--------|-------------|
| `queued` | Waiting to start |
| `in_progress` | Processing |
| `completed` | Finished |
| `failed` | Error occurred (check `failure_message`) |

---

## Common Patterns

### Cursor Pagination

Applied to all list endpoints (`/v2/files`, `/v2/agents`, `/v2/agents/{id}/jobs`, etc.).

| Parameter | Type | Description |
|-----------|------|-------------|
| `after` | string | Return items after this ID |
| `before` | string | Return items before this ID |
| `limit` | int (≥1) | Maximum number of items |
| `order` | `"asc"` \| `"desc"` | Sort by `created_at` (default: `"asc"`) |

Response shape:
```json
{ "object": "list", "data": [...], "first_id": "xxx", "last_id": "yyy", "has_more": true }
```

### Error Response

All errors share the same structure:

```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "No access to agent: agt_xxx",
    "param": "agent_id",
    "code": null
  }
}
```

| HTTP | Type | Description |
|------|------|-------------|
| 400 | `invalid_request_error` | Bad request (missing fields, type mismatch, step validation failure) |
| 404 | `not_found_error` | Non-existent ID |
| 409 | `file_status_error` | State conflict (creating Job with file still being processed) |
| 415 | `unsupported_file_format` | Uploading e.g. `.zip` |
| 500 | `internal_server_error` | Server error |

---

## Output Files

- **Default (full job result)**: write to `<system-temp>/<input-stem>.agent.json` (e.g., `/tmp/document.agent.json`).
- **Default (per-step results)**: write each step's output to `<system-temp>/<input-stem>.<step-name>.json` (e.g., `/tmp/document.document-parse.json`, `/tmp/document.information-extract.json`).
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path(s)** in your response so the user can locate the file(s).

## Tips

- Agent IDs start with `agt_`. Find yours in the Studio UI or list via `GET /v2/agents`.
- Use `include=["all"]` to get intermediate step results for debugging; `["last"]` for final output only.
- Uploaded files can be reused across multiple agents. Delete after processing to save storage.
- Configs are **immutable** — to modify a workflow, create a new Config.
- Always use **v2** base_url, not v1.
- For multi-API pipelines outside of Studio, see `upstage-builder`.
- For dedicated schema generation (without an agent wrapper), see `upstage-schema-generation`.
- For dedicated standalone classification, see `upstage-document-classification`.

---

## Detailed References

| File | Content |
|------|---------|
| `references/files.md` | Files API: upload, get, delete, supported formats, file status, errors |
| `references/agents-and-configs.md` | Agent CRUD, library metadata, publish/unpublish, thumbnails, likes, Config (workflow) definition with conditional branching |
| `references/step-types.md` | Step parameters: `document-parse`, `document-classify`, `information-extract`, `instruct`, schema rules |
| `references/preset-agents.md` | Built-in agents (`schema-generate`, `class-generate`, `schema-update`) — no agent setup required |
| `references/jobs.md` | Run Jobs, poll, list, delete, status values, execution errors, caching, stats API |
| `references/examples.md` | Full end-to-end curl examples (parse→extract, classify→branch, split, instruct chaining, clone, publish, like) |
