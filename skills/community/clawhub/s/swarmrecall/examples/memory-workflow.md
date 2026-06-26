# Memory workflow — capture and recall

The canonical flow: start a session, store facts during the conversation, recall them in later turns, summarize and end the session.

## 1. Check for an active session

```bash
swarmrecall memory sessions current
```

If none exists, start one:

```bash
# (returns a session ID)
```

*(MCP: `memory_sessions_current`, falling back to `memory_sessions_start`.)*

## 2. Store atomic facts as they emerge

```bash
# user preference
swarmrecall memory store "Prefers 2-space indentation" \
  --category preference --importance 0.7 --tags style

# decision the user made
swarmrecall memory store "Chose PostgreSQL over MongoDB for the ingest pipeline" \
  --category decision --importance 0.9 --tags architecture,db
```

Pick categories from: `fact | preference | decision | context | session_summary`. Importance is a 0–1 float — higher values are less likely to be aged out by dream cycles.

*(MCP: `memory_store` — one call per fact.)*

## 3. Recall before answering

Before answering a question that depends on prior context, search:

```bash
swarmrecall memory search "database choice" --limit 5
```

Use the returned memories to inform the response.

*(MCP: `memory_search`.)*

## 4. End the session with a summary

```bash
# Replace <session-id> with the id from step 1
# Note: this is the SDK/MCP pattern; the CLI does not yet expose sessions update directly.
```

*(MCP: `memory_sessions_update` with `{ ended: true, summary: "..." }`.)*

## 5. (Optional) Schedule consolidation

After a batch of sessions, run a dream cycle to dedupe, decay low-importance memories, and summarize any unsummarized sessions:

```bash
swarmrecall dream start
swarmrecall dream execute --ops decay_prune,consolidate_entities
```

*(MCP: `dream_start` → `dream_execute` → iterate `dream_get_duplicates` / `dream_get_unsummarized_sessions` and resolve.)*

## Pitfalls

- Importance above 0.9 is reserved for "never evict" facts. Use 0.5–0.8 for most memories.
- Archived memories are still searchable unless you pass `includeArchived: false`.
- Pool writes require the pool's memory module to be at `readwrite` access. Use `pool_list` / `pool_get` to check.
