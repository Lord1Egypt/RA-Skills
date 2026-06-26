---
name: query-draft
description: "Query a VectCut draft's script content without rendering. Use this skill when the user wants to preview/check a draft's timeline, materials, text, audio, or other content details before rendering. Trigger on requests like \"check this draft\", \"preview draft content\", \"show draft script\", \"verify draft\", or similar inspection requests."
---

# Query Draft Skill

Query a draft's script content (timeline, materials, tracks, text, audio, etc.) without performing full rendering.

API documentation:
- Query script: https://docs.vectcut.com/386764616e0

## When to use

- User wants to preview/inspect a draft before rendering
- User wants to verify draft content, materials, or timeline
- User mentions checking draft details, previewing content, or validating script
- User wants to examine text, audio, or material references without rendering

## Workflow

### Prerequisites

- Python 3 with `requests` library installed
- Check `VECTCUT_API_KEY` before execution; if missing, call `vectcut-login` first and continue only after login succeeds

### Execution

Run the query script with the draft ID:

```bash
python <skill-path>/scripts/query_draft.py "<draft_id>"
```

Optional argument to force refresh:

```bash
python <skill-path>/scripts/query_draft.py "<draft_id>" [--force-update]
```

### What the script does

1. **Request** — `POST /cut_jianying/query_script` with `draft_id` and optional `force_update` flag.

2. **Parse** — The response contains a serialized JSON string in the `output` field. The script automatically parses and returns it.

3. **Display** — Outputs structured information about:
   - **Timeline**: duration, fps, canvas config
   - **Tracks**: video/audio tracks and their segments
   - **Materials**: videos, audios, texts, images, etc.
   - **Text styling**: fonts, colors, sizes
   - **Audio**: volumes and mute status
   - **Material references**: validation of material IDs

### Output

The script prints the parsed draft structure as formatted JSON:

```json
{
  "draft_id": "dfd_cat_1775967933_88321108",
  "success": true,
  "draft": {
    "id": "91E08AC5-22FB-47e2-9AA0-7DC300FAEA2B",
    "duration": 5366667,
    "fps": 30,
    "canvas_config": { "width": 1080, "height": 1920, ... },
    "tracks": [ ... ],
    "materials": { ... },
    ...
  }
}
```

### Determining element layer order (which is on top / in front)

When the user asks which element is "on top", "in front", "above", or "closer to the viewer", use the `render_index` field to determine this:

1. Call `query_script` to get the draft JSON
2. In the result, `tracks` is an array; each track has a `segments` array
3. Each segment has a `render_index` field (integer)
4. **`render_index` 值越大，元素越靠前/越靠上（离观众越近）**
5. Compare the `render_index` values of the relevant segments to determine which element is visually on top

Example: if segment A has `render_index: 2` and segment B has `render_index: 1`, then A is displayed on top of B.

### Determining audio presence (判断草稿是否有声音)

When the user asks whether a draft has sound/audio, follow these rules:

1. Call `query_script` to get the draft JSON
2. Check `tracks` array for `type=audio` and `type=video` tracks

**type=audio 轨道：**
- 遍历 `segments` 数组，每个 segment 有 `volume` 字段
- `volume <= 0` 视为静音，`volume > 0` 视为有声音

**type=video 轨道：**
- 遍历 `segments` 数组，每个 segment 有 `material_id` 和 `volume`
- 用 `material_id` 在 `materials.videos` 中找到对应材料
- 如果材料的 `type == "photo"`，该段始终视为静音（图片没有声音）
- 如果材料的 `type == "video"`，则看 segment 的 `volume`：`volume > 0` 有声音，否则静音

**整体判断：** 只要任一轨道中存在有声音的段，草稿即为"有声音"。

```bash
# 快速检查 audio 轨道音量
jq '.draft.tracks[] | select(.type=="audio") | {type, segments: [.segments[] | {volume}]}'

# 快速检查 video 轨道音量及材料类型
jq '.draft.tracks[] | select(.type=="video") | {type, segments: [.segments[] | {material_id, volume}]}'
```

### Quick inspection queries

After running the script, you can pipe the output to `jq` for targeted queries:

```bash
# Check basic timeline info
jq '.draft | {duration, fps, canvas: .canvas_config}'

# List all tracks
jq '.draft.tracks[] | {name, type, segment_count: (.segments|length)}'

# Check element layer order (render_index)
jq '.draft.tracks[] | {type, segments: [.segments[] | {material_id, render_index, target_timerange}]}'

# Check material references
jq '.draft.materials | keys'

# Validate text styling consistency
jq '.draft.materials.texts[] | {id, font: .font_size, color: .color}'
```

### Error handling

- If `VECTCUT_API_KEY` is not set, call `vectcut-login` first, then rerun this skill
- If the draft doesn't exist, the API returns an error message
- If the script content cannot be parsed, the raw output is returned for debugging

### Configuration

| Parameter | Source | Value |
|-----------|--------|-------|
| API Key | Env var `VECTCUT_API_KEY` | (required) |
| Backend URL | Hardcoded | `https://open.vectcut.com` |
| Force update | Optional arg | `false` (default) |
