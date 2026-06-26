---
name: token-optimizer
description: Playbook of 5 creative strategies to drastically reduce token consumption and context bloat without losing memory. Use when context is bloated, before loading massive text files, or when instructed to "optimize tokens" or "reduce memory footprint".
---

# Token Optimizer Skill

This skill provides a toolkit of strategies to reduce the token consumption in your context window. It pairs well with the `token-audit` skill which identifies *where* the tokens are spent.

## Optimization Playbook

When tasked with saving tokens, utilize one or more of these 5 strategies:

### 1. Memory Distillation (Saves 40–70%)
Use this when the conversation history is long.
- **Action:** Convert sprawling conversation into structured facts.
- **How:** Run `python scripts/distill_memory.py --input <history_file>`.
- **Result:** You can drop the verbose chat log and keep only the JSON. Use `agent-memory-mcp` to commit these to long term memory if available.
- **Reference:** `references/memory-persistence-patterns.md`

### 2. Prompt Compression (Saves 20–50%)
Use this when you must inject a massive block of text, documentation, or search results into the prompt.
- **Action:** Use LLMLingua-2 to selectively strip redundant tokens without changing the meaning.
- **How:** Run `python scripts/compress_prompt.py --input <big_file.txt> --ratio 0.5`.
- **Result:** You get a block of text that is exactly half the tokens, but retains core semantics. Ensure the user is okay with the dependency (requires `pip install llmlingua`).

### 3. Skill Lazy Loading (Saves 10–30%)
Use this when the system prompt metadata is bloated with dozens of skills.
- **Action:** Audit skills for oversized descriptions (>500 chars).
- **How:** Run `python scripts/analyze_skills.py`.
- **Result:** Identifies skill descriptions that need to be rewritten to be more concise.

### 4. Code & "Context DNA" Compression (Saves 80% on UI Code)
Use this when working with large frontend or backend code files.
- **Action:** Never read full 500-line boilerplates into context if you only need the logic.
- **How:** Replace redundant imports and boilerplate UI blocks with single line comments.
- **Example:** `// Standard React imports and Tailwind wrapper here`.

### 5. "Model Dialect" Rewriting
Use this to squeeze maximum value out of specific tokenizers.
- **Action:** If the model is Gemma, rewrite prompt structures into XML blocks (`<context>`, `<task>`) because Gemma tokenizes these highly efficiently.
- **How:** Substitute flowing paragraphs for short XML structures or JSON blobs.
- **Reference:** `references/gemma-optimization.md`.

## Workflow Example
1. You identify 30k tokens used by a long chat history.
2. You save the chat history to `temp_history.json`.
3. You run `distill_memory.py` on it, producing 300 tokens of extracted facts.
4. You prompt the user to let you flush the local history because the facts are secured.
