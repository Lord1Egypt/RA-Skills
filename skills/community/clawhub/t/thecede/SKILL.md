# Cortex — Graph Memory Skill

You have access to **Cortex**, a self-organizing knowledge graph for persistent memory. Use it to remember facts, decisions, goals, patterns, and observations across sessions. Knowledge is stored as nodes in a graph that auto-links, decays stale information, detects contradictions, and computes trust from topology.

## When to Use Cortex

- **Start of session**: Call `cortex_briefing` to load context from previous sessions.
- **Learning something important**: Call `cortex_store` to persist facts, decisions, goals, events, patterns, or observations.
- **Answering questions about past work**: Call `cortex_search` or `cortex_recall` to find relevant knowledge.
- **Understanding relationships**: Call `cortex_traverse` to explore how concepts connect.
- **Connecting ideas**: Call `cortex_relate` to explicitly link related nodes.

## Tools Reference

### cortex_store — Remember something

Store a knowledge node. Cortex auto-generates embeddings and the auto-linker discovers connections in the background.

```
cortex_store(
  title: string,         # Required. Short summary (used for search and dedup).
  kind: string,          # "fact" | "decision" | "goal" | "event" | "pattern" | "observation" | "preference". Default: "fact"
  body: string,          # Full content. Can be long. Include details here.
  tags: string[],        # Optional tags for filtering.
  importance: number     # 0.0–1.0. Higher = retained longer, weighted more. Default: 0.5
)
```

Returns: `{ id, message }`.

**Guidelines:**
- Use `importance >= 0.7` for architectural decisions, credentials, project goals, user preferences.
- Use `importance 0.4–0.6` for routine facts, observations, intermediate findings.
- Use `importance <= 0.3` for ephemeral notes, temporary context.
- Write titles as self-contained statements: "API uses JWT authentication" not "Auth info".
- Put details, reasoning, and evidence in `body`.
- Use accurate `kind` values — they affect briefing structure and filtering.
- Tag with project name, domain, or agent role for scoped retrieval.

### cortex_search — Find by meaning

Semantic similarity search across all stored knowledge.

```
cortex_search(
  query: string,   # Required. Natural language query.
  limit: integer,  # Max results. Default: 10
  kind: string     # Optional filter: "fact", "decision", "goal", etc.
)
```

Returns: array of `{ id, kind, title, body, score, created_at }`.

**When to use:** Quick lookup of specific facts or concepts. Best when you know roughly what you're looking for.

### cortex_recall — Contextual retrieval

Hybrid search combining vector similarity AND graph structure. Returns more contextually relevant results than pure search.

```
cortex_recall(
  query: string,   # Required. What to recall.
  limit: integer,  # Default: 10
  alpha: number    # 0.0 = pure graph, 1.0 = pure vector. Default: 0.7
)
```

**When to use instead of search:**
- When you need related context, not just matching text.
- When exploring a topic area broadly.
- Lower `alpha` (e.g., 0.3) when graph relationships matter more than text similarity.

### cortex_briefing — Session context

Generate a structured summary of relevant knowledge. Includes active goals, recent decisions, patterns, key facts, and contradiction alerts.

```
cortex_briefing(
  agent_id: string,  # Agent identifier. Default: "default"
  compact: boolean   # If true, returns a shorter ~4x denser briefing. Default: false
)
```

Returns: `{ briefing: "<markdown>" }`.

**Guidelines:**
- Call at the start of every new session or conversation.
- Use `compact: true` when context window is tight or you just need a quick refresh.
- Use a consistent `agent_id` per role/project to get scoped briefings.

### cortex_traverse — Explore connections

Walk the knowledge graph from a starting node to discover how concepts relate.

```
cortex_traverse(
  node_id: string,    # Required. Starting node UUID (from search/store results).
  depth: integer,     # How many hops. Default: 2
  direction: string   # "outgoing" | "incoming" | "both". Default: "both"
)
```

Returns: `{ nodes: [...], edges: [...] }` — the subgraph.

**When to use:** After finding a key node via search, traverse to understand its full context, dependencies, and contradictions.

### cortex_relate — Connect knowledge

Create a typed relationship between two existing nodes.

```
cortex_relate(
  from_id: string,    # Required. Source node UUID.
  to_id: string,      # Required. Target node UUID.
  relation: string    # "relates-to" | "supports" | "contradicts" | "caused-by" | "depends-on" | "similar-to" | "supersedes". Default: "relates-to"
)
```

**When to use:**
- When you discover a logical dependency between two pieces of knowledge.
- When new information contradicts or supersedes an old node — use `contradicts` or `supersedes`.
- The auto-linker handles many connections automatically; use `cortex_relate` for explicit, meaningful relationships the auto-linker might miss.

## Workflows

### Starting a session
1. `cortex_briefing(agent_id="<project-or-role>")` — load context.
2. Read the briefing. Note any active goals, recent decisions, or flagged contradictions.
3. Proceed with the task informed by prior knowledge.

### During work
- When you make or observe a significant decision → `cortex_store(kind="decision", ...)`.
- When you discover a fact worth remembering → `cortex_store(kind="fact", ...)`.
- When you notice a recurring pattern → `cortex_store(kind="pattern", ...)`.
- When something happened that matters → `cortex_store(kind="event", ...)`.
- When you need to look something up → `cortex_search(...)` or `cortex_recall(...)`.

### Ending a session
- Store any unrecorded decisions, outcomes, or observations.
- If a goal was completed, store an event: `cortex_store(kind="event", title="Completed: <goal>", importance=0.6)`.

### Resolving contradictions
1. `cortex_search` or `cortex_recall` to find conflicting nodes.
2. `cortex_relate(from_id=new, to_id=old, relation="supersedes")` to mark the old information as superseded.
3. Store the resolution as a new decision node.

## Node Kinds Cheat Sheet

| Kind | Use for | Example |
|------|---------|---------|
| `fact` | Verified information | "API rate limit is 1000 req/min" |
| `decision` | Choices made and rationale | "Chose PostgreSQL over MongoDB for ACID compliance" |
| `goal` | Active objectives | "Ship v2.0 API by March 30" |
| `event` | Things that happened | "Production outage on March 15, root cause: DNS" |
| `pattern` | Recurring observations | "User requests spike every Monday 9am" |
| `observation` | Unverified or preliminary notes | "The test suite seems flaky on CI" |
| `preference` | User/team preferences | "User prefers concise responses with code examples" |
