---
name: shark-autotune
description: "Analyse shark timing history and recommend optimal SHARK_LOOP_TIMEOUT and SHARK_MAX_LOOPS settings"
---

# Shark Autotune

Analyse recorded shark timing data and recommend optimal settings.

## Instructions

1. Read `$SKILL_DIR/../state/timings.jsonl` — each line is a JSON object:
   ```json
   {"ts":1710000000,"loop":1,"elapsed_s":12.3,"timeout_s":25,"result":"ok|timeout|done","task_hash":"abc123"}
   ```

2. If the file doesn't exist or is empty, report "No timing data yet. Run tasks with /shark first to collect data."

3. Compute and report:
   - **Total runs** (unique task_hash values) and **total loops**
   - **Median turn time** (p50) and **p95 turn time**
   - **Timeout rate** — % of turns with result "timeout"
   - **Loops to completion** — median and max (count loops per task_hash that has a "done" entry)
   - **Wasted headroom** — sum of (timeout_s - elapsed_s) for result "ok" turns
   - **Optimal timeout** — p95 turn time + 3s buffer, rounded up to nearest 5s
   - **Optimal max_loops** — p95 loops-to-completion + 2

4. Show recommendations:
   ```
   Current:     SHARK_LOOP_TIMEOUT=25  SHARK_MAX_LOOPS=50
   Recommended: SHARK_LOOP_TIMEOUT=N   SHARK_MAX_LOOPS=M

   Rationale:
   - p95 turn time is Xs, so timeout of Ns covers 95% with buffer
   - p95 completion is N loops, so max_loops of M gives safe margin
   - Timeout rate is X% — [>15%: consider splitting tasks | healthy]
   - Wasted headroom: Xs total
   ```

5. If timeout rate > 30%: "Consider breaking tasks into smaller steps."
6. If median turn time < 5s: "Most turns complete fast. Consider lowering timeout."
