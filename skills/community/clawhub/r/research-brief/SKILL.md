---
name: research-brief
version: 1.0.0
description: 'Progressive research protocol for agents: write a stub file immediately,
  append findings incrementally, never save the write for last. Prevents data loss
  from context-window timeouts or API latency spikes during long research tasks.'
metadata:
  openclaw:
    emoji: 🔬
---

# Skill: Research Brief
_For agents that conduct web research and write output files_

## Problem this solves
Research agents (Archie) timeout before writing output files because they batch all research first, then try to write at the end. API latency spikes or context window limits kill the final write turn. Data is lost.

## The Rule — Non-Negotiable

**FIRST tool call = write the stub file. Always.**

No exceptions. Not "after one quick search". Not "I'll write it when I'm done". First. Tool. Call.

## Stub Pattern

```markdown
# [Topic] Research Brief
_[Agent] · [YYYY-MM-DD]_

## TL;DR
[researching]

## [Section 1]
[researching]

## [Section 2]
[researching]

## Recommendation
[researching]

## Sources
[researching]
```

Write this file in the first tool call. Then do all your research. Update sections as you go — don't batch to the end.

## Update-as-you-go Pattern

After each search angle:
1. Run search / fetch URL
2. Extract key finding
3. **Immediately edit the relevant section** of the output file
4. Move to next angle

Never accumulate findings in memory and flush at the end. The edit is instant. The LLM turn is fragile.

## Why this matters

- Subagent timeout = 4 minutes by default
- Web research easily uses 3+ minutes on fetches + processing
- LLM output generation turn can be killed by latency spike at minute 3:50
- File on disk = data survives timeout. In-memory = data lost.

## Applies to
- Archie (primary)
- Any agent doing research → write tasks
- Quinn when running deep research

## Anti-patterns (never do these)
- ❌ `web_search` before `write`
- ❌ "I'll write when I have all the data"
- ❌ Writing a full draft in the LLM output turn and then saving
- ❌ "Let me do one more search first"

## Signs you're about to fail
- You've done 3+ searches and haven't written a file yet → stop, write stub NOW
- You're composing a long response in your head → write it to file instead
- You think "just one more source" → write what you have, then search
