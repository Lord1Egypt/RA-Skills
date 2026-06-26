---
name: random-thought
description: >
  Autonomous workspace reflection engine. Picks a random file from a configurable corpus,
  writes a reflective observation about what's unresolved, half-finished, or interesting,
  and periodically curates digests that surface actionable patterns. Two stages: writer
  (hourly reflection) and curator (periodic synthesis). Use when: (1) setting up autonomous
  workspace introspection via cron, (2) running a one-off "what should I think about?" reflection,
  (3) building self-awareness about patterns in your codebase or notes. Designed for cron-driven
  operation but works as a manual invocation too.
license: MIT
metadata:
  author: jeremyknows
  version: "1.0.0"
---

# Random Thought

A thinking engine that reads your workspace and writes about what it finds — not summaries,
not status updates, but genuine reflection on what's unresolved, alive, or worth questioning.

## Two Stages

### Writer
Pick a random file from the corpus, read it, write a reflective observation, and deliver it.

### Curator
Read all recent Writer outputs, synthesize patterns, classify observations using configurable
action tags, and produce a digest.

## Quick Start

### Manual invocation
Run the writer for a single reflection:
```bash
bash scripts/corpus-pick.sh        # see what file gets selected
# Then the agent reads the file and writes a reflection
```

### Cron-driven (recommended)
Wire two cron jobs — the writer runs frequently, the curator runs periodically:
```
# Writer: every hour
0 * * * *   openclaw skill run random-thought --stage writer

# Curator: daily at a quiet hour
0 5 * * *   openclaw skill run random-thought --stage curator
```

Each cron invocation runs in an isolated session — no context bleed between runs.

## Configuration

Create `random-thought.config.json` in your workspace root (all fields optional):

```json
{
  "corpus": {
    "watchDirs": ["."],
    "excludePatterns": [
      "node_modules", ".git", ".next", "dist", "build",
      "venv", "__pycache__", "*.png", "*.jpg", "*.gif",
      "*.mp3", "*.ogg", "*.pdf", "*.zip", "*.env",
      "*.pem", "*.key", "package-lock.json", "*.lock"
    ],
    "minFileSize": "100c",
    "maxFileSize": "500k"
  },
  "freshness": {
    "enabled": true,
    "days": 7,
    "historyFile": ".random-thought-history"
  },
  "actionTags": [
    { "name": "you-decide", "description": "Needs human judgment" },
    { "name": "agent-execute", "description": "Agent can act autonomously" },
    { "name": "spark", "description": "Interesting but no action needed" }
  ],
  "output": {
    "dir": "random-thought-output",
    "digestFormat": "markdown"
  }
}
```

### Configuration Reference

- **corpus.watchDirs** — Directories to scan (relative to workspace). Default: `["."]`
- **corpus.excludePatterns** — Glob patterns to exclude. Sensible defaults included.
- **freshness.enabled** — Prevent revisiting files within N days. Default: `true`
- **freshness.days** — Cooldown period per file. Default: `7`
- **freshness.historyFile** — Where to track visited files. Default: `.random-thought-history`
- **actionTags** — Labels the Curator uses to classify observations. Override to match your workflow.
- **output.dir** — Where digests are written. Default: `random-thought-output/`

## Writer Stage

### What it does
1. Run `scripts/corpus-pick.sh` to select a random file (respecting freshness gate)
2. Read the selected file (up to 200 lines if large)
3. Write a reflective observation — not a summary, not a review. Follow the thread wherever it leads.
4. Deliver the output (post to configured channel, write to file, or return to caller)

### Writer output format
- First line: `📂 [absolute path of the file selected in step 1]`
- Blank line
- Flowing prose. No bullets. No headers. No preamble.
- Follow what's unresolved, surprising, half-finished, or alive.
- Make connections to other things in the workspace if they surface naturally.
- Last line: `🖊️ *Writer*`

### Avoid these crutches
The Writer should push past generic phrasing:
- "quietly elegant" / "speaks to something deeper" / "testament to" / "tapestry"
- "there's something almost [adjective] about"
- "beautiful in its simplicity"

Concrete observations beat ornamental ones.

## Curator Stage

### What it does
1. Read all Writer outputs from the configured period (default: last 24 hours)
2. Classify each observation using configured **action tags**
3. Identify recurring themes or convergent patterns across observations
4. Write a structured digest to `output.dir/YYYY-MM-DD.md`

### Digest format
```markdown
# Random Thought Digest — YYYY-MM-DD

## Action Items
### you-decide
- [observation summary] — [why it needs human judgment]

### agent-execute
- [observation summary] — [what the agent should do]

## Patterns
[Recurring themes across today's observations — what's converging?]

## Sparks
- [Interesting observations with no action needed]
```

### Curator guidelines
- Classify every observation into exactly one action tag
- Surface theme convergence — if multiple observations point at the same gap, name it explicitly
- Keep the digest scannable — each item should be one line with context
- Do NOT re-surface items from previous digests unless they've evolved

## Scripts

### `scripts/corpus-pick.sh`
Selects a random file from the corpus, respecting the freshness gate.

**Usage:** `bash scripts/corpus-pick.sh [workspace_root] [config_path]`

- Reads configuration from `random-thought.config.json` if present
- Falls back to sensible defaults if no config exists
- Records selected file to the history file for freshness tracking
- Outputs the absolute path of the selected file

### `scripts/freshness-gate.sh`
Manages the file visit history for the freshness gate.

**Usage:**
- `bash scripts/freshness-gate.sh check <file> [config_path]` — exits 0 if file is fresh (OK to visit), 1 if recently visited
- `bash scripts/freshness-gate.sh record <file> [config_path]` — records a file visit
- `bash scripts/freshness-gate.sh prune [config_path]` — removes entries older than the configured window

## References

- **architecture.md** — Design rationale: why two stages, why cron-driven isolation matters, the hybrid skill+cron model. Read when customizing the pipeline or understanding trade-offs.
