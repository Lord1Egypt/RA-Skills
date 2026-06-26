---
description: "Analyse shark timing history and recommend optimal timeout/loop settings"
---

# Shark Autotune

Analyse recorded shark timing data and recommend optimal settings.

## Instructions

1. Read `$SKILL_DIR/state/timings.jsonl` — each line is a JSON object:
   ```json
   {"ts": 1710000000, "loop": 1, "elapsed_s": 12.3, "timeout_s": 25, "result": "ok|timeout|done", "task_hash": "abc123"}
   ```

2. If the file doesn't exist or is empty, report "No timing data yet. Run tasks with /shark first to collect data."

3. Compute and report:
   - **Total runs** and **total loops** recorded
   - **Median turn time** (p50) and **p95 turn time**
   - **Timeout rate** — % of turns that hit the timeout
   - **Loops to completion** — median and max loops needed
   - **Wasted time** — sum of (timeout - elapsed) for turns that finished early (idle headroom)
   - **Optimal timeout** — p95 turn time + 3s buffer (rounded up to nearest 5s)
   - **Optimal max_loops** — p95 loops-to-completion + 2

4. Show recommendations:
   ```
   Current:     SHARK_LOOP_TIMEOUT=25  SHARK_MAX_LOOPS=50
   Recommended: SHARK_LOOP_TIMEOUT=N   SHARK_MAX_LOOPS=M

   Rationale:
   - p95 turn time is Xs, so timeout of Ns covers 95% of turns with buffer
   - p95 completion is N loops, so max_loops of M gives safe margin
   - Timeout rate is X% — [too high: lower timeout or split tasks | healthy: <15%]
   - Wasted headroom: Xs total — [high: timeout too generous | low: well-tuned]
   ```

5. If timeout rate > 30%, also suggest: "Consider breaking tasks into smaller steps — high timeout rate means turns are consistently too ambitious."

6. If median turn time < 5s, suggest: "Most turns complete very fast. Consider lowering timeout to reclaim resources faster on stuck turns."
