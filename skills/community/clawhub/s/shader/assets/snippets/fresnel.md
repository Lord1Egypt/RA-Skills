# Fresnel Snippet

```glsl
float fresnelTerm(vec3 viewDir, vec3 normal, float power) {
  return pow(1.0 - max(dot(normalize(viewDir), normalize(normal)), 0.0), power);
}
```
