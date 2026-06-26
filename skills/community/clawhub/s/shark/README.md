# 🦈 The Shark Skill

> *A shark that stops swimming dies. An agent that waits for tools wastes compute.*

**Works with:** Claude Code · Codex · Gemini CLI · Cursor · Windsurf · Aider · OpenClaw · any LLM agent

## What Is This?

The **Shark Pattern** is a universal non-blocking execution model for AI coding agents.

**The rule:** Every LLM turn completes in under 30 seconds. Slow operations get spawned as **remoras**. The main agent never waits.

### The Three Fish

| Fish | Role |
|------|------|
| 🦈 **Shark** | Main agent — never stops, always reasoning |
| 🐟 **Remora** | Timed sub-agents — attach to the shark, do the slow work in parallel |
| 🐠 **Pilot Fish** | Time-bounded pre-analysis — swim ahead while remoras are running |

---

## Why?

### The Problem

Most agents work sequentially:
```
think → slow tool → WAIT 45s → think → slow tool → WAIT 30s → ...
```
90% of runtime is spent waiting. You're paying for LLM compute while it stares at a spinner.

### The Solution — Shark + Remoras
```
think → spawn 🐟 remora(web search)  ────────────────► result
      → spawn 🐟 remora(SSH command) ──────────────────────► result
      → spawn 🐟 remora(build/test)  ──────────────────────────► result
      → 🦈 keep reasoning in parallel
      → first remora back → spawn 🐠 pilot fish (pre-analyse)
      → all remoras back → synthesise + incorporate pilot fish draft
```

### Comparison

| | Sequential | Ralph Loop | 🦈 Shark |
|--|--|--|--|
| Execution | Blocking | Iterative, blocking | Parallel, non-blocking |
| Tool wait | Always | Always | Never |
| Idle time | Wasted | Wasted | Pilot fish pre-analysis |
| Speed | Linear | Linear | Bounded by slowest parallel task |
| Works with | Any agent | Any agent | **Any agent** |
| Prior art | — | ghuntley.com/ralph | **Novel — no prior art** |

---

## Lifecycle

```
┌─────────────┐
│  DECOMPOSE  │  Break task into N independent subtasks
└──────┬──────┘
       │ spawn N remoras in parallel
       ▼
┌─────────────┐
│    SPAWN    │  sessions_spawn × N, record IDs, keep swimming
└──────┬──────┘
       │ first remora completes early?
       ├──────────────────────────────► spawn 🐠 pilot fish (pre-analyse)
       │ main agent reasons while waiting
       ▼
┌─────────────┐     timeout ⏱ / crash ❌
│   MONITOR   │ ──────────────────────► partial result still useful
└──────┬──────┘
       │ all done or deadline hit
       ▼
┌─────────────┐
│  AGGREGATE  │  Merge results + pilot fish draft, note failures
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   REPORT    │  Single coherent response: "3/4 succeeded, 1 timed out"
└─────────────┘
```

**No nested remoras** — remoras always run inline. Only the main shark spawns.

---

## Progress Output (chat-friendly)

Works in Telegram, Discord, Signal, iMessage — pure Unicode, no images.

```
🦈 3 remoras · 1 pilot fish

⊙ [A] web search          ████████████ ✅ 12s
⊙ [B] SSH check           ████████████ ✅ 8s
○ [C] build + test         ██████░░░░░░ ~18s left
◈ [P] Pilot fish           ████░░░░░░░░ ~14s left

↳ synthesising…
```

**Symbols:** `◉`=done `○`=pending `⊙`=running `◈`=pilot fish `⏱`=timeout `❌`=error

**Bar fill:** `filled = round(elapsed / timeout * 12)` blocks of `█`, remainder `░`

---

## Repo Structure

```
shark-pattern/
├── SKILL.md              # Main shark skill — load this
├── shark.sh              # Ralph-style loop enforcer (Linux/Mac)
├── shark.ps1             # Ralph-style loop enforcer (Windows)
├── shark-exec/
│   ├── SKILL.md          # Sub-skill: background exec + cron poller
│   ├── scripts/
│   │   └── poll-and-deliver.js
│   └── state/
│       └── .gitkeep
└── tests/
    ├── lint.sh           # Structural lint tests
    └── scenarios.md      # Behavioural test specs
```

---

## Install

### ⚡ Universal one-liner (any agent, any repo)
```bash
curl -sO https://raw.githubusercontent.com/keugenek/shark-pattern/main/SKILL.md \
  && mv SKILL.md SHARK.md && echo "SHARK.md" >> .gitignore
```
Drop `SHARK.md` in your project root. Every agent that reads context files will pick it up.

---

### Claude Code
```sh
# Install as a skill (full repo with shark-exec)
mkdir -p ~/.claude/skills
git clone https://github.com/keugenek/shark-pattern ~/.claude/skills/shark
```
Add to `CLAUDE.md`:
```markdown
## Execution Model
See ~/.claude/skills/shark/SKILL.md — use the Shark Pattern for any multi-step task with slow tools.
```

Or drop just the SKILL.md:
```bash
curl -o SHARK.md https://raw.githubusercontent.com/keugenek/shark-pattern/main/SKILL.md
```

---

### OpenClaw
```sh
# Install for OpenClaw
mkdir -p ~/clawd/skills
git clone https://github.com/keugenek/shark-pattern ~/clawd/skills/shark
```
OpenClaw will auto-discover `SKILL.md` from the cloned directory.

---

### Codex
```bash
curl -o SHARK.md https://raw.githubusercontent.com/keugenek/shark-pattern/main/SKILL.md
```
Add to `AGENTS.md`:
```markdown
## Execution Model
Follow the Shark Pattern (SHARK.md). Never block on slow tools — spawn remoras.
```

---

### Gemini CLI
```bash
curl -o SHARK.md https://raw.githubusercontent.com/keugenek/shark-pattern/main/SKILL.md
gemini --system-prompt SHARK.md -p "your task"
# or pipe:
cat SHARK.md your-task.md | gemini -p -
```

---

### Cursor / Windsurf
```bash
curl -o .cursor/rules/shark.md \
  https://raw.githubusercontent.com/keugenek/shark-pattern/main/SKILL.md
```

---

### Aider
```bash
curl -o SHARK.md https://raw.githubusercontent.com/keugenek/shark-pattern/main/SKILL.md
aider --read SHARK.md
```

---

## Usage

Tell your agent (works in any coding assistant):
- `"Use shark mode"`
- `"Non-blocking — spawn remoras where needed"`
- `"Keep swimming"`
- `"Never wait for tools"`
- `"Follow the Shark Pattern from SHARK.md"`

---

## Enforcing the 30s Timeout

| Runtime | How to enforce |
|---------|---------------|
| OpenClaw subagent | `runTimeoutSeconds: 30` (confirmed in source — hard kill, partial returned) |
| exec / shell | `timeout: 30, background: true` |
| Gemini CLI | `timeout 30 gemini -p "..."` (Linux) or `Start-Process -Timeout 30` (Windows) |
| Pilot fish | `runTimeoutSeconds: min(estimatedRemaining * 0.8, 25)` |

---

## Error Handling

| Failure | Progress bar | Recovery |
|---------|-------------|----------|
| Timeout | `⏱` | Use partial output, note gap in report |
| Crash | `❌` | Skip, note in report, continue synthesis |
| >50% failed | `⚠️` | Degraded mode — fall back to sequential |
| All failed | — | Sequential fallback, no parallel benefit |

Always report: `"3/4 remoras succeeded, 1 timed out"`

---

## Decision Tree

```
Estimated time > 10s AND parallelisable AND not already a remora?
  YES → spawn remora
  NO  → run inline
```

Max 8 concurrent remoras. Tasks >3 sentences → decompose first.

---

## Publishing to ClawHub

```bash
npm install -g clawhub
clawhub login   # GitHub OAuth
clawhub publish . \
  --slug shark \
  --name "Shark" \
  --version 1.0.0 \
  --changelog "Initial release"
```

---

## Related

- [Ralph Loop](https://ghuntley.com/ralph/) — the sequential iteration pattern this builds on
- [OpenClaw](https://openclaw.ai) — agent framework
- [ClawHub](https://clawhub.com/skill/shark) — skill registry

## Author

[Evgeny Knyazev](https://github.com/keugenek)

## License

MIT
