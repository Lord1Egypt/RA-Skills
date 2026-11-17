---
name: xmemory
description: Persistent structured memory — save, recall, and update facts, decisions, people, and projects across sessions via the xmemory MCP server.
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: XMEM_API_KEY
    envVars:
      - name: XMEM_API_KEY
        required: true
        description: Your xmemory API key (create one at https://console.xmemory.ai).
      - name: XMEM_INSTANCE_ID
        required: true
        description: The xmemory instance to read from and write to (a UUID).
    homepage: https://xmemory.ai
    emoji: "🧠"
---

# xmemory memory

xmemory is a first-party memory store: it holds the data you explicitly save to your xmemory
instance, in xmemory's own backend. It does **not** read the assistant's built-in memory, your
past chat history, or your files, email, or cloud drives — it only stores and returns what is written to this instance.

Use xmemory to remember durable facts across sessions (people, preferences, decisions, project
state) and to answer questions from what was saved earlier.

## Setup (one-time)

Register the xmemory MCP server with OpenClaw, using your API key as a static bearer token on the
instance shortcut URL — no OAuth needed:

```bash
openclaw mcp add xmemory \
  --url "https://mcp.xmemory.ai/instance/$XMEM_INSTANCE_ID" \
  --transport streamable-http \
  --header "Authorization: Bearer $XMEM_API_KEY"

openclaw mcp doctor xmemory --probe    # confirm reachability + list tools
```

Keep `XMEM_API_KEY` in your host environment rather than committing it into config.

### Multiple instances at once

A server binds **one** instance (the one in its `/instance/<ID>` path). To use several at once,
add one named server per instance:

```bash
openclaw mcp add xmemory-work     --url "https://mcp.xmemory.ai/instance/<work-id>"     --transport streamable-http --header "Authorization: Bearer $XMEM_API_KEY"
openclaw mcp add xmemory-personal --url "https://mcp.xmemory.ai/instance/<personal-id>" --transport streamable-http --header "Authorization: Bearer $XMEM_API_KEY"
```

### Instance management (optional, admin connection)

To create / list / delete instances and manage schemas, add the **admin** connection (`/admin`).
Its tools include destructive operations (e.g. deleting an instance), so register it deliberately:

```bash
openclaw mcp add xmemory-admin --url "https://mcp.xmemory.ai/admin" \
  --transport streamable-http --header "Authorization: Bearer $XMEM_API_KEY"
```

## When to use

- The user asks you to remember / save something, or says "don't forget".
- The user asks what you know about a person, project, or topic, or to recall something earlier.
- Proactively: persist durable facts the user will want later. Don't save throwaway context.

## How to use (xmemory MCP tools)

- **`write_async`** — preferred write path. Save create / update / delete intent in natural
  language ("Alice's email is alice@acme.com", "forget the Friday meeting"); returns immediately.
- **`write`** — synchronous write; use only when you must read the same data back in the same turn.
- **`read`** — query the instance in natural language (lookups, aggregations, listings).

Call `write_async` to remember and `read` to recall — the instance is bound by the URL path, so
you do not pass an instance id in tool calls.

### Advanced

Beyond the core loop, the instance also exposes:

- **`write_status`** — diagnostic; check once (never poll) if a read that should contain written
  data comes back unexpectedly empty.
- **`get_instance_id`**, **`get_instance_schema`** — the connected instance's ID and its
  object/field/relation schema.
- **Schema evolution** — the engine proposes schema improvements from real read traffic.
  `review_suggestions` is **read-only** (it changes nothing) — surface the proposals to the user
  judiciously (never nag). `decide_suggestions` then `apply_pending_decisions` record the user's
  choices and commit them as a migration, so **always confirm with the user before deciding or
  applying**.
- **Schema management** (opt-in) — `update_instance_schema`, `dry_run_schema_migration`,
  `list_schema_migrations`, `get_schema_migration`, `enhance_schema`: direct schema edits; confirm
  with the user before applying any change.
