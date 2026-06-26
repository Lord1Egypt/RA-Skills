---
name: distill
description: "Use when agent instruction files (AGENTS.md, rules/) need analysis, trimming, or restructuring. Orchestrates /imperatives → /policy-algebra → /visualize into a distillation pipeline."
---

# /distill

Distill agent instruction files into structured imperatives, compose with policy algebra, and visualize the rule system. Three-stage pipeline.

## Usage

```
/distill                                    # full pipeline on default files
/distill ai-workspace/rules/*.md            # specific targets
/distill --stage imperatives                # run only extraction
/distill --stage compose                    # run only policy algebra (requires prior extraction)
/distill --stage visualize                  # run only visualization (requires prior composition)
```

## Pipeline

```
  ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
  │ /imperatives │────▶│/policy-algebra│────▶│ /visualize  │
  │  extract     │     │  compose     │     │  render     │
  └─────────────┘     └──────────────┘     └─────────────┘
        │                    │                    │
    JSONL file         Starlark block      Mermaid diagrams
```

### Stage 1 — Extract (`/imperatives`)

1. Invoke `/imperatives` with the target files (or defaults: `ai-workspace/rules/*.md` + `AGENTS.md`).
2. Save output to `ai-workspace/research/<name>-imperatives.jsonl`.
3. Present the summary (count, level breakdown, scope breakdown).

Ask the user: **"Review the extraction before composing? (y/continue)"**
- If yes: present the JSONL for review, wait for feedback, re-extract if needed.
- If continue: proceed to Stage 2.

### Stage 2 — Compose (`/policy-algebra`)

1. Project the JSONL to natural-language bullets: `<level>[ NOT] <subject> <predicate>[ when <when>]` — one bullet per imperative.
2. Invoke `/policy-algebra` with the projected bullets.
3. Save the Starlark composition to `ai-workspace/research/<name>-policy.md`.
4. Present the surfaced structure (decision functions, branching points).

### Stage 3 — Visualize (`/visualize`)

1. For each major decision function in the Starlark output, invoke `/visualize`.
2. Content shape is typically graph (decision trees) → Mermaid flowcharts.
3. Append diagrams to the policy doc.

## Naming

The `<name>` slug defaults to the current date + "distill" (e.g., `2026-05-04-distill`). Override with `--name <slug>`.

## Output

All artifacts land in `ai-workspace/research/`:
- `<name>-imperatives.jsonl` — structured extraction
- `<name>-policy.md` — Starlark composition + diagrams

## Failure modes

| Condition | Behavior |
|---|---|
| /imperatives finds zero imperatives | Report and stop. No point composing empty input. |
| /policy-algebra unavailable | Skip Stage 2, warn. Stage 3 can still visualize the JSONL directly. |
| User interrupts between stages | Artifacts from completed stages are preserved. Resume with `--stage`. |

## When to use

- AGENTS.md or rules/ grew past a size threshold and needs trimming
- Before a major restructuring of agent instruction files
- To audit what rules actually exist vs what you think exists
- As input to a plan that modifies the rule system
