---
name: sombra-ai-reader-mode
description: Persistent reader mode for AI. Save web pages, organise into collections, distil to dense context, and serve it all through MCP.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - npx
emoji: "📚"
homepage: https://sombra.so
---


# Sombra — Reader Mode for AI

Persistent reader mode for AI. Give your OpenClaw agent a research library that lasts between sessions. Save permanebt copies of web pages as pristine markdown, organise them into collections, distil the important parts, and access it all through MCP.

## What this skill does

Sombra is an MCP server that provides your agent with persistent knowledge management. Instead of starting every session from scratch, your agent reads from a curated library of web pages, notes, and distilled context that you (or the agent) have built up over time.

- **Save** web pages as clean markdown with ads, nav, and layout stripped out
- **Organise** into collections scoped to projects or tasks
- **Distil** collections into dense context summaries that preserve code blocks verbatim
- **Search** across everything you've saved
- **Version history** on every change, so you can roll back if the agent rewrites something you preferred

## Setup

### 1. Get a Personal Access Token

Sign up at [sombra.so](https://sombra.so) and create a token in **Settings > Access Tokens**.

### 2. Configure OpenClaw

Add Sombra to your `openclaw.json`:

```json
{
  "mcpServers": {
    "sombra": {
      "command": "npx",
      "args": ["-y", "sombra-mcp", "--token", "sombra_pat_YOUR_TOKEN_HERE"]
    }
  }
}
```

Replace `sombra_pat_YOUR_TOKEN_HERE` with your actual token.

> Check [sombra.so/mcp](https://sombra.so/mcp) for the latest connection instructions.

Sombra supports OAuth 2.1 for interactive clients and Bearer tokens for headless agents.

### Also works with

Sombra is a standard MCP server (Streamable HTTP transport) that works with any MCP client:

- **Claude Desktop / Claude.ai** — add as a connector in Settings > Connectors
- **Claude Code** — `claude mcp add --transport http sombra https://sombra.so/mcp`
- **ChatGPT** — add as an app in Settings > Apps (Developer mode)
- **Cursor, VS Code, Windsurf** — add as an MCP server in your MCP config

Full setup instructions: [sombra.so/mcp](https://sombra.so/mcp)

## Available tools (19)

### Save & Create

| Tool | Purpose |
|------|---------|
| `save_url` | Save a web page by URL. Re-fetches and updates if previously saved |
| `create_artifact` | Create a new note artifact with markdown content |

### Read & Browse

| Tool | Purpose |
|------|---------|
| `browse_collections` | Browse your collections returning title, id, and description |
| `read_collection` | Read the full content from a specific collection |
| `read_collection_context` | Read the distilled context/summary from a collection |
| `fetch_artifact` | Fetch a single artifact by ID |
| `browse_notes` | Browse all note artifacts, sorted by most recent first |
| `search_artifacts` | Search saved artifacts by title, content, or URL |
| `list_archived` | List all archived (deleted) artifacts |

### Update & Organise

| Tool | Purpose |
|------|---------|
| `update_artifact` | Update an artifact's metadata or content (notes only) |
| `move_artifact` | Move a single artifact to a different collection |
| `bulk_move_artifacts` | Move multiple artifacts to a different collection at once |
| `remove_from_collection` | Remove an artifact from a collection (back to unsorted) |
| `create_collection` | Create a new collection |
| `update_collection` | Update a collection's name, description, or icon |
| `write_collection_context` | Write distilled context/summary to a collection. Preserves all code verbatim |

### Delete & Restore

| Tool | Purpose |
|------|---------|
| `delete_artifact` | Delete an artifact (archives it, content is preserved) |
| `delete_collection` | Delete a collection (archives it, artifacts are preserved) |
| `restore_artifact` | Restore a previously deleted artifact |

Deletes are never permanent. All deleted items can be recovered.

## Prompts (2)

| Prompt | Purpose |
|--------|---------|
| `distill_collection` | Generate a context-engineered distillation prompt for a collection |
| `distill_technical_collection` | Specialised distillation for collections with heavy technical content |

## Resources

Each collection is exposed as an MCP resource with the URI scheme `sombra://project/{id}`.

## Recommended workflows

### Research before coding

Before starting a task, have your agent read the relevant collection context:

```
Read the distilled context from my "Pedestal Migration" collection,
then implement the HTTP handler changes based on those docs.
```

The agent gets dense, accurate context instead of relying on training data.

### Build a research collection

Ask your agent to research a topic and organise what it finds:

```
Research rate limiting approaches for Clojure web services.
Save the most useful pages to a new "Rate Limiting" collection,
then write a distilled context summarising the key approaches.
```

The research persists between sessions. Tomorrow's session picks up where today's left off.

### Save discoveries during work

When your agent finds something useful mid-task, it can save it:

```
That blog post about the transit encoding bug was helpful.
Save it to my "API Performance" collection.
```

### Prevent agent drift

Agent drift happens when your AI gradually diverges from correct behaviour because its context is stale or incomplete. Sombra prevents this by giving your agent access to verified, current documentation instead of months-old training data.

Before a coding session:
```
Read the context from my "API Integration" collection.
Use those docs as the source of truth for endpoint URLs
and auth flows. Do not rely on your training data.
```

## Tips

- **Scope collections tightly.** "EU e-invoicing integration" beats "Work stuff". One collection per project or task.
- **Distil aggressively.** Forty pages of raw docs in context is noise. Five hundred tokens of distilled context with code examples verbatim is signal.
- **Let context compound.** Have your agent save useful discoveries back to the collection. Each session makes the next one better.
- **Use context before code.** Always read the collection context before generating code against external APIs or libraries.

## Links

- [sombra.so](https://sombra.so) — sign up and manage your library
- [MCP setup docs](https://sombra.so/mcp) — setup for all clients
- [What is Sombra?](https://sombra.so/blog/what-is-sombra) — full product overview
- [Why context engineering matters](https://sombra.so/blog/context-failures) — the problem Sombra solves
