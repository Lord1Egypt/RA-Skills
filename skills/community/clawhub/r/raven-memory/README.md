<p align="center">
  <img src="https://github.com/has9800/raven-memory/blob/main/raven_logo.png" 
       alt="Raven Memory" width="100%"/>
</p>


# Raven

**Persistent causal memory for AI agents.**

Raven gives your AI agent a memory that survives across sessions, days, and months. Every significant event: tool calls, decisions, user preferences, session checkpoints etc are recorded as a node in a causal chain. Your agent always knows where things stand and why.

---

## The problem

Every AI agent session starts from zero. Close the chat and your agent forgets everything. Start a new session and you're explaining yourself from scratch. The agent doesn't know what you built last week, what decisions you made, or why you made them.

Existing memory systems help, but only partially:

- **OpenClaw's built-in memory** writes plain Markdown files. Works for simple preferences, breaks down when you need causal reasoning, *why* did we switch materials, *what* caused that deployment to fail.
- **Mem0 / Zep** extract facts from conversations and store them in vector databases. Better retrieval, but they store *what* happened, not *why*. Ask about a decision chain and you get fragments.

Raven stores the full causal picture. Every node knows what came before it and what caused it.

---

## How it works

Raven records three types of nodes:

| Node type | When it's written | Example |
|---|---|---|
| `action` | Tool call executed | `ran smoke tests → all 42 passed` |
| `decided` | Agent writes to memory | `user prefers concise answers` |
| `milestone` | Session start, end, heartbeat | `session end → switched to titanium housing` |

Nodes are stored in a local SQLite database with a `node_parents` join table. This enables:

- **Recursive CTE traversal**: walk the causal chain in pure SQL
- **Semantic search**: find relevant history by meaning via sqlite-vec
- **Branch and merge**: parallel agent tasks tracked as DAG branches, merged when complete
- **Rollback**: non-destructive, moves the tip pointer back N hops

At session start, your agent receives a summary of recent events plus semantically relevant history from past sessions. At session end, a milestone node captures what was accomplished and what comes next.

---

## Architecture

```
┌─────────────────────────────────────────┐
│              OpenClaw Agent             │
│                                         │
│  raven_start_session  ──────────────┐   │
│  raven_record_event   ──────────┐   │   │
│  raven_end_session    ───────┐  │   │   │
│  raven_search         ────┐  │  │   │   │
└───────────────────────────┼──┼──┼───┼──-┘
                            │  │  │   │
                    MCP / JSON-RPC 2.0
                            │  │  │   │
┌───────────────────────────┼──┼──┼───┼──-┐
│           Raven MCP Server              │
├─────────────────────────────────────────┤
│  TaskDAG   │  SessionReconciler         │
├─────────────────────────────────────────┤
│  TCCStore  │  SQLite + sqlite-vec       │
│            │  WAL mode, node_parents    │
│            │  Recursive CTE traversal   │
└─────────────────────────────────────────┘
                     │
              ~/.raven/raven.db
```

All data stays on your machine. No cloud, no vendor, no external API.

---

## MCP tools

Raven exposes six tools over the MCP protocol:

| Tool | What it does |
|---|---|
| `raven_start_session` | Load context at conversation start. Returns a summary of recent events + semantically relevant history. |
| `raven_record_event` | Write an event to the causal chain. Call when something significant happens. |
| `raven_end_session` | Close the session with notes. Records a milestone node so future sessions know where things stood. |
| `raven_search` | Semantic search over full history. Finds relevant past context by meaning, not just recency. |
| `raven_rollback` | Roll back N steps. Non-destructive, History is preserved, tip pointer moves. |
| `raven_get_status` | Health check: node count, tip event, vec search status. |

---

## CausalMemBench

Raven scores 100% on CausalMemBench, a benchmark specifically 
designed to test causal agent memory across six categories that 
existing benchmarks do not cover.

| Category | Score |
|---|---|
| Causal provenance | 5/5 |
| Parallel execution | 5/5 |
| Temporal ordering | 5/5 |
| Rollback provenance | 5/5 |
| Cross-session continuity | 5/5 |
| Merge outcomes | 5/5 |
| **Total** | **30/30 = 100%** |

CausalMemBench tests questions that require understanding *why* 
something happened, not just *what* happened. It is the first 
benchmark designed specifically for causal agent memory systems.

---

## Installation

**Requirements:** Python 3.10+, sqlite-vec (optional, enables semantic search)

```bash
pip install raven-memory
```

**Optional — semantic search:**
```bash
pip install raven-memory['vec']
```

---

## OpenClaw setup

Add Raven as an MCP server in your OpenClaw config:

```json
{
  "mcpServers": {
    "raven-memory": {
      "command": "python3",
      "args": ["-m", "tcc.integration.mcp_server"],
      "env": {
        "RAVEN_DB_PATH": "~/.raven/raven.db"
      }
    }
  }
}
```

Add to your `AGENTS.md` so the agent uses Raven automatically:

```
At the start of every conversation, call raven_start_session with
the user's first message as search_query. Inject the returned
summary into your awareness before responding. Record significant
events with raven_record_event. End sessions with raven_end_session.
```

Or install from ClawHub:

```bash
clawhub install raven-memory
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `RAVEN_DB_PATH` | `~/.raven/raven.db` | Path to the SQLite database |
| `RAVEN_N_RECENT` | `10` | Recent nodes injected at session start |
| `RAVEN_N_SEARCH` | `5` | Semantic search results at session start |

---

## Branching and merging

Raven's DAG tracks parallel work natively. When multiple agents or parallel tool calls run at the same time, each gets its own branch in the causal chain. When they finish, Raven merges them back into a single point on the main chain, capturing exactly what ran in parallel, what completed, and where the main thread resumed.

**Automatic — no code required**

When multiple agents write to the same database concurrently, Raven detects when all open branches are done and fires an auto-merge milestone:

```
main chain ──●──●──●──────────────────────────────●── (merge milestone)
                    └─── branch a3f2: research ───┘
                    └─── branch d8c1: lab, ─────────┘
```

The merge node records all branch tips as parents. Future sessions can walk back through it and see exactly what happened in parallel, what caused what, and in what order.

**Explicit: for orchestrator workflows**

If you're building a multi-agent orchestrator that spawns subagents and waits for results:

```python
# Fork two branches
node_a, _ = dag.branch(tip, "research task", "agent", session_id=sid)
node_b, _ = dag.branch(tip, "lab task", "agent", session_id=sid)

# Subagents do their work and mark done
dag.update_status(node_a.hash, "done")
dag.update_status(node_b.hash, "done")

# Auto-merge fires, or call explicitly:
merge = dag.merge([node_a.hash, node_b.hash], session_id=sid)
```

**Why this matters**

Without branching, concurrent agent writes are just a pile of facts with no record of what ran simultaneously. With Raven's DAG, a future session can answer: what were we doing in parallel, did both complete, and what decision came after? That causal picture is what flat memory systems such as Markdown files, vector stores cant reconstruct.

For most OpenClaw users, automerge handles this transparently. You only need the explicit API if you're orchestrating subagents yourself.

---

## Multi-agent support

Multiple agents can share a single Raven database. Each agent opens the same `.db` file. WAL mode ensures concurrent writes are safe with no corruption at all.

```python
# Agent A and Agent B share the same memory
store_a = TCCStore("~/.raven/shared.db")
store_b = TCCStore("~/.raven/shared.db")
```

No synchronization protocol needed. SQLite handles it.

---

## Performance

Tested on RTX 5090 with 500+ nodes:

| Operation | Time |
|---|---|
| Batch write 500 nodes | 8.7ms |
| `recent(20)` | 0.0ms |
| CTE ancestor traversal (500 deep) | 1.3ms |
| Store reload (500+ nodes) | 9.6ms |
| Session resume | 86.4ms |
| Semantic search per query | ~40ms |
| 10 concurrent agents × 50 nodes | 877ms, 0 errors |

---

## Compared to alternatives

| | Raven | OpenClaw memory | Mem0 | Zep |
|---|---|---|---|---|
| Causal chain | ✅ DAG with parent tracking | ❌ Flat Markdown | ❌ Flat vector store | ❌ Flat vector store |
| Cross-session recall | ✅ | ✅ (limited) | ✅ | ✅ |
| Multi-agent shared memory | ✅ Single SQLite file | ❌ Per-agent silos | ❌ | ❌ |
| Rollback | ✅ Non-destructive | ❌ | ❌ | ❌ |
| Branch / merge | ✅ | ❌ | ❌ | ❌ |
| Semantic search | ✅ sqlite-vec | ✅ | ✅ | ✅ |
| Local / private | ✅ | ✅ | ❌ Cloud | ❌ Cloud |
| OpenClaw plugin | ✅ | ✅ (built-in) | ✅ | ✅ |

---

## Project structure

```
tcc/
├── core/
│   ├── node.py        — TCCNode dataclass, typed schema
│   ├── store.py       — SQLite persistence, CTE traversal, WAL
│   ├── dag.py         — TaskDAG, branch/merge, rollback
│   ├── reconciler.py  — Session lifecycle, OpenClaw event mapping
│   └── embedder.py    — sentence-transformers wrapper
└── integration/
    └── mcp_server.py  — JSON-RPC 2.0 over stdio, 6 MCP tools

skill.md               — OpenClaw / ClawHub skill manifest
```

---

## Roadmap

**Node compression**

Long running chains accumulate intermediate nodes that lose significance over time. Compression will fold consecutive nodes of the same type, or sequences of `action` nodes between two decisions into a single summary node, preserving the causal edges but reducing storage and context injection size. A chain of 40 tool calls between two `decided` nodes collapses into one compressed `action` node with a rollup summary. The original nodes stay in the store; compression only affects what gets surfaced at session start.

**Branch milestones**

Currently, milestone nodes are written at session start, session end, and merge. The next step is writing milestone nodes at branch *creation* too, recording what triggered the parallel work, what each branch is responsible for, and what the expected merge condition is. This gives the causal chain a complete picture of parallel execution: why it forked, what each branch did, and when it rejoined.

**Task Marketplace (Recipes) **

When an agent completes a task successfully, a full branch from fork to merge with all nodes `done` Raven will be able to extract that execution path as a reusable recipe. The recipe captures the sequence of actions, the decisions made along the way, and the final result. Recipes can be shared across agents or exported so other users can seed their Raven instance with proven task patterns, essentially how an agent solved a problem, step by step, ready to be replayed or adapted.

**Encryption**

SQLCipher integration for at-rest encryption of the `.db` file. Opt-in via `RAVEN_ENCRYPTION_KEY` environment variable. No schema changes. Drop-in replacement for the SQLite connection.

**RGAT traversal**

A Relational Graph Attention Network layer over the causal DAG, using two edge types, causal edges from the DAG structure and semantic edges from sqlite-vec similarity. Replaces flat recency-based context injection with learned causal traversal: the model learns which parts of the graph are actually relevant to the current task, not just which are most recent or most similar.

---

## License

Apache 2.0
