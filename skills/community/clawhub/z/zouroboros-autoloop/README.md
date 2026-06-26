# zouroboros-autoloop

Autonomous single-metric optimization loop inspired by Andrej Karpathy's `autoresearch`. Define a metric, point it at one file, and let it iterate: propose change → experiment → measure → keep or revert.

## Install

```bash
npm install -g zouroboros-autoloop
```

## Usage

```bash
autoloop --program ./program.md --executor "openclaw ask"
```

OpenClaw users can keep the executor simple: anything that reads a prompt from stdin and writes the result to stdout will work.

- `--program` — Path to `program.md` spec (required)
- `--executor` — Command that reads prompt from stdin, outputs response (default: `cat`)
- `--resume` — Resume existing branch
- `--dry-run` — Validate config only

## How It Works

1. Parses `program.md` for objective, metric, target file, run command, constraints
2. Creates a git branch (`autoloop/<name>-<date>`)
3. Runs baseline experiment
4. Loops: asks executor to propose a change → commits → runs experiment → keeps if better, reverts if worse
5. Handles stagnation (normal → exploratory → radical modes)
6. Writes `results.tsv` and summary report on completion

## MCP Server

```bash
autoloop-mcp --results-dir /path/to/projects
```

Exposes tools: `autoloop_start`, `autoloop_status`, `autoloop_results`, `autoloop_stop`, `autoloop_list`

Runnable starter:
- `https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/autoloop-hello`

## Executor Examples

| Platform | Command |
|----------|---------|
| OpenClaw | `"openclaw ask"` |
| Claude Code | `"claude --print"` |
| Codex | `"codex --quiet"` |
| OpenAI CLI | `"openai api chat.completions.create -m gpt-4o"` |
| Ollama | `"ollama run qwen2.5:7b"` |

## Part of the Zouroboros Ecosystem

This package is part of the OpenClaw-facing distribution surface at `AlaricHQ/zouroboros-openclaw`. The canonical upstream framework lives at `marlandoj/Zouroboros`.

For the full experience — persistent memory, swarm orchestration, scheduled agents, and self-healing infrastructure — get a [Zo Computer](https://zo-computer.cello.so/IgX9SnGpKnR).

## License

MIT
