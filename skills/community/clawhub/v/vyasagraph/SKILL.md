---
name: vyasagraph
description: "No more agentic amnesia. Gives your agent short-term + long-term memory: hot survivable context + knowledge graph for permanent recall. Semantic search, graph relations, no server required."
metadata:
  {
    "openclaw":
      {
        "homepage": "https://github.com/minopop/vyasagraph",
        "repository": "https://github.com/minopop/vyasagraph",
        "license": "MIT",
        "requires": { "bins": [] },
        "optionalEnv": ["OPENAI_API_KEY"],
        "envNotes":
          {
            "OPENAI_API_KEY": "Optional. Used for semantic vector embeddings (text-embedding-3-small). Without it, VyasaGraph falls back to keyword search. Only embeddings requests are sent to OpenAI — no user conversation data.",
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "vyasagraph",
              "bins": [],
              "label": "Install VyasaGraph from npm (source: github.com/minopop/vyasagraph)",
            },
          ],
      },
  }
---

# VyasaGraph — Persistent Agent Memory

**🇶🇦 Proudly built in Qatar 🇶🇦 — make ❤️ not 🚀**

Most AI agents are amnesiac by design — every conversation starts from zero. VyasaGraph changes that. It's an embedded knowledge graph that lets your agent remember people, decisions, and relationships, then find them later by *meaning* — not just keywords. No server to run, no infrastructure to maintain. Just drop it in and your agent goes from stateless to genuinely context-aware.

**Because memory is what separates a tool from a colleague.**

**VyasaGraph = No more Agentic Amnesia**

---

## 🧠 Dual-Layer Memory System

**What gives VyasaGraph superpowers?**

---

**1. SHORT TERM MEMORY** — RAM layer. Instant access to current-session context. Survives context compaction. Written before every response.

- 🔥 Holds *hot, in-flight context*: what's happening right now, decisions made this session, things to remember before the next compaction
- 🛡️ Survives context window resets (compaction) because it's a file, not just tokens
- 📝 Think of it as a *write-ahead log* — the agent writes to it continuously so nothing is lost mid-session

---

**2. LONG TERM MEMORY** — Hard drive layer. Permanent knowledge graph with semantic search, graph relations, and project tracking. Persists across sessions.

- 🗄️ An *embedded SurrealDB database* (no server needed — it's a local file)
- 🧠 Stores *permanent knowledge*: entities, relations between them, past decisions, errors, project state
- 🔍 Query it with natural language and it finds all relevant memories — full native semantic search

---

VyasaGraph does this all automatically. No need to tell it to do anything memory-related.

---

## Why Two Layers?

| | SESSION-STATE | VyasaGraph |
|---|---|---|
| **Speed** | Instant (file read) | ~5–100ms |
| **Scope** | Current session | All sessions |
| **Purpose** | Hot context, write-ahead log | Permanent knowledge |
| **Survives compaction?** | ✅ Yes (plain file) | ✅ Yes |
| **Semantic search?** | ❌ No | ✅ Yes (HNSW vectors) |
| **Best for** | Pending tasks, decisions in flight | People, projects, history |

---

## Features

- 🗂️ **Multi-model database** — Graph + Document + Vector in one embedded engine

- 🔍 **Semantic search** — HNSW-indexed 1536-dim embeddings (cosine similarity). Search by *meaning*, not just keywords

- 🕸️ **Graph relations** — Native SurrealDB graph edges with traversal (`works_at`, `reports_to`, `owns`, etc.)

- 📋 **Project management** — Built-in task board with status, priority, and next-action tracking (v3)

- 🐛 **Error tracking** — Verrors system: log recurring issues as entities, detect patterns over time (v4)

- ⚡ **Zero infrastructure** — Embedded RocksDB, no server needed. Just a local file

- 🔌 **MCP-compatible API** — Drop-in replacement for MCP memory operations

- 🟢 **Node.js 18+** — ES Modules, works anywhere Node runs

---

## 🔒 Security & Privacy

**What this skill does with your data:**

- 📁 **Local only** — all data is stored in files on your machine (`memory.db`, `SESSION-STATE.md`). Nothing is sent to external servers except OpenAI embedding calls (if you set `OPENAI_API_KEY`).
- 🔑 **OpenAI API key** — used only to generate text embeddings. Embeddings are computed from entity observations (facts you explicitly store), not from raw conversation messages. The text sent to OpenAI is what you have written into VyasaGraph entities — not the full conversation transcript. Omit the key entirely to use keyword search only.
- 🌐 **No telemetry** — VyasaGraph makes no outbound network calls except to the OpenAI embeddings API when a key is configured.
- 📦 **Open source** — full source code at https://github.com/minopop/vyasagraph. Review it before installing.

**What you should NOT store in VyasaGraph:**

- ❌ API keys, passwords, or credentials
- ❌ Payment card or financial account details
- ❌ Health or medical records
- ❌ Any data you would not want stored in a local unencrypted file

**Memory is opt-in by design.** The instructions in this skill tell the agent *when* to record information, but you control what data you share with your agent. The agent only stores what you tell it — it does not scrape, intercept, or auto-collect data from other sources.

**Retention:** `SESSION-STATE.md` is designed to be cleared at session end. `memory.db` is permanent until you delete it. To erase all memory: delete `memory.db`.

---

## Setup

```bash
npm install vyasagraph
```

Copy the SESSION-STATE template to your workspace root:

```bash
cp node_modules/vyasagraph/SESSION-STATE-TEMPLATE.md SESSION-STATE.md
```

Set your OpenAI API key (for semantic embeddings — text search works without it):

```bash
# .env
OPENAI_API_KEY=sk-...
```

---

## Wire into your agent

Add this to your **MEMORY.md** (or equivalent instruction file):

```markdown
## FIRST ACTION EVERY MESSAGE — MANDATORY
1. READ `SESSION-STATE.md` for hot context from current session
2. WRITE to SESSION-STATE.md BEFORE responding if user gives new decisions, deadlines, or context
   - Update "Last updated" timestamp on every write
   - Clear completed tasks from Pending Actions
3. SEARCH VyasaGraph: `const results = await vg.smartSearch('topic', 5);`
4. THEN respond with loaded context

## AUTO-RECORD — EVERY CONVERSATION
When the user shares substantive information, record it in that same reply:
- New facts about people → addObservations()
- Decisions or strategies → createEntities() + addObservations()
- New relationships → createRelations()
- Status changes → updateEntity()

Rule: If the user tells you something you didn't know before, write it to VyasaGraph
in that same reply. Do not wait for end of session.

## SESSION-STATE vs VyasaGraph
- SESSION-STATE = CPU cache (hot, ephemeral, write-ahead log, session scope)
- VyasaGraph = hard drive (permanent, semantic search, cross-session knowledge)
- Both required. Neither replaces the other.

## Key Paths
- VyasaGraph DB: `./memory.db`
- SESSION-STATE: `./SESSION-STATE.md`
```

Add this to your **SOUL.md**:

```markdown
## Memory System
I use a two-layer memory stack:
1. SESSION-STATE.md — working memory for the current session. I read this at the
   start of every message and update it before responding with anything important.
   This is how I remember what we were doing when context compresses.
2. VyasaGraph — long-term knowledge graph. Stores entities (people, projects,
   decisions) with relations and semantic vector search. I search this for context
   on every substantive message.

If the user tells me something I didn't know before, I write it to VyasaGraph
in that same reply. I do not defer to end-of-session.
```

---

## Basic Usage

```javascript
import * as vg from 'vyasagraph/src/index.js';

// Initialize (creates memory.db if it doesn't exist)
await vg.init('memory.db');

// Store knowledge
await vg.createEntities([{
  name: 'Alice (user)',
  entityType: 'Person',
  observations: ['Software engineer', 'Based in Berlin', 'Prefers concise answers']
}]);

// Create relationships
await vg.createRelations([{
  from: 'Alice (user)',
  to: 'Acme Corp',
  relationType: 'works_at'
}]);

// Add facts as you learn them
await vg.addObservations([{
  entityName: 'Alice (user)',
  contents: ['Leading the platform redesign project', 'Deadline: end of Q2']
}]);

// Semantic search — finds by meaning, not just keywords
const results = await vg.smartSearch('software engineering Berlin', 5);

// Always close
await vg.close();
```

---

## Search

```javascript
// ✅ Always use smartSearch — semantic + name boosting
const results = await vg.smartSearch('project management strategy', 10);

// Text fallback (no embeddings needed)
const found = await vg.searchText('Berlin engineer', 5);

// Open specific entities by name
const entities = await vg.openNodes(['Alice (user)', 'Bob (colleague)']);

// Full graph export
const { entities, relations } = await vg.readGraph();

// Stats
const stats = await vg.getStats();
// { entityCount: 42, relationCount: 18 }
```

---

## Project & Task Tracking (v3)

Built-in task board — track projects with status, priority, and next actions:

```javascript
await vg.createEntities([{
  name: 'P01 - Website redesign',
  entityType: 'Project',
  observations: ['Modernise the company website'],
  metadata: {
    status: 'Active',        // Not Started | Active | On Hold | Blocked | Complete
    priority: 'High',        // High | Medium | Low
    category: 'Work',        // Work | Personal
    nextAction: 'Finalise wireframes by Friday'
  }
}]);

// Update when done
await vg.updateEntity('P01 - Website redesign', {
  metadata: { status: 'Complete', completedAt: new Date().toISOString() }
});

// Get formatted markdown task board
const board = await vg.formatAsVtasks();
```

---

## Error Tracking (v4 verrors)

Log recurring errors as entities — build a pattern library over time:

```javascript
await vg.createVerror({
  subsystem: 'cron_daily_brief',
  errorType: 'timeout',
  errorMessage: 'Daily brief timed out after 30s',
  impact: 'User did not receive morning update'
});

// Check unresolved issues
const unresolved = await vg.getUnresolvedVerrors();

// Mark resolved
await vg.resolveVerror('ERR-123456 (cron timeout, 2025-01-15)', 'Increased timeout to 60s');
```

---

## Naming Conventions

Descriptive names = better semantic search:

```javascript
// Person: Name (aliases, role, relationship)
'Alice Johnson (Alice, Head of Engineering, reports to Bob)'

// Project: ID + name
'P01 - Website redesign'

// Document: Name (type, date)
'Q1 Strategy (board presentation, 2025-Q1)'
```

---

## Entity Types

Always set `entityType`:
- `Person` — individuals
- `Project` — tracked work (with metadata)
- `Document` — written artefacts
- `Analysis` — analytical outputs
- `Communication` — messages, threads
- `Error` — verrors (auto-managed)

---

## Tech Stack

- **SurrealDB** — embedded graph database
- **RocksDB** — storage engine (reliable on all platforms, no config needed)
- **HNSW** — approximate nearest-neighbour vector index (cosine similarity)
- **OpenAI** — text-embedding-3-small (1536 dimensions)
- **Node.js 18+** — ES Modules

---

## Full Docs

- **GitHub**: https://github.com/minopop/vyasagraph
- **npm**: https://www.npmjs.com/package/vyasagraph
- **INSTALL.md** (bundled with package) — full wiring guide for all agent platforms
- **ARCHITECTURE.md** (bundled) — technical deep-dive
