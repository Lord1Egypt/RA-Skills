---
name: snip-compressor
description: Semantic conversation compressor — intelligently summarize long chat history while preserving key decisions, facts, and context.
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# Snip Compressor

Distilled from Claude Code's Snip compression engine. Analyzes conversation history and generates a compressed summary that preserves semantic continuity — not a simple truncation.

## When to use

- Conversation exceeds 60% of context window
- User says "continue" / "刚才说到哪了" / "where were we"
- Before compaction to preserve key context
- Session handoff between agents

## How it works

1. **Parse** — Split conversation into segments (user messages, assistant replies, tool calls, tool results)
2. **Score** — Each segment gets a retention score based on:
   - Contains decision/agreement (high)
   - Contains factual data/numbers (high)
   - Contains tool results (medium, summarized)
   - Contains greetings/small talk (low)
3. **Compress** — Low-score segments get dropped or condensed; high-score segments preserved verbatim or lightly summarized
4. **Rebuild** — Output a compressed transcript that reads naturally

## Usage

```bash
# Compress a conversation file
python3 {baseDir}/compressor.py --input conversation.json --output compressed.md

# Compress with custom token budget
python3 {baseDir}/compressor.py --input conversation.json --budget 2000

# Compress from stdin
cat conversation.json | python3 {baseDir}/compressor.py --budget 1500
```

## Input format

JSON array of message objects:

```json
[
  {
    "role": "user",
    "content": "帮我分析一下这个股票"
  },
  {
    "role": "assistant",
    "content": "好的，我来看看...",
    "tool_calls": [
      {"name": "exec", "result": "{...}"}
    ]
  }
]
```

## Output

Markdown with sections:
- **Summary**: 1-2 paragraph overview
- **Key Decisions**: bullet list of decisions made
- **Active Context**: what's currently in progress
- **Compressed Transcript**: compressed conversation (token-optimized)

## Algorithm reference

Based on Claude Code's `src/services/snip/` module:
- Semantic boundary detection: topic shift → new segment
- Importance scoring: decision > data > tool_result > greeting
- Token-aware truncation: respects model-specific limits
- Cross-segment reference preservation: if segment B references segment A, both are retained
