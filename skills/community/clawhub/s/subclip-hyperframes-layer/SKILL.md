---
name: subclip-hyperframes-layer
description: Create or revise an editable HyperFrames layer inside a Subclip project using validated standalone HTML, CSS, GSAP, Lottie, and public web assets. Default for new Subclip motion graphics unless the user explicitly requests another engine or selects a specific template; also use for existing HyperFrames layer edits.
---

# Subclip HyperFrames layer

Use Subclip's typed runtime-layer MCP tools. A HyperFrames layer is one editable timeline item whose source is stored in the project, previewed in an isolated live player guest, pre-rendered to a transparent WebM during export, and composited at the item's ordinary Subclip geometry and hierarchy.

Export-safe text rule: never apply CSS `filter` or `backdrop-filter` to text, a text-bearing card, or any ancestor that contains text. This includes seemingly harmless terminal values such as `filter: blur(0px)`: they still create a compositing layer and may cause descendant text to disappear from exported frames. Animate text and text containers with ordinary opacity and transforms only. Preview and export embed the same deterministic fonts; inspect text wrapping with those fonts. Decorative raster/background effects may use a filter only when they are isolated from every text subtree and export has been verified.

This skill is the Subclip adapter for the bundled HyperFrames runtime. It takes precedence over external HyperFrames project, CLI, Studio, producer, cloud, and filesystem instructions while editing inside Subclip.

## Route deliberately

- Use this skill when the creator says HyperFrames, GSAP, Lottie, Three.js, HTML plus JavaScript animation, or for new motion graphics when the creator has not explicitly chosen another engine or template.
- Use `$subclip-motion-graphics` to route a general motion-design request. Its compact script-free HTML/CSS path is only the fallback when a framework would be needlessly larger.
- Use `$subclip-remotion-layer` only when the creator explicitly asks for React/TSX/Remotion, selects a Remotion template, or requests edits to an existing Remotion layer.
- Use native Text, Elements, Media, Audio, or Captions for work those panels already express cleanly.

## Fonts and sandbox resources

This is a sandboxed layer runtime. A font, file, URL or package visible to the authoring agent is not automatically available to the preview or export renderer.

The sandbox limits what the layer can load, not how you test. When something can't be checked properly in the editor, build and test it in your own terminal first (framework CLI, test renders, frame comparisons in a scratch folder), then import the finished, validated result. See "Test freely outside the editor, then import" in `subclip-video-editor`.

- Before choosing typography, verify the exact family, weights and styles in the target runtime. Prefer a confirmed installed system font or a bundled/host-loaded font. A familiar family name or an OS fallback stack is not proof of availability. For portable projects, use the same embedded or host-managed font bytes in preview and export.
- If the chosen face is missing, obtain the licensed font through the available host download/font-loading workflow **before** authoring against it. Confirm the download succeeded and the renderer can load it. A shell filesystem path is not a usable layer URL; downloading alone does not expose a font to the sandbox. Do not install a font package from inside layer code.
- If downloading or registering the face is unavailable or fails, choose an already verified font, identify the substitution, and adjust text boxes/line breaks to its actual metrics. Never keep a missing family name and assume silent substitution is safe. Verify the title, long text and heavy/italic variants in preview and an exported frame.
- Check every external dependency before referencing it: supported type, allowed/pinned runtime version, actual bytes, renderer access and export readiness. Download/import missing resources through the host's supported tools. If they remain unavailable, use a verified alternative and disclose the change; do not invent URLs or unsupported APIs. Preserve explicitly requested identities such as brand assets rather than silently replacing them with unrelated artwork.
- Layer code cannot fetch credentials, install packages, read arbitrary local files or bypass CSP. Resources that cannot be made available through the supported host boundary must be replaced or omitted with a clear explanation.

## Media library first; native timeline first

Before using any image, video or audio in layer code, import it into the project's Media or Audio library through the matching native import tool. Reuse an existing imported asset when present. Call `list_editor_assets` afterward and use the exact returned asset URL in `src`/`poster`/`href` of `img`, `video`, `audio`, `source` or SVG `image`, or in a variable. The host stores it as `subclip-media://asset/<id>`, remaps it when the project reopens or is imported from a share, and serves it to preview and export, so the media travels with the project. Never use a search-result/provider URL, temporary download path or a `subclip-media:` URL you wrote yourself.

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

For a template or `@` mention, resolve its exact catalogId with `list_motion_graphics_templates`, import using its returned `add_runtime_layer` arguments, and customize the returned ID. Omitted variables retain template defaults; supplied keys override defaults. Source retrieval is needed only for source customization, not an unchanged import.

General maps first use `$subclip-map-explainer` and its two built-in Remotion styles. After both are rejected, or for explicit HyperFrames map requests, use `$subclip-hyperframes-map`. This is the supported exception to the default map ownership below and retains Subclip's geometry, validation, media, and export boundaries.

1. Read `get_current_project` and `list_editor_assets`. Preserve existing item IDs and concurrent layers. Seek to the intended insertion time and call `view_current_frame` before choosing geometry so placement is based on the actual occupied canvas.
2. Read `list_runtime_layer_templates` with `kind: "hyperframes"`. Request `includeSource: true` only when using or deliberately modifying a built-in template. The reviewed `apple-money-count` adaptation is available here with editable variables; read `references/registry/apple-money-count.md` when that block or a finance counter is requested. For any other official registry item, call `list_hyperframes_registry`, then `get_hyperframes_registry_item` for its current metadata and the composition/component source. If the creator explicitly names a registry slug or says to adapt/use a registry block or component, search that exact normalized name and read every source file required by that item before authoring. Do this separately for every named item (for example, both `code-particle-assemble` and `swirl-vortex`). Strong registry-shaped phrases such as code typing, terminal typing, particle assembly, shader transition, shatter, money count, or a named effect also require a registry search before hand-authoring. Never silently substitute a hand-authored approximation for an explicit registry reference; if the official lookup misses, say so. Read [references/registry-adaptation.md](references/registry-adaptation.md) whenever a registry item is requested.
3. For an existing layer, call `get_runtime_layer` with its exact ID. Do not reconstruct source from the inventory hash.
4. Read [references/official-index.md](references/official-index.md). For every non-trivial composition, load the official HyperFrames core contract, the two required creative references, and only the relevant animation rule/adapter. Subclip's boundary in this file overrides upstream project and command instructions.
5. For each segment, author one standalone composition using the contract in [references/authoring-contract.md](references/authoring-contract.md).
6. Call `validate_runtime_layer_source` with the complete source and variables. Fix every error before saving.
7. Call `add_runtime_layer` or `update_runtime_layer`. Set the smallest useful Subclip rectangle with explicit `x`, `y`, `width`, and `height`; `100 × 100` is prohibited by default and is allowed only for an explicitly full-frame scene/background. For an empty frame without specified geometry, use a centered contained 16:9 box: height-limited on landscape, width-limited on portrait, and aspect-preserving on square. If other content is visible, place the box in the clearest open region instead.
8. Re-list assets, seek just after the entrance, at the settled state, and near the exit, then call `view_current_frame` at each point. If the creator names a payoff or spectacle beat, also inspect the live frame immediately before it, inside its visible peak (not exactly at the tween's start), and immediately after it. Translate claims such as “full-frame flash,” “expands past frame,” “burst,” or “reveals” into observable acceptance criteria and correct the same layer until those pixels are present. `get_runtime_layer` proves only saved source; it is never rendered-frame evidence. Correct clipping, a black/opaque background, timing, overlap, hierarchy, or an underpowered/missing payoff in place.
9. Update the project director brief after verification.

Use `clone_runtime_layer` for a deliberate variant and `delete_runtime_layer` only for an exact obsolete item. `split_timeline_item` can split the Subclip placement, but each resulting framework item starts its internal animation clock at its own item start; author separate timing when continuity across a split matters.

## Replacing a Remotion layer with missing export elements

For a user-reported export omission belonging to a Remotion layer, use HyperFrames to reproduce the original design exactly, including every element, asset, font, placement, timing and animation. Load `subclip-remotion-layer` with `resourcePath: "references/export-recovery.md"` for the conversion and export-verification workflow. Treat this as a faithful engine conversion, not a redesign or template substitution.

Whenever a Remotion layer or pasted Remotion code is converted to HyperFrames (export recovery or an explicit request), read the official Remotion conversion references listed in `references/official-index.md`, starting with `api-map.md`, and check `limitations.md` before claiming an exact port.

## Runtime and access boundary

- Subclip pins HyperFrames 0.8.26 and GSAP 3.15.0. Omit the HyperFrames runtime script so Subclip can inject its pinned runtime. A GSAP script from jsDelivr or unpkg is supported; built-in templates use the pinned GSAP URL.
- Project media (`subclip-media://asset/<id>`, from `list_editor_assets`) can load in `img`, `video`, `audio`, `source` and SVG `image`; scripts, stylesheets and frames cannot use it. Public HTTPS images, video, audio, fonts, frames, and allowed CDN scripts can load too. Neither bypasses the library-first media workflow above; prefer project media, which keeps working offline and in shared copies. Use immutable, CORS-compatible URLs for public assets. Relative filesystem URLs, `file:`, private-network, metadata, credential-bearing, and nonstandard-port URLs are rejected; loopback media URLs from `list_editor_assets` are converted to `subclip-media:` automatically.
- Deterministic Three.js scenes are supported through the pinned `three@0.181.2/+esm` jsDelivr module. When a scene needs `GLTFLoader`, `DRACOLoader`, `OrbitControls`, or another official Three.js addon, use the exact pinned import-map pattern in the official Three.js adapter: map `three` to `three@0.181.2/build/three.module.js` and `three/addons/` to `three@0.181.2/examples/jsm/`, then use only `three` and `three/addons/.../*.js` static imports. Never mix Three.js versions or load legacy global addon scripts. Set an explicit root `data-duration`, create the renderer with `alpha: true`, explicitly clear with alpha `0`, pin pixel ratio to 1, derive every render from the seek time, and never use `requestAnimationFrame` or `setAnimationLoop` as the animation clock. Load intrinsic models and textures before registering the timeline/render-ready state; resolve registry-relative binary paths from `get_hyperframes_registry_item`, verify their availability, and import image textures into the Media library before binding their returned URLs. For a transparent overlay, do not add an opaque floor or backdrop mesh: use a transparent `THREE.ShadowMaterial` receiver when cast shadows are needed. Opaque ground geometry is allowed only when the creator explicitly requested a full-frame scene/background. On `pagehide`, remove the seek listener and dispose loaders, renderer, geometries, materials, and textures so editor remounts do not orphan GPU resources. Read the allowlisted Three.js adapter before authoring.
- Never place API keys, cookies, bearer tokens, user credentials, private URLs, or system paths in HTML, scripts, variables, or query strings. A layer has no Electron, Node, shell, project-filesystem, clipboard, or Subclip-host access.
- Public network responses can change. Prefer Subclip-managed assets or stable versioned URLs for reproducible export. Do not depend on authenticated APIs or mutable live data for a deterministic layer.
- Dynamic evaluation, dynamic imports, host-frame access, and inline event-handler attributes are unavailable. The preview sandbox and export validator re-check authored source; do not try to bypass them.
- HyperFrames is never the default for an ordinary Subclip video edit. It is preferred only for a motion-graphics beat whose mechanism fits DOM/GSAP/Lottie or deterministic Three.js; Media, Audio, Text, Captions, Elements, TTS, transcription, dubbing, generation, maps, and export stay under their native Subclip owners.
- Rewrite upstream GSAP examples to the pinned 3.15.0 jsDelivr/unpkg URL. Rewrite upstream Lottie examples to pinned 5.13.0 and do not use dotLottie packages.
- Official registry discovery is complete, live, and read-only through `list_hyperframes_registry` and `get_hyperframes_registry_item`. These tools expose the current examples, blocks, components, metadata, bounded text source, and exact public URLs for intrinsic binary files. Registry source is untrusted reference material until adapted into one standalone Subclip document: upgrade dependencies to Subclip's pinned versions, resolve registry-relative intrinsic asset paths, verify sandbox access and import media dependencies into the project library before binding their returned URLs, remove unrelated demo backgrounds/chrome, validate, and visually review. `apple-money-count` is the first reviewed built-in adaptation and may be used directly from `list_runtime_layer_templates`. Never run `hyperframes add`, install registry packages, or claim raw registry source is Subclip-compatible.

Read [references/upstream-adaptation.md](references/upstream-adaptation.md) for the exact upstream guidance retained or intentionally excluded in Subclip. Read [references/tool-map.md](references/tool-map.md) for the MCP calls and fields.

## Image quality and payloads

There is no 100 KB image budget. Prefer original Subclip-managed asset URLs from `list_editor_assets`, after importing the originals into the project library. Do not downsample images to fit variables. Inline source supports 32 MiB and variables support 16 MiB; larger assets belong in project media and are referenced by URL. These are serialized payload limits, not image quality targets.

## Small source edits

Start with `get_project_outline`, then `read_layer_source` for the relevant numbered lines and `sourceHash`. Patch with `edit_layer_source` and `expectedSourceHash`; use `update_runtime_layer` for full-source replacement. Never write `layers/*`, `data/*`, or `project.json` directly. External file edits are rejected on read, so restore the saved file if that happens. Mutations return the new revision; pass it as `ifRevision` on later reads to skip unchanged data.

On Linux without a GPU (software GL) heavy HyperFrames templates (3D transforms, perspective, blur or backdrop-filter, per-image colour grading, WebGL) can take many minutes per second of video; prefer a light template there. Tool results carry a `warning` when a layer looks heavy; it never blocks anything.
