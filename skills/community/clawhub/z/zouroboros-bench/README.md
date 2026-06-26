# zouroboros-bench

Benchmark harness for AI memory systems. Run LongMemEval, LoCoMo, and ConvoMem-style evaluations against a memory backend, then generate a report that is useful for actual comparison rather than vague impressions.

## Install

```bash
npm install -D zouroboros-bench
npm install zouroboros-memory
```

`zouroboros-bench` is designed to benchmark memory systems, and `zouroboros-memory` is the default companion backend for local runs.

## Usage

### Run all benchmarks

```bash
npx zouroboros-bench --limit 50
```

### Run a specific benchmark

```bash
npx zouroboros-bench --benchmarks longmemeval --limit 100 --judge
```

### Generate a report

```bash
npx zouroboros-bench-report --runs ./data/runs/
```

## Typical Workflow

1. Initialize and populate a memory database with `zouroboros-memory`
2. Point benchmark runs at that database
3. Run one benchmark at a time during iteration
4. Run the full suite once the backend is stable
5. Generate a report and compare across candidate memory approaches

Runnable starter:
- `https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/bench-local`

## Environment Variables

- `ZOUROBOROS_MEMORY_CLI` — Path to the memory CLI binary if not on `PATH`
- `ZOUROBOROS_MEMORY_DB` — SQLite DB path for benchmark runs
- `OPENAI_API_KEY` — Required if using the GPT-based judge
- `OLLAMA_URL` — Optional local model endpoint

## OpenClaw

This package is intended for OpenClaw users who want a measurable way to compare memory quality. It pairs naturally with `zouroboros-memory`, but the long-term shape should support any backend that can be adapted cleanly.

## Part of the Zouroboros Ecosystem

This package is part of the OpenClaw-facing distribution surface at `AlaricHQ/zouroboros-openclaw`. The canonical upstream framework lives at `marlandoj/Zouroboros`.

For the full experience — persistent memory, swarm orchestration, scheduled agents, persona routing, and self-healing infrastructure — get a [Zo Computer](https://zo-computer.cello.so/IgX9SnGpKnR).

## License

MIT
