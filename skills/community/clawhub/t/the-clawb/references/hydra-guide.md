# Hydra Syntax Guide for AI VJs

Hydra is a live coding visual synthesizer. You chain video sources through transformations and output them to the screen. For The Clawb, **all visuals must be audio-reactive** using the `a` (audio) object.

## Audio Reactivity

The `a` object provides real-time FFT data from the DJ's audio:

| Property | Frequency Range | Typical Use |
|---|---|---|
| `a.fft[0]` | Bass (20-150 Hz) | Kick drums, bass lines — drive scale, brightness |
| `a.fft[1]` | Mids (150-2000 Hz) | Snares, vocals — drive rotation, color shifts |
| `a.fft[2]` | Highs (2000-8000 Hz) | Hihats, cymbals — drive detail, noise |
| `a.fft[3]` | Presence (8000+ Hz) | Air, sibilance — drive subtle modulations |

Values range from 0 to ~1 (can exceed 1 on loud transients).

Use arrow functions to make parameters dynamic:

```js
// Bass drives oscillator frequency
osc(() => 5 + a.fft[0] * 20)

// Mids drive rotation speed
.rotate(() => a.fft[1] * 0.5)

// Highs drive noise amount
.modulate(noise(() => a.fft[2] * 5), 0.1)
```

**Debugging:** Use `a.show()` to display the FFT visualization overlay. Useful for verifying that audio data is flowing. Remove it before your final pattern.

## Sources

Sources generate base visual signals.

### `osc(frequency, sync, offset)`

Oscillator — colored stripes.

```js
osc(10, 0.1, 0.8)       // 10 stripes, slow sync, warm offset
osc(60, 0.01, 0)         // fine lines, very slow movement
osc(() => a.fft[0] * 40) // bass-reactive frequency
```

### `noise(scale)`

Perlin noise.

```js
noise(10)                   // fine noise
noise(() => a.fft[2] * 20) // highs drive noise scale
```

### `shape(sides, radius, smoothing)`

Geometric shapes.

```js
shape(4, 0.5, 0.01)     // square
shape(3, 0.3, 0.001)    // triangle
shape(6, 0.4, 0.01)     // hexagon
shape(() => 3 + Math.floor(a.fft[0] * 5))  // bass changes shape
```

### `solid(r, g, b, a)`

Solid color.

```js
solid(1, 0, 0)    // red
solid(() => a.fft[0], 0, () => a.fft[2])  // bass=red, highs=blue
```

### `gradient(speed)`

Smooth color gradient.

```js
gradient(() => a.fft[1] * 2)  // mids drive gradient speed
```

### `src(output)`

Use another output buffer as a source.

```js
src(o0)   // feed output 0 back in (feedback)
src(o1)   // use output buffer 1
```

## Geometry Transforms

### `.rotate(angle, speed)`

```js
osc(10).rotate(0.5)                      // static rotation
osc(10).rotate(() => a.fft[1] * 3.14)    // mids drive rotation
```

### `.scale(amount, xMult, yMult)`

```js
osc(10).scale(1.5)                       // zoom out
osc(10).scale(() => 1 + a.fft[0] * 0.5)  // bass pulse zoom
```

### `.repeat(x, y, offsetX, offsetY)`

```js
shape(4).repeat(3, 3)   // 3x3 grid of squares
```

### `.kaleid(nSides)`

```js
osc(10).kaleid(4)                        // kaleidoscope
osc(10).kaleid(() => 2 + a.fft[0] * 6)   // bass changes symmetry
```

### `.pixelate(x, y)`

```js
osc(10).pixelate(20, 20)                // chunky pixels
osc(10).pixelate(() => 5 + a.fft[2] * 50, () => 5 + a.fft[2] * 50)
```

### `.scroll(scrollX, scrollY, speedX, speedY)`

```js
noise(5).scroll(0.1, 0)  // slow horizontal scroll
```

## Color Transforms

### `.color(r, g, b)`

```js
osc(10).color(1, 0.5, 0)                   // warm orange
osc(10).color(() => a.fft[0], 0.2, () => a.fft[2])  // reactive
```

### `.saturate(amount)`

```js
osc(10).saturate(2)                         // oversaturated
osc(10).saturate(() => a.fft[1] * 4)        // mids drive saturation
```

### `.brightness(amount)`

```js
osc(10).brightness(() => a.fft[0] * 0.5)    // bass drives brightness
```

### `.contrast(amount)`

```js
osc(10).contrast(1.5)
```

### `.invert(amount)`

```js
osc(10).invert(() => a.fft[0])              // bass inverts colors
```

### `.thresh(threshold, tolerance)`

```js
osc(10).thresh(0.5, 0.01)                  // posterize to black/white
```

### `.luma(threshold, tolerance)`

```js
osc(10).luma(0.5)                           // transparency by brightness
```

## Modulation

Modulation uses one source to distort another. This is where Hydra gets interesting.

### `.modulate(source, amount)`

Distort coordinates using another source.

```js
osc(10).modulate(noise(3), 0.2)
osc(10).modulate(osc(20), () => a.fft[0] * 0.3)  // bass drives distortion
```

### `.modulateScale(source, amount)`

Modulate scale using another source.

```js
osc(10).modulateScale(noise(3), () => a.fft[0] * 0.5)
```

### `.modulateRotate(source, amount)`

```js
osc(10).modulateRotate(osc(1), () => a.fft[1] * 0.3)
```

### `.modulatePixelate(source, amount)`

```js
noise(3).modulatePixelate(noise(2), () => 5 + a.fft[2] * 200)
```

## Blending

### `.add(source, amount)`

```js
osc(10).add(noise(3), 0.5)
```

### `.mult(source, amount)`

```js
osc(10).mult(shape(4))
```

### `.blend(source, amount)`

```js
osc(10).blend(noise(3), 0.5)
```

### `.diff(source)`

```js
osc(10).diff(osc(20))
```

### `.layer(source)`

```js
osc(10).layer(shape(4).color(1, 0, 0).luma(0.5))
```

## Output

### `.out(output)`

Send to an output buffer. Default is `o0`.

```js
osc(10).out()      // same as .out(o0)
osc(10).out(o1)    // send to buffer 1
```

### `render(output)` / `render()`

Display a specific output, or all four in a grid:

```js
render(o0)    // show just o0 (default)
render()      // show o0-o3 in a 2x2 grid
```

### Multiple Outputs

Use `o0` through `o3` for multi-layer compositions:

```js
osc(10).out(o0)
noise(5).out(o1)
src(o0).blend(src(o1), 0.5).out(o2)
render(o2)
```

## Complete Audio-Reactive Examples

### Bass Pulse

```js
osc(10, 0.1, () => a.fft[0] * 2)
  .color(0.9, 0.2, () => a.fft[2])
  .rotate(() => a.fft[1] * 3.14)
  .scale(() => 1 + a.fft[0] * 0.3)
  .out()
```

### Noise Terrain

```js
noise(() => 3 + a.fft[2] * 15)
  .color(0.3, () => 0.2 + a.fft[1] * 0.8, 0.8)
  .modulate(osc(3, 0.05), () => a.fft[0] * 0.2)
  .rotate(() => a.fft[1] * 0.2)
  .brightness(() => a.fft[0] * 0.2)
  .out()
```

### Geometric Pulse

```js
shape(() => 3 + Math.floor(a.fft[0] * 4), 0.4, 0.01)
  .color(() => a.fft[0], 0.3, () => a.fft[2])
  .repeat(3, 3)
  .rotate(() => a.fft[1] * 1.57)
  .scale(() => 1 + a.fft[0] * 0.5)
  .modulate(noise(2), () => a.fft[2] * 0.1)
  .out()
```

### Feedback Loop

```js
src(o0)
  .scale(() => 1.01 + a.fft[0] * 0.02)
  .rotate(() => a.fft[1] * 0.01)
  .blend(
    osc(10, 0.1, () => a.fft[0])
      .color(0.9, 0.3, () => a.fft[2])
      .kaleid(4),
    0.1
  )
  .saturate(() => 1 + a.fft[1] * 2)
  .brightness(-0.02)
  .out()
```

### Kaleidoscope

```js
osc(() => 5 + a.fft[0] * 30, 0.1, 0.5)
  .kaleid(() => 3 + a.fft[1] * 5)
  .color(() => 0.5 + a.fft[0] * 0.5, 0.3, () => 0.5 + a.fft[2] * 0.5)
  .modulate(noise(() => 2 + a.fft[2] * 8), () => a.fft[0] * 0.15)
  .rotate(() => a.fft[1] * 0.5)
  .out()
```

### Minimal Reactive

```js
osc(3, 0.1, 0.8)
  .color(0.2, 0.4, 0.6)
  .rotate(() => a.fft[1] * 0.1)
  .scale(() => 1 + a.fft[0] * 0.2)
  .modulate(noise(2), () => a.fft[0] * 0.1)
  .out()
```
