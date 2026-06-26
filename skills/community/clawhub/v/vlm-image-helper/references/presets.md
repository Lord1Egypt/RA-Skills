# Presets

Use presets before manual coordinates whenever the target region is only known semantically.

## Crop Presets

| Preset | Description | Coverage |
|--------|-------------|----------|
| top-left | Top-left quadrant | 0-50% X, 0-50% Y |
| top-right | Top-right quadrant | 50-100% X, 0-50% Y |
| bottom-left | Bottom-left quadrant | 0-50% X, 50-100% Y |
| bottom-right | Bottom-right quadrant | 50-100% X, 50-100% Y |
| left-half | Left half | 0-50% X |
| right-half | Right half | 50-100% X |
| top-half | Top half | 0-50% Y |
| bottom-half | Bottom half | 50-100% Y |
| center | Center 50% | 25-75% X, 25-75% Y |
| center-wide | Wider center region | 10-90% X, 25-75% Y |
| center-tall | Taller center region | 25-75% X, 10-90% Y |
| center-top | Center of the top half | 25-75% X, 0-50% Y |
| center-bottom | Center of the bottom half | 25-75% X, 50-100% Y |

## Scale Presets

| Preset | Factor |
|--------|--------|
| x2 | 2x |
| x3 | 3x |
| x4 | 4x |

## Selection Heuristics

- Start with `center` when the user points to a general middle area.
- Use quadrant presets when the cue is directional, such as "top-right number" or "bottom-left label".
- Use half-image presets when the region is broad and the first pass should stay conservative.
- Use `x2` before `x3` or `x4` unless the region is extremely small.
