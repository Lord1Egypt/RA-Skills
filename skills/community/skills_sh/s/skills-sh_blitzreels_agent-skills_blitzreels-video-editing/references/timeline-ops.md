# Timeline Operations Reference

## Core Edit Operations

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/timeline/trim` | Trim item by start/end deltas (seconds) |
| POST | `/projects/{id}/timeline/split` | Split item at timestamp (non-destructive) |
| POST | `/projects/{id}/timeline/media` | Insert media-library image/video items with `items[]` |
| DELETE | `/projects/{id}/timeline/items/{itemId}` | Delete timeline item |
| POST | `/projects/{id}/timeline/move` | Move one item |
| POST | `/projects/{id}/timeline/transform` | Update one item position/dimensions |
| POST | `/projects/{id}/timeline/edits` | Generic trim/split/delete/move/transform action |
| POST | `/projects/{id}/timeline/batch-trim` | Batch trim items |
| POST | `/projects/{id}/timeline/batch-move` | Batch move items |
| POST | `/projects/{id}/timeline/batch-transform` | Batch transform items |
| POST | `/projects/{id}/timeline/batch-delete` | Batch delete items |

### Trim Input
```json
{
  "timeline_item_id": "string",
  "trim_start_delta_seconds": 0.5,
  "trim_end_delta_seconds": -1.2
}
```
Positive `trim_start_delta_seconds` trims from beginning; negative `trim_end_delta_seconds` trims from end.

### Split Input
```json
{
  "timeline_item_id": "string",
  "split_at_seconds": 15.5
}
```
Creates two items from one at the split point.

---

## Transform & Position

| Method | Path | Description |
|--------|------|-------------|
| POST | `/projects/{id}/timeline/move` | Set start time and optional layer index |
| POST | `/projects/{id}/timeline/transform` | Set position and width/height |
| POST | `/projects/{id}/timeline/batch-move` | Batch update start/layer |
| POST | `/projects/{id}/timeline/batch-transform` | Batch update position/dimensions |

Some dashboard/internal endpoints are not public. If a route is not in OpenAPI, do not call it. Prefer `/timeline/edits`, `/timeline/move`, `/timeline/transform`, or the batch endpoints above for public timeline changes.

### Timeline Media Input

Use `POST /projects/{id}/timeline/media` for visual media library insertions, not audio tracks:

```json
{
  "items": [
    {
      "asset_id": "uuid",
      "start_seconds": 12.5,
      "duration_seconds": 3,
      "position_preset": "full-screen",
      "animation_preset": "fadeIn"
    }
  ],
  "allow_duplicate": true
}
```

Known constraints:
- Use `asset_id`, not `media_id`.
- The endpoint is backed by the B-roll/media insertion tool and supports image/video assets from the media library.
- Audio insertion is public at `POST /projects/{id}/timeline/audio`, but it expects an existing workspace audio asset. Do not guess `/audio` or `/music`.

---

## Clip Management

Use `/clips` for the high-level clipping flow, or `/workspace/media/assets/{assetId}/short-suggestions/{suggestionId}/apply` for applying a selected suggestion. The old timeline clip-management routes (`/timeline/clips`, `/timeline/clips-with-captions`, `/timeline/replace-media`) are not public.

---

## Packing & Ordering

No public pack/auto-order endpoint is registered today. Use explicit `move`/`batch-move` operations when you need to remove gaps or reorder items.

---

## AI-Powered Features

No public timeline silence-detection, mistake-detection, apply-silence-plan, apply-mistake-plan, or caption-recut endpoints are registered today. Use the editor UI or higher-level clipping flow when those workflows are required.

### Silence Detection Flow
1. Use the dashboard/editor UI or clipping flow for silence cleanup.
2. If you need an API-only workaround, read transcript/context and use explicit trim/split/delete/move operations.

### Mistake Detection Flow
1. Use transcript/context reads to identify candidate mistake regions manually.
2. Apply edits with explicit trim/split/delete/move operations.

---

## Effects

Timeline effect CRUD is not public in the live OpenAPI. Use public overlay/background/motion endpoints where possible, or the dashboard for zoom/mask/color-grade effect editing.

---

## Keyframes

Animate properties over time with keyframes.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{id}/keyframes?timeline_item_id={itemId}` | List keyframes |

Only keyframe listing is public in the live OpenAPI. Creation/update/delete are dashboard/internal until OpenAPI lists them.

### Keyframe Properties
`positionX` · `positionY` · `scale` · `rotation` · `opacity`

### Keyframe Easing
`linear` · `ease-in` · `ease-out` · `ease-in-out` · `bounce` · `elastic`

### Keyframe Input
```json
{
  "property": "scale",
  "time_seconds": 2.5,
  "value": 1.5,
  "easing": "ease-out"
}
```

---

## Undo / Redo

Undo/redo routes are not public in the live OpenAPI. Verify state with read endpoints after each write.

---

## Watermarks

Watermark CRUD routes are not public in the live OpenAPI. Use the dashboard or project templates/overlays if a public workflow exists for the specific case.

---

## Layer Index Defaults

| Layer | Index | Content |
|-------|-------|---------|
| Caption | 0 | Caption subtitles |
| Effect | 1 | Zoom, mask, color grade |
| Image | 2 | Image overlays |
| Video | 3 | Video clips |
| Audio | 4 | Audio tracks |
| Background | 5 | Fill layers |
