# Upstream Remotion adaptation

Adapted against Remotion 4.0.530 and the official skill snapshot recorded in [official-index.md](official-index.md). The sandbox-adapted official source is bundled under `references/official/remotion-best-practices/` so the assistant can load exact authoring references on demand.

Retained inside Subclip:

- React/TSX markup and typed serializable props;
- `useCurrentFrame()`, `useVideoConfig()`, `interpolate()`, springs, easing, sequences, shapes, effects, Lottie, captions, and `Video`/`Audio` from `@remotion/media` for embedded media; replace upstream `OffthreadVideo` examples and never invent `OffthreadAudio` (including `OffThread*` spellings);
- frame-derived deterministic animation and rendered-frame review;
- public HTTPS media inputs subject to Subclip's runtime boundary.

Replaced or excluded inside a Subclip layer:

- project creation, package managers, package-installation commands, arbitrary npm imports, and public-folder assets;
- `<Composition>`, `registerRoot`, metadata registration, entry files, and Studio project setup;
- Remotion CLI, Player orchestration, server renderer, Lambda, cloud deployment, and output configuration;
- Node, FFmpeg shell workflows, filesystem access, direct network fetching, environment variables, and secret-bearing APIs;
- the assumption that `Interactive` exposes nested Subclip canvas controls.

Subclip owns the surrounding composition, project FPS, item duration, placement, preview, and export. The layer source owns only its internal React scene. Use Subclip's MCP tools for media import, timing, project export, and visual verification.

Subclip conflict decisions:

- Do not run standalone Remotion CLI commands, Studio, Player orchestration, server/Lambda/Cloudflare rendering, package installation, dependency upgrades, FFmpeg commands, or project scaffolding.
- Only pinned imports accepted by `validate_runtime_layer_source` exist. Supported `@remotion/effects/<effect>` imports resolve through the pinned effects namespace; supported `@remotion/transitions/<presentation>` modules are bundled explicitly.
- Lottie JSON must be supplied through validated props. Direct `fetch()` inside the component is rejected.
- `public/`, `staticFile()`, local font packages, `@remotion/google-fonts`, arbitrary media utilities, `@remotion/sfx`, `zod`, direct MediaBunny, and raw map SDKs are unavailable to authored layers. `@remotion/three` and `three` are the deliberate 3D exceptions: use `ThreeCanvas`, frame-driven animation, no `useFrame()`, and `layout="none"` for nested Sequences. Cesium is available only through the constrained `@subclip/cesium` facade.
- Route flat maps to `$subclip-map-route` and globe explainers to `$subclip-map-explainer`. Elevation-terrain and photorealistic geographic flyovers remain unavailable until Subclip exposes a managed provider and credential broker. Route narration to `$subclip-tts`; route transcription, dubbing, generated media, SFX, primary media and export to their native Subclip tools.
- Primary footage, B-roll, narration, music, SFX, captions, and generated assets remain native layers. A Remotion media element is only for a small visual asset intrinsic to the component.

- New background music and soundtracks use `$subclip-music-generation` and `generate_music`; sung lyrics also use `$subclip-songwriting`. This overrides upstream music-generation helpers or direct provider workflows. Import completed operations through `import_ai_operation_to_timeline` into native Audio lanes when requested.
