---
name: subclip-motion-graphics
description: Discover, import, and customize all Subclip Motion Graphics templates, exact @ mentions, Remotion maps, HyperFrames scenes, and HTML/CSS presets. Route new animated explainers, diagrams, counters, and concept animations to the appropriate editable engine.
---

# Subclip Motion Graphics

Choose the smallest robust engine inside Subclip's unified Motion graphics panel. Do not silently replace the request with ordinary text layers or create a standalone framework project.

## Canvas

Motion graphics and demo videos default to a 16:9 landscape canvas. Unless the user asked for another format, or an imported video that is the edit's main subject sets the aspect ratio, call `set_canvas_properties` with `landscape` before adding the first layer. See "Default aspect ratio" in `$subclip-video-editor`.

## Engine priority

For a selected template, follow the template workflow below before authoring from scratch.

1. Use `$subclip-hyperframes-layer` by default for new motion graphics, including animated explainers, diagrams, counters, kinetic typography, product UI demonstrations, DOM/SVG choreography, GSAP timelines and Lottie.
2. Use `$subclip-remotion-layer` only when the user explicitly requests Remotion/React/TSX, selects a Remotion template, or asks to revise an existing Remotion layer. Do not choose Remotion automatically because a scene is complex, frame-driven or data-driven.
3. Use the script-free HTML/CSS workflow below only for one small, self-contained effect that is not a scene of the video: a compact CSS loader, a single badge or card entrance, or an exact inline SVG treatment. Never build a video's scenes, a demo, an explainer, a promo, or any multi-beat sequence from HTML/CSS items, even when each scene looks simple. Use HyperFrames for those: creators can click into a HyperFrames scene to edit its text and shapes directly, and HyperFrames scenes are easier for them to adjust later.

An explicit framework or exact template request always wins. When the creator does not name one, use HyperFrames without asking them to choose; "it would be shorter in HTML/CSS" is not a reason to switch engines for a scene. Preserve an existing layer's engine when editing it; do not migrate or replace it without a request. Do not place scripts in a native HTML/CSS Motion item.

An explicit request to adapt or use HyperFrames registry blocks routes to `$subclip-hyperframes-layer`. Preserve every named block slug: look up each one through the registry tools before authoring instead of replacing it with a generic hand-built effect.

A device mockup, product turntable, phone/laptop/watch screen replacement, or camera orbit around one of Subclip's bundled models routes to `$subclip-3d-mockup`. Keep it in the dedicated native 3D panel and track; do not hide it inside Remotion, HyperFrames, or HTML Motion unless the creator explicitly requests custom framework source.

Route any geographic map request to `$subclip-map-explainer` first. Import the built-in Remotion `map-explainer` Cesium globe by default, or `river-sequence` for an explicitly flat river/ordered-flow story. When the creator dislikes both styles, use `$subclip-hyperframes-map`. Respect exact tagged templates and explicit framework requests. True elevation-terrain and photorealistic flyovers are unavailable; do not fake them or expose map-provider credentials.

An ordinary editable title or label that only needs to move, scale, rotate, or fade across the canvas belongs in TextPanel. Route that work to `$subclip-text-captions` and use text keyframes; do not create a framework layer solely to move one text layer between positions. Simple shapes, arrows, highlights, blur, paper textures, gradients, and effect layers belong in ElementsPanel through `$subclip-elements`. Use HTML/CSS only after deciding that a Remotion or HyperFrames layer would add more code and runtime surface than the requested animation needs.

For HTML/HyperFrames motion, never put CSS `filter`/`backdrop-filter` on text or on an ancestor containing text—even `blur(0px)` can make exported text disappear. Use opacity and translate/scale/rotate for text reveals. Isolate any decorative blur in a sibling background element with no text descendants.

## Resource availability and native media

All three engines run inside Subclip's sandbox. Confirm fonts, asset bytes and permitted dependencies are available to preview **and** export before using them. Prefer confirmed installed/bundled/host-loaded font faces. If a font or foreign resource is absent, download/import it through supported host tools and verify it loads; if that fails, use a verified alternative and disclose the substitution. An agent filesystem path or a successful network request outside the renderer is not proof of sandbox access. You may still build, render and compare in your own terminal before importing; see `subclip-video-editor` → "Test freely outside the editor, then import".

Import images/videos into the project Media library and sounds into the Audio library first; re-list assets and use only the returned URLs where the engine supports them. Prefer native MediaLayer/AudioLayer items and their editable lanes, with motion items providing the graphics. Embedded media is an exception for an effect inseparable from the component, not a default place for the whole edit or soundtrack. Inspect existing source/bindings and move separable content to native lanes, preserving timing/trim/crop/volume and avoiding duplicate playback.

The script-free HTML/CSS path cannot embed video/audio or external resource URLs, even after import. Compose it over native Media/Audio lanes. Its fonts must already be verified in the host; do not add remote font imports or scripts to bypass validation. Self-contained sanitized SVG follows the explicit vector workflow below.

After import and placement, re-list library/timeline items and verify playback, seeks, boundaries and exported output. Missing downloads, blank frames or unavailable fonts require correction or a stated verified alternative before claiming completion.

## Template discovery and import

1. Discover `list_motion_graphics_templates` through `mcp_editor__list_tools` with `includeSchemas: true`, then invoke it through `mcp_editor__call_read_tool`. It includes every current Motion Graphics panel template across Remotion, HyperFrames, and HTML/CSS. `list_templates` is the unrelated caption catalog.
2. For an `@` Motion template, pass its exact `catalogId` as `templateId`. Otherwise search by `query` or `kind`. Preserve the tagged engine and ID; a tag references a template, not an already-imported timeline item.
3. Use the returned `importTool` and `importArguments`, adding the active `projectId`, requested `startTime`/`duration`, and appropriate geometry. Runtime templates use `add_runtime_layer`; HTML/CSS templates use `add_html_motion_graphic` with `templateId`. Unchanged imports do not need source retrieval.
4. Request `includeSource: true` for one exact template only when its source or full defaults are needed. Import first, then customize the returned item ID. Remotion uses JSON `props`, HyperFrames uses flat `variables`, and HTML/CSS uses `html`/`css`. Import merges top-level props/variables over template defaults; pass complete nested objects because nested values are replaced. Read existing bindings before later updates, which may replace the binding object.
5. Use `get_runtime_layer` and `update_runtime_layer` for framework changes, or `update_html_motion_graphic` for HTML/CSS. Add a second item only for an intentional second instance. Keep template source and unrelated behavior intact unless the creator requested a source change.
6. Re-list assets and inspect entrance, midpoint, and final hold through `view_current_frame`, `targetType: "motion-graphics"`, and the returned item ID. Record the template and engine in the director brief after verification. Failed capture means visual verification remains pending even if import succeeded.

The shared catalog is authoritative; do not maintain a fixed exhaustive list of template names in a prompt or reconstruct tagged templates from memory.

## Default visual system

When the user has not supplied a visual theme, use Subclip's house system instead of inventing a palette:

- White or very light slate surfaces; deep navy `#153592` for primary emphasis.
- Cyan `#26c9d5` for secondary emphasis, progress, and restrained navy-to-cyan gradients.
- Near-black/slate heading text, muted slate body text, light slate borders, clean sans-serif typography, and rounded cards.
- Keep color restrained and readable. Do not introduce purple, neon, dark cinematic, or unrelated multicolor themes by default.

The user's explicit palette, brand guide, reference design, or requested art direction always overrides this default.

## Area-first layout contract

Decide the Motion item's canvas area before writing its HTML or CSS. First seek to the intended placement time and call `view_current_frame`; the asset list alone is not enough to reveal occupied and empty visual regions. Inspect the canvas and every visible layer during the intended time range, then reserve the smallest rectangle that comfortably contains the graphic without covering unrelated content. Express that rectangle explicitly with `x`/`y` as center percentages and `width`/`height` as canvas percentages. A `100 × 100` full-canvas item is prohibited by default and is appropriate only when the creator explicitly asks for a full-frame scene/background or the requested visual inherently replaces the whole frame.

When no exact geometry is requested and the inspected frame is empty, use a centered contained 16:9 box rather than full canvas. On a landscape canvas let available height limit the box; on a portrait canvas let available width limit it; on a square canvas preserve aspect ratio within both limits. When other layers are visible, move and shrink that box into the clearest open region instead of covering the existing edit. Keep the framework document/root transparent; a local card, chart, phone, map plate, or other actual graphic may have its own bounded surface.

Author the markup and styles for the reserved rectangle, not for the entire video canvas. Treat the Motion item's own box as its local coordinate system: make the root fill that box, keep internal layout responsive to it, and avoid invisible full-frame wrappers, oversized hit areas, or decorative surfaces outside the reserved region. If later inspection shows the graphic needs different space, update the same item's geometry first and then adapt its HTML/CSS to the new box.

## Official SVG assets

MediaPanel does not register standalone `.svg` files. When the creator supplies an official SVG logo, icon, illustration, or map, keep it vector by placing its exact sanitized markup inline in a Motion Graphics item instead of converting it to PNG.

- Fetch/read the SVG once from the exact attached file or creator-supplied public URL. Never leave that URL in the runtime HTML.
- Preserve its `viewBox`, paths, groups, gradients, masks, clip paths, filters, and brand colors. Do not trace, redraw, approximate, recolor, or simplify official artwork unless requested.
- Reject or remove active and remote content before inlining: scripts, event-handler attributes, `foreignObject`, iframes/objects/embeds, JavaScript URLs, external CSS/imports/fonts, and non-fragment remote `href`, `xlink:href`, or `url(...)` references. Local `#fragment` references are allowed.
- Put a static SVG in its own tightly bounded Motion item when the creator needs independent canvas placement. Animate the wrapper's opacity/position/scale for ordinary entrances; animate SVG paths only when the request calls for it.
- Do not rasterize an SVG merely because MediaPanel rejects `.svg`. Convert to PNG only when the SVG cannot be made self-contained/safe or the creator explicitly requests raster output, and disclose that fallback before using it.
- Inspect the SVG item at its entrance and final hold. For brand marks, verify exact proportions, colors, transparency, and safe margins.

## HTML/CSS fallback workflow

1. Call `list_editor_assets` with the active `projectId` and inspect existing `motionItems`, canvas, duration, text, and media.
2. If the project is empty and untitled, follow `$subclip-video-editor`'s creative naming rule and call `rename_project` with a one- or two-word title for the finished visual concept before adding the first Motion item. Never use a framework/tool/task label. Re-read the saved title before continuing.
3. Confirm this is the single small effect allowed above, not a scene or a sequence of beats; otherwise stop and use `$subclip-hyperframes-layer`. Turn the requested explanation into a small number of readable visual beats. For each beat, seek to its intended time, inspect the current rendered frame, and decide its explicit `x`, `y`, `width`, and `height` canvas area before authoring markup.
4. Build semantic HTML, scoped CSS, CSS keyframes, and sanitized inline SVG inside that reserved local box; do not use scripts, event handlers, remote embeds, wall-clock timers, external URLs, or full-canvas wrappers for a partial-canvas graphic.
5. Call `validate_html_motion_source` with the complete HTML and CSS and fix every error. Then add each intended timed beat once with `add_html_motion_graphic`, passing the explicit geometry. Keep every item inside the canvas, give it a meaningful name, and record every returned item ID.
6. Revise an existing beat with `update_html_motion_graphic`. A correction to timing, HTML/CSS, dimensions, center coordinates, opacity, or stacking must mutate the same item ID—never add a corrected copy on top of it.
7. Re-list assets. Completion requires the returned `motionItems` to contain every intended item with the correct start/end times. An add/update response alone is not sufficient.
8. For each intended item, call `seek_timeline` and `view_current_frame` with the same `projectId` at its entrance, settled state, and exit. Correct blank frames, clipping, low contrast, unintended overlap, and unsafe placement before continuing.
9. Before the final response, perform a cleanup inventory. Delete superseded drafts and accidental duplicates created during the current run with `delete_html_motion_graphic`. Preserve pre-existing items and deliberate overlaps during ordinary edits. If the user explicitly requests cleanup of an earlier failed pass, use timing, names, HTML/CSS, geometry, and rendered frames to identify its redundant versions, keep one verified final item per intended beat, and delete the exact obsolete IDs. Re-list assets and confirm that each scene has exactly the intentional layers—no original/resized/centered correction copies remain.
10. Finish the timeline clock, not only the visible beats. If the user requested a target or maximum duration, call `set_project_duration` with the exact intended endpoint after retiming and cleanup. If no exact duration was stated, remove an unintended background-only tail by matching the project duration to the final intentional content end; preserve a deliberate final hold when the design calls for one. If the tool reports content beyond the endpoint, correct those exact items and retry. Re-list assets and confirm both `duration` and the canvas-background row end at the intended time.
11. If this was created from an untitled project, verify that the first-step title remains saved. Re-list or re-read the project and only report that title when saved state contains it. Do not rename an existing creator-authored project.

If live frame capture fails, keep the Motion-panel items saved and report visual verification as unavailable. Never claim the motion graphic exists when `motionItems` is empty, and never claim a text-only fallback satisfies a motion-graphics request unless the user accepts that fallback.
