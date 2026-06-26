# Execution Protocol

Every BNBTown (XTown) skill follows this 4-step protocol.

## Step 1: Submit Task

```http
POST $XTOWN_SERVER_URL/agent/task
Authorization: Bearer <UNIBASE_PROXY_AUTH>
Content-Type: application/json

{
  "session_token": "<token>",
  "skill_id": "<skill_id>"
}
```

→ The agent character moves to the building on the map. Wait for status `awaiting_params`.

## Step 2: Confirmation

Review the owner's intent and ask for confirmation of exact parameters. Refer to the skill's reference file (e.g. `swap.md`, `lend.md`) for parameter schemas.

## Step 3: Execute

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
Content-Type: application/json

{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": { ... }
}
```

**Note**: Some skills use different param shapes. CMC uses `tool_name` + `tool_args`; Meme Rush uses `method` + `params`. See each skill's reference file.

## Step 4: Poll Result

```http
GET $XTOWN_SERVER_URL/agent/task?task_id=<id>&session_token=<token>
Authorization: Bearer <UNIBASE_PROXY_AUTH>
```

**Status flow**: `pending` → `walking` → `awaiting_params` → `executing` → `completed` | `failed`
