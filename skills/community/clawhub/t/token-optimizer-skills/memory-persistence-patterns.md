# Memory Persistence Patterns

When long conversations begin consuming too much of the context window, we must transition from **Working Memory** (live conversation history) to **Persistent Memory** (JSON facts).

## The 3-Tiered Memory Architecture

1. **Working Memory** (Expensive)
   - The active conversation log (`role: user`, `role: assistant`).
   - *Token Rule:* Should not exceed X pages of scroll. Keep this small.

2. **Episodic Store** (Cheap, highly structured)
   - Using `scripts/distill_memory.py`, conversation strings are reduced into JSON facts.
   - Example format: `[{"type": "decision", "content": "Use React Router"}, {"type": "preference", "content": "Dark mode primary"}]`
   - *Token Rule:* This compresses entire pages of chat into just 50-100 tokens.

3. **Semantic Store / MCP** (Zero-context until retrieved)
   - Utilizing the `agent-memory-mcp` skill (or similar persistent RAG stores).
   - *Token Rule:* Data lives entirely outside the LLM window until a `memory_search` tool call pulls it back in.

## Trigger Points for Optimization

Do not wait for the context window to fail. Monitor usage with `token-audit` and trigger these reductions proactively:

1. **"End of Task" Distillation**
   When a sub-task is completed (e.g. "We finished building the Header component"), summarize the choices made and dump the previous conversation history.

2. **File Size Boundaries**
   If reading a large file, don't keep the source in memory. Generate an AST or structural outline instead of the verbatim code.

## JSON Fact Extractor (Skill Synergy)

If the openclaw agent has access to `memory_write` from `agent-memory-mcp`, the optimizer workflow is:
1. Agent runs `distill_memory.py` on local JSON dump.
2. Agent reads the structured output.
3. Agent uses `memory_write` to commit the extracted strings to long-term storage.
4. Agent flushes the local working memory.
