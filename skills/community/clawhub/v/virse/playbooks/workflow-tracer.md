# Workflow Tracer

Trace the creation history and lineage of an element.

**Trigger keywords:** "show history", "trace workflow", "how was this created", "lineage"

## Steps

1. **Get workspace** — `list_workspaces` → save `canvas_id`
2. **Get target** — `get_element(canvas_id=..., id=...)` → note `artifact_version_id`
3. **Walk upstream** — `trace_connections(canvas_id=..., id=..., direction="upstream", depth=5)`
4. **Inspect each node** — For each node with `artifact_version_id`:
   - `get_asset_detail(artifact_version_id=...)` → get prompt, model, timestamp
   For text nodes with `asset_id`:
   - `get_asset_detail(asset_id=...)` → get text content
5. **Build lineage** — Assemble chain from earliest ancestor to target:
   ```
   [1] <short_id> (image) — Model: flux-1.1-pro, Prompt: "..."
       ↓
   [2] <short_id> (image) — Model: gpt-image-1, Prompt: "..."
       ↓
   [3] <short_id> (image) ← TARGET
   ```

## Output

Structured lineage document: each step with model, prompt, and parameters. Total depth and models used.
