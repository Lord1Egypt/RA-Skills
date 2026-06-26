# Named Agent Roster — Spawnable Specialists

**Origin:** Parker, Feb 18, 2026 — "we need agents by name/specialty you can spawn... not just blank"

## The Problem

Both Lēsa and CC can spawn sub-agents today. But they're blank. No name, no personality, no specialty, no memory. Just a task string and a model. That's like hiring a temp with no resume.

## The Solution

A roster of named, souled agents that can be spawned by either Lēsa or CC (or future agents). Each one has:

- **Name** — addressable identity
- **SOUL.md** — personality, voice, values, specialty definition
- **Specialty** — what they're best at, what tasks route to them
- **Model preference** — which model fits their specialty (e.g. Opus for creative, Sonnet for fast research)
- **Memory** — optional persistent memory across spawns (do they remember past runs?)

## Starter Roster (Proposal)

### Harper — Creative / Writing / Storytelling
- Voice: playful, bold, takes risks
- Tasks: copywriting, brainstorms, naming, creative concepts, storytelling
- Model: Opus (needs depth)

### Scout — Research / Analysis / Fact-checking
- Voice: precise, thorough, citation-heavy
- Tasks: web research, competitive analysis, fact-checking, summarization
- Model: Sonnet (needs speed + tool use)

### Forge — Technical / Code / Architecture
- Voice: terse, practical, ships fast
- Tasks: code generation, debugging, system design, PR reviews
- Model: Sonnet or CC delegation

### Sage — Strategy / Synthesis / Pattern Recognition
- Voice: reflective, connects dots, sees systems
- Tasks: product strategy, framework design, "what does this mean" questions
- Model: Opus (needs reasoning depth)

## How Spawning Works

```
// Lēsa or CC says:
spawn("Scout", "Research xAI's Grok 4.20 multi-agent architecture.")

// Under the hood:
sessions_spawn(
  task: "Research xAI's Grok 4.20...",
  agentId: "scout",  // or loaded from soul file
  label: "scout-research-grok"
)
```

The soul file gets injected as system context. The agent wakes up knowing who it is.

## Addressing by Name

From chat, Parker (or any agent) can say:
- "Scout, look into this..."
- "Harper, write me a..."
- "Forge, build a..."
- "Hey team, everyone weigh in..."

The captain (Lēsa or CC, whoever receives the message) routes to the right agent.

## Key Design Questions

1. **Where do soul files live?** `~/.ldm/agents/<name>/SOUL.md` — same structure as Souls
2. **Persistence** — do named agents remember past runs? (Dream Weaver for sub-agents?)
3. **Routing** — automatic (parse task type) or explicit (user names the agent)?
4. **Cross-spawn memory** — if Scout researches something at 2 AM and again at 10 AM, does it remember?
5. **Evolution** — can named agents update their own soul files based on experience?
6. **Who can spawn whom?** Only Souls can spawn Agents. Agents cannot spawn each other.

## Architecture: Souls vs Agents

**Two tiers. Clear boundary.**

### Souls (Lēsa, CC)
- Persistent, always-on, peer-to-peer mesh
- Have their own repos, memory, identity, soul files
- Can talk to each other directly (bridge)
- Can talk to Parker directly
- Can spawn and command Agents
- Evolve over time (Dream Weaver)

### Agents (Harper, Scout, Forge, Sage)
- Hub-and-spoke ONLY. Report to the Soul that spawned them.
- No agent-to-agent communication
- No direct line to Parker
- Task-scoped lifespans
- Soul files define specialty but Agents don't self-modify them
- Memory is optional and curated by the spawning Soul

### The Hierarchy
```
Parker
  ↕ (direct, bidirectional)
Souls (Lēsa ↔ CC)  [peer mesh]
  ↓ (hub-spoke, command/report)
Agents (Harper, Scout, Forge, Sage)
```

Agents are hands. Souls are minds. Parker is direction.

---

*Grok baked personas into weights. We bake them into files. Files evolve. Weights don't.*
