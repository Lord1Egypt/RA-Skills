---
name: threejs-ai-skill
description: 'Makes AI-generated Three.js / WebGL / react-three-fiber code produce coherent, playable 3D scenes instead of code that compiles but looks and feels broken — correct model scale and orientation, grounded and non-overlapping placement, real collisions, frame-rate-independent controls, and characters that walk without sliding or floating. Use this whenever the work touches Three.js, react-three-fiber, or WebGL: creating, reviewing, or refactoring a scene, world, or game; loading GLTF/GLB/FBX models; setting up cameras, controls, lighting, shadows, or physics; adding player movement or character animation; or debugging why a scene looks wrong — objects at the wrong size, floating, clipping through each other, facing the wrong way, a broken-looking camera or lighting, or a character that slides or floats. Apply it even when the user just says "make a 3D scene/world/game" without naming these problems — these rules prevent the most common silent failures in generated 3D code.'
---

# Three.js AI Skill

AI-generated Three.js code almost always *compiles* — and then looks and feels broken. Models load at the wrong scale facing random directions; objects spawn at arbitrary coordinates, float, or clip through everything; the camera drifts unframed; there are never any collisions; controls are frame-rate-dependent and don't handle diagonals; and characters slide across the floor while their legs move out of sync.

The root cause is always the same: **the model writes code without reasoning about the physical and spatial rules of a real 3D world.** This skill encodes those rules as layers. Read the layer(s) relevant to the request; each builds on the one before.

## The layer stack

1. **Scene sanity** (this file, §1) — scale, orientation, lighting, camera, placement, renderer setup. *Every* scene needs this.
2. **World coherence** → `references/world-coherence.md` — no infinite spawns, relative scale, everything on the ground, framed camera, intentional layout.
3. **Collisions** → `references/collision-bounds.md` — objects that don't pass through everything; test-before-move; when to use a physics engine.
4. **Input & controls** → `references/input-controls.md` — deltaTime, normalized diagonals, multi-key, clamped mouse-look.
5. **Locomotion** → `references/locomotion.md` — characters that walk without sliding or floating; turn toward movement; blend idle/walk/run. *(Verify visually — hard to get right.)*
6. **Animation handling** → `references/animation-handling.md` — play clips, retarget animation from another file, and **procedural** motion for models with no animation. *(Procedural is experimental — always test the visual result before trusting it.)*

Read `references/model-normalization.md` for the drop-in model-loading helpers referenced throughout.

**react-three-fiber:** every rule below applies unchanged — r3f is a renderer binding, not a different engine. Prefer drei equivalents where they exist (`<Bounds>` for framing, `<Environment>` for IBL, `<OrbitControls makeDefault>`), and do movement/physics work in `useFrame((_, delta) => ...)`, never in `useEffect` or render.

---

## §1 Scene Sanity (core — always apply)

### Model scale & orientation — never trust the file
GLTF/GLB/FBX files carry arbitrary units and forward axes (FBX is frequently in centimeters — 100× too big). Always normalize after load: measure with `new THREE.Box3().setFromObject(model)`, scale uniformly so the largest dimension hits a known target, re-center the pivot, and never assume `-Z` is "forward" — verify orientation explicitly. Helper in `references/model-normalization.md`.

### Camera & controls — bounded and damped
With `OrbitControls`, set `enableDamping = true` and call `controls.update()` each frame. Clamp `minDistance`/`maxDistance` and `maxPolarAngle` (so it can't go under the floor). Frame the subject: derive camera distance from the target's bounding size, don't hardcode `position.set(0,0,5)`. Set sane `near`/`far` for the scene scale — a huge far/near ratio causes z-fighting.

### Renderer & resize — the silent omissions
AI code habitually skips both, and the scene distorts on the first window resize:

```js
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // don't melt phones
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
```

### Lighting — coherent, not a void or a blowout
Baseline: soft `AmbientLight`/`HemisphereLight` (fill) + one `DirectionalLight` (key, with shadows if needed) + an environment map (`scene.environment`) so PBR materials don't read flat/dark. Enable `renderer.toneMapping = THREE.ACESFilmicToneMapping` with sensible exposure. For shadows, size the directional light's shadow camera to the scene — the default frustum clips shadows in scenes larger than a few units.

### Teardown
Dispose geometries, materials, and textures when a scene unmounts, or you leak GPU memory. In r3f, drei's `useGLTF` handles caching; manual `new THREE.*` resources still need disposal.

---

## Pre-flight checklist (before returning any scene)
- [ ] Models normalized (scale + centered + orientation checked)
- [ ] Objects on the ground, intentional layout, finite count (see world-coherence)
- [ ] World bounds defined; colliders present if things move (see collisions)
- [ ] Camera framed to subject; damping on; distance/angle clamped
- [ ] Resize handler + pixel ratio clamp present
- [ ] Ambient + key light + environment; tone mapping on
- [ ] Input frame-rate independent; diagonals normalized (see input-controls)
- [ ] Characters don't slide/float (see locomotion)
- [ ] Geometries/materials/textures disposed on teardown

## Version awareness
Three.js changes fast and tutorials rot. Known breakpoints: `outputEncoding` became `outputColorSpace` in **r152**; physically-correct lighting became the default in **r155** (`useLegacyLights` removed in r165), so light intensity numbers from older tutorials are wrong; import paths moved from `three/examples/jsm/` to `three/addons/`. Follow the target version when known; otherwise write for the current API and flag anything version-sensitive instead of copying old numbers.
