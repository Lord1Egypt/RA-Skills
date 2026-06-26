# Virse Tools Reference

> **`virse_call`** refers to `virse_skill/scripts/virse_call.py`. See SKILL.md for how your agent resolves this path.

All tools are called via:
```bash
virse_call call <tool_name> '<json_args>'
```

---

## Account

### get_account
Get current user info (username, email) and CU balance per organization (with org name and type). For team orgs, also shows your member budget (credit_used / credit_limit).

**Parameters:** none

```bash
virse_call call get_account '{}'
```

---

## Workspace

### list_workspaces
List all workspaces (Spaces) the user has access to. Returns `space_id`, `canvas_id`, and organization context (org name, type) for each.

**Parameters:** none

```bash
virse_call call list_workspaces '{}'
```

### create_workspace
Create a new workspace and its associated Canvas.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Workspace name |
| description | string | no | Workspace description |
| visibility | string | no | `private` (default) or `public` |
| organization_id | string | no | Organization to create under (defaults to personal org) |

```bash
virse_call call create_workspace '{"name": "My Project"}'
```

### update_workspace
Update workspace name, description, or visibility.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| space_id | string | yes | Space UUID to update |
| name | string | no | New name |
| description | string | no | New description |
| visibility | string | no | `private` or `public` |

```bash
virse_call call update_workspace '{"space_id": "UUID", "name": "New Name"}'
```

---

## Canvas

### get_canvas
Get a lightweight overview of a Canvas — element summaries with outgoing connections, plus group summaries.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID (from `list_workspaces`) |
| group_id | string | no | Filter by Group short ID / UUID |
| element_type | string | no | Filter by type: `image` or `text` |
| include_group_detail | boolean | no | If true, append detailed group info (default false) |

```bash
virse_call call get_canvas '{"canvas_id": "UUID"}'
```

### get_element
Get one element's full details by short ID / UUID, plus one-hop incoming/outgoing neighbors.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| id | string | yes | Element short ID or full UUID |

```bash
virse_call call get_element '{"canvas_id": "UUID", "id": "abc1"}'
```

### trace_connections
Traverse workflow connections from one element.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| id | string | yes | Origin element short ID or UUID |
| direction | string | no | `upstream`, `downstream`, or `both` |
| depth | integer | no | Traversal depth (default 1, max 5) |

```bash
virse_call call trace_connections '{"canvas_id": "UUID", "id": "abc1", "direction": "both", "depth": 3}'
```

### create_element
Create a new element (image or text node) in the current Canvas.

**Text fontSize tip**: Text wraps automatically within the element width. Default fontSize is 50. E.g. fontSize 50, 300×80 box → 6 lowercase, 5 uppercase, or 4 Chinese chars in 1 line.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| element_type | string | yes | `image` or `text` |
| position_x | number | yes | X coordinate |
| position_y | number | yes | Y coordinate |
| size_width | number | no | Width in px (default 200) |
| size_height | number | no | Height in px (default 200) |
| artifact_version_id | string | no | Image artifact version ID |
| asset_id | string | no | Image asset ID |
| text / content | string | no | Text content (for text elements) |
| fontSize | number | no | Font size (default 50) |
| textAlign | string | no | `left`, `center` (default), `right` |
| verticalAlign | string | no | `top`, `middle` (default), `bottom` |
| z_index | integer | no | Layer order (higher = front) |
| title | string | no | Element title |

```bash
virse_call call create_element '{"canvas_id": "UUID", "element_type": "text", "position_x": 100, "position_y": 50, "text": "Hello", "fontSize": 32}'
```

### update_element
Update an element (move, resize, or modify content).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| element_id | string | yes | Element short ID or UUID |
| position_x | number | no | New X |
| position_y | number | no | New Y |
| size_width | number | no | New width |
| size_height | number | no | New height |
| rotation | number | no | Rotation in degrees |
| text / content | string | no | New text content |
| fontSize | number | no | Font size |
| textAlign | string | no | `left`, `center`, `right` |
| verticalAlign | string | no | `top`, `middle`, `bottom` |
| z_index | integer | no | Layer order |
| title | string | no | New title |
| artifact_version_id | string | no | New image artifact |
| asset_id | string | no | New image asset |

```bash
virse_call call update_element '{"canvas_id": "UUID", "element_id": "abc1", "position_x": 200, "position_y": 300}'
```

### delete_element
Delete an element from the Canvas. **Destructive — confirm with user first.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| element_id | string | yes | Element short ID or UUID |

```bash
virse_call call delete_element '{"canvas_id": "UUID", "element_id": "abc1"}'
```

### create_edge
Create a directed edge between two elements.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| source_element_id | string | yes | Source element short ID or UUID |
| target_element_id | string | yes | Target element short ID or UUID |

```bash
virse_call call create_edge '{"canvas_id": "UUID", "source_element_id": "abc1", "target_element_id": "def2"}'
```

### delete_edge
Delete an edge. **Destructive — confirm with user first.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| edge_id | string | yes | Edge UUID |

```bash
virse_call call delete_edge '{"canvas_id": "UUID", "edge_id": "EDGE_UUID"}'
```

---

## Groups

### create_group
Create a group by bundling elements. Bounding box is computed automatically.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| element_ids | string[] | yes | Element short IDs / UUIDs to include |
| title | string | no | Group title |

```bash
virse_call call create_group '{"canvas_id": "UUID", "element_ids": ["abc1", "def2"], "title": "My Group"}'
```

### delete_group
Delete a group. Member elements are NOT deleted. **Destructive — confirm with user first.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| canvas_id | string | yes | Canvas UUID |
| group_id | string | yes | Group short ID or UUID |

```bash
virse_call call delete_group '{"canvas_id": "UUID", "group_id": "GRP1"}'
```

---

## Image Generation & Upload

### generate_image
Generate an AI image and place it on a Canvas. A placeholder element appears immediately while the image generates in the background, then fills in when complete. Returns `artifact_version_id` and `element_id`(s). Use `list_image_models` to see all available models and their supported parameters.

**Auto-edge**: When using `asset_id` (image-to-image), an edge is automatically created from each source element to the new element. No need to call `create_edge` separately.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | yes | Image generation prompt |
| model | string | yes | Model ID (use `list_image_models`) |
| space_id | string | yes | Space ID |
| canvas_id | string | yes | Canvas UUID |
| position_x | number | yes | X coordinate |
| position_y | number | yes | Y coordinate |
| width | integer | no | Image width in px |
| height | integer | no | Image height in px |
| aspect_ratio | string | no | Aspect ratio string — supported values vary by model family (see table below). |
| resolution | string | no | `0.5K`, `1K`, `2K`, `3K`, `4K`. Tier availability varies by model — Nano2 supports all tiers; Seedream 4.5 supports up to 4K; Imagen 4 Ultra supports up to 2K. |
| num_images | integer | no | Number of images (default 1) |
| asset_id | string \| string[] | no | Reference image(s) for image-to-image generation. Pass a single asset_id string or an array of asset_id strings for multi-image references (max 10). Auto-edges are created from all referenced source elements. |
| size_width | number | no | Placeholder width (default 512) |
| size_height | number | no | Placeholder height (default 512) |

**Supported `aspect_ratio` values by model:**

| Model | Supported aspect_ratio | Notes |
|-------|----------------------|-------|
| Nano Banana 2 (`nano-banana-2`) | `1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `9:16`, `16:9`, `21:9` | Passed directly to FAL.ai API |
| Gemini 2.5 Flash Image (`gemini-2.5-flash-image`) | `1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `9:16`, `16:9`, `21:9` | Via Vertex AI / APIMART / ONEROUTER |
| Gemini 3 Pro Image (`gemini-3-pro-image-preview`) | `1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `9:16`, `16:9`, `21:9` | Via Vertex AI / APIMART / ONEROUTER |
| Seedream 4.5 (`seedream-4.5`) | `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`, `9:21` | Converted to width/height via resolution base size |
| Seedream V5 Lite (`seedream-v5-lite`) | `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`, `9:21` | Converted to width/height via resolution base size |
| Imagen 4 (`imagen-4.0-*`) | `1:1`, `9:16`, `16:9`, `3:4`, `4:3` | Via Google Vertex AI GenerateImagesConfig |
| FLUX 1.1 Pro (`flux-1.1-pro`) | `1:1`, `16:9`, `3:2`, `2:3`, `4:5`, `5:4`, `9:16`, `3:4`, `4:3` | Via BFL API |
| FLUX 1.1 Pro Ultra (`flux-1.1-pro-ultra`) | `1:1`, `16:9`, `3:2`, `2:3`, `4:5`, `5:4`, `9:16`, `3:4`, `4:3` | Via BFL API |
| FLUX Kontext (`flux-kontext-pro`, `flux-kontext-max`) | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `4:5`, `5:4`, `21:9`, `9:21`, `2:1`, `1:2` | Via BFL API |
| Seedream 4 (`seedream-4`) | `1:1`, `2:1`, `3:2`, `4:3`, `5:4`, `16:9`, `21:9`, `1:2`, `2:3`, `3:4`, `4:5`, `9:16`, `9:21` | Converted to width/height via resolution base size |
| Gemini 2.5 Flash Image Preview (`gemini-2.5-flash-image-preview`) | Not supported | No aspect_ratio parameter |
| GPT Image 1 (`gpt-image-1`) | `1:1`, `3:2`, `2:3` | Uses `size` param (1024x1024, 1536x1024, 1024x1536) |
| GPT Image 1.5 (`gpt-image-1.5`) | `1:1`, `3:2`, `2:3` | Uses `size` param (1024x1024, 1536x1024, 1024x1536) |

```bash
virse_call call generate_image '{"prompt": "cyberpunk city", "model": "flux-1.1-pro", "space_id": "SPACE", "canvas_id": "UUID", "position_x": 0, "position_y": 0}'

# Multiple reference images
virse_call call generate_image '{"prompt": "edit prompt here", "model": "nano-banana-2", "space_id": "SPACE", "canvas_id": "UUID", "position_x": 0, "position_y": 0, "asset_id": ["ASSET_1", "ASSET_2"]}'
```

### upload_image
Upload an image from URL to a workspace or asset folder. Returns created image asset info. Supports three modes: (1) canvas placement — provide `canvas_id` + position to place the image on a canvas; (2) asset folder — provide `folder_id` to store in an asset folder; (3) local file upload — use `get_upload_token` and POST to the HTTP multipart endpoint `/api/upload_image` for local files.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| image_url | string | yes | Public image URL |
| space_id | string | no | Target workspace ID (if not using folder_id) |
| folder_id | string | no | Target asset folder UUID |
| filename | string | no | Filename (default: upload.png) |
| canvas_id | string | no | Canvas UUID (for placement) |
| position_x | number | no | X coordinate for placement |
| position_y | number | no | Y coordinate for placement |
| size_width | number | no | Element width (default 512) |
| size_height | number | no | Element height (default 512) |

```bash
virse_call call upload_image '{"image_url": "https://example.com/img.png", "space_id": "SPACE"}'
```

### list_image_models
List all supported AI image generation models with providers, operations, aspect ratios, and max resolution.

**Parameters:** none

```bash
virse_call call list_image_models '{}'
```

### get_upload_token
Generate a reusable upload token for the HTTP multipart endpoint `POST /api/upload_image`. The token is bound to your IP, expires after 1 hour, and can be reused for multiple uploads. Call this tool again to refresh.

**Parameters:** none

```bash
virse_call call get_upload_token '{}'
```

**Usage** (canvas placement):
```bash
curl -X POST <upload_url> \
  -H 'Authorization: Bearer <upload_token>' \
  -F file=@image.png \
  -F space_id=<space_id> \
  -F canvas_id=<canvas_id> \
  -F position_x=0 -F position_y=0
```

**Usage** (asset folder upload — omit canvas_id):
```bash
curl -X POST <upload_url> \
  -H 'Authorization: Bearer <upload_token>' \
  -F file=@image.png \
  -F space_id=<folder_id>
```

Only one file per request. For multiple images, call curl once per file. The full URL is returned by the tool call result.

---

## Search & Assets

### search_images
Search the Virse image library by query and return a list of images with metadata. Supports pagination via `page_token` returned in previous results.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | Search query |
| limit | integer | no | Results to return (default 10, max 50) |
| page_token | string | no | Token for next page |

```bash
virse_call call search_images '{"query": "sunset landscape", "limit": 10}'
```

### get_asset_detail
Get details of an artifact version or a text asset. Pass `artifact_version_id` to get generation details (prompt, model, parameters, status, output image URLs). Pass `asset_id` to get the full text content of a text asset. At least one of `artifact_version_id` or `asset_id` must be provided.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| artifact_version_id | string | no | From `get_element` output |
| asset_id | string | no | Text asset ID from `get_element` output |

```bash
virse_call call get_asset_detail '{"artifact_version_id": "AV_UUID"}'
```

---

## Asset Folders

### create_asset_folder
Create a new asset folder for organizing images.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Folder name |
| description | string | no | Description |
| visibility | string | no | `private` (default) or `public` |

```bash
virse_call call create_asset_folder '{"name": "Logos"}'
```

### list_asset_folders
List all asset folders the current user has access to. Returns `folder_id`, `name`, `visibility`, and `asset_count`.

**Parameters:** none

```bash
virse_call call list_asset_folders '{}'
```

### list_asset_folder_images
List images in an asset folder with pagination.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| folder_id | string | yes | Asset folder UUID |
| limit | integer | no | Max images (default 50) |
| offset | integer | no | Pagination offset (default 0) |

```bash
virse_call call list_asset_folder_images '{"folder_id": "FOLDER_UUID"}'
```

### add_image_to_asset_folder
Add an existing image asset to an asset folder (zero-copy link). Idempotent.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| asset_id | string | yes | Image asset UUID |
| folder_id | string | yes | Asset folder UUID |

```bash
virse_call call add_image_to_asset_folder '{"asset_id": "ASSET_UUID", "folder_id": "FOLDER_UUID"}'
```

### remove_image_from_asset_folder
Remove an image from an asset folder (unlinks, does NOT delete the image). **Destructive — confirm first.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| asset_id | string | yes | Image asset UUID |
| folder_id | string | yes | Asset folder UUID |

```bash
virse_call call remove_image_from_asset_folder '{"asset_id": "ASSET_UUID", "folder_id": "FOLDER_UUID"}'
```
