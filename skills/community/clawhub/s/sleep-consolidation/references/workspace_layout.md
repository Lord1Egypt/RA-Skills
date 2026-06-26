# Workspace Layout Reference

Full file structure and format examples for the sleep-consolidation skill.

---

## Directory tree

```
~/.agent_workspace/
├── MEMORY.md                      ← long-term curated facts (load every session)
├── .session_count                 ← integer, incremented each sleep cycle
├── memory/
│   ├── 2025-01-15.md              ← today's daily log (append-only)
│   ├── 2025-01-14.md              ← yesterday (auto-loaded)
│   └── ...
└── bank/
    ├── entities/                  ← per-person, per-project pages
    │   ├── alice.md
    │   └── project-phoenix.md
    └── concepts/                  ← per-topic deep-dives
        ├── chunking-strategy.md
        └── rate-limiting.md
```

---

## MEMORY.md format

```markdown
## Session 2025-01-14
- W: Redis default port is 6379
- B: Fixed auth bug by wrapping connection.update in try/catch
- O(c=0.90): User prefers replies under 200 words on WhatsApp
- S: Three consecutive sessions had latency spikes above 2s at >10k memory entries

## Session 2025-01-15
- W: OpenClaw workspace defaults to ~/.openclaw/workspace
- O(c=0.75): User likely uses TypeScript; Python was rejected twice
- B: Implemented hybrid BM25+vector search for memory recall

## REM Synthesis — 2025-01-15

### Insights
- Latency spikes correlate with memory store size — likely O(n) scan in retrieval
- User's verbosity preference + TypeScript preference suggests background in typed, concise codebases

### Creative connections
- Redis port knowledge ↔ rate-limit config: both are network-layer facts; consolidate into a "network config" bank page

### Next session
- [ ] Profile memory_search at 5k / 10k / 20k entries
- [ ] Propose TypeScript migration plan if Python rejected again
```

---

## Daily log format (memory/YYYY-MM-DD.md)

Append-only. Each micro-rest or flush adds a timestamped block.

```markdown
### 09:15 [micro-rest]
## Retain
- W: Project Phoenix repo is at github.com/acme/phoenix
- B: User asked about deployment; recommended Docker Compose

### 14:32 [micro-rest]
## Retain
- O(c=0.85): User prefers to review PRs same day they're opened
- W: Staging environment URL is staging.acme.com

### 23:45 [compaction-flush]
## Retain
- B: Debugged three null-pointer exceptions; all in the auth middleware
- O(c=0.70): Team may switch from Jest to Vitest — mentioned twice
- S: Today was heavily auth-focused; two bugs + one design discussion
```

---

## Bank entity page format (bank/entities/alice.md)

```markdown
# Alice

## Overview
Lead developer on Project Phoenix. Works EST. Direct communication style.

## Preferences
- O(c=0.95): Prefers async code reviews over sync review sessions
- O(c=0.80): Dislikes excessive inline comments

## Key interactions
- B: 2025-01-10: Resolved merge conflict together; she found root cause
- B: 2025-01-14: Reviewed my PR within 2 hours — fast turnaround
```

---

## Bank concept page format (bank/concepts/chunking-strategy.md)

```markdown
# Chunking Strategy

## Overview
Strategy for splitting documents into retrieval chunks.

## Findings
- W: 512-token chunks outperform 256-token for this domain (tested 2025-01-12)
- W: Overlap of 50 tokens reduces context loss at boundaries
- O(c=0.60): 256-token chunks may perform better for code files (untested)

## Open questions
- Does optimal chunk size depend on content type (prose vs. code)?
- How does chunk size interact with the BM25 retrieval step?
```

---

## Memory type reference

| Prefix | Full name | When to use |
|--------|-----------|-------------|
| `W` | World fact | Objective facts about the external world |
| `B` | Biographical/experience | What the agent did, observed, or experienced |
| `O(c=N)` | Opinion/preference | Subjective judgments; N = confidence 0–1 |
| `S` | Summary | Synthesized observations across multiple events |

Confidence (`c`) applies to all types but is most critical for `O`. Update confidence as evidence accumulates.

---

## What goes where

| Content type | Destination |
|-------------|-------------|
| Durable facts, preferences, key decisions | `MEMORY.md` |
| Day-to-day notes, running context | `memory/YYYY-MM-DD.md` |
| Deep knowledge about a specific person | `bank/entities/{name}.md` |
| Deep knowledge about a specific topic | `bank/concepts/{topic}.md` |
| Transient context (current task details) | RAM only — do not persist |

**Rule of thumb**: if you'd want the agent to know this in a fresh session three weeks from now, write it to `MEMORY.md`. If it's useful context for the next few sessions, write it to the daily log.
