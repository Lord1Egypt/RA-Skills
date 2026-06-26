# random-thought

An autonomous workspace reflection engine for AI agents. Picks a random file from your workspace, reads it, and writes a genuine observation — not a summary, not a status update, but reflection on what's unresolved, alive, or worth questioning.

Runs on a cron schedule. Each invocation is isolated. Periodically curates digests that surface patterns across observations.

## What it does

- **Writer stage** — picks a random file from your corpus (respecting a freshness gate to avoid repeats), reads it, and writes a reflective observation in flowing prose
- **Curator stage** — reads all recent Writer outputs, classifies them by action tag, surfaces recurring themes, and writes a structured digest
- **Freshness gate** — prevents revisiting files within a configurable window (default: 7 days)
- **Configurable corpus** — exclude patterns, file size limits, watch directories, custom action tags
- **Zero runtime** — plain bash scripts + agent instructions, no dependencies beyond Python 3

## Install

**OpenClaw:**
```bash
cd ~/.openclaw/skills
git clone https://github.com/jeremyknows/random-thought.git
```

**Claude Code:**
```bash
cd ~/.claude/skills
git clone https://github.com/jeremyknows/random-thought.git
```

**Any Agent Skills-compatible agent:**
```bash
cd /path/to/your/skills/dir
git clone https://github.com/jeremyknows/random-thought.git
```

## Setup

No setup required. Optionally create `random-thought.config.json` in your workspace root to customize behavior (see Configuration below).

Verify scripts are executable:
```bash
chmod +x scripts/corpus-pick.sh scripts/freshness-gate.sh
```

## Usage

### Natural language (just ask your agent)

- "Write a random thought about my workspace"
- "Run the random-thought writer stage"
- "Generate a digest of this week's observations"
- "Set up random-thought to run hourly"
- "What's in the random-thought digest?"

### Manual invocation

Run the writer for a one-off reflection:
```bash
bash scripts/corpus-pick.sh /path/to/workspace   # see what file gets selected
# Then ask your agent: "read that file and write a reflection"
```

Check freshness gate stats:
```bash
bash scripts/freshness-gate.sh stats
```

Prune stale history entries:
```bash
bash scripts/freshness-gate.sh prune
```

### Cron-driven (recommended)

Wire two cron jobs via your agent's scheduler:

```
# Writer: every hour during active hours
0 8-22 * * *   [agent] skill run random-thought --stage writer

# Curator: daily digest at a quiet hour
0 5 * * *      [agent] skill run random-thought --stage curator
```

Each cron invocation runs in an isolated session — no context bleed between runs. This is a feature: each observation is independent, which gives the Curator genuinely diverse inputs.

## Configuration

Create `random-thought.config.json` in your workspace root (all fields optional):

```json
{
  "corpus": {
    "watchDirs": ["."],
    "excludePatterns": [
      "node_modules", ".git", ".next", "dist", "build",
      "*.png", "*.jpg", "*.pdf", "*.env", "*.key"
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

## Commands

| Script | Usage | Description |
|--------|-------|-------------|
| `corpus-pick.sh` | `bash scripts/corpus-pick.sh [workspace] [config]` | Select a random file, record visit, output path |
| `freshness-gate.sh check` | `bash scripts/freshness-gate.sh check <file>` | Exit 0 if OK to visit, 1 if recently visited |
| `freshness-gate.sh record` | `bash scripts/freshness-gate.sh record <file>` | Record a file visit to history |
| `freshness-gate.sh prune` | `bash scripts/freshness-gate.sh prune` | Remove entries older than configured window |
| `freshness-gate.sh stats` | `bash scripts/freshness-gate.sh stats` | Show history entry counts |

## Limitations

- Writer output quality depends on the agent model — better models write better reflections
- Freshness gate uses file paths; if files move, the gate won't recognize them as visited
- The corpus scanner uses `find` — very large workspaces (100k+ files) may have slow first runs
- Curator requires Writer outputs in the configured output directory from a prior run

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No candidate files found` | All files excluded or workspace too small | Check `excludePatterns` in config; verify workspace path |
| Same file selected repeatedly | Freshness gate disabled or history file missing | Set `freshness.enabled: true`; check `historyFile` path |
| Curator produces empty digest | No Writer outputs in the configured window | Run Writer stage first; check `output.dir` in config |
| `sort: illegal option -- R` | macOS vs GNU sort difference | Already handled in corpus-pick.sh via python fallback |

## File Structure

```
random-thought/
├── SKILL.md                    # Agent instructions + frontmatter
├── LICENSE.txt                 # MIT license
├── README.md                   # This file
├── .gitignore                  # Excludes history file + output dir
├── scripts/
│   ├── corpus-pick.sh          # Random file selection with freshness gate
│   └── freshness-gate.sh       # History management (check/record/prune/stats)
└── references/
    └── architecture.md         # Design rationale — why two stages, why cron isolation
```

## License

MIT — see [LICENSE.txt](LICENSE.txt)
