# super_memori v4 — Weak Model Guidance

## Why this file exists
The target operator is a weaker model. The interface must be safe under literal, uneven execution.

## Rules
1. Expose only four public commands.
2. Hide backend choice behind `query-memory.sh`.
3. Prefer `--mode auto` by default and trust `mode_used` for what actually executed.
4. Use explicit exit codes and explicit warnings.
5. Do not require the model to interpret index freshness from raw logs.
6. Do not use absolute wording like "never grep manually" unless it is truly always correct.
7. Degraded mode is valid operation, but must be surfaced clearly.
8. `semantic` and `hybrid` are real runtime modes now; weak models should still default to `auto` unless the task explicitly requires forcing them.
9. Do not invent freeform relation targets in `memorize.sh`; relation links must use canonical forms such as `learn:<signature>`, `chunk:<chunk_id>`, or `path:<canonical_path>`.

## Good pattern
"Run `query-memory.sh --json <query>` and use the returned warnings/results."

## Bad pattern
"Decide whether to use grep, vectors, or direct file scans based on intuition."
