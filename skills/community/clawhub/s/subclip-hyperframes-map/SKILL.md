---
name: subclip-hyperframes-map
description: Build an editable HyperFrames map after the creator rejects both built-in Remotion map styles or explicitly requests HyperFrames. Use verified geographic geometry with custom SVG, GSAP camera motion, routes, and labels inside Subclip.
---

# HyperFrames map alternative

General maps start with `$subclip-map-explainer`: the Cesium `map-explainer` globe and flat `river-sequence` are the two built-in choices. Use this skill after both styles are rejected or for an explicit HyperFrames map request. A failed frame capture alone is not a design rejection.

1. Read `$subclip-hyperframes-layer` and its relevant authoring/GSAP references through `read_subclip_skill`. Follow the host's pinned runtime and source validator; do not create a standalone project or install map packages.
2. Inspect the project and existing map. Apply the creator's feedback to palette, labels, route treatment, and camera progression. If the direction is clear, proceed without another preference question.
3. Resolve places to verified coordinates. For a world route, call `create_route_map_geometry` with the exact labels and coordinates. Preserve returned `motionGraphic.html` geographic paths, coordinate-bound markers, and distance basis. Do not draw approximate continents or invent SVG geometry. Preserve coordinate/projection relationships when using an attached or verified custom dataset.
4. Build one standalone HyperFrames document with explicit composition dimensions/duration. Put the map, route, and anchored markers in a shared world wrapper. Replace the tool's CSS animation rules with one finite paused GSAP timeline, retaining static styles and positions. Do not animate the same transform/stroke with both CSS and GSAP. Keep one projection throughout the shot.
5. Register `window.__timelines[compositionId]` under the HyperFrames contract. Keep source establishment, route travel, arrival, and final hold readable and seekable. Put supported copy/colors in flat `window.__hfVariables`; retain the geography's source. Do not claim satellite imagery, elevation terrain, or photorealistic cities from vector geometry.
6. Validate using `validate_runtime_layer_source`, `kind: "hyperframes"`, then add using `add_runtime_layer`. When replacing a map created during this edit, remove that exact rejected item as part of the requested replacement so it cannot occlude the new one. Preserve unrelated layers and explicitly requested comparisons. Correct subsequent issues using `update_runtime_layer` on the returned ID.
7. Inspect representative frames through `view_current_frame` with `targetType: "motion-graphics"` and the new item ID. Check geographic alignment, continuous routes, labels, transparency, timing, and stacking. Update the director brief with the chosen alternative, coordinate source, and any pending verification. Import success is not visual proof.

This workflow changes map design; it does not authorize unrelated media generation, TTS, export, or paid map services. If required geographic data is unavailable, report that missing input instead of inventing an accurate-looking map.

On Linux without a GPU (software GL) heavy HyperFrames templates (3D transforms, perspective, blur or backdrop-filter, per-image colour grading, WebGL) can take many minutes per second of video; prefer a light template there. Tool results carry a `warning` when a layer looks heavy; it never blocks anything.
