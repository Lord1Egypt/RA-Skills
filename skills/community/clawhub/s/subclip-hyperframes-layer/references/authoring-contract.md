# HyperFrames authoring contract in Subclip

## Standalone document

Store one complete HTML document. Put one visible composition root directly in `body`; do not wrap it in `template`.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <style>
      html, body { margin: 0; width: 100%; height: 100%; overflow: hidden; background: transparent; }
      #scene { position: relative; width: 1920px; height: 1080px; overflow: hidden; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
  </head>
  <body>
    <div id="scene" data-composition-id="scene" data-start="0" data-duration="5" data-width="1920" data-height="1080">
      <div class="card">A seekable scene</div>
    </div>
    <script>
      const timeline = gsap.timeline({paused: true});
      timeline.fromTo('.card', {opacity: 0, y: 48}, {opacity: 1, y: 0, duration: 0.7, ease: 'power3.out'});
      window.__timelines['scene'] = timeline;
    </script>
  </body>
</html>
```

The root needs fixed pixel dimensions that match `data-width` and `data-height`. Keep every ancestor of a percentage-height child explicitly sized. The Subclip item rectangle independently controls placement and scaling on the project canvas.

That fixed local root is not permission to create a full-canvas Subclip item. Seek and inspect the intended frame before adding the layer. Use the smallest useful transparent item rectangle, fit it by height on landscape canvases or width on portrait canvases when centered, and move it into a clear open region when concurrent layers exist. Use full-canvas geometry only for an explicitly full-frame scene or background.

## Timing

- Register exactly one paused GSAP timeline under the same key as `data-composition-id`.
- The Subclip item's `startTime` and `endTime` define when the layer exists in the project. `data-duration` defines its internal authored clock and should match the intended item duration; export normalizes it to the item duration.
- Use finite, seekable animation. No infinite repeats, wall-clock timers, `Date.now()`, `performance.now()`, unseeded randomness, or input-dependent state.
- Use GSAP `x`, `y`, `scale`, and `rotation` for spatial motion. Prefer `fromTo` when an element has an authored initial transform. Do not fight a CSS transform with a GSAP tween of the same property.
- Keep layout stable while seeking. Precompute constants; do not measure geometry inside a tween or frame callback.
- Use `autoAlpha` or explicit opacity for visual entrances. Do not animate `display` or take ownership of framework clip visibility.

## Payoff and spectacle beats

Treat an explicitly requested payoff or spectacle beat as a measurable requirement, not general art direction. Write down what must be visible at its peak and give that state enough time to survive the project frame rate. A high-contrast flash should normally occupy at least two output frames unless the creator explicitly wants a subliminal single-frame hit.

When an element must expand beyond the frame, calculate coverage in the composition's local coordinates. For a centered circle with radius `r` on a `width × height` composition, its scale must exceed `sqrt((width / 2)^2 + (height / 2)^2) / r`; add margin so antialiasing cannot expose the corners. Scaling a focal ring by an arbitrary value such as `1.2` is not a full-frame expansion.

Keep visibility ownership on one level. A child opacity set to zero still suppresses a visible parent, so do not mix a hidden child class with an ancestor reveal without explicitly restoring the child. After saving, inspect a frame before the beat, a frame inside the visible peak, and a frame after it. Seeking to the exact start of a tween verifies its initial state, not the promised effect.

## Deterministic Three.js

For genuine mesh geometry, perspective cameras, lights, and cast shadows, use a `<script type="module">` with exactly `https://cdn.jsdelivr.net/npm/three@0.181.2/+esm` when the base module is sufficient. When official Three.js addons are required, use the exact pinned import map from the allowlisted official Three.js adapter:

```html
<script type="importmap">
  {"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/"}}
</script>
<script type="module">
  import * as THREE from "three";
  import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
  import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js";
</script>
```

Never combine different Three.js versions or use legacy global addon scripts. The composition root must have an explicit `data-duration`. Create `WebGLRenderer` with `{alpha: true, antialias: true}`, call `renderer.setClearColor(0x000000, 0)` and `setPixelRatio(1)`, and render only from a `renderAt(time)` function invoked by `hf-seek`; initialize once from `window.__hfThreeTime || 0`. Load GLTF models, textures, and decoder dependencies before registering the composition timeline or render-ready state. Intrinsic public assets are allowed when their URLs are direct, public, CORS-compatible HTTPS; for registry assets, replace every relative model/texture path with the exact URL returned by `get_hyperframes_registry_item`. On `pagehide`, remove the `hf-seek` listener and dispose the loaders, renderer, geometries, materials, and textures. Do not use `requestAnimationFrame`, `setAnimationLoop`, `THREE.Clock`, wall-clock time, relative asset paths, or seek-time asset loading. A CSS `perspective` transform is not an acceptable substitute when the creator explicitly requests real Three.js meshes, lighting, or shadows.

`alpha: true` makes untouched WebGL pixels transparent; it does not make rendered geometry transparent. A large floor built with `MeshStandardMaterial`, `MeshBasicMaterial`, or another opaque material still paints its color into every covered pixel. For a transparent overlay that needs cast shadows, use a shadow-only receiver:

```js
const floor = new THREE.Mesh(
  new THREE.PlaneGeometry(30, 30),
  new THREE.ShadowMaterial({color: 0x000000, transparent: true, opacity: 0.16}),
);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);
```

Use an opaque floor or backdrop only when the creator explicitly requested a full-frame scene/background.

## Variables and assets

HyperFrames variables are a flat JSON object whose values are strings, finite numbers, or booleans. Read them from `window.__hfVariables`. Keep defaults in the HTML so preview remains understandable when a variable is absent.

Project media is the preferred transport: import media/audio into the project Media/Audio library and bind the exact URL `list_editor_assets` returns. The host stores it as `subclip-media://asset/<id>` (allowed in `img`, `video`, `audio`, `source`, SVG `image` and variables), remaps it on reopen or import, and serves it at export. Public HTTPS also works, but only after the same import step. Prefer native Media/Audio lanes. For an inseparable embedded video or audio asset, give each element a stable unique ID, use a direct source URL, and avoid `crossorigin`. Do not nest a media element with its own `data-start` inside another timed plain element. Never use guessed custom-scheme URLs or an unimported provider URL. Verify the downloaded resource is available inside the sandbox and at export; otherwise use a verified alternative.

Primary footage, B-roll, narration, music, SFX, captions, TTS, maps, and generated media belong in native Subclip layers and operations. Use a framework media URL only for a small, already imported visual asset intrinsic to the composition. Confirm fonts and all external dependencies before authoring against them; a font family name alone is not proof that its face/weight is loaded. Never put credentials in source or variables: credential-shaped keys, bearer/provider tokens, cookies, authorization headers, signed URLs, and token/signature query parameters are rejected.

Lottie is appropriate for an existing animation payload. Verify the pinned public CDN runtime and JSON asset are accessible to the sandbox/exporter before use, then expose a seekable instance using the HyperFrames runtime convention. Prefer importing the JSON with `import_public_lottie_json` and inlining its checked, licensed `animationData` when it fits the source budget. Inspect any image/audio dependencies inside the payload too: import them into the project library and bind their returned URLs. Do not assume that loading the JSON proves its dependent resources are available.

## Layering and transparency

The document background and composition root should be transparent for overlay graphics. Put an opaque fill on the composition root or a full-bleed child only when the scene intentionally replaces the background inside that Motion item's bounds; Subclip preserves that authored background during alpha-proxy export. Use `layerOrder`, `zIndex`, and `lane` on the Subclip item for cross-panel hierarchy; internal CSS `z-index` controls only elements inside this layer.

Validate source before every add or source revision. A successful static check does not replace rendered-frame inspection.
