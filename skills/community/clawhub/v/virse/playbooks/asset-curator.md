# Asset Curator

Organize canvas images into persistent asset folder collections.

**Trigger keywords:** "save to folders", "organize into collections", "sort by model/style", "curate"

## Steps

1. **Get canvas** — `get_canvas(canvas_id=..., include_group_detail=true)`
2. **Inspect images** — For each image element:
   - `get_element(id=...)` → get `asset_id`, `artifact_version_id`
   - `get_asset_detail(artifact_version_id=...)` → get model, prompt, params
3. **Categorize** — Propose categories based on:
   - Model used (e.g. "Flux Generations", "GPT-Image Outputs")
   - Prompt themes (e.g. "Landscapes", "Portraits")
   - Existing canvas groups
   - User-specified criteria
4. **Confirm with user** — Present proposed categorization
5. **Create folders** — `list_asset_folders` → reuse existing, `create_asset_folder` for new ones
6. **Link images** — `add_image_to_asset_folder(asset_id=..., folder_id=...)` — zero-copy linking

## Output

Summary: N images categorized into M folders (new and existing).
