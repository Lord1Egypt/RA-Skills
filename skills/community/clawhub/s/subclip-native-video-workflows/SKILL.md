---
name: subclip-native-video-workflows
description: Create complete prompt-led videos in Subclip using native Media, Text, Captions, Audio, Elements, plus editable Remotion, HyperFrames, or compact HTML/CSS motion layers. Use for product/site launches, explainers, PR reveals, talking-head packages, music edits, presentation-style videos, and catalog motion recipes.
---

# Subclip native video workflows

Turn ambitious video prompts into editable Subclip timelines. Native Media, Audio, Text, Captions, and Elements keep ownership of ordinary editing. For motion-design beats, use `$subclip-motion-graphics`, which builds scenes in HyperFrames by default (creators can click into them to edit text and shapes), uses Remotion only when requested or when editing an existing Remotion layer, and keeps script-free HTML/CSS for one small standalone effect, never for a video's scenes. Never scaffold an external HyperFrames or Remotion project.

## Native ownership

- MediaPanel owns raster screenshots, video, photos, cutouts, raster maps, and generated visual assets. It does not own standalone `.svg` files.
- TextPanel owns ordinary titles, labels, lower thirds, and CTA copy. Keep them static in ordinary editing unless the creator asks for animation. Native Text keyframes are allowed when the request explicitly asks for text motion or when coordinated text motion is intrinsic to a prompt-led motion-graphics video; this permission does not require every Text layer to animate.
- Captions owns transcript-derived subtitles and speaker styling.
- AudioPanel owns music, narration, SFX, fades, volume, trim, and loop state.
- ElementsPanel owns shapes, lines, arrows, highlights, backgrounds, blur, texture, and primitive keyframed effects.
- The unified Motion graphics panel owns three independent layer types: HyperFrames (the default for scenes) for seekable DOM/GSAP/Lottie scenes, Remotion for requested frame-driven React scenes, and script-free HTML/CSS for one small standalone effect or exact sanitized inline SVG artwork.

Read [references/workflows.md](references/workflows.md) for route-specific decisions. Read [references/prompt-library.md](references/prompt-library.md) when the user names a catalog pattern or asks for ideas/examples.

## Shared production contract

1. Inspect the active project and route every requested element to its native owner before mutating.
2. For a public product URL, call `inspect_public_website` directly before searching connected services. It renders the real page and returns verified visible copy, computed colors, font families, typography samples, logo candidates, image candidates, and project-local PNGs in `screenshotPaths` and `logoAssetPaths`. Summarize those verified brand findings before editing. Import raster screenshots/logo captures with `import_generated_media_to_timeline`. When the creator supplies an official SVG or a verified logo candidate points to one, read that exact SVG once, sanitize it under `$subclip-motion-graphics`, and inline it in a tightly bounded Motion item; do not convert it to PNG or leave a remote URL in Motion HTML. Only stop when the named scanner itself returns a concrete capture failure—never claim it is unavailable without calling it.
3. For a GitHub PR URL, call `fetch_public_github_pull_request` first. Then discover connected GitHub tools and use `mcp_remote__call_read_tool` for authenticated/private context, commits, files, or diff cross-checks. Lead with the user benefit, then show only the minimum code evidence.
4. Build the timeline with named native tools. Use one focal action per beat, restrained support motion, and at most one deliberately exaggerated spectacle beat unless the user asks for more.
5. Before creating any motion layer, inspect the canvas during that beat and reserve the smallest useful item rectangle using explicit center `x/y` and canvas-relative `width/height`. Use a full-canvas item only for an intentional full-frame scene or background.
6. Follow the selected framework adapter. Remotion animation is frame-derived; HyperFrames uses one finite seekable timeline; HTML/CSS fallback remains deterministic and script-free.
7. Keep each layer independently editable. Do not bake captions, ordinary text, audio, or replaceable raster media into Motion HTML merely for convenience. An exact sanitized SVG is the deliberate exception because standalone SVG is represented as editable Motion markup rather than MediaPanel media.
8. Verify entrances, landings, cuts, and exits with live frame inspection. Check text wrapping, safe margins, contrast, source accuracy, and intentional project duration. Update existing item IDs instead of stacking corrections.

## Capability honesty

- A “presentation” is a slide-style video timeline, not an interactive deck.
- True editable 3D/WebGL device work belongs to Subclip's native 3D panel and `$subclip-3d-mockup`; never embed it in Motion HTML. Use CSS perspective only for deliberately flat card or interface treatments.
- Audio-reactive graphics require actual analysis data. Without it, create a deterministic beat/BPM-matched visual and describe it accurately.
- MP4/H.264 does not preserve alpha. Use the named WebM/VP9, MKV/VP9, or MOV/ProRes 4444 export options when transparent delivery is explicitly required.
- Accurate maps require an authoritative map asset or geometry source. Never present invented continent paths as geographic data.
- Route flat maps to `$subclip-map-route`; call `create_route_map_geometry` before editing and require its familiar standard-map orientation, shared camera/world wrapper, and one-subpath continuous route. Route explicit globes and orbital journeys to `$subclip-map-explainer`. Do not fake elevation-terrain or photorealistic geographic flyovers; they remain unavailable until Subclip exposes a managed provider and credential broker.
