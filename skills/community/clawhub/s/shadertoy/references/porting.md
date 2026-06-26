# ShaderToy Porting

Use this reference when moving a ShaderToy effect into another runtime.

## Raw WebGL

- rewrite `mainImage` into `main`
- replace `fragCoord` with `gl_FragCoord.xy`
- replace ShaderToy built-ins with explicit uniforms
- create a full-screen quad

## Three.js

- decide whether the effect should stay screen-space or become a mesh material effect
- use `ShaderMaterial` or a fullscreen pass host
- wire `uTime`, `uResolution`, and channel textures explicitly

## React Three Fiber

- keep the first pass tiny
- update `uTime` in `useFrame`
- treat ShaderToy channels and feedback passes as explicit resources
- do not hide multi-pass complexity inside React abstractions too early

## Porting rule

Do not rewrite everything at once.

1. Make the ShaderToy version obviously correct.
2. Port built-ins to uniforms.
3. Recreate the full-screen host.
4. Re-add channels and feedback.
5. Only then adapt style or optimize.
