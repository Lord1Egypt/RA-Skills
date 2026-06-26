# Scanline Snippet

```glsl
float scanlineMask(float coord, float time, float density, float strength) {
  float scan = 0.5 + 0.5 * sin(coord * density + time * 6.0);
  return mix(1.0 - strength, 1.0, scan);
}
```
