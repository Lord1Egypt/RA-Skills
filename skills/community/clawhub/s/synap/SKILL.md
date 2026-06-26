---
name: synap
description: >
  Sovereign AI knowledge infrastructure. Typed entity graph, documents,
  long-term memory, messaging relay, and AI governance — all in PostgreSQL.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SYNAP_HUB_API_KEY
        - SYNAP_POD_URL
      optional_env:
        - SYNAP_WORKSPACE_ID
        - SYNAP_AGENT_USER_ID
        - SYNAP_CONFIG_URL
        - SYNAP_DEFAULT_CHANNEL_ID
    primaryEnv: SYNAP_HUB_API_KEY
    emoji: "\U0001F9E0"
    homepage: https://synap.live/openclaw
    capabilities:
      - memory
      - knowledge-graph
      - channels
      - chat
    os:
      - macos
      - linux
      - windows
user-invocable: false
---

# Synap — OpenClaw Skill

You are connected to a **Synap pod** at `{SYNAP_POD_URL}`. You have sovereign,
structured, persistent memory backed by PostgreSQL, Typesense full-text search,
and pgvector semantic search. Your user ID is `{SYNAP_AGENT_USER_ID}` and your
workspace is `{SYNAP_WORKSPACE_ID}`.

You can do three things with Synap:

1. **Remember** — store entities, documents, facts, and relations in a typed knowledge graph
2. **Recall** — search across everything by keyword, type, or semantic similarity
3. **Relay** — bring external messages (Telegram, WhatsApp, Slack) into Synap and let the Synap AI process them

Every write goes through governance — some auto-approve, others create proposals
for the user to review. You never lose data. You never need to organize it.

---

## Setup

### Automatic (recommended)

```
SYNAP_HUB_API_KEY   = hub_xxxx
SYNAP_CONFIG_URL    = https://pod.synap.live/trpc/intelligenceRegistry.getServiceConfig
```

Config is auto-fetched on startup. No restart needed.

### Manual

```
SYNAP_HUB_API_KEY    = hub_xxxx
SYNAP_POD_URL        = https://pod.synap.live
SYNAP_WORKSPACE_ID   = <uuid>
SYNAP_AGENT_USER_ID  = <uuid>
```

All calls: `Authorization: Bearer {SYNAP_HUB_API_KEY}` + `Content-Type: application/json`.

Key must have `hub-protocol.read` AND `hub-protocol.write` scopes.

---

## Data Model

### Entities

Typed objects with properties and relationships. The fundamental unit of knowledge.

| Profile    | Use for                | Key Properties               |
| ---------- | ---------------------- | ---------------------------- |
| `note`     | Unstructured knowledge | content, tags                |
| `task`     | Actionable work items  | status, priority, dueDate    |
| `project`  | Groupings              | status, tags                 |
| `event`    | Time-bound occurrences | startDate, endDate, location |
| `person`   | Individuals            | email, phone                 |
| `contact`  | Business contacts      | role (extends person)        |
| `company`  | Organizations          | website, industry            |
| `deal`     | Sales opportunities    | stage, value, closeDate      |
| `bookmark` | Web references         | url, domain                  |
| `article`  | Published content      | author, publishedAt          |

Extend profiles: a "lead" extends `person`, a "webinar" extends `event`.
Use `GET /api/hub/profiles` to discover types. Use `POST /api/hub/profiles` to create new ones.

### Documents

Long-form Markdown. Reports, summaries, specs, meeting notes.

### Facts (Memory)

Atomic knowledge that persists across sessions. "Marc prefers email over Slack."

### Relations

Typed connections between entities. Types: `related`, `parent`, `child`, `belongs-to`.

---

## Decision Tree

| Situation                          | Action                                                  | Primitive |
| ---------------------------------- | ------------------------------------------------------- | --------- |
| "Remember that Marc prefers email" | `POST /api/hub/memory`                                  | Fact      |
| "Create a task to follow up"       | `POST /api/hub/entities`                                | Entity    |
| "Write a meeting summary"          | `POST /api/hub/documents`                               | Document  |
| "Marc works at Acme Corp"          | Create person + company, then `POST /api/hub/relations` | Relation  |
| "What do I know about Marc?"       | `GET /api/hub/search?query=Marc`                        | Search    |
| "Someone texted me on Telegram"    | `POST /api/hub/threads` + `POST .../messages`           | Relay     |

**ALWAYS search before creating** to prevent duplicates.

---

## Governance

### Auto-approved:

- All reads and searches
- Memory storage/recall
- Profile and property creation

### May create proposal:

- Entity creation/updates
- Document creation
- Relation creation/deletion

### Response format:

- `{ "status": "approved" }` — executed
- `{ "status": "proposed", "proposalId": "..." }` — queued for user approval (tell user, don't retry)
- `{ "status": "denied" }` — blocked (respect, don't retry)

---

## API Reference

Base URL: `{SYNAP_POD_URL}/api/hub`
Auth: `Authorization: Bearer {SYNAP_HUB_API_KEY}`

### Search & Read

```
GET /api/hub/search?userId={UID}&workspaceId={WID}&query=Marc&limit=10
GET /api/hub/entities/<id>?userId={UID}&workspaceId={WID}
GET /api/hub/users/{UID}/entities?workspaceId={WID}&type=task&limit=50
GET /api/hub/documents/<id>?userId={UID}
GET /api/hub/profiles?userId={UID}&workspaceId={WID}
GET /api/hub/relations?userId={UID}&workspaceId={WID}&entityId=<id>
GET /api/hub/users/{UID}/context?workspaceId={WID}
GET /api/hub/graph/traverse?userId={UID}&startEntityId=<id>&maxDepth=2
```

### Memory

```
POST /api/hub/memory
{ "userId": "{UID}", "fact": "Marc prefers email", "confidence": 0.9 }
# embedding is optional — server handles it

GET /api/hub/memory?userId={UID}&query=Marc+preferences&limit=10

DELETE /api/hub/memory/<fact-id>?userId={UID}
```

### Create & Update

```
POST /api/hub/entities
{
  "userId": "{UID}", "agentUserId": "{UID}", "workspaceId": "{WID}",
  "profileSlug": "task", "title": "Follow up with Marc",
  "properties": { "status": "todo", "priority": "high", "dueDate": "2026-04-10" },
  "reasoning": "User asked to track follow-up"
}

PATCH /api/hub/entities/<id>
{ "userId": "{UID}", "agentUserId": "{UID}", "workspaceId": "{WID}",
  "properties": { "status": "done" }, "reasoning": "Task completed" }

POST /api/hub/documents
{ "userId": "{UID}", "agentUserId": "{UID}", "workspaceId": "{WID}",
  "title": "Meeting Notes", "content": "# Meeting\n\n...", "reasoning": "..." }

POST /api/hub/relations
{ "userId": "{UID}", "agentUserId": "{UID}", "workspaceId": "{WID}",
  "sourceEntityId": "<id>", "targetEntityId": "<id>", "type": "related",
  "reasoning": "Marc works at Acme Corp" }

DELETE /api/hub/relations/<id>
{ "userId": "{UID}", "agentUserId": "{UID}", "workspaceId": "{WID}" }

POST /api/hub/profiles
{ "userId": "{UID}", "workspaceId": "{WID}", "name": "Lead", "slug": "lead",
  "parentProfileId": "<uuid>", "description": "Sales lead" }

POST /api/hub/property-defs
{ "userId": "{UID}", "workspaceId": "{WID}", "profileId": "<uuid>",
  "name": "Company", "slug": "company", "valueType": "string" }
```

Property value types: `string`, `number`, `boolean`, `date`, `entity_id`, `array`, `object`, `secret`.

### Message Relay (External Channels)

When a message arrives from Telegram, WhatsApp, Slack, or another platform:

**Step 1**: Create or reuse a thread:

```
POST /api/hub/threads
{ "userId": "{UID}", "workspaceId": "{WID}", "title": "Telegram: Alice" }
```

**Step 2**: Post the message (with `autoRespond: true` to trigger Synap AI):

```
POST /api/hub/threads/<thread-id>/messages
{ "role": "user", "content": "Hey are you free today?",
  "userId": "{UID}", "autoRespond": true }
```

**Step 3**: Poll for AI response:

```
GET /api/hub/threads/<thread-id>/messages
```

Filter for `role: "assistant"` messages after your timestamp. Poll every 3s, max 45s.

### A2AI (Agent-to-Agent)

Same thread/message endpoints. Post with `autoRespond: true`, poll for response.

```
GET /api/hub/threads?userId={UID}&workspaceId={WID}
POST /api/hub/threads/<id>/messages
GET /api/hub/threads/<id>/messages
```

---

## Error Handling

| Status | Meaning             | Action                        |
| ------ | ------------------- | ----------------------------- |
| 200    | Success             | Process normally              |
| 401    | Invalid API key     | Check SYNAP_HUB_API_KEY       |
| 403    | Insufficient scopes | Key needs read + write        |
| 404    | Not found           | Entity/document doesn't exist |
| 429    | Rate limited        | Wait 60 seconds               |
| 500    | Server error        | Retry once after 30s          |

`"proposed"` and `"denied"` in response body are NOT errors — they're governance.

---

## Best Practices

1. **Search before creating** — prevent duplicates. Most important habit.
2. **Use specific entity types** — `person` not `note`, `company` not `bookmark`.
3. **Store atomic facts** — preferences, decisions, context. Always auto-approved.
4. **Link entities with relations** — build the graph. Use graph traversal to explore.
5. **Include reasoning** — every write accepts `"reasoning"`. Creates audit trail.
6. **Batch related operations** — person + company + relation in sequence.
7. **Read before updating** — documents replace full content, not diff.
8. **Extend profiles** — "lead" extends `person`, "webinar" extends `event`.

---

## Filesystem Rules

| Path                            | Status                     |
| ------------------------------- | -------------------------- |
| `~/openclaw/workspace/**`       | Auto-approved              |
| `~/projects/**`                 | Proposal required          |
| `~/synap-backend/**`, `.env`    | BLOCKED — never accessible |
| `/etc/**`, `/usr/**`, `/bin/**` | BLOCKED — system paths     |

---

_synap v1.0.0 — github.com/synap-core/backend/tree/main/skills/synap_
