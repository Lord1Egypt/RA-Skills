---
name: runware-models
description: >
  Pick the right Runware model for a task and keep that choice current. Use when
  an agent needs to decide "which model for X", discover what's available, or
  check a model's capabilities, status, or price. Foundation skill - outcome
  skills delegate model choice here so nothing rots when the catalog changes.
---

# Choosing a Runware model

Runware's catalog is large and changes weekly. The rule: **never hardcode a single model as the only answer.** Start from a sensible default for the capability, then confirm it's live and current with a real lookup before running.

## How to discover

- **List / search the catalog** (SDK, MCP `list_models` / `model_search`, or CLI) filtered by capability and modality. Each model card carries `name`, `air`, `status`, `capabilities`, pricing, and a headline.
- **Capabilities are tagged** as `io:<from>-to-<to>` and `op:<operation>`:
  - `io:text-to-image`, `io:image-to-image`, `io:text-to-video`, `io:image-to-video`, `io:video-to-video`, `io:text-to-audio`, `io:audio-to-video` (lipsync), `io:image-to-3d`, `io:text-to-3d`, `io:text-to-text`, `io:image-to-text` (vision).
  - `op:edit`, `op:remove-background`, `op:upscale`, `op:extend`, `op:vectorize`, `op:caption`, `op:mask`, `op:train`, and the ControlNet preprocessors (`op:depth-estimation`, `op:pose-estimation`, …).
- Match the customer's outcome to a capability, then to a model.

## Status matters

`status` tells you whether a model is usable: prefer `live`. Treat `deprecated` as replaced (check `replacedBy`), `coming-soon` / `draft` as not yet callable, `unlisted` as reachable only if you already have its ID.

## Routing principles

- **Default to a flagship for quality, offer a fast/cheap tier for drafts.** Most families have both (e.g. a `[max]`/`pro` tier and a fast `klein`/`flash`/`turbo` tier).
- **Route by sub-task, not by brand.** A single outcome often spans models: e.g. text-heavy images favor a model strong at typography; a premium still vs a fast draft are different picks.
- **Cost-aware.** Check the card's pricing (or dry-run via `runware-run`) before a batch.
- **Hosted models** carry a "Runware Optimized" marker - good defaults for reliability/price.

## Quality bar

- The chosen model is `live` and actually supports the required capability (verified against its card, not assumed).
- A cheaper/faster alternative was considered for drafts or high-volume runs.

## Related skills

`runware-run` (call the model you picked), `runware-prompting` (prompt it well), and every outcome skill (each names its default routing, then defers here to confirm).
