---
name: zouroboros-autoloop
description: "Autonomous optimization loop inspired by Andrej Karpathy's autoresearch: edit, experiment, measure, keep or revert. Best for any task with a numeric metric."
version: "1.0.0"
compatibility: "OpenClaw, Claude Code, Codex CLI, any Node.js 22+ environment"
metadata:
  author: marlandoj.zo.computer
  openclaw:
    emoji: "🔄"
    requires:
      bins: [node, git]
    install:
      - id: node-zouroboros-autoloop
        kind: node
        package: "zouroboros-autoloop"
        bins: [autoloop, autoloop-mcp]
        label: "Install Zouroboros Autoloop (npm)"
    homepage: https://github.com/AlaricHQ/zouroboros-openclaw
---

# Zouroboros Autoloop

Autonomous single-metric optimization loop. Reads a `program.md` spec, creates a git branch, and loops: propose change → commit → run experiment → measure metric → keep improvements, revert regressions. Inspired by Andrej Karpathy's `autoresearch` concept.

## Quick Start

```bash
npm install -g zouroboros-autoloop

# Create a program.md (see template below), then:
autoloop --program ./program.md --executor "openclaw ask"
```

## Usage

```bash
autoloop --program <path/to/program.md> [--executor <command>] [--resume] [--dry-run]
```

- `--program` — Path to your program.md specification (required)
- `--executor` — Shell command that reads a prompt from stdin and outputs a response
  - OpenClaw: `"openclaw ask"`
  - Claude Code: `"claude --print"`
  - Any LLM CLI that reads stdin
- `--resume` — Resume from an existing autoloop branch
- `--dry-run` — Validate program.md without running

## MCP Server

Autoloop includes an MCP server for tool-based integration:

```bash
autoloop-mcp --results-dir /path/to/projects
```

Tools exposed: `autoloop_start`, `autoloop_status`, `autoloop_results`, `autoloop_stop`, `autoloop_list`

## program.md Template

```markdown
# Program: my-optimization

## Objective
Optimize the trading strategy parameters for maximum Sharpe ratio.

## Metric
- **name**: sharpe_ratio
- **direction**: higher_is_better
- **extract**: `tail -1 results.csv | cut -d, -f3`

## Target File
`params.json`

## Run Command
```bash
node backtest.js --config params.json
```

## Constraints
- **Time budget per run**: 60
- **Max experiments**: 50
- **Max duration**: 4
- **Max cost**: 5

## Stagnation
- **Threshold**: 8
- **Double threshold**: 15
- **Triple threshold**: 25

## Read-Only Files
- backtest.js
- historical-data.csv

## Setup
```bash
npm install
```

## Notes
Focus on risk-adjusted returns. Avoid overfitting to recent data.
```

## Use Cases

- **Trading backtests** — Optimize strategy parameters against historical data
- **Prompt optimization** — Tune prompts to maximize a quality metric
- **Site performance** — Reduce load time, optimize bundle size
- **Model fine-tuning** — Iterate on hyperparameters with measurable output

## Part of the Zouroboros Ecosystem

Zouroboros is a self-improving AI orchestration framework. These standalone packages give you a taste of what's possible. For the full experience — persistent memory, swarm orchestration, scheduled agents, persona routing, and self-healing infrastructure — get a [Zo Computer](https://zo-computer.cello.so/IgX9SnGpKnR).

Built by [@Xmarlandoj](https://x.com/Xmarlandoj)
