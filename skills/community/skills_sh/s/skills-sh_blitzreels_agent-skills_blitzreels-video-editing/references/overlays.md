# Overlays Reference

BlitzReels' supported public text layer is the same editable layer shown in the dashboard under **Combined Text > Text**.

Use the content item API. Do not guess alternate overlay or generated graphics routes for video-editing tasks.

## Editable Text Overlays

Create a canonical overlay:

```bash
bash scripts/blitzreels.sh POST /projects/PROJECT_ID/content-items '{
  "kind": "overlay",
  "text": "5 Tips for Better Code",
  "start_seconds": 0,
  "duration_seconds": 3,
  "layer_index": 1
}'
```

List overlays and related editable content:

```bash
bash scripts/blitzreels.sh GET /projects/PROJECT_ID/content-items
```

Update or delete:

```bash
bash scripts/blitzreels.sh PATCH /projects/PROJECT_ID/content-items/CONTENT_ITEM_ID '{
  "name": "Opening hook"
}'

bash scripts/blitzreels.sh DELETE /projects/PROJECT_ID/content-items/CONTENT_ITEM_ID
```

Expected list/create response fields:

| Field | Meaning |
|-------|---------|
| `kind` | `overlay`, `title_card`, or `watermark` |
| `content_item_id` | Stable ID for patch/delete |
| `timeline_item_id` | Timeline row used for move/trim/transform |
| `playground_composition_id` | Internal renderer ID for canonical overlay specs |
| `spec` | Canonical single-root overlay spec used by the editor |

For placement, use the returned `timeline_item_id` with timeline operations such as `/timeline/move`, `/timeline/transform`, or `/timeline/batch-transform`.

## Motion Code

Motion code is a separate code-block primitive, not the general overlay layer. Use it only when the user specifically asks for animated code.

```bash
bash scripts/blitzreels.sh POST /projects/PROJECT_ID/motion-code '{
  "code": "const greet = (name: string) => `Hello, ${name}`;",
  "language": "typescript",
  "filename": "greeting.ts",
  "code_theme": "github-dark",
  "position_preset": "center",
  "show_window_chrome": true,
  "show_line_numbers": true,
  "start_seconds": 5,
  "duration_seconds": 8,
  "transition_type": "typewriter"
}'
```

### Motion Code Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{id}/motion-code` | List motion code items |
| POST | `/projects/{id}/motion-code` | Add motion code |

## Unsupported Surfaces

For normal editable text, use `/projects/{id}/content-items` with `kind: "overlay"` only. If OpenAPI does not list a route, do not infer or call it.
