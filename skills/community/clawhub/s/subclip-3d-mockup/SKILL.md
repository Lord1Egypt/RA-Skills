---
name: subclip-3d-mockup
description: Create, inspect, clone, style, retime, animate, and deliver native editable 3D device layers in Subclip using approved models and semantic MCP tools.
---

# Subclip 3D mockups

Use this skill for bundled phone, laptop, tablet, watch, device-screen, product-turntable, camera, and 3D keyframe requests. Native 3D belongs in the dedicated 3D panel and 3D timeline track, never inside Motion Graphics, HyperFrames, or Remotion.

For every custom 3D keyframe request, immediately load `references/keyframes.md` through `read_subclip_skill` before writing animation. The reference defines the complete MCP lifecycle and is mandatory even when the requested motion appears simple.

Discover native 3D operations through `mcp_editor__list_tools` with `domain: "3d"` and `includeSchemas: true`. Invoke reads through `mcp_editor__call_read_tool` and mutations through `mcp_editor__call_tool`. Every tool name below is the delegated `tool` value.

## Mandatory inspect-first workflow

1. Call `get_current_project`, `list_editor_assets`, `list_3d_models`, and `inspect_3d_composition` before changing anything.
2. Use only returned model IDs, item IDs, media file IDs, and semantic screen slot IDs. Never invent a GLB path, mesh name, material name, URL, or Three.js UUID.
3. Read `inspect_3d_composition.warnings`. Resolve missing screen media and out-of-range keyframes before adding decorative motion.
4. Call `view_current_frame` at the insertion time. Preserve readable content and avoid covering existing focal elements unless the creator explicitly asks for a full-frame product scene.
5. Mutate through the dedicated 3D tools. Never author raw `threeDLayerData` through `update_editor_state` or `set_project_data`.
6. Immediately call `get_3d_layer` after adding or changing a model. Its `modelId` must exactly equal the creator-requested ID returned by `list_3d_models`; never substitute Google Pixel, another phone, or a preset-friendly model.
7. For multi-point custom animation, prefer one `set_3d_keyframe_sequence` call so all holds and transitions save atomically.
8. Call `verify_3d_layer_setup` with every requested model, timing, slot/file binding, appearance value, lighting value, scene background type, and keyframe time. A failed or omitted requirement check is not validation.
9. Inspect the rendered result at every animation boundary and transition midpoint. Verify the same screen content, orientation, framing, and layer order in preview and export-oriented frame capture.

## Decision table

| Creator intent | Required action |
| --- | --- |
| Add a device without specified media | Call `add_3d_layer` without `sourceFileId`; keep the built-in YOUR MEDIA placeholder. |
| Show existing project media | Choose one exact file from `list_editor_assets`, then call `set_3d_screen_content`. Never pick the first file implicitly. |
| Replace screen media | Call `set_3d_screen_content` with the new exact file ID. |
| Remove screen media | Call `clear_3d_screen_content`; do not delete and recreate the 3D item. |
| Change screen fit, padding, roundness, color, transparency, or background image | Call `set_3d_screen_appearance`; do not rebind media merely to change appearance. |
| Clone a device | Call `clone_3d_layer`; use the returned item ID and unique name for later edits. |
| Rename, retime, place, resize, reorder, or change model/camera/light settings | Call `update_3d_layer` with only intended fields. |
| Delete a device | Call `delete_timeline_item` with `itemType: "3d"` and the exact item ID. |
| Split a device on the timeline | Call `split_timeline_item` with `itemType: "3d"` at a time strictly inside the item. |
| Add motion to an already animated item | Call `append_3d_animation_preset` from the intended project time. Existing keyframes must remain. |
| Reset the complete animation | Call `apply_3d_animation_preset` only when the creator explicitly asks to replace all keyframes. |
| Inspect custom movement | Call `list_3d_keyframes`; use its stable IDs and absolute project times for every later edit. |
| Create custom movement | Call `create_3d_keyframe` at explicit project times. Omitted transform values inherit from the preceding state. |
| Create a complete custom sequence | Call `set_3d_keyframe_sequence` once with ordered absolute times; use `replace` only for a new layer or explicit reset. |
| Change or move one keyframe | Call `update_3d_keyframe` with its exact stable ID. |
| Create a timed hold | Call `duplicate_3d_keyframe` to copy the same state to the hold end. |
| Remove keyframes | Call `delete_3d_keyframe` for one exact ID or `clear_3d_keyframes` only when every editable keyframe should be removed. |
| Change the whole layer on the 2D canvas | Use `update_3d_layer` x, y, width, and height. These are canvas percentages. |
| Move the model inside its 3D viewport | Use model position. These are GLB units, not canvas percentages. |
| Orbit or push the view | Use camera position, target, and FOV. Do not fake camera movement with canvas X/Y. |
| Use a short video in a long layer | Set source in/out and `loop: true`. |
| Use one segment of a long video | Set explicit source start/end. Keep the layer duration independent unless matching was requested. |
| Match layer length to screen video | Use `set_3d_screen_content` with `matchLayerDuration: true`; existing keyframes are proportionally retimed. |

For a requested axis-specific move such as positive Z to negative Z with timed holds, use explicit custom keyframes. Create the first pose, duplicate it at the end of the opening hold, create the ending pose at the start of the closing hold, and duplicate that pose at the layer end. For a 10-second layer with two-second holds, the canonical times are 0s, 2s, 8s, and 10s. Never substitute Hero Orbit or another preset merely because it is convenient.

Interpret axes precisely. `modelRotationDegrees` is `[x, y, z]`. A Z-axis rotation changes the third value and rolls the model in the image plane. Revealing the opposite physical face normally requires a 180-degree Y rotation while the camera remains in front. Do not move a camera linearly from positive Z through its target to negative Z; that crosses the model and creates an unreadable transition. Use model Y rotation or an orbiting camera path with intermediate points instead.

## Geometry and timing contract

- New 3D viewports default to a composition-correct 16:9 rectangle.
- Canvas x/y identify the layer center. Width/height are percentages and may extend beyond the canvas for intentional cropping.
- Model position and scale use model-specific GLB units. Registry defaults vary by orders of magnitude; preserve them unless the visual result requires a change.
- MCP rotation inputs are degrees. Stored Three.js rotation values are radians and remain internal.
- Use `update_3d_layer` model/camera fields for a static base pose. Once keyframes exist, use `create_3d_keyframe` or `update_3d_keyframe` at the intended absolute project time instead of silently changing only the base pose.
- Changing `modelId` resets the base scene to the new registry default, retargets existing model/camera keyframes relative to that default, preserves canvas keyframes, and remaps screen bindings by slot order. Inspect every animation boundary after a swap because model proportions still differ.
- Screen source start/end are source-media seconds. Layer start/end are project-timeline seconds.
- A layer longer than a short screen video should loop only when repetition is intentional.
- Matching media duration rescales keyframe offsets. It must not delete keyframes.
- Shrinking a layer must not strand keyframes after its new end. Move or delete those keyframes first; `update_3d_layer` rejects destructive timing.
- When `lockAspectRatio` is true, changing only width or height through `update_3d_layer` updates the other dimension proportionally. Supply both dimensions only when an intentional new aspect ratio is required.
- Parallel 3D lanes are supported. Lane 0 is visually front-most among overlapping items unless layer order explicitly overrides it.

## Animation rules

- Prefer `device-entrance` for a clean introduction, `hero-orbit` for a product angle change, `tilt-reveal` for profile-to-front motion, and `screen-push-in` when display content is the focal point.
- Use `turntable` only when continuous product rotation was requested.
- Use `gentle-float` only for a looping hold and verify that the loop does not conflict with later custom keyframes.
- Keep at least one readable hold where the device display faces the camera.
- Do not stack multiple presets at the same time without inspecting the existing keyframes first.
- Presets produce ordinary editable model and camera keyframes. They are not baked videos.
- A model returned with `nativeAnimation` also plays its reviewed GLTF clip deterministically from the layer start. Native motion is independent of editable preset/keyframe motion. For `macbook-pro-13-2020`, the lid opens during the reviewed 0-4 second clip segment and then holds open.

## Screen-media rules

- Accept only project image or video file IDs returned by tools.
- Do not route screen-media audio through the 3D layer. Keep audible sound on Media or Audio tracks.
- Default to `cover` for full-bleed app screens and `contain` when every edge of the source must remain visible.
- A landscape image on a portrait screen is intentionally cropped heavily by `cover` and appears as a smaller letterboxed card with `contain`. Do not describe this expected aspect-ratio behavior as UV warping. If readability matters more than the requested fit, ask before changing it.
- Leave padding and roundness at zero unless the device UV or creator intent requires them.
- If no source is specified, preserve the placeholder over the registry default Midnight 16 screen background. A placeholder is better than an unrelated automatic media choice.
- `set_3d_screen_content` preserves existing appearance fields unless they are explicitly supplied. Use `set_3d_screen_appearance` when no content change is required or while the placeholder is active.
- For a screen background image, call `list_canvas_background_presets`, then pass one exact `backgroundPresetId`; alternatively pass one verified project image as `backgroundSourceFileId`. Never supply both.
- A screen background sits behind media inside the device display. It is not the whole 3D scene background and not the canvas background.
- If conversation attachments are screen sources, use `import_attachment_to_project_media` for each exact attachment path. Retain each returned file ID and bind those IDs to the requested semantic slots. Never use `import_attachment_to_timeline` and then delete temporary clips for 3D-only media. Never replace a missing second attachment with an existing project image.
- Independent screen slots reject reusing a file ID by default. Set `allowDuplicateSourceAcrossIndependentSlots: true` only when the creator explicitly requests the same source on multiple independent slots.
- For `iphone-14-pro-dual`, bind Front A and Front B independently. The registry uses reviewed flat fitted overlays and high-quality minification so fine UI text remains stable during oblique rotations; agents must not compensate with padding, roundness, or model-scale changes.
- `replacementStrategy: "fitted-overlay"` means Subclip safely handles a texture-atlas model through reviewed overlay geometry. Use the same semantic screen tools; never compensate with model transforms or try to write overlay coordinates.
- `hasCameraCutout: true` means the registry preserves a physical punch-hole while media fills the surrounding display. Do not add padding solely to protect that camera.

## Reviewed recent models

| Model ID | Screen behavior | Agent usage |
| --- | --- | --- |
| `macbook-pro-13-2020` | Direct `primary-screen`; native lid clip opens from 0-4 seconds and holds | Add normally, bind landscape media, then layer editable camera/model keys over the native opening when requested. |
| `macbook-neo` | Registry-managed fitted landscape overlay | Bind `primary-screen` through normal screen tools; do not edit mesh or overlay geometry. |
| `macbook-air-m2` | Registry-managed fitted full-screen landscape overlay | Bind landscape media to `primary-screen`; the model's physical notch renders above media automatically, so no synthetic cutout is used. |
| `macbook-air-15-2023` | Direct isolated display mesh with native notch geometry | Bind landscape media to `primary-screen`; no manual orientation or notch correction is needed. |
| `samsung-galaxy-s26-black` | Registry-managed portrait overlay with camera cutout | Prefer portrait media with `cover`; use `contain` only when preserving every source edge is intentional. |

## Scene backgrounds and lighting

- Use `update_3d_layer` for `lightingPreset` and whole-scene background changes.
- `backgroundType: "transparent"` exposes the canvas or lower layers behind the complete 3D viewport.
- `backgroundType: "color"` uses `backgroundColor` behind the model.
- `backgroundType: "image"` requires exactly one `backgroundPresetId` from `list_canvas_background_presets` or one project image `backgroundSourceFileId` from `list_editor_assets`.
- Project-image references are stored by file ID and remapped after project reload or cross-project clipboard paste. Never persist a temporary localhost media URL.
- Backgrounds uploaded by a person through the app-wide IndexedDB picker are available in the UI but are not enumerable by the main-process MCP server. Agents should use a bundled preset or an exact project image ID.
- Keep the three scopes distinct: canvas background is behind every layer, scene background is inside one 3D viewport, and screen background is inside the device display.

## Tool coverage

- Discovery and inspection: `list_3d_models`, `list_3d_animation_presets`, `inspect_3d_composition`, `get_3d_layer`, `list_editor_assets`.
- Layer lifecycle: `add_3d_layer`, `clone_3d_layer`, `update_3d_layer`, `split_timeline_item`, `delete_timeline_item`.
- Screen content and styling: `set_3d_screen_content`, `set_3d_screen_appearance`, `clear_3d_screen_content`.
- Animation inspection: `list_3d_keyframes`, `get_3d_layer`, `inspect_3d_composition`, `verify_3d_layer_setup`.
- Animation editing: `set_3d_keyframe_sequence`, `create_3d_keyframe`, `update_3d_keyframe`, `duplicate_3d_keyframe`, `delete_3d_keyframe`, `clear_3d_keyframes`, `append_3d_animation_preset`, `apply_3d_animation_preset`.
- Background source discovery: `list_canvas_background_presets`.
- Delivery: `get_export_configuration`, `export_video`; load `subclip-export` when format or alpha matters.
- UI-only gestures such as single-click container selection, double-click scene editing, gizmo dragging, viewport orbit, and canvas hover outlines are not MCP mutations. Represent their durable result through the semantic tools above.

## Verification checklist

- `get_3d_layer.modelId` exactly matches the requested model.
- Every requested semantic screen slot exists and is bound to the intended tool-returned project file ID.
- The intended 3D item is active at the inspected playhead.
- Screen media is not mirrored, upside down, missing, or replaced by the GLB's original wallpaper.
- The device is not clipped unintentionally by its 16:9 viewport.
- Canvas placement and model transform are not confused.
- Every keyframe lies inside the item duration and is visible on the 3D timeline lane.
- A requested custom animation must not finish with an empty keyframe list. After `list_3d_keyframes`, use its returned `writeTools` rather than claiming keyframe mutation is unavailable.
- Every screen `sourceFileId`, screen `backgroundImageFileId`, and scene `imageFileId` resolves to a current project media file after reload.
- Existing keyframes remain after append operations.
- Axis-specific motion uses explicit keyframes at the requested hold boundaries; no fallback preset silently replaces it.
- Preview and exported frame show the same device pose and screen content.
- Require `verify_3d_layer_setup.passed: true`, then re-read `inspect_3d_composition` and `get_3d_layer` before updating the director brief with model, screen source, source segment, layer timing, lane, and animation.

## Canvas backgrounds

Use canvas backgrounds deliberately when composing 3D devices with Motion, HyperFrames, Remotion, text, or media layers.

- Call `list_canvas_background_presets` before choosing a bundled image. Never invent preset IDs or asset URLs.
- Use `set_canvas_background` for a timed color, transparent segment, bundled image, or an explicitly identified project image. Canvas images always use cover.
- Use `set_canvas_background_visibility` only when the user wants the complete background track hidden or needs alpha export. A transparent segment affects only its own time range.
- Prefer midnight backgrounds behind bright interfaces, light devices, white typography, or luminous product renders.
- Prefer daytime backgrounds behind dark devices, dark UI, restrained editorial layouts, or content that needs a clean commercial tone.
- Prefer landscape backgrounds only when atmosphere or place supports the story. Avoid detailed scenery behind dashboards, captions, charts, or small UI text.
- Prefer color-flow backgrounds for energetic, colorful, or abstract product moments. Use the exact `colorFlow-1` through `colorFlow-74` IDs returned by `list_canvas_background_presets`; never reconstruct an ID from a display label.
- Keep foreground readability primary. If the device, chart, or text already has high visual detail, choose a quiet background with low local contrast behind the subject.
- Do not confuse the canvas background with a device screen binding. Canvas images sit behind all layers; device screen media belongs to `set_3d_screen_content`.
- For compositing deliverables, expose alpha and choose WebM VP9 or ProRes 4444. MP4/H.264 does not preserve transparency.

## Export handoff

When a 3D composition is ready for delivery, call `get_export_configuration` before choosing an alpha format. Use `export_video` with explicit `format`, `quality`, and `transparent` values. Choose MP4/H.264 for normal delivery, WebM/VP9 or MKV/VP9 for transparent client output, and MOV/ProRes 4444 for an editing or compositing master. Alpha requires either a hidden canvas background track or a transparent background segment. For the complete export workflow, load the `subclip-export` skill.

## Layer identity and keyframes

- Give every new 3D layer a concise semantic name when its role is known, such as `Hero phone`, `Secondary watch`, or `Checkout laptop`.
- Before naming, inspect existing 3D items. Subclip automatically suffixes collisions with `2`, `3`, and so on; never identify a layer by model type alone when multiple instances exist.
- Use exact item IDs for edits even when names are unique. Names are for human and agent orientation, not identity.
- Treat keyframe IDs as stable editor targets. When discussing or modifying a keyframe, preserve its exact item ID, keyframe ID, and absolute timeline time.
- A timeline keyframe click selects the owning 3D layer, seeks to the exact frame, highlights the matching inspector row, and scrolls that row into view.
## 3D template insertion

- Create a model with `add_3d_layer`. This uses the same shared model-template builder as the 3D Studio library and defaults to `animationPresetId: "tilt-reveal"`.
- Treat the returned layer as the editable template instance. Bind project media, change its scene, or replace/append keyframes on that item instead of creating a second bare model.
- Use another `animationPresetId` only when the creator requests that preset. Use `animationPresetId: "none"` only for a fully custom motion, then immediately write the requested sequence with `set_3d_keyframe_sequence`.
- Do not infer attachment content, media type, source range, screen role, or ordering from an example. Inspect the actual project media and use returned IDs and slot IDs.

## Screen video audio

- When the creator asks to hear a video bound to a 3D screen, call `set_3d_screen_content` with `audioEnabled: true` and the requested `volume`.
- Keep that media in Project Media and on the 3D screen binding. Do not extract or add a duplicate audio timeline item unless the creator explicitly requests a separate editable audio track.
- Keep `allowConcurrentAudioPlayback` false unless the creator explicitly requests the same source to play from multiple audible owners.
- Keep the screen texture video and its audio on the same source range, playback rate, loop setting, and 3D layer timing.
- Images cannot provide screen audio. Verify the inspected Project Media item is a video before enabling it.

## Cross-layer requests

- A request can require native text, media, elements, captions, or motion graphics alongside the 3D layer. Every named layer is required; completing the model does not complete the other edits.
- Discover the relevant native tool with `mcp_editor__list_tools`, then create each requested layer using the creator's exact content and the requested timing and placement.
- When wording such as "with the 3D model" or "in the same scene" refers to timing, align the added layer to the 3D item's actual start and end. Do not invent copy, content, or semantics that the creator did not provide.

## Exact visual verification

- Call `view_current_frame` with `timeSeconds`, `targetType: "3d"`, and the 3D `itemId` at every hold, transition midpoint, and final visible frame.
- The returned image is the complete composed canvas, not an isolated thumbnail. Use it to verify screen pixels, model animation, framing, transparency, and stacking against other layers.
- Do not report visual success from saved state, keyframe lists, or source validation alone.
