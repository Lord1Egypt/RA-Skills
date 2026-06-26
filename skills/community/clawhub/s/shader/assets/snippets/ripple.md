# Ripple Snippet

```glsl
float rippleRing(vec2 uv, float time) {
  vec2 p = uv * 2.0 - 1.0;
  float dist = length(p);
  float wave = sin(dist * 24.0 - time * 4.0);
  return smoothstep(0.2, 0.21, wave) - smoothstep(0.21, 0.22, wave);
}
```
