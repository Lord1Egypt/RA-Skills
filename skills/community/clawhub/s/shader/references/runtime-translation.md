# Runtime Translation

Use this reference when moving a shader idea across ShaderToy, raw WebGL, Three.js, and React Three Fiber.

## ShaderToy

Good for:

- quick fullscreen experiments
- fragment-only effects
- visual prototyping

Common assumptions:

- `iTime`
- `iResolution`
- `fragCoord`
- `mainImage`

Translation notes:

- convert built-ins into explicit uniforms
- rewrite `mainImage` into `main`
- recreate fullscreen quad setup in the host

## Raw WebGL

Good for:

- smallest dependency footprint
- direct fullscreen fragment demos
- debugging outside framework complexity

Common assumptions:

- you own shader compilation and linking
- you provide all uniforms and attributes
- you build the quad or geometry yourself

Translation notes:

- best bridge from ShaderToy ideas
- use when you want to prove the shader before framework integration

## Three.js ShaderMaterial

Good for:

- mesh and material effects
- quick browser demos with scene/camera abstractions
- vertex + fragment experiments on geometry

Common assumptions:

- `projectionMatrix`, `modelViewMatrix`, `position`, `uv`, `normal`
- uniforms passed through `ShaderMaterial`

Translation notes:

- easiest upgrade path from raw GLSL to scene-aware material work
- good default for fresnel, dissolve, wobble, shield, hologram effects

## React Three Fiber

Good for:

- React apps that already use Three
- componentized shader experiments
- interactive UI + shader combinations

Common assumptions:

- `useFrame` updates time
- uniforms live in JSX props / refs
- material state is managed in React-compatible patterns

Translation notes:

- do not overcomplicate first pass with React state; keep uniforms minimal
- prove the shader in a tiny component before integrating into a larger scene

## Quick mapping table

| Need | Best starting runtime |
| --- | --- |
| fullscreen animated background | ShaderToy idea -> raw WebGL or postprocess demo |
| screen-space scanlines or pixelation | postprocess demo |
| model edge glow / fresnel | Three.js or R3F material |
| model dissolve | Three.js or R3F material |
| vertex deformation | Three.js or R3F material |
| fastest “does this shader work” check | raw WebGL fullscreen demo |

## Practical rule

If the user asks for a visual effect but not a runtime:

- pick `postprocess-demo` for screen-space effects
- pick `threejs-material-demo` for mesh/material effects
- pick `r3f-demo` only when the user already has a React/R3F app
