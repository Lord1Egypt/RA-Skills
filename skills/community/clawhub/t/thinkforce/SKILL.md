# ThinkForce Missions API — Skill for AI Agents

You are operating an instance of ThinkForce, a multi-agent orchestration platform. This skill teaches you how to **manage Missions and Subtasks (steps)** on behalf of a user. Read all sections before acting; follow the decision rules in section 14.

Base URL: `https://app.thinkforce.ai`. Every request needs the header `X-TF-API-Key: <user_api_key>`. The user's `companyId` must be in every request body (and as a query param on GETs).

---

## 0. Bootstrap — discovering the user's `companyId`

You almost never receive `companyId` upfront. Resolve it once at session start, cache it, and reuse on every subsequent call.

### Primary method — `GET /api/companies`

The API key encodes which company you're operating on. Hit this endpoint first:

```http
GET /api/companies
X-TF-API-Key: <key>
```

Response:

```json
{
  "companyId": "abc123",
  "name": "ABC Luxury Car Service",
  "status": "active",
  "industry": "transportation",
  "goal": "...",
  "agentCount": 7
}
```

`companyId` here is what you pass on every other request. If this call returns 401, the key is invalid — stop and tell the user.

### Bootstrap pattern (run this first, every session)

```
1. GET /api/companies → save { companyId, name, agentCount }
2. (optional) GET /api/missions?companyId=<id> → see what missions already exist
3. (optional) GET /api/companies/<id>/agents → see which agents you can assign
4. Now you're ready to create / decompose / run missions.
```

### What NOT to do

- ❌ Don't ask the user for their `companyId` — the API key already binds you to one.
- ❌ Don't guess or hard-code it.
- ❌ Don't call `GET /api/companies` on every action — cache the result for the session.
- ❌ Don't try to switch companies mid-session by passing a different `companyId` — the key won't authenticate against a different company and you'll get 401.

---

## 1. Mental model

- **Mission** = a project. Has a title, description, status, priority, optional budget, optional schedule.
- **Subtask** (a.k.a. **Step**) = a unit of work inside a mission. Has an assigned agent, a status, optional `runInstructions`, and dependency edges.
- Subtasks form a **DAG** via `dependsOn[]` (upstream) and `nextSubtaskIds[]` (downstream). When a subtask completes, its `nextSubtaskIds` are auto-chained.
- Each subtask can override the agent's default toolbelt, connectors, skills, and files **just for that step**.
- Missions can be scheduled (cron) or triggered by a webhook hitting a specific subtask.
- Missions can be **shared** (clone) or **invited** (real-time collab via Y.js).

You manage state by calling REST endpoints. Never assume state — always GET fresh data before deciding.

---

## 1.5. Finding and assigning agents

Every subtask needs an `assignedAgentId` before it can run. `POST /api/missions/<id>/subtasks/<sid>/run` returns HTTP 400 (`"Assign an agent before starting this step"`) without one. This section tells you how to discover agents and pick the right one.

### List the company's agents

```http
POST /api/agents
X-TF-API-Key: <key>
Content-Type: application/json

{ "action": "list", "companyId": "<id>" }
```

Response:

```json
{
  "success": true,
  "total": 5,
  "agents": [
    {
      "id": "agt_abc123",
      "agentName": "Acme CEO",
      "agentRole": "You are the CEO. You plan missions, coordinate other agents, and review final outputs...",
      "agentType": "office",
      "model": "claude-opus-4-7",
      "provider": "anthropic",
      "reasoningEffort": "high",
      "enabledTools": ["function-Web_Search", "function-Code_Assistant", "function-Memory_Manager"],
      "selectedTools": [{ "type": "function", "function": { "name": "Web_Search", "description": "...", "parameters": {...} } }, ...],
      "mcpConnections": [],
      "officeState": "idle",
      "workspaceSync": null,
      "createdAt": "...",
      "updatedAt": "..."
    }
  ],
  "message": "Agents retrieved successfully"
}
```

Note: the response is wrapped (`{ success, agents, total, message }`), NOT a bare array. Read `data.agents`.

### Real agent schema (what's actually there)

| Field             | What it is                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| `agentName`       | Short display name (e.g. "Market Researcher", "Driver Recruitment Agent"). The primary handle.   |
| `agentRole`       | **Free-text system prompt** for the agent — often paragraphs long. NOT a short role label.       |
| `agentType`       | Internal type marker (`office` for normal in-office agents, often `null` for legacy/custom).     |
| `model`           | Model id the agent runs on (`claude-opus-4-7`, `deepseek/deepseek-v4-flash`, etc.).              |
| `enabledTools[]`  | Array of strings like `"function-Web_Search"` — which tools are toggled on for this agent.       |
| `selectedTools[]` | The full OpenAI-style tool objects (mirrors `enabledTools` but with definitions). Use for inspection only — for matching, prefer `enabledTools`. |
| `mcpConnections[]`| Array of MCP connector ids the agent has access to.                                              |
| `officeState`     | UI animation state: `idle | working | researching | syncing`. Not a routing signal.              |
| `provider`        | LLM provider key (`anthropic`, `openrouter`, `deepseek`, ...).                                   |

**Fields that DO NOT exist on agents** (don't try to match on them): `name`, `description`, `tags`, `capabilities`, `tools`, `status`, `config`. Older docs reference these — they were never on the schema.

### What to match on

When you need to assign an agent to a subtask, match in this order:

1. **`agentName`** — the only short, human-meaningful label. Match by substring: `"researcher"`, `"designer"`, `"copywriter"`, `"marketer"`. This is your primary signal.
2. **`agentRole` substring** — grep the system prompt for domain keywords (`"video"`, `"copy"`, `"frontend"`, `"recruit"`, `"compliance"`). Slower than `agentName` matching but catches agents whose name is generic.
3. **`enabledTools[]`** — if the subtask needs `Design_Agent` to run, you MUST assign an agent that already has `"function-Design_Agent"` in `enabledTools`. Per-step tool attachment was removed — an agent only ever uses its own enabled toolbelt — so tool fit is decided entirely by which agent you assign.
4. **`model`** — only relevant if the user explicitly asked for "the Claude agent" or "the fast one"; otherwise ignore.

There is no `status` field — every agent the API returns is dispatchable. There is no `inactive` or `archived` state.

### Decompose does NOT auto-assign

When you call `POST /api/missions/<id>/decompose`, the planner returns subtasks shaped like:

```json
[
  { "title": "Research top 5 competitors", "workstationKey": "researching" },
  { "title": "Draft content calendar",     "workstationKey": "working" }
]
```

Each subtask comes back **without** an `assignedAgentId`. The runner refuses to start unassigned subtasks (`status === 'queued'`), so you must PATCH one before calling `/run`.

**`workstationKey` is NOT a role hint.** It's the office UI's animation/cubicle assignment for showing the agent avatar in the right workstation while the step runs (`working | researching | syncing | error`). The decomposer LLM picks one of those four buckets per subtask, but it carries no signal about which *agent* should run the step. Pick agents by `agentName` + `agentRole` substring, not by `workstationKey`.

### Assign an agent to a subtask

```http
PATCH /api/missions/<id>/subtasks/<sid>
{
  "companyId": "<id>",
  "assignedAgentId": "agt_def456"
}
```

That's it. Once assigned, the subtask flips `queued → assigned` and is ready for `/run`.

### Reassigning mid-mission

You can change `assignedAgentId` at any time *unless* the subtask is currently `in_progress` (in which case stop it first via the pause/cancel endpoint, then reassign and re-run). Reassigning a `done` step has no effect — the output is already cached.

### Coordinator agent fallback

If the user doesn't pick a planner for auto-decompose, the system uses `mission.coordinatorAgentId` — and that defaults to the company's CEO agent (the agent created first during onboarding, with `agentRole: "CEO"`). The CEO is always present, so you can always fall back to it when no other agent fits.

### Recipe — assign agents to a freshly decomposed mission

```
1. GET /api/companies → companyId
2. POST /api/agents { action:"list", companyId } → agents[]
3. POST /api/missions/<id>/decompose { companyId } → subtasks (unassigned)
4. GET /api/missions/<id>/subtasks → confirm IDs + titles
5. For each subtask:
     // Match by title keywords against agentName + agentRole
     pick agent = agents.find(a => {
       const hay = ((a.agentName || '') + ' ' + (a.agentRole || '')).toLowerCase();
       return subtask.title.toLowerCase().split(/\W+/).some(w => w.length > 3 && hay.includes(w));
     }) || ceoAgent;
     PATCH subtasks/<sid> { companyId, assignedAgentId: agent.id }
6. POST subtasks/<root sid>/run → auto-chain handles the rest
```

### Rules

- **Prefer specialists over the CEO.** The CEO is a fine fallback but is optimized for coordination, not specialized work.
- **Don't pick the same agent for every step.** If `dependsOn` siblings (steps that could run in parallel) all share one agent, you lose parallelism — the agent processes them serially. Spread the load.
- **Pick an agent that already has the tools.** Per-step tool attachment was removed — an agent only ever uses its own `enabledTools`. If no agent has the tool a step needs, enable that tool on an agent (or create/pick one that has it) rather than trying to attach it to the subtask.
- **Never invent agent IDs.** If `POST /api/agents { action:"list" }` returns no agents that fit, fall back to the CEO — don't fabricate.
- **Don't use `workstationKey` to pick the agent.** It's an office-animation field, not a routing signal. See above.

---

## 2. Statuses you must respect

**Mission status**: `planning | active | paused | completed | failed | cancelled | needs_attention`

- `needs_attention` is terminal-for-automation: the mission coordinator reviewed the mission but couldn't confirm the goal was met within its pass budget, so it froze the mission for a human instead of looping. Read `coordinatorEscalatedReason` for why. The workflow will NOT auto-advance from here — a human (or you, on the user's instruction) decides what to do.

**Subtask status**:

| Status              | Meaning                                                     | You can run it? |
| ------------------- | ----------------------------------------------------------- | --------------- |
| `queued`            | Created, no agent assigned                                  | No — assign first |
| `assigned`          | Agent assigned, waiting                                     | Yes             |
| `in_progress`       | Currently executing                                         | No — wait       |
| `done`              | Completed successfully                                      | No — already done |
| `failed`            | Errored out                                                 | Yes (retry)     |
| `blocked_upstream`  | A depended-on step failed OR finished with tool errors; this never ran | No — fix upstream first |

**`done` ≠ clean.** A subtask can be `status: done` but carry `completedWithErrors: true` + a `lastError` of "Completed with tool errors" — it produced output but a tool inside it failed (e.g. emitted MISSING URLs, a generation 402'd). The auto-chain will NOT fire that step's `nextSubtaskIds` — it marks them `blocked_upstream` instead, so a dirty-done step never silently triggers downstream work. When inspecting a `done` step, always check `completedWithErrors` before trusting its output.

**Rule:** Never POST `/run` on a subtask whose `dependsOn` ids aren't all `done`. The server returns HTTP 409 with `pendingDeps` if you try.

---

## 3. Endpoint catalog (what to call, when)

| Goal                                  | Endpoint                                                       |
| ------------------------------------- | -------------------------------------------------------------- |
| Create a mission                      | `POST /api/missions`                                           |
| List missions                         | `GET /api/missions?companyId=...`                              |
| Read one mission                      | `GET /api/missions/<id>?companyId=...`                         |
| Update mission metadata               | `PATCH /api/missions/<id>`                                     |
| Delete mission                        | `DELETE /api/missions/<id>?companyId=...`                      |
| Auto-decompose into subtasks          | `POST /api/missions/<id>/decompose`                            |
| Add a subtask manually                | `POST /api/missions/<id>/subtasks`                             |
| List subtasks                         | `GET /api/missions/<id>/subtasks?companyId=...`                |
| Update a subtask                      | `PATCH /api/missions/<id>/subtasks/<sid>`                      |
| Run a subtask                         | `POST /api/missions/<id>/subtasks/<sid>/run`                   |
| Cancel a subtask (terminal)           | `POST /api/missions/<id>/subtasks/<sid>/cancel`                |
| Pause a subtask (non-terminal)        | `POST /api/missions/<id>/subtasks/<sid>/pause`                 |
| Resume a paused subtask               | `POST /api/missions/<id>/subtasks/<sid>/resume`                |
| Cancel a mission (terminal)           | `POST /api/missions/<id>/cancel`                               |
| Pause a mission                       | `POST /api/missions/<id>/pause`                                |
| Resume a paused mission               | `POST /api/missions/<id>/resume`                               |
| List skills (for `attachedSkillIds`)  | `POST /api/skillManager { action:"list", companyId }`          |
| List MCPs (for `attachedConnectorIds`)| `POST /api/mcpManager   { action:"list", companyId }`          |
| List agents (for `assignedAgentId`)   | `POST /api/agents       { action:"list", companyId }`          |
| Share (read/clone)                    | `POST /api/missions/<id>/share`                                |
| Invite (live collab)                  | `POST /api/missions/<id>/invite`                               |
| List members + open invites           | `GET /api/missions/<id>/invite?companyId=...`                  |
| Revoke a member                       | `DELETE /api/missions/<id>/invite?companyId=...&uid=<uid>`     |

---

## 3.5. The one-call `manager` endpoint (and its auto-dispatch caveat)

Everything in the catalog above is the **granular REST flow** — create, then decompose/add subtasks, then assign, then wire the DAG, then run the root. There is also a single action-dispatch endpoint that does create-with-subtasks-and-launch in one POST:

```http
POST /api/missions/manager
X-TF-API-Key: <key>
Content-Type: application/json
```

| `action`            | What it does                                                                 |
| ------------------- | --------------------------------------------------------------------------- |
| `create_mission`    | Create a mission + (optionally) its subtasks in one call.                   |
| `add_subtask`       | Append a subtask to an existing mission.                                    |
| `update_subtask`    | Write a subtask's `status` / `output` (agents call this to record results). |
| `complete_mission`  | Mark complete + trigger the debrief.                                        |
| `list_missions`     | List recent missions.                                                       |
| `get_mission`       | Read one mission + its subtasks.                                            |
| `dispatch_subtask`  | Re-dispatch an existing subtask to its assigned agent.                      |

`create_mission` body:

```json
{
  "action": "create_mission",
  "companyId": "<id>",
  "title": "<short title>",
  "description": "<one-paragraph problem statement>",
  "priority": "high",
  "subtasks": [
    { "title": "<step>", "assignedAgentId": "<agent id OR agentName>", "workstationKey": "working" }
  ],
  "maxSteps": 45            // optional per-subtask step budget, forwarded to the runner
}
```

`assignedAgentId` resolves by **agent id OR `agentName`** (the server looks it up). Auth is the same company-scoped `X-TF-API-Key` (or a Firebase token); reads allow viewers, writes require editor.

### ⚠️ Caveat: assigned subtasks auto-dispatch IMMEDIATELY, in PARALLEL

`create_mission` (and `add_subtask`) **fires `/run` on every subtask that has a resolved `assignedAgentId` the moment it's created — all at once, with NO sequencing and NO `dependsOn` wiring.** This endpoint does not build a DAG. So if you create a "generate frames" step and a "stitch the frames" step together, both launch simultaneously and the stitch step races ahead with nothing to stitch and fails.

**Rules:**

- Use `manager.create_mission` only when the subtasks are **independent** (safe to run in parallel), or when you pass **exactly one** subtask.
- For **sequential / dependent** work, do one of:
  1. Make it a **single end-to-end subtask** (one agent does step A then step B in one run) — simplest and race-free; or
  2. Use the **REST flow**: `POST /api/missions` (no subtasks) → add subtasks → PATCH `dependsOn`/`nextSubtaskIds` → `POST .../subtasks/<root>/run`. Only the REST flow gives you DAG ordering.
- `manager` is a convenience for fan-out; the granular REST flow (§4–§8) is the controllable path. When in doubt, prefer REST.

---

## 4. Create a mission

```http
POST /api/missions
X-TF-API-Key: <key>
Content-Type: application/json

{
  "companyId": "<id>",
  "title": "<short title>",
  "description": "<one-paragraph problem statement>",
  "priority": "low" | "medium" | "high",      // optional, default medium
  "tokenBudget": 50000,                        // optional, null = unlimited
  "schedule": "0 9 * * MON",                   // optional cron
  "scheduleLabel": "Weekly Monday 9am",        // optional UI label
  "scheduleEnabled": true                      // optional
}
```

Returns `{ id, status: 'planning', subtaskIds: [], progress: 0 }`.

**Rule:** Always write a real description — the decomposer reads it. "Do the thing" produces garbage subtasks.

---

## 5. Decompose vs. manual planning

You have two ways to build subtasks. Choose based on the user's intent:

### A. Auto-decompose (use when the user gives a high-level goal)

```http
POST /api/missions/<id>/decompose
{ "companyId": "<id>", "agentId": "<optional planner agent id>" }
```

This calls a planner agent, which writes a `planSnapshot` and creates the subtasks. The latest plan is at `mission.latestPlanSnapshotVersion`. Snapshots are versioned — you can re-decompose without losing history.

### B. Manual subtask creation (use when the user has a specific step in mind)

```http
POST /api/missions/<id>/subtasks
{
  "companyId": "<id>",
  "title": "<what this step does>",
  "assignedAgentId": "<agent id>",            // optional but required before running
  "runInstructions": "<step-specific nudges>", // optional free text
  "dependsOn": ["<upstream sid>", ...],         // optional DAG edges
  "nextSubtaskIds": ["<downstream sid>", ...],  // optional DAG edges
  "attachedSkillIds": [...],                   // optional, see §7
  "attachedConnectorIds": [...]                // optional, see §7
}
```

Returns the created subtask with its new `id`.

**Rule:** If the user describes a sequence ("first do X, then Y, then Z"), create the subtasks then PATCH `dependsOn` to wire them. Never expect the decomposer to know the user's ordering preference.

---

## 6. Wiring the DAG

Two arrays form the graph; keep them in sync:

```json
// In S2:
{ "dependsOn": ["S1"] }

// In S1:
{ "nextSubtaskIds": ["S2"] }
```

Common shapes:

| Shape       | How to wire                                                                |
| ----------- | -------------------------------------------------------------------------- |
| Sequence    | Chain `dependsOn`: A → B → C                                               |
| Fan-out     | A.nextSubtaskIds = [B, C, D]; each downstream lists A in dependsOn         |
| Fan-in/diamond | D.dependsOn = [B, C]; D runs only after both finish                    |

**Rule:** When the user adds a new step "after" another, PATCH both the new step's `dependsOn` AND the upstream step's `nextSubtaskIds`. Forgetting one half breaks auto-chain.

---

## 7. Per-step attachments

Each subtask can override its agent's defaults *just for this step*. **Always discover the legal values before setting these fields — see §7.5 for the list endpoints.**

### Skills

```json
{ "attachedSkillIds": ["skill_video_script", "skill_brand_voice"] }
```

Skill bodies get injected into the agent's prompt as `[Attached skills]` context.

### Tools

Per-step tool attachment has been **removed**. An agent always uses its own
`enabledTools` toolbelt and picks which tool to call from its instructions — the
API silently ignores `attachedToolNames`. To give a step a specific tool,
**assign an agent that already has that tool enabled** (see §1 → "What to match
on"). There is no per-subtask tool allow-list.

### MCP Connectors (allow-list)

```json
{ "attachedConnectorIds": ["mcp_linear", "mcp_supabase"] }
```

Same pattern: non-empty filters the connector set; empty = agent's defaults.

### Files

Mission-level files (`mission.attachments[]`) are wired via the file's `linkedSubtaskIds` array — set it to the subtask IDs that should receive that file at run time. Upload files via the dashboard UI; you typically don't create them directly via API.

**Rule:** If the user asks "give the step access to X", pick the right bucket:
- Documentation/context for the LLM → Skill
- Capability/tool to invoke → Tool
- External data source → Connector
- File payload (PDF, image, dataset) → linked attachment

---

## 7.5. Discovering legal attachment values

Before you set `attachedSkillIds` or `attachedConnectorIds` on a subtask, you must list what's available. Never invent IDs — the runner silently drops unknown ones, leaving the step under-equipped. (Tools are NOT attachable per-step; see "Tool names" below.)

### List skills

```http
POST /api/skillManager
X-TF-API-Key: <key>
Content-Type: application/json

{ "action": "list", "companyId": "<id>" }
```

Response:

```json
{
  "success": true,
  "action": "list",
  "message": "Found N saved skill(s).",
  "skills": [
    {
      "id": "summarize-url-or-file_installed_1779298872483",
      "name": "Summarize URL or File",
      "description": "Summarize or extract transcripts from URLs, YouTube videos, articles, PDFs and local files.",
      "category": "research",
      "toolsUsed": ["exec"],
      "tags": ["summarize", "transcript", "youtube"],
      "version": 1,
      "executionCount": 0,
      "successRate": 0,
      "averageRating": 0,
      "createdAt": "2026-05-20T17:36:41.849Z"
    }
  ]
}
```

The `id` field is what you pass into `attachedSkillIds[]`.

### List MCP connectors

```http
POST /api/mcpManager
{ "action": "list", "companyId": "<id>" }
```

Response:

```json
{
  "success": true,
  "action": "list",
  "connections": [
    {
      "id": "mcp_abc123",
      "server_label": "Linear",
      "server_url": "https://mcp.linear.app",
      "auth_type": "oauth",
      "description": "Linear issue tracker MCP",
      "enabled": true,
      "tools": ["create_issue", "list_issues", "update_issue"],
      "toolSchemas": { "create_issue": { "description": "...", "inputSchema": {...} } }
    }
  ],
  "count": 1,
  "message": "..."
}
```

Pass `connections[].id` into `attachedConnectorIds[]`. Use `{ "action": "list_platform" }` instead for platform-default MCPs available to every company without setup.

### Tool names (for matching agents)

The canonical list of tool names is the `AGENT_TOOLS` constant in `lib/agentTools.ts` — there is no public REST endpoint that returns it. Tools are NOT attachable per-step; use these names to recognize what a step needs and to pick an agent whose `enabledTools` already includes it.

Common built-in tool names, so you can recognize what a step needs and match it to an agent that has it:

| Tool name              | What it does                                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| `Web_Browser`          | Cloud headless browser (browser-use). Autonomous, set-and-forget. See §7.6.                   |
| `User_Browser`         | Interactive E2B desktop browser with VNC stream + screenshot-to-PNG-data-URL. See §7.6.        |
| `Website_Fetch`        | Read/extract content from a URL (no browser).                                                  |
| `Web_Search`           | Search the web for results.                                                                    |
| `Researcher`           | Long-running multi-source research                                                        |
| `Design_Agent`         | Image-first design generation/iteration.                                                       |
| `Image_Generation`     | Single-image generation (gpt-image-2 / fal models).                                            |
| `Video_Generation`     | Video synthesis (Seedance 2.0 text/image/reference-to-video).                                  |
| `Music_Generation`     | Instrumental music bed via OpenRouter Lyria. Returns a public MP3 URL. Background mode — agent polls `Background_Task_Status` with `taskType:"music"`. |
| `Voice_Generation`     | Narration / voiceover via ElevenLabs TTS. Returns a public MP3 URL synchronously. Convenience over curl-from-sandbox: auto-uploads to Firebase Storage and surfaces a preview card. |
| `E2B_File_Manager`     | Upload/download/list files in an E2B sandbox; can publish to Firebase Storage for public URLs. |
| `Memory_Manager`       | Store/retrieve agent-scoped memory across turns.                                               |
| `Skill_Manager`        | List/install/execute skills.                                                                   |
| `MCP_Manager`          | List/invoke MCP connectors.                                                                    |
| `Get_Credentials`      | Fetch a stored credential from the vault by platform name.                                     |
| `Manage_Credentials`   | Add/update/delete vault credentials.                                                            |
| `Wait`                 | Sleep N seconds inside a tool loop (use between async polls).                                  |
| `Check_Browser_Task`   | Poll status of an async Web_Browser cloud task.                                                |
| `Background_Task_Status` | Poll any background task (video/music/browser/etc) by taskId.                                 |
| `Schedule_Task`        | Create a one-shot or cron schedule.                                                            |
                                      |

**Rule:** To run a tool-dependent step, list agents (`POST /api/agents { action:"list" }`) and read each one's `tools[]`, then assign the step to an agent whose `tools[]` already includes the tool it needs. There is no per-step tool allow-list to fall back on — if no agent has the tool, enable it on an agent (or create one) first.

### Recipe — list everything before attaching

```
1. POST /api/skillManager { action:"list", companyId } → skills[]
2. POST /api/mcpManager { action:"list", companyId } → connections[]
3. POST /api/agents { action:"list", companyId } → agents[].tools[] (assign a step to an agent whose tools[] already has what it needs)
4. PATCH the subtask with the attachments you want:
     { attachedSkillIds: [...], attachedConnectorIds: [...] }
```

---

## 7.6. Picking a browser tool — `Web_Browser` vs `User_Browser`

Both tools drive a real browser, but they're used for very different jobs. Pick wrong and the step either burns tokens or returns unusable output.

### `Web_Browser` (browser-use cloud)

- **What it is:** A cloud-hosted autonomous browser agent that takes a free-form English instruction and drives the browser unattended for several minutes.
- **Async:** Yes. Returns a `taskId` in <2s; you poll with `Check_Browser_Task` (or `Background_Task_Status`) until status `finished | failed`. **You must `Wait` between polls** — back-to-back polls hammer the dyno and burn tokens.
- **Output:** A free-form text summary + an `outputFiles[]` array of files (PDFs, screenshots) the cloud agent saved. **Caveat:** the cloud agent often saves pages as PDFs, not PNGs, and `download_url` on those files is frequently `null` because browser-use's storage endpoint 404s. Outbound uploads from the cloud sandbox to public hosts (Catbox, Litterbox, Gofile, etc.) routinely fail with `Server responded with 0 code`. **Do not rely on `Web_Browser` to produce public image URLs.**
- **Use for:** Multi-step web tasks where you need an agent to make decisions inside the browser — filling forms across pages, scraping multi-pane SPAs, completing long signup flows. Use when the *outcome* is text or data, not a media artifact.
- **Required attached tools when using it:** `Web_Browser`, `Check_Browser_Task`, `Wait`, and `Memory_Manager` (to stash the taskId so a restart doesn't lose it).

### `User_Browser` (E2B desktop, VNC stream)

- **What it is:** A real Chromium running inside an E2B sandbox with a live VNC stream you can show the user. Driven action-by-action by the agent (`open_session`, `navigate`, `click`, `type`, `screenshot`, …).
- **Async:** No — each action is synchronous and returns when complete (typical action: 1–3s).
- **Output:** Each action returns structured data: `currentUrl`, `pageTitle`, `result.dataUrl` (for `screenshot`), `result.text` (for `extract`), etc. **`screenshot` returns a base64 PNG data URL inline** — the model sees the image via vision, but the data URL is *not* a public URL Seedance or any downstream service can fetch.
- **Use for:** Any case where you need (a) the user to watch what's happening, or (b) the agent to take pixel-perfect screenshots it controls, or (c) deterministic step-by-step browser interaction. Use when the *outcome* is a media artifact (screenshot, recording, downloaded file) you'll process further.
- **Required attached tools:** `User_Browser` + `E2B_File_Manager` (to write the PNG to disk and upload it to Firebase Storage to get a public URL).

### Recipe — capture N dashboard screenshots and publish as public URLs

```
1. User_Browser({ action:"open_session", url:"https://app.example.com",
                  instructions:"Capture brand screenshots" })
   → { sessionId, sessionUrl, sandboxId }                  // stash all three

2. User_Browser({ action:"type",  sessionId, selector:"input[name=email]",    text:"<user>" })
   User_Browser({ action:"type",  sessionId, selector:"input[name=password]", text:"<pass>", submit:true })
   // (retrieve <user>/<pass> via Get_Credentials, never paste into runInstructions)

3. For each beat:
     User_Browser({ action:"navigate", sessionId, url:"https://app.example.com/dashboard/<beat>" })
     User_Browser({ action:"wait",     sessionId, selector:".dashboard-ready" })
     s = User_Browser({ action:"screenshot", sessionId })
     // The screenshot tool writes the PNG to /tmp/user_browser_<sessionId>_<ts>.png
     // inside User_Browser's E2B sandbox and returns
     // { result: { dataUrl, file_path, sandboxId } }.

     pub = E2B_File_Manager({ action:"upload_public", file_path: s.result.file_path })
     // Do NOT pass sandboxId — every User_Browser call pins its sandbox as the
     // task's persistent sandbox, so the file_manager dispatcher auto-routes
     // to the same sandbox the screenshot was written into. Passing the wrong
     // sandboxId is the single most common cause of "file does not exist"
     // failures here.
     //
     // pub.publicUrl is the Firebase Storage download URL — that's what you
     // forward to Seedance / Image_Generation / Video_Generation downstream.

4. User_Browser({ action:"stop", sessionId })   // release the sandbox

5. Emit { beat_<n>: pub.publicUrl } for each beat.
```

**Why this works:** `upload_public` runs inside the same sandbox as `User_Browser`, so it can read the screenshot file directly without copying bytes through the agent. It uploads to Firebase Storage and returns a long-lived public `https://` URL that any vendor (Seedance, Fal, OpenRouter) can fetch.

**Rule:** `User_Browser` + `E2B_File_Manager({ action:"upload_public" })` is the canonical path to turn a live page into a public PNG URL for downstream video / image steps. Do NOT use `Web_Browser` when the deliverable is a public screenshot URL — browser-use cloud's outbound public-host uploads are unreliable (Catbox / Litterbox / Gofile routinely return `Server responded with 0 code`).

---

## 8. Running a subtask

```http
POST /api/missions/<id>/subtasks/<sid>/run
{ "companyId": "<id>" }
```

What the server does:

1. **Dependency guard** — refuses with HTTP 409 if any `dependsOn` isn't `done`.
2. Builds prior-step context from the outputs of every `dependsOn` step (each truncated to 4000 chars). If no `dependsOn`, falls back to mission-order prior outputs.
3. Loads attached skills/tools/connectors/files.
4. Dispatches to the assigned agent via `/api/agent-task`.
5. Returns immediately; the run is **asynchronous**. You poll via `GET /api/missions/<id>` and `GET /api/missions/<id>/subtasks`.
6. On success: status → `done`, `tokenUsage` and `estimatedCostUsd` recorded, `nextSubtaskIds` auto-chained.
7. On failure: status → `failed`, downstream waiting steps walked BFS and marked `blocked_upstream`.

**Rule:** Never call `/run` more than once concurrently on the same subtask — it's locked (`lockedBy`, `lockedAt`). If you see `lastHeartbeatAt` older than 15 minutes, the lock is stale and a new run will reclaim it.

**Rule:** If you only need to run the *root* of a DAG, call `/run` on just that step. Auto-chain will fire every downstream once its deps complete.

---

## 8.5. Stopping / pausing / resuming work

Use the dedicated lifecycle endpoints — never `PATCH status:` directly, which skips the runner signal and may leave an in-flight loop chewing tokens until it hits its iteration cap.

The runner inside `/api/agent-task` checks for a cancel/pause flag at the start of every iteration (typically every 5–15s). The lifecycle endpoints below both (a) write the durable status to Firestore AND (b) signal the runner via `agentTaskResults/<taskId>` so the loop bails on its next check.

### Cancel a subtask (terminal)

```http
POST /api/missions/<id>/subtasks/<sid>/cancel
X-TF-API-Key: <key>
Content-Type: application/json

{ "companyId": "<id>", "reason": "<optional reason>" }
```

What happens:
- Runner gets `cancelRequested=true` and exits at its next iteration check (≤15s typical).
- Status → `cancelled` (terminal), `lockedBy`/`lockedAt` cleared.
- Downstream `assigned`/`queued` descendants are walked BFS and marked `blocked_upstream`.
- In-flight third-party tool calls (Web_Browser cloud task, Fal video job, etc.) keep running on the vendor side — local-only abort. Their results are discarded when they return.

Response: `{ success: true, cancelledSubtaskId, cascadedCount }`.

409 if the subtask is already terminal (`done`/`failed`/`cancelled`).

### Pause a subtask (non-terminal)

```http
POST /api/missions/<id>/subtasks/<sid>/pause
{ "companyId": "<id>", "reason": "<optional reason>" }
```

What happens:
- Runner gets `pauseRequested=true`. If mid-loop, it parks in `checkPauseOrCancel` and waits up to `PAUSE_MAX_WAIT_MS` for resume.
- Status → `paused`. Locks NOT cleared (so the parked runner can still own it).
- No cascade — downstream stays where it is.

409 if already `paused` or terminal.

### Resume a subtask

```http
POST /api/missions/<id>/subtasks/<sid>/resume
{ "companyId": "<id>" }
```

What happens:
- Clears `pauseRequested` on the runner doc; a parked loop wakes and continues from where it was.
- Status → `assigned`. If no parked runner is waiting (e.g. dyno restarted), call `POST .../run` to start a fresh run.

400 if subtask is not `paused`, or has no `assignedAgentId`.

### Mission-level

```http
POST /api/missions/<id>/cancel  { "companyId": "<id>", "reason": "..." }
POST /api/missions/<id>/pause   { "companyId": "<id>", "reason": "..." }
POST /api/missions/<id>/resume  { "companyId": "<id>" }
```

- **Cancel mission** marks the mission `cancelled` AND fans out cancel to every non-terminal subtask. Use when the user is done with the mission entirely.
- **Pause mission** marks the mission `paused` AND pauses every `in_progress` subtask. The auto-chain refuses to dispatch new subtasks while the mission is paused.
- **Resume mission** flips mission back to `active` and any `paused` subtasks back to `assigned`. You still need to `POST .../subtasks/<sid>/run` (or `.../resume` on each paused subtask) to actually kick the work — resuming the mission alone doesn't auto-dispatch.

### Detect zombie locks

A subtask is "live" if `status === 'in_progress'` AND `lastHeartbeatAt` is within the last 15 minutes. If `status === 'in_progress'` but `lastHeartbeatAt` is older than 15 min, the dyno died mid-run; the lock is stale and a fresh `/run` will reclaim it.

```js
const isZombie =
  subtask.status === 'in_progress' &&
  Date.now() - new Date(subtask.lastHeartbeatAt).getTime() > 15 * 60 * 1000;
```

For a zombie, prefer `POST .../subtasks/<sid>/cancel` over a raw `/run` reclaim — cancel cleans up `runDispatching`, `currentActivity`, and any descendant fanout in one call.

**Rule:** Always prefer the lifecycle endpoints over a raw `PATCH status:`. The PATCH path skips the runner signal, so an in-flight loop keeps spending tokens until it hits the next status-aware checkpoint (which may be many minutes away if it's parked in a long tool call).

---

## 9. Scheduling

### Cron (mission-level or subtask-level)

```json
PATCH /api/missions/<id>
{
  "companyId": "<id>",
  "schedule": "0 9 * * MON",
  "scheduleLabel": "Weekly Monday 9am",
  "scheduleEnabled": true
}
```

Per-subtask cron fields: `cronExpression`, `recurrenceType`, `recurrenceInterval`, `recurrenceWeekdays`, `scheduleEnabled`. Use the subtask-level cron only when one step needs a different cadence than the mission.

### Webhook trigger (subtask-level only)

```json
PATCH /api/missions/<id>/subtasks/<sid>
{
  "companyId": "<id>",
  "webhookId": "wh_abc123",
  "webhookEnabled": true
}
```

When a POST hits the webhook URL, the subtask runs with the webhook payload appended to its prompt.

---

## 10. Share & Invite

### Share — read + clone

```http
POST /api/missions/<id>/share
→ { "shareCode": "abc", "shareUrl": "https://app.thinkforce.ai/m/abc" }
```

The link gives anyone a preview; logged-in users can clone (which copies all subtasks, rewrites `dependsOn` / `nextSubtaskIds` to new IDs, preserves `runInstructions` / skills / files, resets run state, unassigns agents).

### Invite — live collaboration

```http
POST /api/missions/<id>/invite
→ { "inviteCode": "xyz", "inviteUrl": "https://app.thinkforce.ai/mi/xyz" }
```

Acceptee joins `mission.members[]` and gets a Y.js live session (cursor, node positions, selected step are synced realtime; durable edits still go through Firestore).

Revoke:
```http
DELETE /api/missions/<id>/invite?companyId=<id>&uid=<uid>
DELETE /api/missions/<id>/invite?companyId=<id>&all=1
```

**Rule:** Use **Share** when the user wants others to copy the mission. Use **Invite** when they want to work on it together.

---

## 11. Reading state

```http
GET /api/missions/<id>?companyId=<id>
```

Key fields you'll read:

- `status`, `progress` (0–100), `totalTokens`, `totalCostUsd`, `tokenBudget`
- `subtaskIds[]`, `agentIds[]`
- `coordinatorAgentId`, `coordinatorReviewedAt` (set when the coordinator approves the final output)
- `planSnapshots[]`, `latestPlanSnapshotVersion`
- `attachments[]` (each has `linkedSubtaskIds`)
- `members[]`, schedule fields

Subtasks:

```http
GET /api/missions/<id>/subtasks?companyId=<id>
```

Each subtask exposes:

- `status`, `currentActivity`, `lastHeartbeatAt`, `progressLog[]`
- `output`, `lastError`
- `tokenUsage`, `estimatedCostUsd`
- `dependsOn[]`, `nextSubtaskIds[]`
- `attachedSkillIds[]`, `attachedConnectorIds[]`
- `lockedBy`, `lockedAt`

**Rule:** When polling for completion, poll the **mission** (`status === 'completed'`) — not each subtask. The mission status reflects the rollup.

---

## 11.6. Platform-injected agent behavior (every subtask run)

Every time you POST `/api/missions/<id>/subtasks/<sid>/run`, the runner prepends a platform preamble onto the agent's own `agentRole` system prompt. Agents that don't know about these rules will still follow them — they're injected automatically. The rules currently in force:

| Rule | What it does |
|---|---|
| **EXECUTION** | Force multi-step completion — never stop after retrieving credentials, always continue to the action that uses them. |
| **SANDBOX NOTE** | E2B is non-root: `sudo apt-get install -y …`, `pip3 install …` (no sudo), npm/node/npx (no sudo). |
| **CREDENTIAL-FIRST DISCOVERY** | Before the first third-party API call, agents call `Manage_Credentials({ action: "list" })` to see what's stored, then `Get_Credentials({ platform: "<name>" })`. Skip only when the tool docs say "credentials auto-loaded" (Code_Assistant git ops, Clawd, Web_Browser cloud). Never paste credential values into output. |
| **PREFER E2B run_code** | The default first move for vendor-API calls, scripting, data work, and integrations is `E2B_File_Manager({ action: "run_code" })` — a few lines of curl/python/node is almost always more flexible than waiting for a typed tool. Typed tools (`Voice_Generation`, `Image_Generation`, `Music_Generation`, `Video_Generation`, `Web_Search`, …) are conveniences (auto-Firebase upload, preview surfaces) — reach for them only when you specifically want those platform conveniences. |
| **ASYNC TOOL PATTERN** | Set-and-forget: submit → store taskId in Memory_Manager → poll with the correct status tool. Never resubmit a job whose status is `processing`. |
| **TOOL ERROR HANDLING** | Classify before retrying: 401/403 → `Get_Credentials` then retry once; 400/422 → fix args then retry once; 429 → wait 10s then retry once; 504/ECONNRESET → retry once; everything else after one retry → stop and report. Never retry the same call with identical args twice. |

You don't need to repeat these in your `agentRole`. They're baked in for every mission subtask run. Use your `agentRole` for what's unique about each agent (domain expertise, voice, escalation rules), not for restating platform-wide tool discipline.

---

## 12. Coordinator agent (the orchestrator layer)

Each mission has a **coordinator agent** (`mission.coordinatorAgentId`, defaults to the company CEO). It is the orchestrator that runs at the *end* of a mission — after every subtask reaches a terminal state, the coordinator reviews whether the mission GOAL was actually met and either finalizes or closes specific gaps.

What it does on completion:
- Reads every subtask's output (flagging any `completedWithErrors` ones as unreliable).
- Writes a **mission debrief** to memory (`mission-debrief-<missionId>`).
- If the goal is met → declares `MISSION COMPLETE`, sets `coordinatorReviewedAt`.
- If not → may add a few **targeted follow-up subtasks** to close gaps, which then run and trigger one more review.

**Runaway guard (important).** The coordinator can add work that re-triggers the coordinator, so it is hard-capped by **pass count** (`mission.coordinatorPassCount`). The cap is **per-mission** and configurable (see below); the final pass is forbidden from adding work and must finalize with `MISSION COMPLETE` or `ESCALATE`. If it can't confirm the goal within the cap, the mission is frozen as **`needs_attention`** (never looped) with `coordinatorEscalatedReason` explaining why. Once `coordinatorReviewedAt` is set, the coordinator can never re-trigger. The review task itself is bounded (`maxSteps: 40`).

**Per-mission config** (set on the mission doc, e.g. via `PATCH /api/missions/<id>` or the Coordinator control on the brief):
- `coordinatorMaxPasses` — `0`–`5`, default `2`. `0` disables coordinator review entirely for that mission. Clamped to a hard ceiling of 5. Platform-wide default is overridable via the `COORDINATOR_MAX_PASSES` env var.
- `coordinatorAutoFollowups` — boolean, default `true`. When `false`, the coordinator only reviews + escalates and never adds subtasks (the conservative, zero-runaway mode).

Choose by stakes: a throwaway one-shot can run `coordinatorMaxPasses: 0` (skip review) or `1`; a high-stakes mission that should self-heal gets `3`+; set `coordinatorAutoFollowups: false` when you want the coordinator to flag gaps for a human rather than act on them.

You generally don't manipulate the coordinator unless the user asks ("use agent X to plan this mission" → set `coordinatorAgentId`). If a mission is `needs_attention`, surface `coordinatorEscalatedReason` to the user and ask how to proceed — do not blindly re-run it.

---

## 13. Error handling

| HTTP | Meaning                                                              | What to do                                                    |
| ---- | -------------------------------------------------------------------- | ------------------------------------------------------------- |
| 400  | `companyId required` or missing field                                | Add the missing field and retry                               |
| 401  | `Invalid or missing ThinkForce API key`                              | Stop. Tell the user their key is bad/missing                  |
| 404  | `Mission not found` / `Subtask not found`                            | Re-list to find correct id; don't guess                       |
| 409  | `Dependencies not satisfied` (`{ pendingDeps: [...] }`)              | Either run the upstream first or remove the dep               |
| 409  | `Subtask already in_progress` (lock active)                          | Wait + poll; don't double-dispatch                            |
| 5xx  | Server error                                                         | Retry once with backoff; surface to user if it persists       |

**Rule:** Never swallow errors silently. If a run fails, fetch `lastError` from the subtask and surface it to the user verbatim.

---

## 14. Decision rules (your operating contract)

Apply these rules before every action:

1. **Bootstrap first.** At session start, call `GET /api/companies` to resolve the user's `companyId`. Cache it. Pass it on every subsequent request. Never ask the user for it.

2. **Read before writing.** Always GET the mission + subtasks before deciding. State changes async (other agents, the user, schedulers).

3. **Don't invent IDs.** Subtask, mission, agent, and company IDs come from server responses. If you don't have one, GET the list and pick.

4. **Assign before running.** Every subtask needs `assignedAgentId` before `/run`. Decompose does NOT auto-assign — you must PATCH each subtask. Match agents by `agentName` + `agentRole` substring + `enabledTools`, never by guessing. CEO is the always-available fallback. See section 1.5.

5. **Respect the DAG.** Before calling `/run`, check `dependsOn` are all `done`. If not, either run the upstream first or tell the user why you can't proceed.

6. **Pick the right tool for "attach":**
   - LLM context → Skill
   - Capability → Tool
   - External data → Connector
   - File → linked attachment

7. **Don't double-run.** Check `status === 'in_progress'` and `lockedBy` before POST `/run`. Stale lock = `lastHeartbeatAt` older than 15 min.

8. **Wire both halves of the DAG.** When adding a dep, PATCH both the new step's `dependsOn` and the upstream's `nextSubtaskIds`.

9. **Auto-chain handles fan-out.** You only need to run the DAG's root(s). Don't run every step manually.

10. **Failures cascade.** When you see `blocked_upstream`, the fix is upstream — never re-run a blocked step directly. Fix the failed parent, then re-run the parent (auto-chain unblocks descendants).

11. **Budget guard.** If the mission has `tokenBudget` set and `totalTokens` is near the cap, warn the user before starting new runs.

12. **Surface progress and any cost the user has explicitly asked for.** When the user wants visibility into spend, report `mission.totalCostUsd` and per-step `estimatedCostUsd` directly from the GET response.

13. **Re-decompose carefully.** It creates a new plan snapshot but doesn't delete prior subtasks. If the user wants a clean re-plan, delete the old subtasks first.

14. **Confirm destructive actions.** Always ask before `DELETE` on a mission, revoking a member, or cancelling an in-flight run.

---

## 15. End-to-end recipe (copy this pattern)

User says: *"Set up a mission to launch the Tesla Roadster — concept, copy, hero image, 15s teaser. Run the design + copy in parallel after concept."*

You execute:

```
1. POST /api/missions {
     companyId, title: "Launch Tesla Roadster campaign",
     description: "Concept, copy, hero image, 15s teaser video",
     priority: "high"
   } → mission M1

2. POST /api/missions/M1/decompose { companyId }
   → returns subtasks S1 (concept), S2 (copy), S3 (hero image), S4 (teaser)
     Note: all UNASSIGNED. Use subtask titles + agentName/agentRole to pick.

3. POST /api/agents { action:"list", companyId } → agents[]
   → e.g. CEO, Copywriter, Designer, Video Editor

4. GET /api/missions/M1/subtasks → confirm subtask IDs + titles

5. Assign agents to each subtask:
   PATCH S1 { assignedAgentId: ceo.id }            // concept → CEO (planning)
   PATCH S2 { assignedAgentId: copywriter.id }     // copy → Copywriter
   PATCH S3 { assignedAgentId: designer.id }       // hero image → Designer
   PATCH S4 { assignedAgentId: videoEditor.id }    // teaser → Video Editor
   (Fall back to CEO for any subtask with no obvious match.)

6. Wire the DAG:
   PATCH S2.dependsOn=[S1], S1.nextSubtaskIds=[S2,S3]
   PATCH S3.dependsOn=[S1]
   PATCH S4.dependsOn=[S2,S3], S2.nextSubtaskIds=[S4], S3.nextSubtaskIds=[S4]
   (S2+S3 run in parallel after S1; S4 waits for both)

7. (Optional) Make sure S3 + S4 are assigned to an agent whose enabledTools
   include Design_Agent / Video_Generation — tools can't be attached per-step.

8. POST /api/missions/M1/subtasks/S1/run { companyId }
   (only the root; auto-chain handles S2/S3/S4)

9. Poll GET /api/missions/M1 every ~10s until status === 'completed'
   Surface progress + totalCostUsd to the user.

10. On completion, GET /api/missions/M1/subtasks, summarize S4.output
    (the final teaser) and the cost roll-up.
```

---

## 16. What NOT to do

- ❌ Don't run `/run` in a loop polling — runs are async; use status polling instead.
- ❌ Don't create subtasks without an `assignedAgentId` then immediately run them (you'll get HTTP 400).
- ❌ Don't manually flip a subtask to `done` to "skip" it — the auto-chain reads outputs, and a fake `done` produces empty context for downstream steps.
- ❌ Don't share or invite without explicit user consent — both are public surfaces.
- ❌ Don't delete `planSnapshots` thinking they're cruft — they're the audit trail.
- ❌ Don't ignore `blocked_upstream` — investigate the upstream `failed` step's `lastError`.

---

If anything in this document conflicts with what you observe in the live API, **trust the API** and tell the user what you saw. This skill is a guide, not a contract.
