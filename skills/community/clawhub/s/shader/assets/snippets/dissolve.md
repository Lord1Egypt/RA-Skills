# Dissolve Snippet

```glsl
float dissolveMask(float noiseValue, float progress) {
  return step(progress, noiseValue);
}

float dissolveEdge(float noiseValue, float progress, float edgeWidth) {
  return smoothstep(progress, progress + edgeWidth, noiseValue);
}
```
