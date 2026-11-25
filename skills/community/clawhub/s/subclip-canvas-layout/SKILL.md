---
name: subclip-canvas-layout
description: Design and adjust Subclip canvas aspect ratio, dimensions, backgrounds, framing, layer position, size, crop, and visual hierarchy. Use for vertical, landscape, square, social formats, safe zones, composition, alignment, responsive framing, or direct canvas manipulation.
---

# Subclip Canvas Layout

1. Read `canvasConfig` and list all visible items at the target playhead.
2. Use `set_canvas_properties` with exactly one supported preset: `landscape`, `vertical`, or `square`. Do not create custom canvas dimensions. With no explicit format: keep the aspect ratio of an imported video that is the edit's main subject; otherwise use `landscape` (16:9) for motion graphics and demo videos.
3. Adjust media with normalized 0–1 coordinates and text with percentage 0–100 positions.
4. Use `contain` when preserving the whole image matters; use `cover` when edge-to-edge framing matters.
5. Inspect the result using `view_current_frame`. Inspect more than one time when layers animate or enter later.
6. Correct every visible offset, black bar, crop, overlap, or unsafe margin, then inspect the corrected frames again. Do not report completion until this second inspection passes.

For bespoke graphics not expressible through native layers, route to `$subclip-motion-graphics`, which uses HyperFrames by default. Before authoring any motion layer, inspect concurrent layers and reserve the graphic's intended canvas rectangle with explicit center `x/y` and `width/height`; treat that box as the layer root's local coordinate system. Do not start with a full-canvas item for a partial-canvas graphic and reposition only its inner content afterward. Create each intended beat once, then correct placement or size by updating that same item (`update_runtime_layer`, or `update_html_motion_graphic` for the rare HTML/CSS effect) rather than stacking a corrected copy.

Maintain a clear focal point, keep faces and text away from crop-prone edges, preserve intentional layer order, and avoid stretching sources. When converting aspect ratio, recompose visible layers; changing only canvas dimensions is incomplete.

Layer order is explicit: a larger media `zIndex` is visually in front and is shown in the top timeline lane. Background/tutorial footage belongs behind at `zIndex: 0`; presenter cameras, logos, and intentional overlays belong in front at a larger `zIndex`. Use `set_media_layer_order` instead of assuming array order. For simultaneous media, confirm both items occupy different lanes and inspect a frame after the shorter source's original duration when looping is involved.

For temporary split screens, call `apply_two_way_split_scene`. It splits each source at the scene boundaries in UnifiedTimeline, then assigns real left/right container dimensions to only the middle segments. Never resize a full-duration source into a temporary split with layout keyframes. Keep each segment's `scale` at 1, the tutorial audible in the lower lane, and the muted presenter in the upper lane. Add keyframes only for motion or effects within the isolated segments.

After resizing, inspect the composed frame and reposition media, text, captions, and HTML motion graphics for the new shape. A successful canvas resize does not imply existing layers are well framed.
