# Example run

Use this only as a pattern, not a rigid template.

## Example user task

> Analyze my message export and reconstruct my work year.

## Recommended decomposition

- `1` root `synthesis` — final narrative and chronology
  - `1.1` `research` — index relevant work-related threads
  - `1.2` `research` — infer travel, TDYs, and place/date anchors
  - `1.3` `research` — infer workstreams, duties, and achievements
  - `1.4` `review` — challenge weak claims and identify ambiguity

## Suggested run layout

```text
runs/run-20260306-work-year/
  tree.json
  events.jsonl
  summary.md
  nodes/
    1/
      spec.json
      notes.md
      result.md
      merged-children.md
    1.1/
      spec.json
      notes.md
      result.md
    1.2/
      spec.json
      notes.md
      result.md
```

## Suggested commands

```bash
python3 skills/recursive-swarm/scripts/init_run.py \
  "Analyze my message export and reconstruct my work year" \
  --runs-dir ~/work-research/recursive-swarm-runs \
  --mode research \
  --max-depth 2 \
  --fanout 3 \
  --concurrency 3 \
  --max-nodes 9

python3 skills/recursive-swarm/scripts/upsert_node.py \
  --run ~/work-research/recursive-swarm-runs/<run-id> \
  --id 1.1 --parent-id 1 \
  --goal "Index relevant work-related threads" \
  --type research --executor subagent

python3 skills/recursive-swarm/scripts/list_ready_nodes.py \
  --run ~/work-research/recursive-swarm-runs/<run-id>

python3 skills/recursive-swarm/scripts/merge_results.py \
  --run ~/work-research/recursive-swarm-runs/<run-id> \
  --id 1

python3 skills/recursive-swarm/scripts/render_tree.py \
  --run ~/work-research/recursive-swarm-runs/<run-id>
```

## Practical guidance

- Prefer 2-4 children per node.
- Prefer depth 2; treat depth 3 as exceptional.
- Add a final `review` node for high-stakes runs.
- Use worktrees only for coding leaves inside a git repo.
- Read `events.jsonl` when you need a compact audit trail of state changes.
- For quiet orchestration, instruct routine children to reply `ANNOUNCE_SKIP` during the announce step and let the parent deliver the final merged answer.
- Do not clean up quiet child sessions until the parent has harvested the needed results.
