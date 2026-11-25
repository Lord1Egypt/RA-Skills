# Upstream HyperFrames adaptation

Adapted against the installed HyperFrames 0.8.26 runtime and the official skill snapshot recorded in [official-index.md](official-index.md). The official source is bundled under `references/official/` so the assistant can load exact design and animation guidance on demand.

Retained inside Subclip:

- standalone composition roots with explicit dimensions and duration;
- one paused, registered, seekable timeline;
- deterministic animation and media ownership rules;
- finite GSAP choreography, deterministic Three.js `hf-seek` rendering, transparent output, and frame inspection;
- public web assets and pinned runtime URLs subject to Subclip validation.

Replaced by Subclip-native operations:

- project scaffolding, folders, `index.html` writes, open-ended registry installation, and CLI commands;
- HyperFrames Studio timeline/project management;
- direct producer, cloud, Lambda, or command-line rendering;
- standalone output delivery and producer cache management.

Subclip stores source inside one timeline item, owns item timing/geometry/hierarchy, validates source at every execution boundary, renders a transparent WebM proxy during export, and composites it through the normal media pipeline. Therefore external instructions to run `init`, `add`, `catalog`, `preview`, `check`, `snapshot`, or `render` do not apply to an in-app layer.

Subclip conflict decisions:

- HyperFrames is not the default for every video. Native Subclip panels remain the default owners; HyperFrames is the default for new motion graphics unless the user explicitly chooses another engine or template. Preserve the engine of an existing layer during edits.
- Never run upstream project initialization, validation, preview, render, producer, publish, registry-install, or package-install commands. Use Subclip's runtime-layer validation, preview, frame inspection, and export tools. Discover the complete current official catalog through `list_hyperframes_registry` and read exact metadata/source through `get_hyperframes_registry_item`; treat it as reference until adapted and validated. Reviewed registry adaptations such as `apple-money-count` are available through `list_runtime_layer_templates`.
- Never use upstream HeyGen generation/translation helpers, HyperFrames transcription, Kokoro/other TTS, or media preprocessing. Route generation and dubbing to `$subclip-ai-generation`/`$subclip-dubbing`, transcription to `transcribe_project`, and narration to `$subclip-tts` plus `list_ai_models`, `list_ai_voices`, and `generate_speech`.
- Verify exact system/bundled/host-loaded font faces in the target renderer. If absent, download and register a licensed face through supported host tools before use; if that fails, use a verified available alternative. Do not run upstream font-discovery/install scripts inside the sandbox or assume a fallback stack preserves layout.
- Three.js is limited to version `0.181.2` with time-driven `hf-seek` rendering. Base-only scenes use the pinned `+esm` module; official Three.js addons use only the pinned `three`/`three/addons/` import-map pattern from the bundled adapter. Legacy global addon scripts, version mixing, arbitrary import-map packages, Anime.js, dotLottie, TypeGPU/WebGPU, and unlisted runtimes remain unavailable. Intrinsic registry GLTF may use the exact public HTTPS file URL returned by the registry tool after checking sandbox/export access; relative registry paths remain unavailable. Image textures still follow the Media-library import requirement before their URLs are bound.
- Translate GSAP 3.14.2 examples to pinned 3.15.0. Translate compatible Lottie examples to pinned 5.13.0 from jsDelivr/unpkg; do not preserve unpinned or cdnjs runtime URLs.
- Primary footage, B-roll, narration, music, SFX, captions, and generated assets remain native layers. A framework media URL is only for a small asset intrinsic to the composition, after library import and playback/export verification.

- New background music and soundtracks use `$subclip-music-generation` and `generate_music`; sung lyrics also use `$subclip-songwriting`. This overrides upstream music-generation helpers or direct provider workflows. Import completed operations through `import_ai_operation_to_timeline` into native Audio lanes when requested.
