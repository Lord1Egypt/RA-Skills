---
name: subclip-remotion-layer
description: Create or revise an editable Remotion React/TSX layer inside a Subclip project using the pinned runtime, typed props, frame-driven animation, and approved packages. Use when requested explicitly for a selected Remotion template, or when revising an existing Remotion layer.
---

# Subclip Remotion layer

Use Subclip's typed runtime-layer MCP tools. A Remotion layer is one default-exported React component stored in the project and rendered natively at the layer's Subclip timing, rectangle, opacity, lane, and hierarchy.

This skill adapts Remotion best practices to Subclip's embedded component boundary. It takes precedence over external Remotion project scaffolding, package installation, Studio, Player setup, renderer, cloud, Lambda, and filesystem instructions while editing inside Subclip.

## Route deliberately

- Use this skill when the creator explicitly asks for Remotion/React/TSX, selects a Remotion template, or requests edits to an existing Remotion layer. For new motion graphics without an explicit engine choice, use `$subclip-hyperframes-layer`; complexity or frame-driven animation does not override that default.
- Use `$subclip-hyperframes-layer` for explicitly requested HyperFrames, GSAP DOM timelines, or Lottie/HTML JavaScript animation.
- Use `$subclip-motion-graphics` to route a general motion-design request. Its script-free HTML/CSS path is only the fallback when that result is materially smaller.
- Prefer native Text, Elements, Media, Audio, or Captions when they express the requested edit cleanly.

## Export-safe CSS (client-side rendering)

Subclip exports Remotion layers with Remotion's client-side renderer, which re-draws elements from their computed styles and silently drops anything it does not implement. The preview is a real browser, so an unsupported style looks right in preview and is missing from the exported video. Read [references/client-side-rendering.md](references/client-side-rendering.md) before authoring and follow it over any upstream example.

Never use in a Remotion layer: `z-index` (stack by JSX order instead), `backdrop-filter`, `mix-blend-mode`, `background-blend-mode`, `radial-gradient` / `conic-gradient` / repeating gradients, `background-image: url(…)` (use `<Img>`), inset or spread `box-shadow`, `object-position`, `perspective`, `transform-style`, `writing-mode`, CSS `filter` / `clip-path` / `mask` with `url(#…)`, `<iframe>`, `<OffthreadVideo>`, `<Html5Video>`, `<Html5Audio>`, `<AnimatedEmoji>`. `validate_runtime_layer_source` reports these as "Export can't draw this: …" warnings; fix every one before saving.

## Recover a reported export omission

When the user complains that an element from this Remotion layer is missing in the exported video, convert the affected layer to HyperFrames while preserving the exact design, layout, assets and animation. This is an exception to keeping existing Remotion layers in their original framework. Follow [the export recovery workflow](references/export-recovery.md); do not settle for a visually simplified Remotion workaround or claim success from preview alone.

## Fonts and sandbox resources

This is a sandboxed layer runtime. A font, file, URL or package visible to the authoring agent is not automatically available to the preview or export renderer.

The sandbox limits what the layer can load, not how you test. When something can't be checked properly in the editor, build and test it in your own terminal first (framework CLI, test renders, frame comparisons in a scratch folder), then import the finished, validated result. See "Test freely outside the editor, then import" in `subclip-video-editor`.

- Before choosing typography, verify the exact family, weights and styles in the target runtime. Prefer a confirmed installed system font or a bundled/host-loaded font. A familiar family name or an OS fallback stack is not proof of availability. For portable projects, use the same embedded or host-managed font bytes in preview and export.
- If the chosen face is missing, obtain the licensed font through the available host download/font-loading workflow **before** authoring against it. Confirm the download succeeded and the renderer can load it. A shell filesystem path is not a usable layer URL; downloading alone does not expose a font to the sandbox. Do not install a font package from inside layer code.
- If downloading or registering the face is unavailable or fails, choose an already verified font, identify the substitution, and adjust text boxes/line breaks to its actual metrics. Never keep a missing family name and assume silent substitution is safe. Verify the title, long text and heavy/italic variants in preview and an exported frame.
- Check every external dependency before referencing it: supported type, allowed/pinned runtime version, actual bytes, renderer access and export readiness. Download/import missing resources through the host's supported tools. If they remain unavailable, use a verified alternative and disclose the change; do not invent URLs or unsupported APIs. Preserve explicitly requested identities such as brand assets rather than silently replacing them with unrelated artwork.
- Layer code cannot fetch credentials, install packages, read arbitrary local files or bypass CSP. Resources that cannot be made available through the supported host boundary must be replaced or omitted with a clear explanation.

## Media library first; native timeline first

Before using any image, video or audio in layer code, import it into the project's Media or Audio library through the matching native import tool. Reuse an existing imported asset when present. Call `list_editor_assets` afterward and use the exact returned, renderer-supported asset URL; never use a search-result/provider URL, temporary download path or guessed custom-scheme URL directly in the composition.

Prefer editable MediaLayer/AudioLayer items in the Media/Audio lanes for footage, B-roll, stills, narration, music and SFX. Keep motion code focused on graphics and synchronize its item timing with those native items. Use embedded media only when the requested effect needs it inside the component (for example a texture or a masked screen); it must still come from the imported library. Do not hide an entire edit or soundtrack inside framework source.

For an existing layer, inspect source and bindings for remote media and hidden audio. Import missing assets, replace URLs, and move separable media/audio to native lanes while preserving trim, timing, crop, hierarchy and volume. Avoid duplicate visible footage or doubled audio: verify one intended playback owner after migration. Keep the existing item IDs when updating graphics.

Double-check the asset inventory and timeline after changes, then verify play, pause, forward/backward seek, scene boundaries and an exported frame/short clip. A successful import or static validation alone does not prove a resource loads or plays in the sandbox.

## Generate background music through Subclip

For a request to create new background music, underscore, or a soundtrack, read [Subclip music generation](../subclip-music-generation/SKILL.md) and use its `generate_music` workflow. Discover `text_to_music` models and current pricing with `list_ai_models(kind: "audio")`; follow the music skill's authorization and async-completion rules. Default music generation to Google Lyria 3 Pro (`modelId: "lyria-3-pro"`); switch models only at the user's explicit request. Default background music to `settings.mode: "instrumental"` and leave room for narration. For sung lyrics, also read [Subclip songwriting](../subclip-songwriting/SKILL.md).

Use Subclip's managed music tools instead of upstream generation helpers, direct provider API calls, or synthesizing a replacement in framework code. Reuse a user-provided or already suitable Audio asset when generation was not requested. After a successful operation, use `import_ai_operation_to_timeline` when placement is authorized, inspect the actual duration, and trim, fade and mix through native audio tools. Keep the soundtrack in an editable Audio lane and preserve one playback owner; do not embed a duplicate in the animation layer.

## Keep timeline segments small

Never put an entire long video and all of its animation code into one runtime layer. Divide a multi-scene sequence into short, independently editable segments at natural scene or beat boundaries. Give each segment its own focused source, descriptive name, explicit timeline start, and duration, then add it as a separate timeline item. A single short beat can remain one item.

Validate, add, and visually verify each segment before moving to the next so errors can be isolated and fixed by updating that segment's ID. Keep animation time local to each segment and verify adjoining boundaries for gaps or unintended overlaps. Do not create one giant layer and split it afterward: splitting restarts the framework clock and retains the original source instead of producing focused code. Share visual conventions through matching props or variables across segments.

## Required loop

For a template or `@` mention, resolve its exact catalogId with `list_motion_graphics_templates`, import using its returned `add_runtime_layer` arguments, and customize that item ID. Imports preserve defaults and merge top-level prop overrides; nested objects are replaced. For maps, read `$subclip-map-explainer` and start from `map-explainer` or `river-sequence`; use `$subclip-hyperframes-map` when both styles are rejected. Do not hand-author an approximation of an explicitly selected template.

1. Read `get_current_project` and `list_editor_assets`. Preserve existing item IDs and concurrent layers. Seek to the intended insertion time and call `view_current_frame` before choosing geometry so placement is based on visible pixels, not inventory alone.
2. Read `list_runtime_layer_templates` with `kind: "remotion"`. Request source only when deliberately adapting a template.
3. For an existing item, call `get_runtime_layer` with its exact ID.
4. Read [references/official-index.md](references/official-index.md), then load the Subclip authoring contract, the curated official timing reference, and only the allowlisted topic references relevant to this component. For a non-trivial visual design, also load the two framework-neutral official HyperFrames creative references named by the index; use their visual direction without changing the requested Remotion framework. The Subclip adapter rules in this file override upstream project, Studio, package, and render instructions.
5. For each segment, author one component using [references/authoring-contract.md](references/authoring-contract.md). The source must contain one named `export default function` and no composition registration.
6. Put creator-editable data in JSON props. Call `validate_runtime_layer_source` with the full source and props; fix every error and every "Export can't draw this" warning.
7. Call `add_runtime_layer` or `update_runtime_layer`. Reserve the smallest useful Subclip rectangle with explicit geometry. Do not pass `width: 100` and `height: 100` unless the request explicitly calls for a full-frame scene or background. For an empty frame without specified geometry, use a centered contained 16:9 box: height-limited on landscape, width-limited on portrait, and aspect-preserving on square. If other content is visible, place the box in the clearest open region instead.
8. Re-list assets, seek just after entrance, at the settled state, and near exit, then call `view_current_frame`. Correct clipping, timing, opacity, hierarchy, or missing media in place.
9. Update the project director brief after verification.

Use `clone_runtime_layer` for a deliberate variation and `delete_runtime_layer` for an exact obsolete item. Splitting a Remotion placement restarts `useCurrentFrame()` from zero in the second item; create explicit props/timing when continuous internal time is required.

## snapcn templates (`snapcn-*`)

The Product demo shots are snapcn scenes (MIT). Most carry one self-contained source: the scene, the snapcn UI kit it uses (theme, fonts, color, motion, timeline helpers) and `SnapcnStage`, ending in `export default function SnapcnTemplate`. A few are bundled scenes whose source is only `<SnapcnScene scene="…" />`; for those only props can change, so choose another template when the request needs code changes.

- Scenes are designed for a 1280×720, 30fps stage. Keep `SnapcnStage` as the root: it scales and letterboxes the stage into the layer and maps the layer's frame clock to 30fps. Inside the scene use the inlined `useCurrentFrame`, `useVideoConfig` and `Sequence`, not Remotion's, or timing breaks at other project frame rates. Frame-count props (durations, delays) are in 30fps frames.
- `stageBackground` fills the layer around the stage. Set it to `transparent` for an overlay, or match the scene's own background.
- Replace built-in demo content before delivery. Defaults point at snapcn.dev and media.snapcn.dev (sample logos, avatars, photos, demo videos) and read "snapcn", "Acme" and so on. Image lists such as `images` or `DEFAULT_IMAGES` and props such as `logoSrc`, `mark` or `brandName` take project media from `list_editor_assets` or verified public HTTPS URLs. Never guess snapcn asset URLs: an image host must send CORS headers or the export draws it black.
- Extra imports these sources may use: `culori`, `class-variance-authority`, and the `@remotion/google-fonts/<Font>` modules they already import. Do not add other fonts or packages.
- After customizing, verify the settled frame and the final frame with `view_current_frame`. Many scenes resolve to a logo or headline at the end.

## Runtime and access boundary

For embedded media that genuinely belongs inside a layer, import `Video` and `Audio` from `@remotion/media`. Never author `OffthreadVideo` / `OffThreadVideo` or `OffthreadAudio` / `OffThreadAudio`, including aliases or namespace access. `OffthreadAudio` is not a supported component. Do not copy upstream server-renderer examples using these names. When revising existing code, replace legacy video usage and translate `startFrom`/`endAt` to `trimBefore`/`trimAfter`, preserving timing and volume; prefer native Media/Audio lanes whenever possible. The host's legacy video adapter exists for old projects, not as an authoring recommendation.

For Cesium maps, read [references/globe-rendering.md](references/globe-rendering.md). Surface routes use `arcHeight: 0`; the host keeps a small clearance and hides far-side geometry. Render-critical async work must use `useDelayRender()` and `useRemotionEnvironment()` from the current render context, not their global counterparts. Loading or blank pixels remain failed visual verification even when the visible player has finished loading.

- Subclip pins Remotion 4.0.530, `@remotion/three` 4.0.530, Three.js 0.181.2, MediaBunny 1.56.1, and the trusted CesiumJS runtime at 1.145.0. Do not install packages or change runtime versions from a layer.
- Imports are limited to React, Remotion, selected pinned `@remotion/*` packages including `@remotion/three`, `three`, `d3-geo`, `topojson-client`, the packaged `world-atlas/countries-50m.json` topology, and Subclip's constrained `@subclip/cesium` facade. Read the exact allowlist in the authoring contract.
- A layer has no Electron, Node, shell, filesystem, DOM-global, storage, worker, socket, or direct fetch access. Never place API keys, cookies, user credentials, system paths, or private URLs in source or props.
- Media URLs in props/literals must come from the project library after import and verification. Pass the exact URL `list_editor_assets` returns; the host stores it as `subclip-media://asset/<id>` and remaps it when the project reopens. Public HTTPS support is a runtime capability, not permission to bypass the library-first workflow. Do not invent `subclip-media:` URLs.
- The embedded layer is not a standalone Remotion project: no `<Composition>`, `registerRoot`, `staticFile`, CLI render, Studio server, or cloud renderer.
- Lottie animation data must be supplied as validated JSON props; never follow upstream examples that call `fetch()` inside the component.
- When the request supplies a public Lottie JSON URL, call `import_public_lottie_json`. It stores a checked project-local copy and returns the exact `animationData` object for item props. Pass that prop directly to `<Lottie>`; authored TSX cannot read the stored path, and a failed/404 URL must be reported rather than replaced silently.
- Supported `@remotion/effects/<effect>` and `@remotion/transitions/<presentation>` deep imports are adapted by Subclip's pinned runtime. Do not import any other subpath or package.
- For genuine 3D, read the allowlisted official `remotion-markup/3d.md` reference. Wrap the scene in `ThreeCanvas` with explicit width and height and `gl={{preserveDrawingBuffer: true}}` so still-frame export retains WebGL pixels. Include lighting, derive all animation from `useCurrentFrame()`, never import or call React Three Fiber's `useFrame()`, and give any `Sequence` inside `ThreeCanvas` `layout="none"`.
- Media, Audio, Captions, TTS, transcription, dubbing, generation, and export remain owned by their native Subclip tools unless a small visual asset is intrinsic to this component. Route globe maps through `$subclip-map-explainer`; it uses the trusted Cesium facade without exposing provider credentials. Do not emulate unavailable elevation-terrain or photorealistic flyovers.

Read [references/upstream-adaptation.md](references/upstream-adaptation.md) for retained and excluded upstream behavior. Read [references/tool-map.md](references/tool-map.md) for exact operations.

## Small source edits

Start with `get_project_outline`, then `read_layer_source` for the relevant numbered lines and `sourceHash`. Patch with `edit_layer_source` and `expectedSourceHash`; use `update_runtime_layer` for full-source replacement. Never write `layers/*`, `data/*`, or `project.json` directly. External file edits are rejected on read, so restore the saved file if that happens. Mutations return the new revision; pass it as `ifRevision` on later reads to skip unchanged data.
