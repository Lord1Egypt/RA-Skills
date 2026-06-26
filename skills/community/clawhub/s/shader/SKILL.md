---
name: shader
description: "Write, explain, adapt, and debug practical shader code for GLSL, WebGL, Three.js ShaderMaterial, React Three Fiber, postprocess-style full-screen effects, and ShaderToy-style fragment shaders. Use when the user wants to create an effect shader, port a shader between runtimes, fix black screens or compile errors, wire uniforms like time or resolution, troubleshoot UV, normal, or color-space mistakes, or turn a visual idea into a runnable vertex/fragment pair. Also use when pairing shader output with OpenClaw canvas demos. NOT for full rendering-engine architecture, advanced offline rendering theory, or GPU-vendor-specific optimization claims that have not been verified in the target runtime."
metadata: { "openclaw": { "emoji": "🟦" } }
---

# Shader

Use this skill to turn shader requests into runnable code and fast debugging steps.

Default target: browser-friendly GLSL. If the runtime is unclear, narrow it before writing code:

- ShaderToy fragment-only
- raw WebGL / GLSL ES
- Three.js `ShaderMaterial`
- React Three Fiber
- postprocess-style full-screen pass

## Workflow

### 1. Lock the runtime and effect shape

Resolve these first:

- runtime
- fragment-only vs vertex + fragment
- screen effect vs material effect vs postprocess pass
- required inputs: `uTime`, `uResolution`, UVs, normals, textures, mouse

If the request is vague, start with the smallest visible version of the effect.

### 2. Build from a visible baseline

- Start with a constant color or UV gradient.
- Add one moving term at a time.
- Reintroduce uniforms, varyings, noise, lighting, and distortion step by step.

For blank output, compile failures, or “nothing shows”, read `references/black-screen-checklist.md`.

### 3. Match the host, not the idea source

Do not hand over ShaderToy code unchanged if the user asked for Three.js or R3F.

Common translations:

- `iTime` -> `uTime`
- `iResolution` -> `uResolution`
- `fragCoord` -> `gl_FragCoord.xy`
- ShaderToy fullscreen logic -> quad / plane / postprocess host setup

For live previews inside OpenClaw, pair this skill with `canvas`.

### 4. Keep answers practical

Prefer responses that include:

- runnable shader code
- required uniforms and defaults
- host-side glue code
- the first debugging step if it fails

## Common Uses

- Full-screen effects: flowing gradients, ripples, ShaderToy-style animated backgrounds
- Material effects: fresnel, dissolve, edge glow, scanlines, vertex wobble
- Porting: ShaderToy -> WebGL / Three.js / R3F
- Debugging: black screen, all-white / all-black output, broken UVs, wrong varyings, missing uniforms

## Commands

### Intake

```bash
node {baseDir}/scripts/shader.js intake "fullscreen ocean background in three.js"
node {baseDir}/scripts/shader.js intake "port this shadertoy to r3f" --json
```

Use this to structure an underspecified request.

### Debug

```bash
node {baseDir}/scripts/shader.js debug black-screen
node {baseDir}/scripts/shader.js debug uniform
node {baseDir}/scripts/shader.js debug varyings
```

### Effects

```bash
node {baseDir}/scripts/shader.js effects
```

Maps user phrases to likely starter techniques like `gradient`, `noise`, `fresnel`, `dissolve`, `ripple`, `scanline`, and `pixelate`.

### Boilerplate

```bash
node {baseDir}/scripts/shader.js boilerplate fresnel
node {baseDir}/scripts/shader.js boilerplate dissolve --json
```

Returns stage split, likely uniforms, varyings, build order, and common failure points.

### Snippet

```bash
node {baseDir}/scripts/shader.js snippet fresnel
node {baseDir}/scripts/shader.js snippet ripple --json
```

Points to the nearest bundled GLSL starter.

### Demo

```bash
node {baseDir}/scripts/shader.js demo webgl ripple
node {baseDir}/scripts/shader.js demo r3f fresnel --json
```

Chooses the best bundled runtime template for a target + effect combination.

### Scaffold

```bash
node {baseDir}/scripts/shader.js scaffold r3f dissolve
node {baseDir}/scripts/shader.js scaffold postprocess scanline --json
```

Combines the nearest demo, boilerplate, snippet, and first integration steps.

## Assets

Bundled templates:

- `assets/webgl-fullscreen-demo/index.html`
- `assets/threejs-material-demo/index.html`
- `assets/postprocess-demo/index.html`
- `assets/r3f-demo/App.jsx`
- `assets/r3f-demo/main.jsx`
- `assets/r3f-demo/index.html`
- `assets/r3f-demo/package.json`
- `assets/r3f-demo/vite.config.js`

Bundled snippets:

- `assets/snippets/fresnel.md`
- `assets/snippets/dissolve.md`
- `assets/snippets/ripple.md`
- `assets/snippets/scanline.md`
- `assets/snippets/pixelate.md`
- `assets/snippets/vertex-wobble.md`

Use the postprocess template for screen-space effects. Use the Three.js or R3F templates for mesh/material effects.

## References

- `references/glsl-quick-reference.md`
- `references/black-screen-checklist.md`
- `references/effect-starters-zh.md`
- `references/snippets.md`
- `references/runtime-translation.md`

## Guardrails

- Default to the smallest working shader that proves the effect.
- Use host-friendly uniform names like `uTime`, `uResolution`, `uMouse`, `uTexture`.
- Do not assume WebGL2 unless the host clearly uses it.
- Do not invent runtime-specific macros or built-ins.
- Call out likely precision, color-space, or postprocess-order bugs explicitly.
- For performance advice, stay directional unless the actual runtime and GPU are known.
