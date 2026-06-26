# Fill Layers (Background) Reference

Fill layers are background elements placed behind video content (layer index 5).

## Preset Categories

### Solid (7)
| ID | Name | Color |
|----|------|-------|
| `black` | Pure Black | #000000 |
| `near_black` | Near Black | #0a0a0a |
| `dark_gray` | Dark Gray | #1a1a1a |
| `charcoal` | Charcoal | #2d2d2d |
| `white` | Pure White | #ffffff |
| `off_white` | Off White | #f5f5f0 |
| `transparent` | Transparent | transparent |

### Gradient (8)
| ID | Name | Description |
|----|------|-------------|
| `gradient_midnight` | Midnight | Deep blue → black |
| `gradient_purple` | Purple Haze | Rich purple 3-stop |
| `gradient_ocean` | Deep Ocean | Teal → deep blue |
| `gradient_sunset` | Sunset | Orange → purple 5-stop |
| `gradient_aurora` | Aurora | Northern lights 5-stop |
| `gradient_radial_spotlight` | Spotlight | Radial light from center |
| `gradient_warm` | Warm Ember | Warm brown tones |
| `gradient_cool` | Cool Steel | Blue-gray professional |

### Cinematic (5)
| ID | Name | Description |
|----|------|-------------|
| `cinematic_letterbox` | Cinematic 2.35:1 | Widescreen bars + vignette + 35mm grain |
| `cinematic_ultrawide` | Cinematic 2.76:1 | Ultra-widescreen + vignette + grain |
| `cinematic_noir` | Film Noir | Low saturation, heavy vignette, grain |
| `cinematic_teal_orange` | Teal & Orange | Hollywood color grade overlay |
| `cinematic_anamorphic` | Anamorphic | Lens flare + chromatic aberration |

### Pattern (4)
| ID | Name | Description |
|----|------|-------------|
| `pattern_dark_grid` | Dark Grid | Animated white grid on black |
| `pattern_scanlines` | Scanlines | CRT monitor scanline effect |
| `pattern_dots` | Halftone Dots | Print-style dot pattern |
| `pattern_hexagon` | Hexagon Grid | Blue honeycomb pattern |

### Retro (4)
| ID | Name | Description |
|----|------|-------------|
| `retro_vhs` | VHS | Scanlines + colorized grain + chromatic aberration |
| `retro_super8` | Super 8 | Heavy grain + warm tint + vignette |
| `retro_16mm` | 16mm Film | Medium grain + vignette + slight contrast |
| `retro_neon` | Neon Glow | Purple gradient + magenta grid + glow |

### Transition (5)
| ID | Name | Description |
|----|------|-------------|
| `transition_fade_black` | Fade to Black | Smooth fade in/out |
| `transition_flash` | Flash | Quick white flash |
| `transition_iris` | Iris | Circle reveal in/out |
| `transition_glitch` | Glitch | Digital glitch + chromatic aberration |
| `transition_zoom` | Zoom In | Zoom with blur |

### Overlay (5)
| ID | Name | Description |
|----|------|-------------|
| `overlay_vignette` | Vignette | Dark edges focus effect |
| `overlay_film_grain` | Film Grain | 35mm grain overlay blend |
| `overlay_light_leak` | Light Leak | Warm orange light leak |
| `overlay_lens_flare` | Lens Flare | Anamorphic blue lens flare |
| `overlay_bokeh` | Bokeh | Dreamy bokeh circles |

---

## FillLayerSettings Schema

### Base Fill
| Field | Type | Description |
|-------|------|-------------|
| `color` | string | Solid background color |
| `gradientEnabled` | boolean | Use gradient instead of solid |
| `gradient` | object | `{type, angle, stops[], centerX, centerY, radius}` |
| `blendMode` | enum | How layer blends with content |
| `opacity` | number | 0–1 |

### Pattern
| Field | Type | Description |
|-------|------|-------------|
| `pattern` | enum | Pattern type (see below) |
| `patternColor` | string | Pattern line/dot color |
| `patternOpacity` | number | Pattern opacity |
| `patternScale` | number | Pattern size multiplier |
| `patternAnimated` | boolean | Animate the pattern |
| `patternSpeed` | number | Animation speed |
| `patternBlendMode` | enum | Pattern blend mode |

### Film Grain
| Field | Type | Description |
|-------|------|-------------|
| `filmGrainStyle` | enum | Grain style (see below) |
| `filmGrainIntensity` | number | 0–1 |
| `filmGrainSize` | number | Grain size multiplier |
| `filmGrainAnimated` | boolean | Animate grain |
| `filmGrainColorized` | boolean | Colored grain |

### Vignette
| Field | Type | Description |
|-------|------|-------------|
| `vignetteIntensity` | number | 0–1 |
| `vignetteColor` | string | Vignette color |
| `vignetteSize` | number | 0–1 (smaller = tighter) |
| `vignetteSoftness` | number | 0–1 |

### Transitions
| Field | Type | Description |
|-------|------|-------------|
| `enterEffect` | enum | Enter transition effect |
| `enterDurationMs` | number | Enter duration |
| `enterEasing` | enum | Enter easing |
| `exitEffect` | enum | Exit transition effect |
| `exitDurationMs` | number | Exit duration |
| `exitEasing` | enum | Exit easing |

### Color Adjustments
| Field | Type | Description |
|-------|------|-------------|
| `colorTemperature` | number | Warm/cool shift |
| `colorTint` | number | Tint shift |
| `saturation` | number | 0–2 (1=normal) |
| `contrast` | number | 0–2 (1=normal) |
| `brightness` | number | 0–2 (1=normal) |

### Special Effects
| Field | Type | Description |
|-------|------|-------------|
| `blur` | number | Gaussian blur |
| `noiseAmount` | number | Noise overlay |
| `letterboxRatio` | number | Letterbox aspect (e.g., 2.35) |
| `chromaticAberration` | number | RGB offset amount |
| `glowIntensity` | number | Glow strength |
| `glowColor` | string | Glow color |
| `glowRadius` | number | Glow spread |
| `lightEffects` | array | Light leak/flare/bokeh objects |

---

## Enums

### Pattern Types (11)
`none` · `dots` · `grid` · `lines` · `diagonal` · `noise` · `crosshatch` · `hexagon` · `triangle` · `wave` · `scanlines`

### Film Grain Styles (8)
`none` · `subtle` · `moderate` · `heavy` · `16mm` · `35mm` · `super8` · `vhs`

### Blend Modes (12)
`normal` · `multiply` · `screen` · `overlay` · `darken` · `lighten` · `color-dodge` · `color-burn` · `hard-light` · `soft-light` · `difference` · `exclusion`

### Transition Effects (19)
`none` · `fade` · `wipe-left` · `wipe-right` · `wipe-up` · `wipe-down` · `iris-in` · `iris-out` · `radial-wipe` · `dissolve` · `zoom-in` · `zoom-out` · `spin` · `glitch` · `blur-in` · `blur-out` · `pixelate` · `slide-left` · `slide-right`

### Easing Options
`linear` · `ease-in` · `ease-out` · `ease-in-out` · `bounce` · `elastic`

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{id}/backgrounds` | List existing background/fill layers |
| POST | `/projects/{id}/backgrounds` | Add background/fill layer |

The public API uses `/backgrounds`, not `/fill-layers`. There is no public fill-layer preset list, patch, or delete route in the live OpenAPI. Prefer `style_keyword` or explicit settings when adding a background.
