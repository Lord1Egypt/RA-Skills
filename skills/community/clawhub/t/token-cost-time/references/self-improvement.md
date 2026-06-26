# Self-Improvement Guide

`token-cost-time` ships with baseline priors — published benchmark data that gives you a working triangle on day one. But the real value is what happens after you start using it.

Every LLM run you record teaches the tool about *your* workload. Your prompt style. Your task mix. How your actual token consumption compares to the baseline. After enough runs, the estimates stop being generic and start being yours.

This document explains how to close that loop.

---

## What to Capture After Every LLM Run

After any LLM task completes, you have everything you need to feed the calibration engine:

| Field | Where to get it |
|-------|----------------|
| `model` | The model you used (e.g. `claude-haiku-3`) |
| `taskClass` | What kind of task it was — run `classify` if unsure |
| `inputTokens` | From your provider's usage response |
| `outputTokens` | From your provider's usage response |
| `durationMs` | Wall-clock time from send to last token |
| `cost` | Actual dollar cost from your provider dashboard or usage API |
| `retries` | How many times you re-ran or heavily edited the output (0 if clean) |

You don't need all fields every time. `model`, `taskClass`, `inputTokens`, `outputTokens`, and `durationMs` are the minimum useful set. Cost and retries add calibration depth over time.

---

## How to Record — Three Ways

### 1. CLI (quickest for manual logging)

```bash
node cli/index.js record \
  --model claude-haiku-3 \
  --task-class summarization \
  --input-tokens 1340 \
  --output-tokens 290 \
  --duration-ms 4100 \
  --cost 0.00071
```

Profile saves to `~/.token-cost-time/profile.json` by default.

### 2. Node script (embed in your own tooling)

```js
import { record } from './src/record.js';

record({
  model: 'claude-sonnet-4',
  taskClass: 'code_generation',
  inputTokens: 2840,
  outputTokens: 680,
  durationMs: 9200,
  cost: 0.0189,
  retries: 0
});
```

Call this at the end of any script that makes an LLM call. No extra setup required.

### 3. OpenClaw cron (automated, runs after agent sessions)

Wire a lightweight cron that reads your session's token usage from `session_status` and calls `record()` automatically. This closes the loop without any manual step.

Minimal cron prompt:

```
After this session completes: read the token usage from session_status,
classify the primary task objective, then run:
node /path/to/token-cost-time/cli/index.js record \
  --model <model> \
  --task-class <class> \
  --input-tokens <n> \
  --output-tokens <n> \
  --duration-ms <n>
```

---

## How to Know It's Working

After recording runs, inspect your profile at `~/.token-cost-time/profile.json`. Open it in any text editor or JSON viewer.

A cold profile (0 runs) looks like:
```json
{
  "version": 1,
  "modelTaskStats": {},
  "modelStats": {}
}
```

After 10 runs on `claude-haiku-3` / `summarization`:
```json
{
  "modelTaskStats": {
    "claude-haiku-3::summarization": {
      "runs": 10,
      "inputAvg": 1420,
      "outputAvg": 305,
      "durationAvg": 3900,
      "costAvg": 0.00068,
      "retryRate": 0.1
    }
  }
}
```

The `confidence` field in `calibrate()` output tells you where you stand:

| Runs | Confidence | What it means |
|------|-----------|---------------|
| 0 | 0.20 | Pure baseline — treat as directional only |
| 10 | 0.35 | Early signal — estimates improving |
| 25 | 0.58 | Meaningful personalization |
| 50+ | 0.95 | Well-calibrated — trust it |

The triangle saturation in any UI built on top of this engine should reflect these confidence values directly. Washed out = low confidence. Solid = earned.

---

## Inspecting Your Execution Log

Every recorded run appends to:

```
~/.token-cost-time/execution-log.jsonl
```

Each line is one run. You can grep, sort, or analyze it:

    # See all runs for a specific model
The log is newline-delimited JSON. Each line is one execution record. Open it in any text editor, import it into a spreadsheet, or parse it with any JSON tool of your choice. Fields: model, taskClass, inputTokens, outputTokens, durationMs, costUsd, retries, timestamp.

---

## The Cold Start Warning

The first 10 runs on any model + task class combination are still heavily weighted toward baseline priors. Don't read too much into estimates during this period — confidence will show 0.20–0.35 and that's accurate.

By 25–30 runs on a given combination, the estimates are meaningfully personalized. By 50, they reflect your actual workload.

If you use multiple models across multiple task types, each combination calibrates independently. You might have 50 runs on `claude-haiku-3 / summarization` and 0 runs on `gpt-4o / code_audit` — the triangle shows different confidence levels for each, which is exactly right.

---

## The Self-Improvement Loop in Practice

The full loop, once wired:

1. You describe an objective
2. `calibrate()` estimates tokens/cost/time using your profile (or baseline if cold)
3. You choose a model and proceed
4. Task completes — provider returns actual token counts and duration
5. `record()` updates your profile with actuals
6. Next time you run the same model + task class, the estimate is tighter

The tool gets smarter every time you use it. After a few weeks of consistent recording, your estimates will be specific to how *you* use LLMs — not how the average developer does.

That's the point of this tool. The baseline is just the starting gun.
