---
name: statb-dashboard
description: >-
  Push real-time progress and key metrics to a live statb.io dashboard during
  any long-running task. Use this skill whenever the agent is performing work
  that takes multiple steps, iterations, or extended time — such as coding,
  data processing, batch operations, training loops, deployments, migrations,
  CI runs, scraping, file conversions, or any multi-step automation. The agent
  should push numeric progress indicators (steps completed, items processed,
  errors encountered, percentages, durations, counters) to statb.io so the
  user can monitor progress in real time from a browser without interrupting
  the agent. Trigger phrases: "push to dashboard", "monitor progress",
  "track metrics", "show me a live board", "report status to statb",
  "use statb", "push to statb.io", "keep me updated on progress".
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📊"
    homepage: https://statb.io
---

# statb.io — Live Dashboard for Agent Runs

Push numeric key-value pairs to a statb.io board with a single `curl` call.
The user opens the board URL in a browser and sees live-updating cards —
no signup, no API key, no SDK required.

## Quick Reference

```
curl -s 'https://statb.io/b/{board_id}/push?key1=value1&key2=+1&key3=-0.5'
```

Board viewer: `https://statb.io/board.html?board={board_id}`

## Board ID Rules

- Use only **lowercase letters and hyphens** (`a-z`, `0-9`, `-`).
- Make it **long and unique** to avoid collisions (e.g. `acme-deploy-x7k9m`, `agent-training-4feb`).
- The board is created automatically on first push.

## Value Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `42` | **Set** to this value | `?cpu=72.5` |
| `+N` | **Increment** by N (starts at 0 if key missing) | `?steps=+1` |
| `-N` | **Decrement** by N | `?errors=-1` |

Only numeric values (int or float). Non-numeric values are silently skipped.
Multiple keys in one request are fine.

## Workflow

When the user asks you to run a multi-step or long-running task:

1. **Generate a board ID.** Combine a short project/task label with a random
   suffix: e.g. `migrate-db-k8r2q` or `scrape-run-20260414`. Tell the user:
   > You can monitor progress live at:
   > `https://statb.io/board.html?board={board_id}`

2. **Push an initial snapshot** before starting work:
   ```bash
   curl -s 'https://statb.io/b/{board_id}/push?status=1&total_steps=10&completed=0&errors=0'
   ```
   Use `status=1` for running, `status=0` for finished.

3. **Push updates during work.** After each meaningful step or batch:
   ```bash
   curl -s 'https://statb.io/b/{board_id}/push?completed=+1'
   ```
   Push changed values only — no need to resend unchanged keys.

4. **Push final state** when done:
   ```bash
   curl -s 'https://statb.io/b/{board_id}/push?status=0&completed=10&duration_sec=47'
   ```

## What to Push

Choose keys that let the user understand progress at a glance:

- **Progress counters:** `completed`, `total`, `remaining`, `percent`
- **Rates / speed:** `items_per_sec`, `tokens_per_sec`
- **Quality signals:** `errors`, `warnings`, `success_rate`
- **Resource usage:** `cpu`, `mem_mb`, `gpu_temp`
- **Timing:** `elapsed_sec`, `eta_sec`, `duration_sec`
- **Domain-specific:** `loss`, `accuracy`, `rows_processed`, `files_converted`

Keep key names short, lowercase, underscore-separated.

## ⚠ Common Pitfall — Push Must Be Continuous

**The #1 mistake is pushing once at the start and never again.** The board
then shows stale numbers for the entire run, which defeats the purpose.

Push calls must be placed **inside the actual work** — not just before it:

- **Loops:** Put the push call inside the `for` / `while` body, not above it.
- **Batch callbacks:** Push after each batch completes, not only before the
  first batch.
- **Long scripts:** If you generate a script or code for the user, embed a
  push call after each major stage, not just at the top.
- **Timer / interval:** For continuous processes with no natural loop
  boundary, register a recurring timer (e.g. every 15–30 seconds) that
  pushes the latest metrics.

**Self-check before executing:** Look at your plan. If there is only one
`curl …/push` call at the beginning, you are doing it wrong. There must be
at least one push inside the loop or between stages, plus a final push at
the end.

Bad:
```bash
curl -s 'https://statb.io/b/board/push?total=100&done=0'   # ← only push
for f in *.csv; do process "$f"; done                       # board stays at 0
```

Good:
```bash
curl -s 'https://statb.io/b/board/push?total=100&done=0'
for f in *.csv; do
  process "$f"
  curl -s 'https://statb.io/b/board/push?done=+1'          # ← push inside loop
done
curl -s 'https://statb.io/b/board/push?status=0'           # ← final push
```

## Rules

- **Always tell the user the board URL** at the start so they can open it.
- **Push at meaningful intervals**, not every line of code. Once per logical
  step, batch, or every 10–30 seconds for continuous work.
- **Use increment (`+N`) for counters** so concurrent pushes don't clobber.
- **Use set (plain number) for gauges** like percentages, temperatures, rates.
- **Do not push sensitive data.** Board IDs are unguessable but boards are
  not access-controlled. Never push passwords, tokens, PII, or secrets.
- **Silent push.** Use `curl -s` to suppress output. Push failures are
  non-fatal — do not let a failed push stop the actual work.
- **Free tier limits:** max 16 keys per board. Keep it focused.

## Examples

### Multi-file processing
```bash
# Start
curl -s 'https://statb.io/b/convert-imgs-a9x2/push?total=200&done=0&errors=0&status=1'

# After each file
curl -s 'https://statb.io/b/convert-imgs-a9x2/push?done=+1'

# On error
curl -s 'https://statb.io/b/convert-imgs-a9x2/push?errors=+1'

# Finish
curl -s 'https://statb.io/b/convert-imgs-a9x2/push?status=0'
```

### Code migration with metrics
```bash
curl -s 'https://statb.io/b/migrate-v3-kq82/push?files_total=48&files_done=+1&tests_pass=142&tests_fail=3'
```

### Training loop
```bash
curl -s "https://statb.io/b/train-bert-e4p1/push?epoch=+1&loss=${LOSS}&acc=${ACC}&lr=${LR}"
```
