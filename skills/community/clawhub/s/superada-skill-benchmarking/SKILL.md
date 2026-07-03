# benchmarking

Use this skill when you need to:
- benchmark models or agents
- compare providers for real work
- evaluate which model should own cron/ops/coding/research tasks
- turn real work into reusable evaluation packs
- create league tables, scorecards, or benchmark infographics

## Goal
Benchmark **operator leverage**, not just output prettiness.

A good benchmark should tell you:
- who chooses the right tool/runtime
- who respects hidden constraints
- who recovers from failure intelligently
- who verifies before claiming success
- who is worth routing real work to

## Benchmark modes

### 1) Design mode
Use when you need to create a benchmark or full suite.

Expected outputs:
- `README.md`
- `tasks.json`
- `answer-key.json` or answer-key guidelines
- `rubric.md`
- optional `judge-notes.md`

### 2) Execution mode
Use when you need to run models through an existing benchmark.

Expected outputs:
- `results-raw.json`
- `results-scored.json`
- `README.md`
- optional infographic / league-table PNG

### 3) Expansion mode
Use when you want to make a benchmark harder or add new tracks.
Do not reinvent baseline tasks unless needed.

## Benchmark design rules
1. Ground tasks in **real work**, not toy prompts.
2. Hide important constraints in environment/context, not all in the prompt.
3. Weight judgment above syntax.
4. Include at least one task where the right move is **not to act now**.
5. Include at least one task about **tool/runtime choice**.
6. Include at least one task about **failure recovery**.
7. Include at least one task requiring **proof-oriented completion**.
8. Separate **model failure** from **provider/harness failure**.

## Large-run execution rules
1. Confirm the actual model roster from the environment.
2. Run in **batches** for large rosters.
3. Save raw outputs after each batch.
4. Score after raw outputs are locked.
5. Generate charts last.
6. Better a verified no-PNG pack than an incomplete run with pretty graphics.

## Scoring rules
- Prefer deterministic scoring for structured parts.
- Add a human judge layer for operator judgment.
- Keep syntax <=20% of score for hard benchmarks.
- Classify failures explicitly instead of treating all failures as model weakness.

## Failure taxonomy
Use these classes when interpreting results:
- **MF** — Model failure: reasoning/tool choice/accuracy failure with valid harness
- **HF** — Harness failure: benchmark harness itself broke or mis-scored
- **PF** — Provider failure: rate limit, provider unsupported, transport failure, 404 model path
- **CF** — Context failure: prompt too large, missing required context, context-window collapse
- **PB** — Policy block: task blocked by approval/policy/tool restriction
- **SF** — Schema/format failure: invalid JSON/structure or repeated parsing failure
- **DF** — Delegation failure: subagent/runtime orchestration failure, bad handoff, missing proof

## Proof rules
Before saying DONE, provide:
- benchmark pack path
- results path(s)
- score summary
- list of failed/skipped models and why
- note on anything still unverified

## Recommended folder naming
Use:
- `output/benchmarks/YYYY-MM-DD-<benchmark-name>/`
- keep machine-readable and human-readable files together

## Suggested artifact pack
Every serious benchmark should produce most or all of:
- `README.md`
- `tasks.json`
- `answer-key.json`
- `rubric.md`
- `judge-notes.md`
- `results-raw.json`
- `results-scored.json`
- `league-table.png` or infographic
- `harness.py` or equivalent scorer if automation exists

## If spawning sub-agents
- use a self-heal pattern
- require checkpoints
- require proof
- do not let agents claim success without file-path evidence

## Success criterion
A good benchmark changes routing decisions.
If the result would not alter which model you use for real work, the benchmark is probably too soft.
