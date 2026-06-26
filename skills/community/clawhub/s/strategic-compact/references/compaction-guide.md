# Strategic Compaction Guide

## Compaction Decision Table

Use this table to decide when to compact:

| Phase Transition | Compact? | Why |
|-----------------|----------|-----|
| Research → Planning | Yes | Research context is bulky; plan is the distilled output |
| Planning → Implementation | Yes | Plan is in notes or a file; free up context for code |
| Implementation → Testing | Maybe | Keep if tests reference recent code; compact if switching focus |
| Debugging → Next feature | Yes | Debug traces pollute context for unrelated work |
| Mid-implementation | No | Losing variable names, file paths, partial state is costly |
| After a failed approach | Yes | Clear the dead-end reasoning before trying a new approach |

## What Survives Compaction

| Persists | Lost |
|----------|------|
| Project instructions | Intermediate reasoning and analysis |
| Task notes or TodoWrite lists | File contents you previously read |
| Memory/context files | Conversation history and tool calls |
| Git state (commits, branches) | Nuanced user preferences stated verbally |
| Files on disk | Request-specific context |

## Implementation Strategy

### Token Tracking

Monitor these consumption sources:

- **Project instructions** — Always loaded, keep lean
- **Loaded skills** — Each skill adds 1-5K tokens
- **Conversation history** — Grows with each exchange
- **Tool results** — File reads, search results add bulk

### Checkpoint Strategy

When compacting:

1. **Save important context to files** — Don't lose key findings
2. **Update project notes** — Document progress
3. **Use `/compact` with summary** — Add context: `/compact Now implementing auth middleware`
4. **Reference saved files** — After compact, can reload from disk if needed

## Compaction Patterns

### Pattern 1: Research → Build

1. **Research phase** — Gather info, take notes
2. **Save findings** — Write key insights to a research doc
3. **Compact** — Free context for implementation
4. **Implementation phase** — Reference saved notes, build focused

### Pattern 2: Exploration → Execution

1. **Explore codebase** — Read files, understand structure
2. **Document structure** — Write CLAUDE.md or architecture notes
3. **Compact** — Clear exploration context
4. **Implementation phase** — Use saved structure docs as reference

### Pattern 3: Debug → Next Feature

1. **Debug current issue** — Analyze logs, test theories
2. **Document fix** — Commit change, write notes
3. **Compact** — Clear debug traces and error context
4. **Next feature** — Start fresh with minimal context

## Context Optimization

If approaching limits before natural compaction point:

1. **Extract learnings** — Save insights to memory files
2. **Document current state** — Commit progress, write status
3. **Compact with summary** — `/compact Working on auth next`
4. **Continue focused** — Reference saved docs, build with clarity

## Token Budgeting

Estimate when to compact:

- **150K tokens used** → Remind yourself about strategic compaction
- **180K tokens used** → Consider compacting if a natural boundary exists
- **200K+ tokens used** → Should have compacted at boundary; next boundary is critical
