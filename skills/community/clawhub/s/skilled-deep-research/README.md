# skilled-deep-research 🔬

A production-grade deep research framework for [OpenClaw](https://openclaw.ai) agents. Built on parallel sub-agents with full protocol integration — **ACP** for spawning, **MCP** for browser tools, **A2A** for worker-to-orchestrator signaling.

Designed to be reused across all research tasks, not just one-offs.

---

## Features

- **Parallel workers** — orchestrator fans out across 3–6 domain-specific agents simultaneously
- **Four-tier fetch stack** — Brave Search → DDG → Chrome UA curl (IPv4) → Playwright (MCP)
- **Checkpointed progress** — workers write results after every URL; timeouts lose nothing
- **A2A event signaling** — workers signal the orchestrator on completion; no blind polling
- **Deduplication** — shared `known-urls.txt` + merge-script dedup at synthesis
- **Quality scoring** — sources rated 1–5; reports ranked automatically
- **Retry queue** — failed fetches collected and re-run via a dedicated retry worker
- **Three usage tiers** — simple (inline) / standard (4 workers) / deep (6 workers + Sonnet synthesis)
- **Skills-data convention** — code and data separated; skill is publishable to ClawHub

---

## Protocol Stack

| Protocol | Role |
|----------|------|
| **ACP** (OpenClaw Agent Communication Protocol) | Spawning orchestrator and workers via `sessions_spawn(runtime: "subagent")`. Auto-announce on completion. |
| **MCP** (Model Context Protocol) | Playwright browser access via `mcporter`. Full headless Chromium for JS-rendered and bot-protected pages. |
| **A2A** (Agent-to-Agent) | Workers `sessions_send` the orchestrator on completion. Orchestrator `sessions_send` Ada on report complete. Event-driven coordination, file heartbeats as fallback. |

---

## Architecture

```
Ada (main session — ACP root)
  └── Orchestrator (ACP depth 1) ─────────────── receives A2A worker signals
        ├── Worker: gov        (ACP depth 2) ─── MCP Playwright for .gov sites
        ├── Worker: github     (ACP depth 2)
        ├── Worker: reddit     (ACP depth 2)
        ├── Worker: consulting (ACP depth 2)
        └── Worker: news       (ACP depth 2)
              └── On complete → A2A sessions_send → orchestrator
```

---

## Fetch Stack

| Tier | Tool | When |
|------|------|------|
| 1 | `web_search` (Brave API) | All searches — primary |
| 2 | `ddg` script | Brave quota hit or no results |
| 3 | `fetch` script (Chrome UA + IPv4) | All full-page fetches — beats basic bot filters |
| 4 | `mcporter call playwright.*` (MCP) | JS-rendered pages, Akamai/Cloudflare blocks |

> **IPv4 note:** The fetch script forces `-4` on all requests. Our LXC uses IPv6 which Akamai CDNs can block on `.gov`/`.mil` sites. `web_search` uses Brave's servers and is unaffected.

---

## How to Call It

Just ask naturally — Ada loads this skill automatically when the request matches:

```
# Simple (inline reply)
"Quick research on X"
"What is X?"

# Standard (orchestrator + workers, default)
"Research X"
"Find sources on X"
"Find templates / examples for X"

# Deep (6 workers + Sonnet synthesis)
"Deep dive into X"
"Comprehensive report on X"
"Research X and save the report to ~/path/report.md"
```

If Ada doesn't auto-trigger it: *"Use skilled-deep-research to research X"*

---

## Usage Tiers

### Simple — Ada inline
**When:** "quick", "brief", "what is", topic ≤ 5 words
```
Ada runs 3–5 searches inline, replies with summary + top 5 sources
```

### Standard — Orchestrator + 3–4 workers
**When:** "research", "find", "look into", multi-source topic (default)
```
init-run.sh → orchestrator → 4 parallel workers → merged report
```

### Deep — Orchestrator + 5–6 workers + Sonnet synthesis
**When:** "comprehensive", "full report", "deep dive", formal document output
```
init-run.sh → orchestrator → 6 parallel workers → Sonnet synthesis agent → report
```

### Retry pass — after any standard/deep run
```bash
bash scripts/retry-run.sh <slug> [output_path]
```

---

## Data Directory

Working state lives in the skills-data directory (separate from skill code):

```
~/.openclaw/workspace/skills-data/skilled-deep-research/
  └── <slug>/
        ├── workers/
        │     ├── <name>-results.md       # checkpoint: appended after each URL
        │     ├── <name>-progress.json    # heartbeat: updated after each URL
        │     └── retry-queue.md          # failed fetches
        ├── known-urls.txt                # dedup registry
        ├── report.md                     # final report
        └── meta.json                     # run metadata + output path
```

Final reports are copied to the user-specified output path. Working state stays in skills-data.

---

## Scripts

| Script | Usage |
|--------|-------|
| `init-run.sh <slug> <topic> [output]` | Create data dir, write meta.json |
| `status.sh <slug>` | Live worker status — phase, %, heartbeat age |
| `update-heartbeat.py <data_dir> <name> [opts]` | Worker heartbeat checkpoint |
| `merge-reports.py <slug> [--output path]` | Dedup + rank + write final report |
| `retry-run.sh <slug> [output]` | Print spawn call for retry worker |

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| [OpenClaw](https://openclaw.ai) | Agent runtime |
| Brave Search API key | `web_search` tool — primary search |
| `ddg` script | DDG fallback — see [ddg-search](https://github.com/seanford/ddg-search) |
| `fetch` script | Chrome UA + IPv4 curl wrapper |
| `mcporter` + `playwright` MCP server | `npm install -g mcporter && npx playwright-mcp` |
| `maxSpawnDepth: 2` | `openclaw config set agents.defaults.subagents.maxSpawnDepth 2` |
| `runTimeoutSeconds: 1800` | `openclaw config set agents.defaults.subagents.runTimeoutSeconds 1800` |

---

## Installation

```bash
# Via ClawHub
npx clawhub install seanford/skilled-deep-research

# Or clone directly
git clone https://github.com/seanford/skilled-deep-research.git \
  ~/.openclaw/workspace/skills/skilled-deep-research
```

---

## Related

- [skilled-openclaw-advisor](https://github.com/seanford/skilled-openclaw-advisor) — reference implementation of the skills-data convention
- [OpenClaw docs](https://docs.openclaw.ai) — ACP, MCP, and sub-agent documentation

---

## License

MIT
