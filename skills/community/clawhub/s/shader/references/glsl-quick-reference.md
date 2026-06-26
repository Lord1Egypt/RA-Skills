# GLSL Quick Reference

Use this reference when writing or porting practical browser-side shaders.

## Default assumptions

- Prefer GLSL ES style code unless the host clearly uses desktop GLSL.
- Prefer `uTime`, `uResolution`, `uMouse`, `uTexture` as uniform names.
- For screen effects, normalize coordinates explicitly instead of assuming ShaderToy built-ins.

## Common translations

### ShaderToy to generic GLSL

- `iTime` -> `uTime`
- `iResolution.xy` -> `uResolution`
- `fragCoord.xy / iResolution.xy` -> `gl_FragCoord.xy / uResolution`
- `mainImage(out vec4 fragColor, in vec2 fragCoord)` -> `void main()`

### Fragment-only effect baseline

```glsl
precision mediump float;

uniform float uTime;
uniform vec2 uResolution;

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution.xy;
  vec3 color = vec3(uv, 0.5 + 0.5 * sin(uTime));
  gl_FragColor = vec4(color, 1.0);
}
```

### Material baseline

Vertex shader:

```glsl
varying vec2 vUv;

void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

Fragment shader:

```glsl
precision mediump float;

varying vec2 vUv;

void main() {
  gl_FragColor = vec4(vUv, 0.0, 1.0);
}
```

## Practical pitfalls

- Black screen often means:
  - nothing is drawn
  - uniforms are missing
  - varyings do not match
  - bad math produces NaN
  - shader version does not match host
- A fully white or black output often means:
  - UVs are out of range
  - smoothstep thresholds are inverted
  - noise or lighting terms saturate
  - texture sampling is invalid
- A flipped or mirrored effect often means:
  - Y axis assumptions differ
  - screen UV and model UV are being mixed

## Good default progression

1. constant color
2. UV gradient
3. animated scalar
4. mask / shape
5. noise / distortion
6. lighting / blending / post tweaks

If the user is stuck, move backward through that ladder until the bug disappears.
