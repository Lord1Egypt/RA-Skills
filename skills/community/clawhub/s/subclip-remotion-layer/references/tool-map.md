# Remotion layer tool map

- `list_motion_graphics_templates`: unified panel/@ catalog; filter by `kind: "remotion"`, exact templateId/catalogId, or query. Import using returned importArguments. Props merge over template defaults at import; nested objects are replaced.

- `list_editor_assets`: resolve `remotionItems`, timing, geometry, props, lane, hierarchy, and source hash.
- `list_runtime_layer_templates`: list stable Remotion templates; request source only for deliberate authoring.
- `import_public_lottie_json`: download and validate a stable public Lottie JSON file, keep a project-local copy, and return the exact animation object for Remotion props. Never load it with `fetch()` in authored TSX.
- `get_runtime_layer`: read exact TSX and props for one item.
- `plan_globe_route`: resolve direct/Pacific/Atlantic/custom globe points and camera props. Ocean corridors are illustrative, not navigable routes.
- `validate_runtime_layer_source`: dry-run syntax, import, forbidden-runtime, URL, complexity, and props validation.
- `add_runtime_layer`: create one item with `kind: "remotion"` and either `templateId` or `source`.
- `update_runtime_layer`: revise the existing ID in place, including source, props, time, geometry, fit, opacity, lane, z-index, and cross-panel order.
- Imported templates are fully editable. Use `mergeBindings: true` for partial props changes, or `templateId` to refresh/replace template source in the same timeline item while retaining placement and bindings. Inspect custom source before replacing it. A missing UI slider does not prevent validated TSX/prop edits.
- `clone_runtime_layer`: make a numbered editable copy.
- `delete_runtime_layer`: remove one exact recoverable item.
- `split_timeline_item`: split with `itemType: "remotion"`; local frame time restarts at zero in the second placement.
- `seek_timeline` plus `view_current_frame`: mandatory visual verification.
- `validate_project`: final structural validation.

Generic `set_project_data` and `update_editor_state` reject paths under `remotionLayerData`. Named tools enforce source/props validation and preserve history.

Geometry is expressed as canvas percentages. `x` and `y` are center coordinates; `width` and `height` are the item rectangle. `fitMode` is `contain`, `cover`, or `stretch`. Opacity is 0–1. Lane 0 is the track's visually highest row; cross-panel visibility is resolved with `layerOrder`.

For new background music, follow `subclip-music-generation`: `list_ai_models(kind: "audio")` → authorized `generate_music` → async completion / `get_ai_operation` → `import_ai_operation_to_timeline` when placement is requested. Keep the result in a native Audio lane; use native audio-editing tools for trim, fades and gain.
