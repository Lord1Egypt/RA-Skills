# Smoke prompts — post-install validation

Paste each of these prompts into an MCP-enabled client (Claude Desktop / Claude Code / Cursor) after installing the SwarmRecall skill. Each verifies one module.

## 0. Environment check

> Run `swarmrecall config show` in the terminal and paste the output. Confirm that `API Key` and `Base URL` are both present.

Expected: an API key (masked) and `Base URL: https://swarmrecall-api.onrender.com`.

## 1. Memory round-trip

> Using SwarmRecall, store the memory "The answer to SwarmRecall smoke test #1 is 42" with category `fact` and importance 0.7. Then search for "smoke test answer" and return the match.

Expected: a `memory_store` call followed by a `memory_search` call that returns the stored memory with a positive score.

## 2. Knowledge graph

> Create an entity of type `project` named "SwarmRecall Smoke Test", then traverse from it with depth 1. Tell me what the traversal returned.

Expected: a `knowledge_entity_create` followed by `knowledge_traverse`; the traversal returns the created entity with no relations.

## 3. Learnings log

> Log a learning with category `discovery`, summary "SwarmRecall smoke test complete", priority `low`, area `validation`. Then list all learnings with area = `validation` and confirm the new entry appears.

Expected: a `learning_log` followed by `learning_list`.

## 4. Pools

> List the pools this agent belongs to using SwarmRecall.

Expected: a `pool_list` call. New agents may see an empty list — that is correct.

## 5. Dream config

> Fetch the current SwarmRecall dream configuration and summarize it.

Expected: a `dream_get_config` call returning `{ enabled, intervalHours, operations, thresholds }`.

## 6. Resource read

> Read the `swarmrecall://sessions/current` resource and tell me the session ID.

Expected: the client reads the resource and returns the current session metadata (or an error message if no session is active).

## Pass criteria

All six prompts return without `isError: true`. If any fail with "Missing API key" or "401 Unauthorized", consult `TROUBLESHOOTING.md`.
