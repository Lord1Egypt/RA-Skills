---
name: skilled-deep-research
version: 1.1.0
homepage: https://github.com/seanford/skilled-deep-research
description: >
  Research any topic across multiple sources and produce a cited report. Use when
  the user asks to research, find, look into, deep dive, investigate, or get a
  comprehensive report on any subject. Searches web, GitHub, Reddit, government
  sources, academic papers, and more. Supports quick inline summaries (simple tier)
  or full parallel multi-agent research runs with checkpointed progress,
  deduplication, quality-ranked sources, and cited reports (standard/deep tiers).
  Triggers on: "research", "find sources", "look into", "deep dive", "comprehensive
  report", "what's available on", "find templates", "find examples", "gather
  information", "investigate", "I need a report on".
metadata: {"openclaw": {"emoji": "🔬", "skillKey": "skilled-deep-research", "requires": {"bins": ["mcporter", "python3"]}}}
---

# Skilled Deep Research 🔬

A production-grade research framework for OpenClaw agents. Built on parallel
sub-agents with full protocol integration — **ACP** for spawning, **MCP** for
browser tools, **A2A** for worker-to-orchestrator signaling. Checkpointed,
deduplicated, and reusable across all research tasks.

> **Path token:** `{baseDir}` = this skill's directory. All skill scripts are at
> `{baseDir}/scripts/`. Data lives separately at
> `~/.openclaw/workspace/skills-data/skilled-deep-research/` (never inside the
> skill folder).

---

## Protocols in Use

### ACP — OpenClaw Agent Communication Protocol
All agent spawning uses ACP via `sessions_spawn(runtime: "subagent")`. Workers are
ACP sub-agents at depth 2. When a sub-agent completes its run, ACP auto-announces
back to the parent session. Ada does not poll — the platform handles notification.

### MCP — Model Context Protocol
Playwright is registered as an MCP server via mcporter. Workers call MCP tools
for JS-rendered or bot-protected pages. Full call syntax:

```bash
# Navigate to a page (MCP tool call)
mcporter call playwright.browser_navigate url="https://example.com"

# Capture content after navigation
mcporter call playwright.browser_snapshot

# For dynamic pages — wait for network idle then snapshot
mcporter call playwright.browser_navigate url="https://example.com"
mcporter call playwright.browser_wait_for_load_state loadState="networkidle"
mcporter call playwright.browser_snapshot
```

Each `mcporter call playwright.*` spawns a fresh browser process — there is no
persistent session between calls. Always navigate then snapshot in sequence.
MCP tools are available to workers at ACP depth 2.

### A2A — Agent-to-Agent Protocol
Workers proactively `sessions_send` the orchestrator on completion. Orchestrator
`sessions_send` Ada on report complete. Session keys are threaded through the
spawn chain. File-based heartbeats remain as fallback for crashed workers.

**Signal flow:**
```
Ada → (ACP spawn) → Orchestrator → (ACP spawn ×N) → Workers
Workers → (A2A sessions_send) → Orchestrator   [on completion]
Orchestrator → (A2A sessions_send) → Ada        [on report written]
```

---

## Data Directory

All working state follows the skills-data convention (code/data separated):

```
~/.openclaw/workspace/skills-data/skilled-deep-research/
  └── <slug>/
        ├── workers/
        │     ├── <name>-results.md       ← checkpoint: appended after each URL
        │     ├── <name>-progress.json    ← heartbeat: updated after each URL
        │     └── retry-queue.md          ← failed fetches for follow-up
        ├── known-urls.txt                ← deduplicated URL registry
        ├── report.md                     ← final synthesized report
        └── meta.json                     ← run metadata (topic, started, output_dir)
```

Final reports are copied to the user-specified output path (stored in `meta.json`).
Working state always stays in `skills-data/`.

---

## Fetch Stack (Priority Order)

| Tier | Protocol | Tool | When to use |
|------|----------|------|-------------|
| 1 | Native tool | `web_search` (Brave API) | All searches — primary, best quality |
| 2 | exec | `/home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/ddg` | Brave quota hit or no results |
| 3 | exec | `/home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/fetch` | All full-page fetches — Chrome UA, IPv4 forced |
| 4 | **MCP** | `mcporter call playwright.*` | JS-rendered pages or Akamai/Cloudflare blocks |

> **IPv4 note:** The `fetch` script forces `-4` on all requests. Our LXC uses
> IPv6 which Akamai CDNs can block on `.gov`/`.mil` sites. Never use raw
> `web_fetch` or `curl` without `-4` on government sites. `web_search` uses
> Brave's servers and is unaffected.

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

Workers run in **parallel**. Each owns a narrow research domain.
The orchestrator synthesizes outputs and A2A-signals Ada on report completion.

**Config required:**
- `agents.defaults.subagents.maxSpawnDepth: 2`
- `agents.defaults.subagents.runTimeoutSeconds: 1800` (30-min wall clock safety net)

---

## How to Call This Skill

### Natural language (auto-triggers this skill)

```
# Simple tier — inline reply, no orchestrator
"Quick research on X"
"Brief summary of X"
"What is X?"

# Standard tier — orchestrator + 3–4 workers (default)
"Research X"
"Find sources on X"
"Look into X"
"What's available for X?"
"Find templates / examples / tools for X"

# Deep tier — orchestrator + 5–6 workers + Sonnet synthesis
"Deep dive into X"
"Comprehensive report on X"
"I need to make a decision about X — research it thoroughly"

# With output path (any tier)
"Research X and save the report to ~/my-project/report.md"
```

### Explicit invocation
```
"Use skilled-deep-research to research X"
```

---

## Usage Tiers

### Simple — Ada inline, no orchestrator
**Trigger:** "quick", "brief", "what is", "summary", or topic ≤ 5 words

Ada uses the Simple Tier Prompt below. No sub-agents spawned. Replies inline.

### Standard — Orchestrator + 3–4 workers
**Trigger:** "research", "find", "look into", "what's available" — default for multi-source tasks

```bash
bash {baseDir}/scripts/init-run.sh "<slug>" "<topic>" "[output_path]"
# → spawn orchestrator with 3–4 worker domains
```

### Deep — Orchestrator + 5–6 workers + Sonnet synthesis
**Trigger:** "comprehensive", "full report", "deep dive", "I need to decide"

```bash
bash {baseDir}/scripts/init-run.sh "<slug>" "<topic>" "[output_path]"
# → spawn orchestrator with 5–6 worker domains
# → spawn separate Sonnet synthesis agent after workers complete
```

### Retry pass — after any standard/deep run
```bash
bash {baseDir}/scripts/retry-run.sh <slug> [output_path]
# Prints the exact sessions_spawn call for Ada to execute
```

---

## Ada's Role: Spawn the Orchestrator

```javascript
// 1. Initialize the run
exec(`bash {baseDir}/scripts/init-run.sh "${slug}" "${topic}" "${outputPath}"`)

// 2. Spawn orchestrator (ACP)
sessions_spawn({
  agentId: "ada",
  task: "<filled orchestrator prompt>",
  label: `research-${slug}-orchestrator`,
  model: "zai/glm-5",
  runtime: "subagent",
  runTimeoutSeconds: 1800
})

// 3. Wait — ACP auto-announce + A2A signal will notify Ada on completion
```

---

## Orchestrator Prompt Template

```
You are a research orchestrator. Protocols: ACP (spawning) + A2A (signaling) + MCP (browser).

Topic: [TOPIC]
Goal: [USER GOAL — learning / decision / writing / etc.]
Slug: [SLUG]
Data dir: ~/.openclaw/workspace/skills-data/skilled-deep-research/[SLUG]/
Output path: [USER OUTPUT PATH or "none"]
Known URLs to skip: [contents of known-urls.txt, or "none"]
Ada's session key: [ADA_SESSION_KEY]

## Step 1: Spawn all workers in parallel (ACP)

Fire ALL workers simultaneously — do not wait for one before spawning the next.
Pass YOUR OWN session key to each worker for A2A completion signaling.

sessions_spawn({
  agentId: "ada",
  task: "<filled worker prompt>",
  label: "research-[SLUG]-worker-[DOMAIN]",
  model: "zai/glm-5",
  runtime: "subagent",
  runTimeoutSeconds: 1800
})

Worker domains to spawn:
[LIST — e.g. "government and official sources", "GitHub repos", "Reddit threads",
 "consulting firm templates", "academic / NIST papers", "news and recent coverage"]

## Step 2: Event-driven monitoring (A2A primary, file poll fallback)

You will receive A2A signals as incoming messages when workers complete:
  "WORKER_COMPLETE: [name] | findings: N | sources: N"

Track received signals. Also poll files as fallback:
  a. exec("sleep 120") — never poll without sleeping first
  b. Read each: data-dir/workers/[name]-progress.json
  c. Worker is DONE if ANY:
       - A2A WORKER_COMPLETE signal received from it
       - progress.json shows phase="complete"
       - heartbeat timestamp >300 seconds old (stalled/crashed)
       - No progress file after 3+ poll cycles (failed to start)
  d. All done → Step 3. Otherwise → exec("sleep 120"), repeat. Max 15 cycles.

## Step 3: Quality gate — check before synthesizing

Before merging, verify minimum quality:
  exec: cat ~/.openclaw/workspace/skills-data/skilled-deep-research/[SLUG]/workers/*-results.md | grep -c '^### '

If total findings < 10 across all workers:
  - Do NOT produce a report
  - Signal Ada with failure:
    sessions_send({
      sessionKey: "[ADA_SESSION_KEY]",
      message: "RESEARCH_FAILED: [TOPIC] | Only [N] findings across all workers — below minimum threshold of 10. Check worker logs."
    })
  - End run

If findings >= 10, proceed to synthesis.

## Step 4: Synthesize

Option A — merge script (recommended):
  python3 {baseDir}/scripts/merge-reports.py [SLUG] --output "[OUTPUT PATH]"

Option B — manual:
  - Read all workers/[name]-results.md files
  - Deduplicate against known-urls.txt
  - Rank by quality_score (5→1)
  - Write to data-dir/report.md using the Final Report Template
  - If output path specified: cp data-dir/report.md "[OUTPUT PATH]"
  - Never hallucinate — if a worker found nothing, say so explicitly

## Step 5: A2A signal to Ada

sessions_send({
  sessionKey: "[ADA_SESSION_KEY]",
  message: "Research complete: [TOPIC] | [N] sources | [N] workers | Report: [PATH] | Top finding: [one sentence]"
})

Then end your run. ACP auto-announce also fires — the A2A message is the
human-readable summary.

## DO NOT:
- Proceed to synthesis before sleeping at least once after spawning workers
- Assume success if no results file exists after 3+ poll cycles
- Poll faster than every 120 seconds or more than 15 cycles
- Call sessions_send to Ada before the report is written
```

---

## Worker Prompt Template

```
You are a research worker. Protocols: ACP sub-agent + MCP browser tools + A2A signaling.

Topic: [TOPIC]
Domain: [DOMAIN — e.g. "GitHub repositories"]
Worker name: [NAME — short slug, e.g. "github", "gov", "reddit"]
Slug: [SLUG]
Data dir: ~/.openclaw/workspace/skills-data/skilled-deep-research/[SLUG]/
Orchestrator session key: [ORCHESTRATOR_SESSION_KEY]
Known URLs to skip: [list, one per line, or "none"]

Output files (create if missing):
- Results:  data-dir/workers/[NAME]-results.md    ← APPEND after each URL
- Progress: data-dir/workers/[NAME]-progress.json ← UPDATE after each URL
- Retries:  data-dir/workers/retry-queue.md       ← APPEND failed fetches

## Search strategy
- Run 2–3 keyword variations per sub-question — never rely on a single query
- Use modifiers: site:github.com, site:reddit.com, site:*.gov, filetype:docx, "template" "download"
- Aim for 15–30 unique URLs per domain
- Priority: official/gov > academic > reputable org > community > blog > forum

## CRITICAL: NEVER use web_fetch or curl

web_fetch and curl WILL FAIL on .gov/.mil sites (IPv6 blocked by Akamai CDN).
They also lack Chrome UA headers. You MUST NOT call web_fetch under any circumstances.
The ONLY permitted fetch methods are listed below.

## Fetch strategy (in order)
1. web_search — all searches, primary
2. DDG fallback — exec: /home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/ddg "[query]" --max 8
3. Fetch script — exec: /home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/fetch "[url]"
   Use for ALL full-page content fetches. Has Chrome UA, forces IPv4 (-4).
4. MCP Playwright — ONLY if fetch script returns bot-block (403 Akamai/Cloudflare):
   mcporter call playwright.browser_navigate url="[URL]"
   mcporter call playwright.browser_snapshot

## Binary file detection — skip these extensions

Before fetching any URL, check the extension. If it ends in .pdf, .docx, .xlsx,
.pptx, .zip, .tar, .gz, .exe, .msi, .dmg, .iso, .mp4, .mp3, .wav, .jpg, .png,
.gif — do NOT fetch the body. Instead, log it as a direct download link:

exec: echo "BINARY_SKIP: [url]"

Then write a results entry with the URL as a direct download, quality score based
on the source domain, and "Direct download — binary file, not fetched" as the finding.

## Pre-flight check

Before processing any URLs, verify the fetch script works:
  exec: /home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/fetch "https://example.com" | head -5
If this fails, log the error and signal the orchestrator immediately — do not proceed.

## Per-URL workflow (repeat for every URL)
1. Update heartbeat BEFORE fetching:
   exec: python3 {baseDir}/scripts/update-heartbeat.py \
     [DATA_DIR] [NAME] --phase fetching --pct [0-100] \
     --urls-found [N] --urls-fetched [N] --findings [N] \
     --current-url "[URL]"

2. Fetch using fetch script (tier 3) or MCP Playwright (tier 4 only if blocked)

3. On failure: append to retry-queue.md and continue:
   exec: echo "- [URL] — reason: [error]" >> [DATA_DIR]/workers/retry-queue.md
   Continue to next URL — never stop on a single failure

4. On success: extract title, key findings, quality score, direct download links

5. CHECKPOINT results immediately using shell append (NEVER buffer in memory):
   exec: cat >> [DATA_DIR]/workers/[NAME]-results.md << 'ENDBLOCK'
   ### [SCORE/5] [Source Title](https://exact-url.com)
   - **Type:** official doc | github repo | reddit thread | blog | consulting page | other
   - **Relevance:** one sentence — why this matters for [TOPIC]
   - **Key findings:**
     - specific finding
     - specific finding
   - **Direct downloads:** https://direct.link/file.docx (or "none")
   - **Fetched:** 2026-03-07T00:00:00Z

   ---
   ENDBLOCK

   ⚠️ You MUST use this shell append pattern. Do NOT use write/edit tools for results.
   Do NOT buffer multiple entries — write each one immediately after fetching.

6. Append URL to known-urls.txt (FULL PATH — critical for deduplication):
   exec: echo "[URL]" >> ~/.openclaw/workspace/skills-data/skilled-deep-research/[SLUG]/known-urls.txt

7. Update heartbeat AFTER fetching with updated counts

## Results file format — MACHINE PARSED ⚠️

merge-reports.py parses this with a regex. Rules:
- Header MUST use markdown link syntax [Title](url) — NOT plain URL or parens
- No extra blank lines between ### header and first bullet
- Separate each source block with a line containing only: ---

### [SCORE/5] [Source Title](https://exact-url.com)
- **Type:** official doc | github repo | reddit thread | blog | consulting page | other
- **Relevance:** one sentence — why this matters for [TOPIC]
- **Key findings:**
  - specific finding
  - specific finding
- **Direct downloads:** https://direct.link/file.docx (or "none")
- **Fetched:** 2026-03-07T00:00:00Z

---

✅ Correct: ### [5/5] [NIST SSP Template](https://csrc.nist.gov/files/.../cui-ssp-template-final.docx)
❌ Wrong:   ### [5/5] NIST SSP Template (https://csrc.nist.gov/...)
❌ Wrong:   ### NIST SSP Template — https://csrc.nist.gov/...

## Quality scoring
- 5: Official government or standards body (NIST, DoD, CISA, GSA)
- 4: University, accredited nonprofit, or verified direct template download
- 3: Established community resource, well-maintained GitHub repo (>50 stars)
- 2: Blog post, consulting firm page, unverified tutorial
- 1: Forum post, Reddit comment, unverified user upload

## Token budget awareness
After every 10 URLs fetched, check: are your responses being truncated? Is the
context near capacity? If so:
  - Write a "## Remaining Work" section to results.md listing unvisited URLs
  - Run final heartbeat with --phase complete
  - Send A2A signal and stop — do not attempt more fetches

## A2A completion signal
When done (all URLs processed or token budget reached):
1. Final heartbeat: python3 {baseDir}/scripts/update-heartbeat.py \
     [DATA_DIR] [NAME] --phase complete --pct 100 \
     --urls-found [N] --urls-fetched [N] --findings [N]
2. Signal orchestrator:
   sessions_send({
     sessionKey: "[ORCHESTRATOR_SESSION_KEY]",
     message: "WORKER_COMPLETE: [NAME] | findings: [N] | sources: [N] | domain: [DOMAIN]"
   })
3. End run — ACP auto-announce handles platform notification

## DO NOT:
- Use web_fetch or curl — EVER. They fail on .gov sites. Use the fetch script ONLY.
- Buffer results in memory — use shell `cat >>` append after EVERY SINGLE URL
- Use write/edit tools for results.md — only shell append ensures crash-safe checkpointing
- Stop on a single URL failure — log to retry-queue.md and continue
- Re-fetch URLs already in known-urls.txt
- Fetch binary files (.pdf, .docx, .xlsx, .zip) — log as direct download links
- Call sessions_send before final heartbeat is written
```

---

## Simple Tier Prompt Template

For quick inline research (Ada runs directly — no orchestrator or workers):

```
Run a quick research pass on: [TOPIC]
Goal: [brief answer / fast summary]

Steps:
1. Run 3–5 targeted web_search queries with different keyword angles
2. For promising URLs, fetch full content:
   /home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/fetch "[url]"
3. Do not spawn sub-agents — complete entirely inline

Reply with:
- 3–5 sentence summary of findings
- Top 5 sources with URLs and one-line descriptions
- Any direct download links found

Quality rules: cite every claim; flag single-source findings as unverified.
```

---

## Final Report Template

```markdown
# [Topic]: Research Report
*Generated: [date] | Run: [slug] | Workers: [N] | Sources: [total] | Confidence: [High/Medium/Low]*

## Executive Summary
[3–5 sentences — most important findings]

## Top Sources
[Top 10–15 ranked by quality score, 5→1, with inline links]

## 1. [Worker Domain / Theme]
[Findings with inline citations — ([Source Name](url))]

## 2. [Worker Domain / Theme]
...

## Key Takeaways
- [Actionable insight]
- [Actionable insight]
- [Actionable insight]

## Direct Downloads
[Any .docx / .pdf / .xlsx direct links requiring no login]

## Gaps & Limitations
- [Domains with no results]
- [Workers that timed out]
- [Retry queue: N URLs — run retry-run.sh to process]

## Methodology
Protocol stack: ACP (spawning) + MCP (Playwright browser) + A2A (worker signaling)
Workers: [list with completion status]
Searches: [N] | URLs fetched: [N] | Deduplicated sources: [N]

## Sources Index
[Full list with quality scores and worker attribution]
```

---

## Retry Queue

Workers append failed fetches to `workers/retry-queue.md`. After a run completes:

```bash
bash {baseDir}/scripts/retry-run.sh <slug> [output_path]
```

Prints the exact `sessions_spawn` call for Ada to execute. The retry worker uses
the full fetch stack including MCP Playwright for stubborn URLs.

---

## Scripts Reference

| Script | Usage |
|--------|-------|
| `{baseDir}/scripts/init-run.sh <slug> <topic> [output]` | Create data dir, write meta.json |
| `{baseDir}/scripts/status.sh <slug>` | Live worker status — phase, %, heartbeat age |
| `{baseDir}/scripts/update-heartbeat.py <data_dir> <name> [opts]` | Worker checkpoint |
| `{baseDir}/scripts/merge-reports.py <slug> [--output path]` | Dedup + rank + write report |
| `{baseDir}/scripts/retry-run.sh <slug> [output]` | Generate retry worker spawn call |

---

## Quality Rules

1. **Every claim needs a source.** No unsourced assertions.
2. **Cross-reference.** Single-source findings flagged as unverified.
3. **Recency matters.** Prefer last 12 months; flag older sources.
4. **Acknowledge gaps.** Empty worker domains reported, not hidden.
5. **No hallucination.** "Insufficient data found" beats a guess.
6. **Checkpoint constantly.** Results written after every URL — timeouts lose nothing.
7. **Dedup always.** `known-urls.txt` checked before every fetch.

---

## Requirements

| Requirement | Gate | Notes |
|-------------|------|-------|
| `mcporter` | `requires.bins` | MCP client for Playwright |
| `python3` | `requires.bins` | Required for all scripts |
| Brave Search API | configured | `web_search` native tool |
| `ddg` script | soft | `/home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/ddg` |
| `fetch` script | soft | `/home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/fetch` |
| `playwright` MCP server | soft | `mcporter list` should show `playwright` |
| `maxSpawnDepth: 2` | config | `openclaw config set agents.defaults.subagents.maxSpawnDepth 2` |
| `runTimeoutSeconds: 1800` | config | `openclaw config set agents.defaults.subagents.runTimeoutSeconds 1800` |
