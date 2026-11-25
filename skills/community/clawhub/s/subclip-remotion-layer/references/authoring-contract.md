# Remotion authoring contract in Subclip

## Component shape

Write a single named default-exported function. Subclip supplies the layer-local clock and canvas facts:

```tsx
import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';

type Props = {
  title?: string;
  accent?: string;
  layerDurationInFrames?: number;
  layerWidth?: number;
  layerHeight?: number;
  layerFps?: number;
};

export default function MetricCard({
  title = 'Launch',
  accent = '#26c9d5',
  layerDurationInFrames = 150,
}: Props) {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 18, layerDurationInFrames - 12, layerDurationInFrames - 1], [0, 1, 1, 0], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity}}>
    <div style={{padding: '36px 52px', borderRadius: 28, color: 'white', backgroundColor: accent, fontSize: 72}}>{title}</div>
  </AbsoluteFill>;
}
```

Do not include `<Composition>`, `registerRoot`, a Player, metadata calculation, or filesystem entry points. Do not import CSS files. Keep all essential styling in the component.

## Timing and animation

- Derive every animated value from `useCurrentFrame()`, the injected layer props, or `useVideoConfig()`.
- Use `interpolate`, `spring`, and `Easing`; clamp both sides when a value should stop outside its active range.
- CSS transitions, CSS animations, Tailwind animation utilities, timers, `requestAnimationFrame`, wall-clock time, and random runtime state do not render deterministically.
- The component's local frame 0 begins at the Subclip item's `startTime`. `layerDurationInFrames` is the item's duration at the project FPS.
- Keep expensive layout and generated arrays deterministic. Seed any pseudo-random pattern from stable props and calculate it without system time.

## Props and editability

Put copy, colors, counts, URLs, and design variants in the layer's JSON props. Props must be serializable, no deeper than 12 levels, and no larger than the runtime binding limit. Functions, class instances, binary blobs, and secrets do not belong in props.

The upstream Remotion `Interactive` markup convention improves Remotion Studio editing, but Subclip does not expose Remotion Studio's nested-element editor. In Subclip, manual editability is the layer's source, JSON props, timing, rectangle, fit, opacity, lane, and hierarchy. Use `Interactive` only when it materially helps component semantics, not as a promise of nested Subclip canvas controls.

## Approved imports

- `react`
- `remotion`
- `@remotion/captions`
- `@remotion/effects`
- installed `@remotion/effects/<effect-slug>` entry points
- `@remotion/gif`
- `@remotion/gsap`
- `@remotion/lottie`
- `@remotion/media`
- `@remotion/motion-blur`
- `@remotion/shapes`
- `@remotion/three`
- `@remotion/transitions`
- installed `@remotion/transitions/<presentation>` entry points
- `three`
- `d3-geo`
- `topojson-client`
- `world-atlas/countries-50m.json` for Subclip's packaged Natural Earth country topology
- `@subclip/cesium`, exposing only `CesiumRouteGlobe`

No arbitrary npm module, dynamic import, CommonJS require, `import.meta`, or user-installed package is available.

## Remotion Three.js

Use `ThreeCanvas` from `@remotion/three` for genuine 3D meshes. Pass explicit `width` and `height` and set `gl={{preserveDrawingBuffer: true}}`; otherwise the browser may discard WebGL pixels before Subclip captures a still frame. Add appropriate lights, and drive every animated transform, material, camera, or shader value from `useCurrentFrame()`. Do not import `@react-three/fiber` or use `useFrame()`; the fiber package is an internal runtime peer, not an authored-layer API. A Remotion `Sequence` nested inside `ThreeCanvas` must use `layout="none"`. Import Three.js constants or helpers from the pinned `three` package only when the declarative JSX primitives are insufficient.

## Export-safe styles

Only CSS that Remotion's client-side renderer can draw reaches the exported video. Follow [client-side-rendering.md](client-side-rendering.md): no `z-index` (order JSX back to front), no `backdrop-filter`, blend modes, radial/conic gradients, CSS background images, inset shadows, `object-position`, `perspective`, `writing-mode` or `url(#…)` CSS filters/clips/masks. Linear gradients, ordinary shadows, filter functions, clip-path shapes, transforms, `<Img>`, inline `<svg>`, `<Video>`/`<Audio>` from `@remotion/media`, `<Lottie>`, `<Gif>` and `<ThreeCanvas>` are safe.

## Assets and hierarchy

Use `Video` and `Audio` from `@remotion/media` for permitted embedded media. Do not write or import `OffthreadVideo`, `OffThreadVideo`, `OffthreadAudio`, or `OffThreadAudio`, even under another name. The audio variants are not supported exports. Migrate legacy video props `startFrom`/`endAt` to `trimBefore`/`trimAfter` and verify playback/export after replacement; old-project runtime compatibility is not permission to generate legacy components.

Import media/audio into the project library first and confirm it with `list_editor_assets`. Prefer native Media/Audio lanes. Only an intrinsic component asset should use approved Remotion media components with that exact imported asset URL supplied as a prop. Prefer `Video` from `@remotion/media` for embedded video in the browser exporter. There is no layer-local `public/` folder, so upstream `staticFile()` guidance does not apply. Keep the component background transparent for overlays; use an intentional fill only for a full-frame scene.

## Canvas-aware placement

The component's 1920×1080 local coordinate space does not imply a 100%×100% Subclip item. Before adding it, seek to the intended time and inspect the current frame. Fit a centered contained box when the frame is empty, using available height on landscape canvases and available width on portrait canvases while preserving the component aspect ratio. When existing layers occupy the frame, choose the clearest open region and size the box to that region. Full-canvas geometry is reserved for an explicitly full-frame visual. Keep transparent pixels transparent so the creator can layer and reposition the item later.

For a globe route, read `$subclip-map-explainer` and import the trusted component from `@subclip/cesium`. Authored code supplies serializable coordinates and visual/camera props only. It cannot access the raw Cesium namespace, arbitrary tile URLs, provider tokens, or Cesium's asset loader. True elevation-terrain or photorealistic flyovers are not available in the layer runtime.

Use `arcHeight: 0` for normal surface routes; raised arcs are opt-in and may be visible above the horizon. Keep globe depth testing enabled. Read [globe-rendering.md](globe-rendering.md) for sampling and capture readiness. In asynchronous React code, obtain `delayRender`, `continueRender`, and `cancelRender` from `useDelayRender()`, and use `useRemotionEnvironment()` for the active capture context. A global delay handle does not block `renderStillOnWeb`'s scoped render. Release readiness only after the ready UI commits and render-critical assets/canvas drawing finish, and release each abandoned task's own handle during cleanup.

Lottie animation JSON must arrive as a validated prop and be passed directly to `<Lottie animationData={...} />`; direct `fetch()` is unavailable. For a public Lottie JSON URL, use `import_public_lottie_json` first. It saves a checked project-local copy and returns the exact object to place in props. Do not use `useState()`/`useEffect()` as a network loader, and do not try to read the project-local file from authored TSX. Primary footage, B-roll, narration, music, SFX, captions, TTS, and generated media belong in native Subclip layers and operations. Use framework media only when a small visual asset is inseparable from the component, and import it into the project library before binding its URL. Verify fonts and external dependencies in both preview and export as required by the skill; installing or downloading a file in the agent environment does not make it accessible here.

No source or props may contain credential-shaped keys such as `apiKey`, `token`, `authorization`, `cookie`, `password`, `secret`, `sessionToken`, or signatures. Signed URLs and literal bearer/provider credentials are rejected.

Subclip `layerOrder` controls hierarchy across panel types, `zIndex` and lane control overlapping peers, and internal React/CSS stacking controls only this component's children. Validate before persisting and inspect rendered pixels afterward.

## Remotion 4.0.530 guidance

- Give independently editable scenes/layers separate JSX nodes and serializable props. Keep frame-derived effect parameters close to their JSX usage. Studio-only interactivity guidance does not enable nested Subclip controls.
- Use `lightLeak` from `@remotion/effects/light-leak` on a transparent `Solid`. Animate progress from 0 to 1 over the effect window; seed selects the pattern and hueShift selects the color (0 warm; verify the hue visually in the pinned runtime). Read the allowlisted `remotion-markup/light-leaks.md` reference. Dependencies and export WebGL configuration are already owned by Subclip; skip its CLI setup instructions.
- In 4.0.530, `durationInFrames` is measured before `playbackRate` is applied. A 60-frame Sequence at playbackRate 2 occupies 30 composition frames. Keep the native timeline item duration in project time; avoid applying speed twice when embedding a trimmed asset. Sequence `loop` repeats its local content; do not use it to extend native source clips implicitly.
- Preserve the sandbox, verified/downloaded fonts/resources, library imports, native media/audio lanes, and prohibition on OffthreadVideo/OffthreadAudio described above when adapting upstream examples.
