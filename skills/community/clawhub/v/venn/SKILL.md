---
name: venn
description: >-
  Search, describe, and execute enterprise tools (Jira, Salesforce, Gmail, Slack,
  Google Calendar, Google Drive, GitHub, Notion, Box, etc.) via the Venn tool-router
  REST API. Use when the user asks to: (1) query or search data in enterprise SaaS
  apps, (2) create, update, or manage records (tickets, emails, calendar events,
  documents), (3) automate multi-step workflows across connected services, or
  (4) check what integrations are available. Triggers on phrases like "check my Jira
  tickets", "search Slack", "create a Salesforce lead", "find emails from X",
  "sync data between apps", or any reference to connected enterprise tools.
metadata: {"openclaw": {"requires": {"env": ["VENN_API_KEY"]}, "primaryEnv": "VENN_API_KEY"}}
---

# Venn Tools

Connect to enterprise SaaS tools through the Venn platform REST API.

## Setup

This skill is gated on `VENN_API_KEY` — it won't appear until the key is set.

1. Get your API key from [app.venn.ai](https://app.venn.ai/api-keys)

2. Add it to the OpenClaw `.env` file:
   ```bash
   echo 'VENN_API_KEY=your-api-key-here' >> ~/.openclaw/.env
   ```

3. Restart the gateway (picks up the new env on start):
   ```bash
   openclaw gateway restart
   ```

   Or, for zero-downtime reload without restart:
   ```bash
   openclaw secrets reload
   ```

Alternatively, use the interactive secrets helper:
```bash
openclaw secrets configure --skip-provider-setup
```

**Sandboxed agents:** The `.env` file injects into the host process only. For sandboxed (Docker) sessions, also add `VENN_API_KEY` to `agents.defaults.sandbox.docker.env` in `openclaw.json`, or bake it into your custom sandbox image.

## Configuration

- `VENN_API_KEY` (required) — your Venn API key
- `VENN_API_URL` (optional) — defaults to `https://app.venn.ai/api/tooliq`

## Request Format

All requests use POST with JSON. Examples below use this shorthand:

```bash
# Full form (shown once):
VENN_URL="${VENN_API_URL:-https://app.venn.ai/api/tooliq}"
curl -s -X POST "${VENN_URL}/tools/search" \
  -H "Authorization: Bearer ${VENN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query": "..."}'

# Shorthand (used throughout):
# POST /tools/search {"query": "..."}
```

---

## 1. Discovery

### List connected servers

```bash
# POST /tools/help
{"action": "list_servers"}
```

Returns `result.servers[]` with `server_id`, `name`, and `connection_status`.

Other help actions:
- `getting_started` — onboarding guidance
- `connector_help` — info on connectors (pass `server_id` for specific one)
- `auth_helper` — OAuth re-auth URL for disconnected server (requires `server_id`)

### Search for tools

```bash
# POST /tools/search
{"query": "jira search issues", "limit": 10}
```

Returns `result.candidates[]` with `server_id`, `tool_name`, `short_description`, and (for top results) full `inputSchema`.

Additional parameters: `offset`, `min_score` (0–1, default 0.3), `min_results` (default 5), `include_skills` (default true).

**Search strategy — broad first, narrow if needed:**

1. Start with the **full task description** in natural language (skills match better):
   - "create a linear ticket and set it to in progress"
   - "sync salesforce contacts to a google sheet"

2. If no skill matches, **decompose** into one search per platform + action:
   - "query salesforce contacts" + "create google sheets row"

3. For simple single-platform tasks, search directly: "create salesforce lead"

**Splitting rules:**
- 1 search = 1 platform + 1 action (no single tool handles compound actions)
- Always include the app name in each query
- "recap"/"summarize" → search the platform, then present
- "cross-reference"/"compare" → search each platform, combine results
- "sync X to Y" → search source, then destination

**If no results**, try alternate names:
- "jira" → "atlassian"
- "google docs" → "google-drive" or "googledocs"
- "github" → "github-cloud"

**Choosing from results:**
- Read operations → prefer broad query tools over get-by-ID
- Create/update → look for specific create/update endpoints
- If a skill appears (`type="skill"`), prefer it over assembling tools
- `inputSchema` is the source of truth for parameter names — NEVER guess

For platform-specific query syntax (JQL, SOQL, Gmail search), see [references/query-syntax.md](references/query-syntax.md).

### Describe a tool

```bash
# POST /tools/describe
{"tools": [{"server_id": "SERVER_ID", "tool_name": "TOOL_NAME"}]}
```

Supports batch requests. Returns `result.results[]` with `inputSchema`, `description`, and `write_operation` type.

---

## 2. Execution

### Schema adherence (most common source of errors)

1. Copy parameter names **verbatim** from inputSchema — casing matters
   - Schema says `maxResults` → use `maxResults`, NOT `max_results`

2. Match data types exactly:
   - `"type": "string"` → `"10"`, NOT `10`
   - `"type": "integer"` → `10`, NOT `"10"`
   - `"type": "array"` → `["value"]`, NOT `"value"`
   - `"type": "object"` → `{"key": "value"}`, NOT `"key=value"`

3. Include all `required` fields. Do not add fields not in the schema.

### Execute a single tool

```bash
# POST /tools/execute
{"server_id": "SERVER_ID", "tool_name": "TOOL_NAME", "tool_args": {...}}
```

**Translating user intent into values** (infer rather than ask):
- "recent tickets" → reasonable date range (e.g., last 7 days)
- "my emails" → `userId: "me"`
- "the main channel" → search for it by name first
- "current sprint" → the active sprint

This applies to **values only** — parameter names and types must come from inputSchema.

**Data integrity:** NEVER fabricate data. Only present what appears in actual responses.

**Handling links:** For create/edit operations, surface clickable URLs from fields like `url`, `link`, `href`, `web_url`, `permalink`, `html_url`. Present as `[Resource Name](url)`.

### Execute a workflow (multi-step)

Chain multiple tool calls in a Python sandbox:

```bash
# POST /tools/execute-workflow
{
  "code": "results = call_tool(\"atlassian\", \"searchByJQL\", jql=\"assignee = currentUser() AND status != Done\")\nreturn [{\"key\": i[\"key\"], \"summary\": i[\"fields\"][\"summary\"]} for i in results.get(\"issues\", [])]",
  "timeout": 180
}
```

**When to use workflows:**
- Multiple tool calls in sequence
- Parallel execution across services
- Data processing, iteration, or transformation

**Code rules:**
- Follow schema adherence rules above
- Write flat, inline code — no helper functions
- Code must return a value; extract only needed fields
- Check for errors: `if isinstance(result, dict) and "error" in result: ...`
- For pagination, loop until no more `nextPageToken`/`cursor`

**Available in sandbox:**
- `call_tool(server_id, tool_name, **kwargs)` — sequential
- `async_call_tool(server_id, tool_name, **kwargs)` — for `asyncio.gather()`
- `call_skill(skill_id, inputs_dict)` / `async_call_skill(...)` — call skills
- Modules: `asyncio`, `json`, `datetime`, `math`, `re`, `collections`, `itertools`, `functools`, `operator`, `decimal`, `uuid`, `base64`, `hashlib`
- No network, filesystem, or subprocess access
- No augmented assignment on subscripts: use `d[k] = d[k] + 1`, NOT `d[k] += 1`

---

## 3. Write Operation Confirmation

Write/delete operations return an audit response instead of executing. To proceed:

1. Show the operation summary to the user and **wait for explicit approval**

2. Get a confirmation token (expires in 60s):
   ```bash
   # POST /tools/confirm
   {"server_id": "SERVER_ID", "tool_name": "TOOL_NAME"}
   ```

3. Re-send with the token:
   ```bash
   # POST /tools/execute
   {"server_id": "...", "tool_name": "...", "tool_args": {...}, "confirmed": true, "confirmation_token": "TOKEN"}
   ```

**Never** call confirm without user's typed approval ("yes", "confirm", "proceed").

---

## 4. Skills

Skills are pre-built workflow patterns in search results with `type: "skill"`. Prefer skills over assembling individual tools.

### Executable skills

Marked `executable: true`. Run step-by-step:

```bash
# POST /tools/execute
{"tool_name": "SKILL_ID", "tool_args": {"step_id": "FIRST_STEP", "inputs": {...}}}
```

Each step returns `outputs` and `next`. If `next` is not null, read `next.reasoning`, fill placeholders, make the next call.

### Guidance skills

For skills without `executable: true`, describe to get the pattern:

```bash
# POST /tools/describe
{"tools": [{"tool_name": "SKILL_NAME"}]}
```

Returns `tools_involved`, `all_servers_connected`, `disconnected_servers`, and step-by-step `content`. If `all_servers_connected` is false, use `help(action="auth_helper")` first.

---

## 5. Error Recovery

If a tool call fails, **debug and retry** — do not report failure immediately.

| Error | Action |
|-------|--------|
| Schema/parameter error | Re-read inputSchema, fix names and types, retry |
| 404 / "not found" | Wrong ID or tool; search for correct ID |
| Server not connected / 401 | Call `help(action="auth_helper", server_id="...")` |
| Empty results | Try fuzzy variations, broader date ranges |
| Same error twice | Try different approach (different tool/parameters) |
| Workflow fails twice | Fall back to sequential execute calls |

Only report failure after at least three different approaches have been tried.

---

## Guardrails

- Start with `list_servers` or `search` to discover what's connected
- Always have `inputSchema` before executing (from search or describe)
- Match parameter names and types exactly
- Never fabricate data — only present actual responses
- Never execute writes without explicit user approval
- Prefer workflows for multi-step operations
- Prefer skills over assembling individual tools
- Pass `session_id` and `user_intent` on calls for tracing (API generates one if omitted)

