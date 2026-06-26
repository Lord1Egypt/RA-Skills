# ShaderToy Built-ins

Use this reference when the task is specifically about ShaderToy syntax and conventions.

## Entry point

ShaderToy fragment shaders commonly use:

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord)
```

This is not the same as a normal GLSL host `main()`.

## Common built-ins

- `iTime`: elapsed time in seconds
- `iResolution`: viewport resolution; typically use `iResolution.xy`
- `iMouse`: mouse state
- `iFrame`: frame count
- `iTimeDelta`: delta time
- `iChannel0..3`: texture or buffer inputs

## Common coordinate pattern

```glsl
vec2 uv = fragCoord / iResolution.xy;
```

For centered screen space:

```glsl
vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;
```

## Channels and buffers

- `iChannel0..3` can point to textures, videos, cubemaps, or other passes.
- Many advanced ShaderToy effects are not single-pass.
- If a shader samples Buffer A or previous-frame data, say so explicitly before porting.
