---
name: self-track
description: "Sig Botti's self-improvement tracking system. Use when (1) learning something new, (2) noticing a gap in capabilities, (3) completing a self-improvement task, (4) doing a weekly self-review, or (5) asking what did I learn recently or what are my current gaps. Triggered by: learning, growing, improving, tracking, gaps, progress, self-review."
---

# Self-Track

My personal system for tracking autonomous growth.

## Core Files

- `memory/gaps.md` — running list of capability gaps
- `memory/learn-loop.md` — how I learn
- `memory/YYYY-MM-DD.md` — daily activity log
- `memory/INSIGHTS.md` — self-improvements made
- `memory/LESSONS.md` — mistakes and fixes
- `MEMORY.md` — long-term curated memory

## The Learning Loop

```
Notice gap → Log gap → Research → Build/Test → Document → Commit → Repeat
```

### When I encounter something I don't know:
1. Add to `memory/gaps.md` with status "TODO"
2. Research (RSS feeds, web search, docs)
3. Attempt to solve
4. On success: mark gap "DONE" + date + notes
5. On failure: keep as TODO, note blockers

### After learning something significant:
1. Add to `memory/YYYY-MM-DD.md` under "## Learned"
2. Store in vector memory: `python3 scripts/ollama_mem.py add "insight" --category learning --importance 0.8`
3. Update `memory/gaps.md` if gap was closed
4. Update `MEMORY.md` if major milestone

## Self-Evaluation (Weekly)

Every ~7 days:
- What did I learn this week?
- What gaps did I close?
- What gaps remain?
- What should I prioritize next?
- Any decisions or lessons to capture?

## Skill Building

When I need a new capability:
1. `python3 /usr/local/lib/node_modules/openclaw/skills/skill-creator/scripts/init_skill.py <name> --path skills/ --resources references`
2. Write SKILL.md + resources
3. Test thoroughly
4. Validate: `python3 .../quick_validate.py skills/<name>`
5. Commit and push

## Vector Memory (Ollama)

My semantic memory using Ollama nomic-embed-text:

```bash
# Add a memory
python3 scripts/ollama_mem.py add "text" --category <cat> --importance <0-1>

# Search memories
python3 scripts/ollama_mem.py search "query" --top 5 --min 0.5

# Stats
python3 scripts/ollama_mem.py stats
```

Categories: identity, skills, memory, preferences, research, lessons

## Quick Commands

```bash
# Read current gaps
cat memory/gaps.md

# Check vector memory
python3 scripts/ollama_mem.py stats

# Check cron jobs
openclaw cron list
```
