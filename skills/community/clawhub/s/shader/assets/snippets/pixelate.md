# Pixelate Snippet

```glsl
vec2 pixelateUv(vec2 uv, vec2 pixelSize) {
  return floor(uv * pixelSize) / pixelSize;
}
```
