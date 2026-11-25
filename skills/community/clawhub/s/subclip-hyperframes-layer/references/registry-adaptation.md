# Adapting an official registry item

Use this contract when the creator names a HyperFrames registry block/component or asks for a move that strongly matches one.

## Read the implementation, not only the card

1. Search each exact slug separately with `list_hyperframes_registry`.
2. Call `get_hyperframes_registry_item` for every match with `includeSources: true`, or request every composition/component path listed by its metadata. Binary files are intentionally not copied into assistant context, but each returned file entry includes its exact official public URL; preserve that URL for intrinsic GLTF, texture, shader, or data assets needed by the block.
3. Identify the item's signature mechanism, inputs, runtime, deterministic clock, dependencies, and visible payoff before writing Subclip source.
4. Adapt that mechanism into one validated standalone Subclip document. Registry blocks are often gallery demonstrations: remove prompt labels, blueprint grids, catalog chrome, and unrelated demo backgrounds, but retain the actual shader, particle system, transition, or effect engine the creator requested.
5. Retarget copy, colors, timing, scene textures, and local geometry to the creator's brief. Use Subclip's pinned dependency URLs and runtime contract. Replace registry-relative binary paths with the exact HTTPS URLs returned by the registry tool. For Three.js addons, convert legacy global scripts to the pinned import-map form documented in the authoring contract and load all render-critical assets before registering readiness. If the signature mechanism cannot be supported, say that before choosing a different implementation; never claim the registry item was used when only its appearance was approximated.

## Fidelity checks

- Treat nouns in the registry description as acceptance criteria. A GPU particle block must remain a GPU particle system; a shader transition must remain a shader transition; a shatter block must produce fragments rather than a scale/fade.
- Preserve quantitative requirements from the request. For “about 1200 seeded particles,” create at least that deterministic particle count and verify visible convergence. For motion trails and bloom, verify both as pixels at the effect's peak rather than merely declaring variables for them.
- A transition requires visible outgoing and incoming states. Because a HyperFrames layer cannot sample arbitrary Subclip layers behind its iframe, put both transition states inside the same standalone layer unless the requested source is already available through supported composition media.
- Full-frame shader transitions are valid full-canvas exceptions. Partial overlays and logo lockups should remain contained and transparent unless the creator explicitly requests a background.
- Inspect frames before, during, and after every named mechanism. Compare the visible mechanism with the registry metadata/preview and correct the same layer when the signature effect is missing, flattened, obscured by demo chrome, or reduced to boxes and fades.

## Named examples

- `code-particle-assemble`: sample the requested glyph/wordmark pixels, drive seeded WebGL/GPU points from scattered positions to those targets, and preserve readable final contours. DOM spans or a simple opacity reveal are not equivalent.
- `swirl-vortex`: render a genuine WebGL shader transition between two scene textures with time-driven vortex distortion. A CSS rotation, blur, wipe, or static background is not equivalent.
