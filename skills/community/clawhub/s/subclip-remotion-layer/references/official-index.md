# Official Remotion skill snapshot

Installed from the Remotion-maintained `remotion-dev/skills` repository at commit `a1b09e904a995f8bbf6d3b865fc612eedf7a4c43` on 2026-09-30 as a vendored snapshot. The snapshot identifies itself as Remotion 4.0.530.

The upstream files are adapted for the Subclip sandbox under `references/official/remotion-best-practices/`. Only the curated markup/topic paths listed here and accepted by `read_subclip_skill` are readable. Project creation, Studio, renderer, SaaS/cloud, upgrade, maps, direct provider voiceover, audio/SFX, FFmpeg, package-install, local-font and unsupported-runtime references are intentionally blocked. The remaining files are reference material for one embedded Subclip component; Subclip's adapter and validator remain authoritative.

## Required reading

Read these with `read_subclip_skill` using `skillName: "subclip-remotion-layer"`:

1. [references/authoring-contract.md](authoring-contract.md), which replaces the upstream top-level markup router inside Subclip.
2. [references/client-side-rendering.md](client-side-rendering.md): the CSS and components the export renderer can draw. It overrides any upstream example that uses `z-index`, blend modes, `backdrop-filter`, radial gradients or CSS background images.
3. `references/official/remotion-best-practices/remotion-markup/timing.md` for every animated component.
4. Only the allowlisted topic references needed by the component. If `read_subclip_skill` rejects a path, that upstream capability is deliberately incompatible with the embedded layer.

The official Remotion skills deliberately focus on implementation rather than prescribing a design style. For a non-trivial visual, additionally call `read_subclip_skill` for `skillName: "subclip-hyperframes-layer"` and read:

- `references/official/hyperframes-creative/references/house-style.md`
- `references/official/hyperframes-creative/references/video-composition.md`

Use those two as framework-neutral composition and visual-quality guidance only. Continue authoring React/TSX and follow every Remotion/Subclip runtime constraint.

## Compatible topic routes

| Need | Official resource |
| --- | --- |
| Timing and easing | `remotion-markup/timing.md` |
| Sequencing | `remotion-markup/sequencing.md` |
| Transitions | `remotion-markup/transitions.md` |
| Text highlights | `remotion-markup/text-highlights.md` |
| Images | `remotion-markup/images.md` |
| Video embedding | `remotion-markup/embedding-videos.md` |
| Cropping | `remotion-markup/cropping.md` |
| GIFs | `remotion-markup/gifs.md` |
| Lottie | `remotion-markup/lottie.md` |
| Three.js / React Three Fiber | `remotion-markup/3d.md` |
| Light leak overlays | `remotion-markup/light-leaks.md` |
| Motion blur | `remotion-markup/motion-blur.md` |
| Native voiceover routing | `remotion-markup/voiceover.md` |
| Supported visual effects | `remotion-markup/effects.md` |
| Measuring text/layout | `remotion-markup/measuring-text.md` and `measuring-dom-nodes.md` |
| Multi-scene internal composition | `remotion-markup/multi-scene-video.md` |

Every path in the table is relative to `references/official/remotion-best-practices/`.

## Subclip compatibility overrides

- Never follow `remotion-create`, `remotion-studio`, `remotion-render`, `remotion-saas`, `remotion-upgrade`, CLI, server, Lambda, Cloudflare, package-install, or project-scaffolding instructions for an embedded layer.
- Ignore `staticFile()`, `public/`, local-font, FFmpeg-shell, and arbitrary package guidance. Use Subclip-managed/public HTTPS inputs and only the imports accepted by `validate_runtime_layer_source`.
- Remotion Studio's `Interactive` conventions do not create nested Subclip canvas controls. The Subclip item remains editable through source, JSON props, time, geometry, fit, opacity, lane, and hierarchy.
- Route ordinary project audio, SFX, captions, voiceover, and media editing to Subclip's native panels. Use corresponding Remotion markup only when the creator explicitly wants it inside this component and validation accepts it.
- `@remotion/three` and the pinned `three` package are available for deterministic React Three Fiber scenes through `ThreeCanvas`; `@react-three/fiber` imports and `useFrame()` remain unavailable. Raw map SDKs, external font packages, arbitrary npm libraries, direct fetch, Node, Electron, and filesystem APIs are unavailable in the current embedded layer. Cesium routes are the exception only through Subclip's constrained `@subclip/cesium` facade and the dedicated `$subclip-map-explainer` skill. Elevation-terrain and photorealistic flyovers are not exposed.
- Rewrite Lottie examples so animation JSON comes through props rather than `fetch()`. Supported effects and transition presentation deep imports are bundled by Subclip; other deep imports remain unavailable.

The included `REMOTION-LICENSE.md` mirrors the license shipped with the installed Remotion 4.0.530 package. Organizations must satisfy Remotion's applicable licensing terms.
