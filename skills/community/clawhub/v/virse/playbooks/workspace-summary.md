# Workspace Summary

Get a full overview of workspace contents.

**Trigger keywords:** "what's in this workspace", "workspace overview", "summarize canvas"

## Steps

1. **List workspaces** — `list_workspaces` → user selects one, save `canvas_id`
2. **Get canvas** — `get_canvas(canvas_id=..., include_group_detail=true)`
3. **Analyze** — Count elements by type (image/text), edges, groups
4. **Drill down** (optional) — `get_element` for specific items, `trace_connections(direction="both", depth=2)` for workflow chains
5. **Report** — Element stats, group details, workflow chains

## Output

```
Workspace: <name>
Images: X | Text: Y | Groups: Z | Edges: M
Group details: ...
Workflow chains: ...
```
