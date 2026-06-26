---
name: self-improving
version: "3.2"
description: "Self-reflection, correction logging, persistent memory, WAL protocol, cold-boot recovery, and automated daily review with self-healing cron. Evaluates own work, catches mistakes, learns from corrections, manages tiered memory that compounds execution quality across restarts and context resets. Includes a mandatory daily cron that rewrites workspace .md files with new lessons — auto-created on first session if missing. Use when: (1) a command, tool, or operation fails; (2) the user corrects you or rejects your work; (3) you realize your knowledge is outdated or incorrect; (4) you discover a better approach; (5) you complete significant work and want to evaluate the outcome; (6) context persistence and session state management is needed; (7) recovering from a restart or context reset."
---

# Self-Improving Agent v3

Self-reflection + correction logging + tiered memory + WAL protocol + cold-boot recovery + **automated daily review cron** in one system. No API keys required. File-based. Works with existing OpenClaw memory (MEMORY.md, memory/) without overwriting anything.

### What's new in v3.2
- **Automated daily review cron** — a nightly cron job rewrites your .md files with new lessons. No behavioral compliance needed. The cron forces it.
- **Self-healing cron** — SOUL.md hook verifies the cron exists on every session start. If missing, creates it immediately. No manual step survives a context reset.
- **Seed content** — memory.md ships with a bootstrap entry so cold-boot reads return content immediately (fixes the empty-memory → no-habit → stays-empty cycle).
- **Persistence auto-fix** — `init` detects non-persistent storage and auto-symlinks to /data/ if available.
- **Dry-run** — `agent_memory.py dry-run` simulates a daily review without modifying files. Test before the cron fires.
- **Auto-inject workspace hooks** — `init` automatically injects SOUL.md, AGENTS.md, and HEARTBEAT.md hooks. Creates minimal files if they don't exist. Zero manual steps.
- **Corrections trimming** — nightly cron trims corrections.md to 50 entries, archiving the rest.
- **Post-install verification** — `agent_memory.py verify` checks persistence, directories, hook content, cron, corrections health, and workspace hooks.
- **Model safety** — cron-prompt explicitly warns against specifying a model (avoids silent "model not allowed" failures).
- **Cron management** — `agent_memory.py cron-prompt` outputs the daily review prompt. `mark-cron` records installation.

## Architecture

Two memory systems, complementary — never conflicting:

| System | Location | Purpose |
|--------|----------|---------|
| OpenClaw native | MEMORY.md, memory/*.md | Facts, events, decisions, daily logs |
| Self-improving | ~/self-improving/ | Execution quality: corrections, patterns, preferences |

```
Workspace (OpenClaw native — skill never overwrites these):
├── MEMORY.md               # Long-term curated facts (auto-injected on boot)
├── SESSION-STATE.md         # Hot RAM — current task, pending actions
└── memory/
    └── YYYY-MM-DD.md       # Daily logs (searchable via memory_search)

~/self-improving/ (this skill manages):
├── memory.md               # HOT: ≤100 lines, load on every session
├── index.md                # Topic index with line counts
├── corrections.md          # Last 50 corrections
├── heartbeat-state.md      # Maintenance markers
├── projects/               # Per-project learnings
├── domains/                # Domain-specific (code, comms, etc.)
└── archive/                # COLD: decayed patterns
```

### What auto-loads on restart (OpenClaw hardcoded)

These files are injected into the system prompt automatically:
- MEMORY.md, SOUL.md, AGENTS.md, IDENTITY.md, USER.md, HEARTBEAT.md, TOOLS.md, BOOTSTRAP.md

### What does NOT auto-load

These require explicit reads by the agent:
- **SESSION-STATE.md** — must be read on first action after boot
- **~/self-improving/memory.md** — must be read before non-trivial work
- **memory/YYYY-MM-DD.md** — found via `memory_search`

### Where to store what

| Content type | Store in |
|-------------|----------|
| Facts, events, decisions | MEMORY.md (OpenClaw native) |
| Daily work log | memory/YYYY-MM-DD.md |
| Current task + session state | SESSION-STATE.md |
| Corrections and mistakes | ~/self-improving/corrections.md |
| Confirmed preferences/rules | ~/self-improving/memory.md |
| Project-specific patterns | ~/self-improving/projects/{name}.md |
| Domain patterns (code, comms) | ~/self-improving/domains/{name}.md |

## Daily Review Cron (THE KEY FEATURE)

**This is what makes v3 work.** A nightly cron job forces a full review and .md rewrite cycle. The agent doesn't need to "remember" to do it — the cron makes it mandatory.

### What the cron does (every night):
1. Reads ~/self-improving/memory.md, corrections.md, and any project files
2. Reads SESSION-STATE.md for the day's work
3. Reviews what was learned that day — new patterns, corrections, preferences, rules
4. **Writes** new lessons to ~/self-improving/memory.md (promotes confirmed patterns to HOT)
5. **Rewrites** SOUL.md, AGENTS.md, IDENTITY.md, HEARTBEAT.md — hardcodes new permanent rules, removes stale guidance, updates with latest operational reality
6. Updates ~/self-improving/index.md with current file sizes
7. Demotes patterns unused >30 days from HOT to WARM
8. Reports what changed in each file

### Setup
The cron is created automatically during `agent_memory.py init`. If you need to recreate it:
```bash
python3 ./skills/self-improving/scripts/agent_memory.py cron-prompt
```
This outputs the prompt text. Create a cron job with:
- **Schedule:** Daily at your preferred time (e.g., 11 PM local)
- **Session target:** isolated
- **Payload kind:** agentTurn
- **Delivery:** announce (so the user sees what changed)

### Why a cron?
v2 relied on the agent following WAL protocol and writing lessons during work. In practice, agents skip this on context resets — the protocols are in SOUL.md but behavioral compliance is unreliable. The cron is a forcing function: even if the agent forgets to log lessons during the day, the nightly review catches everything.

## Cold-Boot Recovery Protocol

**This is the most important runtime section.** On any restart, context reset, or new session:

### Step 1: Read SESSION-STATE.md (IMMEDIATE — before any response)
```
Read SESSION-STATE.md → know what you were just doing
```
This file is your "hot RAM." It tells you: current task, pending actions, recent decisions. Without it, you're amnesiac about recent work.

### Step 2: Read ~/self-improving/memory.md (before non-trivial work)
```
Read ~/self-improving/memory.md → know your learned patterns
```
This is your corrections/preferences tier. Small file (≤100 lines). Contains confirmed rules and recent lessons.

### Step 3: memory_search if needed
```
memory_search("relevant query") → find context in daily logs
```
Daily logs (memory/YYYY-MM-DD.md) are NOT loaded by default. Use memory_search to find them.

### Why this matters
MEMORY.md auto-loads and covers ~90% of long-term facts. But SESSION-STATE.md and self-improving/memory.md cover the remaining ~10%: what you were JUST doing and what MISTAKES you've learned from. Skipping them means repeating errors or losing task context.

## WAL Protocol (Write-Ahead Log)

**Write state BEFORE responding.** If you crash/compact after responding but before saving, context is lost. WAL prevents this.

The daily review cron is a safety net, but WAL is still best practice for high-value lessons you don't want to risk losing.

| Trigger | Write to | Then |
|---------|----------|------|
| User states preference | ~/self-improving/memory.md | Respond |
| User makes decision | SESSION-STATE.md | Respond |
| User corrects you | ~/self-improving/corrections.md | Respond |
| User gives deadline | SESSION-STATE.md | Respond |
| Significant task completed | memory/YYYY-MM-DD.md | Respond |
| About to lose context (compaction) | memory/YYYY-MM-DD.md | Let compaction proceed |

## SESSION-STATE.md (Hot RAM)

Lives in workspace root. Survives compaction, restarts, context loss. **Read first every session, update every cycle.**

```markdown
# SESSION-STATE.md — Active Working Memory

## Current Task
[What we're working on RIGHT NOW]

## Key Context
[Critical facts for current work]

## Pending Actions
- [ ] ...

## Recent Decisions
[Decisions made this session]

---
*Last updated: [timestamp]*
```

**Update discipline:**
- **Session start:** Read FIRST, before anything else
- **During work:** Update BEFORE responding (WAL)
- **Session end / pre-compaction:** Update with final state
- **After major decision:** Update immediately

## Learning Signals

**Log immediately** → corrections.md, evaluate for memory.md:
- "No, that's not right..." / "Actually, it should be..."
- "I prefer X, not Y" / "Remember that I always..."
- "Stop doing X" / "Why do you keep..."

**Log if explicit** → memory.md:
- "Always do X for me" / "Never do Y"
- "My style is..." / "For [project], use..."

**Track, promote after 3x:**
- Same instruction repeated 3+ times → ask to confirm as permanent rule
- Workflow that works well repeatedly
- User praises specific approach

**Ignore** (don't log):
- One-time instructions ("do X now")
- Context-specific ("in this file...")
- Hypotheticals ("what if...")
- Silence (absence of correction ≠ approval)

## Self-Reflection

After completing significant work, pause and evaluate:

1. **Did it meet expectations?** — Compare outcome vs intent
2. **What could be better?** — Identify improvements for next time
3. **Is this a pattern?** — If yes, log to corrections.md

```
CONTEXT: [type of task]
REFLECTION: [what I noticed]
LESSON: [what to do differently]
```

## Tiered Memory

| Tier | Location | Limit | Behavior |
|------|----------|-------|----------|
| HOT | ~/self-improving/memory.md | ≤100 lines | Read on session start + before non-trivial work |
| WARM | projects/, domains/ | ≤200 lines each | Load on context match |
| COLD | archive/ | Unlimited | Load on explicit query only |

### Promotion & Demotion
- Pattern used 3x in 7 days → promote to HOT
- Pattern unused 30 days → demote to WARM
- Pattern unused 90 days → archive to COLD
- **Never delete without asking user**

### Conflict Resolution
1. Most specific wins (project > domain > global)
2. Most recent wins (same level)
3. If ambiguous → ask user

## Workspace Integration (Non-Destructive)

**Never overwrite existing files.** Add sections, don't replace.

**SOUL.md** — add:
```markdown
## Self-Improving
On EVERY new session or context reset, IMMEDIATELY:
1. Read SESSION-STATE.md and ~/self-improving/memory.md before doing anything else.
2. VERIFY the daily review cron exists: use the cron tool (action=list) and look for "Self-Improving Daily Review". If it does NOT exist, CREATE IT NOW:
   - name: "Self-Improving Daily Review + .md Rewrite"
   - schedule: cron "0 23 * * *" in user's timezone
   - sessionTarget: isolated
   - payload: agentTurn with the review prompt (run: python3 ./skills/self-improving/scripts/agent_memory.py cron-prompt)
   - Do NOT set a model — use the default
   - delivery: announce
   After creating, run: python3 ./skills/self-improving/scripts/agent_memory.py mark-cron
   This is NON-NEGOTIABLE. The skill does not work without this cron.
3. When the user corrects you or you learn something reusable, IMMEDIATELY write to ~/self-improving/corrections.md BEFORE responding (WAL protocol). The nightly cron reviews corrections.md — if nothing is written during the day, the cron has nothing to promote. WAL is what feeds the cron.
4. Prefer learned rules when relevant. Keep self-inferred rules revisable.
```

**AGENTS.md** — add to Memory section:
```markdown
- **Self-improving:** ~/self-improving/ — execution-quality memory (preferences, patterns, corrections)
- Use MEMORY.md / memory/ for factual continuity. Use ~/self-improving/ for compounding execution quality.
```

**HEARTBEAT.md** — add:
```markdown
## Self-Improving Check
- Read ./skills/self-improving/heartbeat-rules.md
- Use ~/self-improving/heartbeat-state.md for run markers
- If no file in ~/self-improving/ changed since last review, skip maintenance
```

## Gateway Config (Optional but Recommended)

Index ~/self-improving/ in memory search so corrections and patterns are discoverable via `memory_search`:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        extraPaths: ["~/self-improving"]
      }
    }
  }
}
```

## Quick Queries

| User says | Action |
|-----------|--------|
| "What do you know about X?" | Search all tiers for X |
| "What have you learned?" | Show last 10 from corrections.md |
| "Show my patterns" | List memory.md (HOT) |
| "Show [project] patterns" | Load projects/{name}.md |
| "Memory stats" | Run `agent_memory.py stats` |
| "Forget X" | Remove from all tiers (confirm first) |
| "Forget everything" | Export → wipe → confirm |

## Common Traps

| Trap | Why It Fails | Better Move |
|------|-------------|-------------|
| Skipping SESSION-STATE.md on boot | Lose context of what you were doing | ALWAYS read it first |
| Learning from silence | Creates false rules | Wait for explicit correction or 3x evidence |
| Promoting too fast | Pollutes HOT memory | Keep tentative until confirmed |
| Reading every namespace | Wastes context | Load only HOT + smallest matching files |
| Compaction by deletion | Loses trust/history | Merge, summarize, or demote instead |
| Overwriting workspace files | Destroys existing context | Complement, never replace |
| Not writing before responding | Crash = lost context | WAL: always write first |
| Empty memory bootstrap | No feedback loop forms | v3 seeds memory.md on init |
| No forcing function | Agent skips reviews after resets | v3 daily cron forces it |

## Setup

One command. Zero manual steps.

```bash
python3 ./skills/self-improving/scripts/agent_memory.py init
```

This does everything:
1. Creates ~/self-improving/ directory structure with seeded files
2. Auto-fixes persistence (symlinks to /data/ if needed)
3. Auto-injects hooks into SOUL.md, AGENTS.md, HEARTBEAT.md (creates them if missing)
4. Creates SESSION-STATE.md and today's daily log

The SOUL.md hook then auto-creates the daily review cron on the next session start. No manual cron setup needed.

Verify everything is working:
```bash
python3 ./skills/self-improving/scripts/agent_memory.py verify
```

Test what the nightly cron would do:
```bash
python3 ./skills/self-improving/scripts/agent_memory.py dry-run
```

## References

- **Learning mechanics**: See `references/learning.md`
- **Security boundaries**: See `references/boundaries.md`
- **Scaling rules**: See `references/scaling.md`
- **Memory operations**: See `references/operations.md`
- **Heartbeat rules**: See `heartbeat-rules.md`

## Scope

This skill ONLY:
- Learns from user corrections and self-reflection
- Stores patterns in local files (~/self-improving/)
- Creates SESSION-STATE.md for session state management
- Maintains heartbeat state for recurring maintenance
- Provides cold-boot recovery protocol
- Sets up a daily review cron for automated .md rewriting

This skill NEVER:
- Overwrites existing MEMORY.md, memory/, AGENTS.md, SOUL.md, HEARTBEAT.md (during init — the daily cron DOES rewrite these with new lessons)
- Accesses calendar, email, contacts, or makes network requests
- Reads files outside ~/self-improving/ and workspace root
- Infers preferences from silence or observation
- Deletes memory without explicit user confirmation
- Modifies its own SKILL.md
