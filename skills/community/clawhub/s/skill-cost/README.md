# skill-cost

**Which of my OpenClaw skills is burning the most money?**

I've been running OpenClaw with a growing collection of skills — chat connectors, code generators, grid monitors, you name it. The monthly bill kept climbing and I had no idea which skill was the culprit. The existing cost trackers on ClawHub (session-cost, openclaw-cost-tracker, tokenmeter) all break down spending by *model*, but none of them answer the question I actually care about:

> *"Is it my poe-connector or my web-search that's eating all my tokens?"*

So I built **skill-cost** — a dead-simple, zero-dependency tool that reads your local OpenClaw session logs and tells you exactly how much each skill is costing you.

## What It Does

```
────────────────────────────────────────────────────────────
Skill                      Calls     Tokens       Cost     %
────────────────────────────────────────────────────────────
(conversation)               420       6.2M     $14.20   45%
web-search                   180       2.8M      $5.60   18%
poe-connector                95       1.5M      $4.20   13%
github-tools                 72       1.1M      $3.30   10%
(built-in)                    48     780.0K      $2.10    7%
code-runner                  32     520.0K      $1.56    5%
file-utils                   18     290.0K      $0.87    3%
────────────────────────────────────────────────────────────
Total                        857      13.2M     $31.83  100%
```

Now I know: web-search and poe-connector are my money pits. Time to optimize (or at least stop blaming the small ones).

## Install

```bash
# If you're using ClawHub:
clawhub install dzwalker/skill-cost

# Or manually:
git clone https://github.com/dzwalker/skill-cost.git ~/.openclaw/workspace/skills/skill-cost
```

No pip install needed — pure Python stdlib, zero external dependencies.

## Usage

All commands go through the wrapper script:

```bash
# Full per-skill cost report
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report

# Last 7 days only
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --days 7

# Since a specific date
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --since 2026-03-01

# Top 10 skills by cost
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh ranking

# Deep dive into a specific skill (by model + by day)
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh detail poe-connector

# Compare two skills side by side
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh compare poe-connector web-search

# JSON output (for dashboards, scripts, etc.)
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --format json
```

### Global Options

| Option | Description |
|--------|-------------|
| `--days N` | Only include data from the last N days |
| `--since YYYY-MM-DD` | Only include data since this date |
| `--agent NAME` | Filter by agent name |
| `--agents-dir PATH` | Custom agents directory |
| `--format text\|json` | Output format (default: text) |
| `--top N` | Show only top N skills |

## How It Works

1. Scans `~/.openclaw/agents/*/sessions/*.jsonl` for session data
2. Parses each assistant message for tool calls and token usage
3. **Attributes tokens to skills** by:
   - Matching bash/exec command paths (`~/.openclaw/workspace/skills/<name>/`)
   - Mapping tool names to skills via SKILL.md frontmatter discovery
4. Proportionally splits tokens when a message involves multiple skills
5. Categorizes unattributable usage as `(built-in)` or `(conversation)`

### Cost Calculation

Costs are computed using the `cost.total` field from session logs when available (preferred). Falls back to token count × model pricing for older entries that lack cost data.

## Why Not Just Use session-cost?

| | session-cost | skill-cost |
|---|---|---|
| **Dimension** | By model | By skill |
| **Answers** | "How much did Claude vs GPT cost?" | "How much did poe-connector vs web-search cost?" |
| **Use case** | Model selection | Skill optimization |

They're complementary — use both if you want the full picture.

## Requirements

- Python 3.9+
- OpenClaw with session data in `~/.openclaw/agents/`
- No external dependencies

## License

MIT
