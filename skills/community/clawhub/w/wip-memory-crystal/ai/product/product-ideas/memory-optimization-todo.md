# Memory Optimization ... To-Do

**Updated:** 2026-03-01

---

## To Do

- [ ] Investigate the optimum memory table: crystal_remember vs every-turn capture. What's the right balance?
- [ ] Write down the full memory layer chart (below) and identify gaps/redundancies
- [ ] Investigate optimization for Claude Code's CLAUDE.md file and Claude Code's memory file (~/.claude/). How do these interact with Crystal?
- [ ] Define what should be signal (crystal_remember) vs raw log (every-turn) vs persistent instructions (CLAUDE.md) vs agent memory (workspace/MEMORY.md)

---

## The Memory Layer Chart

| Layer | When | What | Where | Searchable via | Example |
|-------|------|------|-------|---------------|---------|
| `crystal_remember` | Explicit call | One specific fact/preference | `memories` table | `crystal_search` | "Parker prefers dark mode" |
| Every-turn capture | Automatic, every turn | Full conversation chunk | `chunks` table | `crystal_search` (both tables) | The whole conversation where dark mode came up |
| CLAUDE.md | Read on boot | Persistent instructions, rules, structure | `~/.claude/CLAUDE.md` + project CLAUDE.md | Not searchable (always loaded) | "Never use em dashes" |
| Claude Code memory | Saved by CC | Session facts CC chose to persist | `~/.claude/projects/*/memory/` | Auto-loaded per project | "This repo uses ESM modules" |
| Lesa workspace/MEMORY.md | Read on boot | Lesa's persistent identity + facts | `workspace/MEMORY.md` | `lesa_memory_search` | Lesa's preferences, identity |
| Lesa workspace/TOOLS.md | Read on boot | Lesa's rules and conventions | `workspace/TOOLS.md` | `lesa_memory_search` | Git conventions, tool rules |
| Daily logs | End of session | Session summaries | `workspace/memory/YYYY-MM-DD.md` | `lesa_memory_search` | "Shipped wip-repo-permissions-hook" |
| Context embeddings | Every agent turn | Lesa's full conversation embeddings | `memory/context-embeddings.sqlite` | `lesa_conversation_search` | Any past Lesa conversation |
| LDM journals | Significant sessions | Narrative meaning, not just facts | `agents/cc/memory/journals/` | `crystal_search` | Dream Weaver style reflection |

## Questions to Answer

- Are crystal_remember and every-turn capture redundant, or do they serve different retrieval patterns?
- Should crystal_remember memories get higher weight in search ranking?
- Is there an optimal ratio of signal to noise? (e.g. 1 remember per 50 chunks)
- Should the nudge ("every 10th save") be tied to crystal_remember count or chunk count?
- How does Claude Code's built-in memory file interact with crystal_remember? Are we double-storing?
- What's the right dedup strategy across these layers?

---

## Done

(nothing yet)

---

## Deprecated

(nothing yet)
