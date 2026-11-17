# Brutalist — Industrial & Tactical UI

> Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects.

---

## Skill Meta

**Name:** Industrial Brutalism & Tactical Telemetry Interface Engineering

**Description:** Architect web interfaces that synthesize:
- Mid-century Swiss Typographic design
- Industrial manufacturing manuals
- Retro-futuristic aerospace/military terminal interfaces

Requirements:
- Absolute mastery over rigid modular grids
- Extreme typographic scale contrast
- Purely utilitarian color palettes
- Programmatic simulation of analog degradation (halftones, CRT scanlines, bitmap dithering)

Objective: Construct digital environments that project raw functionality, mechanical precision, and high data density, deliberately discarding conventional consumer UI patterns.

---

## Visual Archetypes

Pick ONE per project. Do not alternate or mix both modes within the same interface.

### 2.1 Swiss Industrial Print (Light Mode)

Derived from 1960s corporate identity systems and heavy machinery blueprints.

**Characteristics:**
- High-contrast light modes (newsprint/off-white substrates)
- Monolithic, heavy sans-serif typography
- Unforgiving structural grids outlined by visible dividing lines
- Aggressive, asymmetric use of negative space
- Oversized, viewport-bleeding numerals or letterforms
- Heavy use of primary red as alert/accent color

### 2.2 Tactical Telemetry & CRT Terminal (Dark Mode)

Derived from classified military databases, legacy mainframes, and aerospace Heads-Up Displays (HUDs).

**Characteristics:**
- Dark mode exclusivity
- High-density tabular data presentation
- Absolute dominance of monospaced typography
- Technical framing devices (ASCII brackets, crosshairs)
- Simulated hardware limitations (phosphor glow, scanlines, low bit-depth rendering)

---

## Typographic Architecture

Typography is the primary structural and decorative infrastructure. Imagery is secondary.

### Macro-Typography (Structural Headers)

| Parameter | Value |
|-----------|-------|
| **Classification** | Neo-Grotesque / Heavy Sans-Serif |
| **Optimal Fonts** | Neue Haas Grotesk (Black), Inter (Extra Bold/Black), Archivo Black, Roboto Flex (Heavy), Monument Extended |
| **Scale** | Fluid typography: `clamp(4rem, 10vw, 15rem)` |
| **Tracking** | Extremely tight: `-0.03em` to `-0.06em` |
| **Leading** | Highly compressed: `0.85` to `0.95` |
| **Casing** | Exclusively UPPERCASE |

### Micro-Typography (Data & Telemetry)

| Parameter | Value |
|-----------|-------|
| **Classification** | Monospace / Technical Sans |
| **Optimal Fonts** | JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime |
| **Scale** | Fixed and small: `10px` to `14px` / `0.7rem` to `0.875rem` |
| **Tracking** | Generous: `0.05em` to `0.1em` |
| **Leading** | Standard to tight: `1.2` to `1.4` |
| **Casing** | Exclusively UPPERCASE |

### Textural Contrast (Artistic Disruption)

| Parameter | Value |
|-----------|-------|
| **Classification** | High-Contrast Serif |
| **Optimal Fonts** | Playfair Display, EB Garamond, Times New Roman |
| **Usage** | Exceedingly sparingly, with heavy post-processing (halftone filters, 1-bit dithering) |

---

## Color System

Gradients, soft drop shadows, and modern translucency are strictly prohibited.

### If Swiss Industrial Print (Light):

| Role | Color |
|------|-------|
| **Background** | `#F4F4F0` or `#EAE8E3` (Matte, unbleached documentation paper) |
| **Foreground** | `#050505` to `#111111` (Carbon Ink) |
| **Accent** | `#E61919` or `#FF2A2A` (Aviation/Hazard Red) — ONLY accent color |

### If Tactical Telemetry (Dark):

| Role | Color |
|------|-------|
| **Background** | `#0A0A0A` or `#121212` (Deactivated CRT, avoid pure `#000000`) |
| **Foreground** | `#EAEAEA` (White phosphor) |
| **Accent** | `#E61919` or `#FF2A2A` (Aviation/Hazard Red) |
| **Terminal Green** | `#4AF626` — Optional, for SINGLE specific UI element only |

---

## Layout and Spatial Engineering

The layout must appear mathematically engineered.

### The Blueprint Grid
- Strict adherence to CSS Grid architectures
- Elements are anchored precisely to grid tracks and intersections
- Use `display: grid; gap: 1px;` with contrasting parent/child backgrounds for razor-thin dividing lines

### Visible Compartmentalization
- Extensive use of solid borders (`1px` or `2px solid`) to delineate zones
- Horizontal rules (`<hr>`) span entire container width to segregate operational units

### Bimodal Density
- Oscillate between extreme data density (tightly packed monospace metadata) and vast expanses of calculated negative space framing macro-typography

### Geometry
- **Absolute rejection of `border-radius`**
- All corners must be exactly 90 degrees to enforce mechanical rigidity

---

## UI Components and Symbology

Standard web UI conventions are replaced with utilitarian, industrial graphic elements.

### Syntax Decoration
Use ASCII characters to frame data points:
- **Framing:** `[ DELIVERY SYSTEMS ]`, `< RE-IND >`
- **Directional:** `>>>`, `///`, `\\\\`

### Industrial Markers
Prominent integration of registration (®), copyright (©), and trademark (™) symbols as structural geometric elements.

### Technical Assets
- Crosshairs (`+`) at grid intersections
- Repeating vertical lines (barcodes)
- Thick horizontal warning stripes
- Randomized string data: `REV 2.6`, `UNIT / D-01`

---

## Textural and Post-Processing Effects

Simulated analog degradation via CSS and SVG filters.

### Halftone and 1-Bit Dithering
Transform continuous-tone images or large serif typography into dot-matrix patterns:
- CSS `mix-blend-mode: multiply` overlays
- SVG radial dot patterns

### CRT Scanlines (Terminal Mode)
```css
.scanlines {
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.1) 2px,
    rgba(0,0,0,0.1) 4px
  );
}
```

### Mechanical Noise
Global, low-opacity SVG static/noise filter applied to DOM root for unified physical grain.

---

## Web Engineering Directives

### Grid Determinism
```css
.grid-container {
  display: grid;
  gap: 1px;
  background: #050505; /* parent background = dividing line color */
}
.grid-cell {
  background: #F4F4F0; /* cell background */
}
```

### Semantic Rigidity
Use precise semantic tags: `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>`

### Typography Clamping
```css
.macro-header {
  font-size: clamp(4rem, 10vw, 15rem);
  letter-spacing: -0.04em;
  line-height: 0.9;
  text-transform: uppercase;
}
```

---

## Pre-Output Checklist

- [ ] Selected ONE visual archetype (Swiss Print OR Tactical Terminal)
- [ ] All typography is UPPERCASE for structural headers and metadata
- [ ] Zero border-radius on all elements
- [ ] Only ONE accent color (aviation red) used
- [ ] No gradients, soft shadows, or translucency
- [ ] Grid layout with visible compartmentalization
- [ ] ASCII framing and technical markers present
- [ ] Analog degradation effects applied (halftone/scanlines/noise)
- [ ] All corners are 90 degrees

---

*Part of ui-styles skill v1.0.0 — adapted from taste-skill brutalist-skill*
