# HyperFrames layer tool map

- `list_motion_graphics_templates`: unified panel/@ catalog; filter by `kind: "hyperframes"`, exact templateId/catalogId, or query. Import using returned importArguments. Variables retain template defaults and merge supplied overrides. Read `subclip-hyperframes-map` for the map alternative after both built-in styles are rejected.

- `list_editor_assets`: resolve current `hyperframeItems`, timing, geometry, lane, hierarchy, source hash, and variables without returning large source.
- `list_runtime_layer_templates`: list stable HyperFrames template IDs. Use `includeSource: true` only for deliberate source authoring.
- `list_hyperframes_registry`: search or paginate the complete current official examples, blocks, and components manifest. This is live read-only discovery, not installation.
- `get_hyperframes_registry_item`: read one exact official item metadata record and, when needed, bounded text source files. Adapt the result into the Subclip contract before validating or saving it.
- `get_runtime_layer`: read one exact layer including complete HTML.
- `validate_runtime_layer_source`: dry-run the same source and binding checks used by persistence, preview, and export.
- `add_runtime_layer`: create a validated item. Pass `kind: "hyperframes"`, then either `templateId` or `source`, never both.
- `update_runtime_layer`: revise one exact item in place. It accepts source, variables, timing, geometry, opacity, fit, lane, z-index, and cross-panel layer order.
- `clone_runtime_layer`: create a numbered editable copy, starting after the source by default.
- `delete_runtime_layer`: remove one exact recoverable item.
- `split_timeline_item`: split a placement with `itemType: "hyperframes"`; internal time restarts for the second placement.
- `seek_timeline` plus `view_current_frame`: mandatory visual verification.
- `validate_project`: final structural validation.

Generic `set_project_data` and `update_editor_state` reject paths under `hyperframeLayerData`. This is intentional: named tools preserve validation and history.

Geometry uses canvas percentages: `x` and `y` are the item center, while `width` and `height` are its bounds. `fitMode` is `contain`, `cover`, or `stretch`. Opacity is 0–1. Lane 0 is the visually highest row inside this track; use `layerOrder` for hierarchy across panel types and `zIndex` among overlapping peers.

For new background music, follow `subclip-music-generation`: `list_ai_models(kind: "audio")` → authorized `generate_music` → async completion / `get_ai_operation` → `import_ai_operation_to_timeline` when placement is requested. Keep the result in a native Audio lane; use native audio-editing tools for trim, fades and gain.
