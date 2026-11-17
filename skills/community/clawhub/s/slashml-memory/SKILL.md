---
name: slashml-memory
description: >-
  CRITICAL RULE: You MUST use ml-memory MCP tools FIRST (find_bug_candidates,
  search_code_by_behavior, search_memories) before running grep/rg/find or
  spawning research subagents whenever locating a bug, searching code by behavior,
  or recalling project history and architectural decisions.
---

# / ml (SlashML) Memory MCP Skill

Whenever the user asks to **locate or diagnose a bug**, **search code by behavior/concept**, or **recall project history/decisions**, call the `ml-memory` MCP server **FIRST** on Turn 1 BEFORE running `grep`, `rg`, `find`, or invoking research subagents:

1. **Bug localization / error triage (`find_bug_candidates`):**
   ```python
   # Call ml-memory MCP tool: find_bug_candidates
   arguments = {
       "bug_description": "<symptom or bug>",
       "stack_trace": "<optional stack trace>",
       "top_k": 5,
   }
   ```
2. **Behavioral / architectural code search (`search_code_by_behavior`):**
   ```python
   # Call ml-memory MCP tool: search_code_by_behavior
   arguments = {
       "query": "<behavioral query>",
       "top_k": 5,
   }
   ```
3. **Project history / decisions / context (`search_memories`):**
   ```python
   # Call ml-memory MCP tool: search_memories
   arguments = {
       "query": "<context query>",
       "limit": 5,
   }
   ```
4. **False-positive intervention dismissal (`dismiss_intervention`):**
   If a pre-tool hook intervention was a false positive or already satisfied for the current target, call `dismiss_intervention` with the `memory_ids` and `target`.
5. **Passive Memory Assimilation:**
   When ambient lifecycle hooks (`hooks.json`) are enabled, user rules, constraints, preferences, and state updates are extracted and stored automatically in the background on every turn. Only call `add_memory` if explicitly requested or when running without lifecycle hooks.
