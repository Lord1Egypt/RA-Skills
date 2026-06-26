# Cross-Workspace Collect

Gather images from multiple workspaces into one place.

**Trigger keywords:** "collect from all workspaces", "consolidate", "gather images matching X"

## Steps

1. **List workspaces** — `list_workspaces` → Show user the full scan scope (workspace names and count). **Confirm before proceeding** with the scan.
2. **Scan each** — For each workspace:
   - `get_canvas(canvas_id=...)` → get all elements
   - For image elements matching criteria: `get_asset_detail(artifact_version_id=...)` → check model, prompt keywords
   - Collect matching `asset_id`s with metadata
3. **Report** — Show matches per workspace, ask where to collect
4. **Collect to asset folder** (preferred, zero-copy):
   - `list_asset_folders` → check existing
   - `create_asset_folder(name=...)` if needed
   - `add_image_to_asset_folder(asset_id=..., folder_id=...)` for each match
5. **Or collect to canvas** (alternative):
   - `upload_image(image_url=..., canvas_id=..., position_x=x, position_y=y)` in grid

## Output

Report: N images found across M workspaces, N collected, N skipped (with reasons for skipping).
