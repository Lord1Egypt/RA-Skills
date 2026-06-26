---
name: shadertoy
description: "Write, explain, debug, and port ShaderToy-style fragment shaders. Use when the user asks for ShaderToy code, wants help with `mainImage`, `fragCoord`, `iTime`, `iResolution`, `iMouse`, `iChannel0..3`, buffer passes, common fullscreen coordinate math, or needs to migrate a ShaderToy effect into raw WebGL, Three.js, React Three Fiber, or a browser canvas demo. NOT for general material shaders, vertex shaders, or non-ShaderToy rendering pipelines unless the task clearly starts from ShaderToy code or ShaderToy concepts."
metadata: { "openclaw": { "emoji": "🟥" } }
---

# ShaderToy

Use this skill for ShaderToy-native work and ShaderToy-to-runtime migration.

This skill is narrower than `shader`. If the problem is fundamentally about ShaderToy built-ins, `mainImage`, channels, buffers, or porting out of ShaderToy, use this one first.

## Workflow

### 1. Confirm the ShaderToy shape

Resolve these first:

- single `Image` pass or multi-pass with `Buffer A/B/C/D`
- uses of `iTime`, `iResolution`, `iMouse`
- channel usage: `iChannel0..3`
- whether the code is pure procedural or samples textures / buffers

If the user posts ShaderToy code, keep the original structure visible until the effect works.

### 2. Debug in ShaderToy terms first

Before porting, reduce the effect inside ShaderToy conventions:

- replace output with a constant color
- visualize `fragCoord / iResolution.xy`
- bypass texture reads and channels temporarily
- isolate one term at a time

Read `references/builtins.md` for the built-in variable map.

### 3. Port only after the effect is understood

When porting away from ShaderToy:

- convert `mainImage(out vec4 fragColor, in vec2 fragCoord)` to the host entry point
- replace built-ins with explicit uniforms
- recreate full-screen quad or postprocess host setup
- account for channel textures and buffer passes explicitly

Read `references/porting.md` before rewriting host-side glue.

### 4. Keep answers concrete

Prefer:

- a corrected ShaderToy fragment shader
- a mapping of built-ins to host uniforms
- a minimal migration plan
- the first likely failure point

## Commands

### Inspect built-ins and channels

```bash
node {baseDir}/scripts/shadertoy.js builtins
node {baseDir}/scripts/shadertoy.js channels --json
```

### Generate a porting checklist

```bash
node {baseDir}/scripts/shadertoy.js port three
node {baseDir}/scripts/shadertoy.js port webgl --json
```

Use this when converting ShaderToy code into another runtime.

### Print a debug checklist

```bash
node {baseDir}/scripts/shadertoy.js debug black-screen
node {baseDir}/scripts/shadertoy.js debug channels
```

### Generate an intake plan

```bash
node {baseDir}/scripts/shadertoy.js intake "port a shadertoy ocean to r3f"
node {baseDir}/scripts/shadertoy.js intake "fix my iChannel feedback effect" --json
```

### Pick the right demo starting point

```bash
node {baseDir}/scripts/shadertoy.js demo single-pass
node {baseDir}/scripts/shadertoy.js demo feedback --json
```

### Generate a scaffold recommendation

```bash
node {baseDir}/scripts/shadertoy.js scaffold three single-pass
node {baseDir}/scripts/shadertoy.js scaffold webgl feedback --json
```

Use this when the user wants the fastest route from a ShaderToy idea to a runnable host setup.

## Assets

Bundled templates:

- `assets/shadertoy-single-pass-demo/index.html`
- `assets/shadertoy-feedback-notes.txt`

## References

- Built-ins, channels, and pass semantics: `references/builtins.md`
- Migration rules to WebGL / Three.js / R3F: `references/porting.md`
- Buffer and feedback triage: `references/buffers-feedback.md`

## Guardrails

- Keep ShaderToy naming intact until the effect is understood.
- Do not invent channels or buffer passes the user did not specify.
- If the shader relies on buffers or feedback, say so explicitly before pretending it is a single-pass effect.
- When porting, make every implicit ShaderToy input explicit in the host code.
