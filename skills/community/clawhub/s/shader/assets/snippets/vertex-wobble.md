# Vertex Wobble Snippet

```glsl
vec3 vertexWobble(vec3 position, float time, float amplitude, float frequency) {
  vec3 transformed = position;
  transformed.z += sin(position.x * frequency + time * 2.0) * amplitude;
  transformed.y += sin(position.y * (frequency * 0.75) + time * 1.5) * (amplitude * 0.6);
  return transformed;
}
```
