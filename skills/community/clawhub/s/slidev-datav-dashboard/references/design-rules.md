# 大屏 (Large-Screen Dashboard) Design Rules

How to make a DataV dashboard look like a professional command center, not a web page. Distilled
from Chinese big-screen design guides (人人都是产品经理, 即时设计, FineReport/帆软, FIT2CLOUD).

## Three principles: 聚焦 · 平衡 · 简洁 (focus · balance · simplicity)

- **聚焦 Focus** — one screen answers one question. The single most important metric is the
  largest element and sits at the optical center (or center-top). Everything else supports it.
- **平衡 Balance** — distribute visual weight symmetrically; mirror left/right columns; keep panel
  sizes on a rhythm. Avoid a heavy corner.
- **简洁 Simplicity** — show extracted indicators, not raw tables. Generous spacing. If a viewer
  3 meters away can't read it in 5 seconds, simplify.

## Color

**Dark base, bright data.** Deep navy/black background; high-saturation accents for the data so
figures pop. This is the defining look of 大屏.

**60 / 30 / 10 rule:** 60% dominant (the dark background + panel fills), 30% secondary (borders,
gridlines, dim text, secondary series), 10% accent (the hero numbers, the active series, alarms).
**Keep to ≤ 3 main hues.** Differentiate by **brightness + saturation**, never by adjacent hues.

Reserve a dedicated **status palette**: success/green, warning/amber, danger/red — used *only* for
state, never decoratively.

### Ready-to-use palettes (drop into `styles/dashboard.css`)

```css
/* A) Tech Blue — the classic monitoring screen (default) */
:root {
  --dv-bg:        #07142b;   /* page background */
  --dv-bg-2:      #0b1a2c;   /* gradient stop */
  --dv-panel:     rgba(12, 30, 60, 0.45);  /* panel fill behind borders */
  --dv-text:      #c9e0ff;   /* primary text */
  --dv-text-dim:  #7fa6cc;   /* labels, axes */
  --dv-primary:   #00baff;   /* hero / main series */
  --dv-secondary: #3de7c9;   /* second series */
  --dv-accent:    #f7b500;   /* highlight */
  --dv-success:   #2ed47a;
  --dv-warning:   #ffb02e;
  --dv-danger:    #ff5b5b;
  --dv-line:      #16314e;   /* gridlines / dividers */
}

/* B) Deep Space Purple — sleek, "AI/data" feel */
:root.theme-purple {
  --dv-bg: #0a0a1f; --dv-bg-2: #12122e; --dv-panel: rgba(40,28,80,.4);
  --dv-text: #e6e1ff; --dv-text-dim: #9d93c7;
  --dv-primary: #8b6cff; --dv-secondary: #21d4fd; --dv-accent: #ff6ac6;
  --dv-line: #241a44;
}

/* C) Command Green — terminal / situational-awareness feel */
:root.theme-green {
  --dv-bg: #04130c; --dv-bg-2: #07241a; --dv-panel: rgba(8,40,28,.42);
  --dv-text: #c7ffe6; --dv-text-dim: #6fbf9b;
  --dv-primary: #2effa0; --dv-secondary: #3df0e7; --dv-accent: #c8ff00;
  --dv-line: #0d3a2a;
}
```

Pass these into DataV components, e.g. `:color="['var(--dv-primary)', 'var(--dv-secondary)']"`
won't work inside DataV's canvas — DataV needs literal colors. So define a JS palette object too and
feed components real hex values:

```ts
export const palette = {
  primary: '#00baff', secondary: '#3de7c9', accent: '#f7b500',
  text: '#c9e0ff', dim: '#7fa6cc', line: '#16314e',
  series: ['#00baff', '#3de7c9', '#f7b500', '#fb7293', '#9b8bff', '#2ed47a'],
}
```

## Layout

Design on a **1920 × 1080** canvas (16:9). Use a 12- or 24-column grid with consistent gutters
(12–16 px). Three archetypes:

### Center-focus (situational / single subject)
```
┌──────────────────────── HEADER : title · clock · status ────────────────────────┐
├──────────────── KPI row : 4–6 DigitalFlop ─────────────────────────────────────┤
│ ┌────────┐ ┌────────────────────────────┐ ┌────────┐ │
│ │ rank   │ │                            │ │ ring   │ │
│ │ board  │ │    HERO: map / big chart   │ │ gauges │ │
│ ├────────┤ │   (largest, center stage)  │ ├────────┤ │
│ │ capsule│ │                            │ │ scroll │ │
│ └────────┘ └────────────────────────────┘ └────────┘ │
└────────────────────────────────────────────────────────────────────────────────┘
```

### Three-column (overview / monitoring)
Equal-weight left | center | right columns, each a vertical stack of 2–3 panels. Center column
slightly wider for the main chart. This skill's example deck uses this.

### Left-right (comparison / before-after)
Two big halves, mirrored. Good for A/B or region-vs-region.

**Rules:** key metric center & biggest · secondary indicators orbit by priority · align everything to
the grid · equal gutters · leave breathing room (don't fill 100%) · group related panels visually.

## Typography

- **Numbers are the star.** Use a technical/“digital” face for figures: DIN, Orbitron, DS-Digital,
  Bebas Neue, or `Rajdhani`. `DvDigitalFlop` already renders crisp animated numerals.
- **Labels/body:** a clean sans — 思源黑体 / Source Han Sans, 微软雅黑, PingFang, or system
  `ui-sans-serif`. One title face + one body face, max.
- **Hierarchy by size & brightness:** hero number 40–64px, panel titles 16–20px, axis/labels
  12–14px and dimmed (`--dv-text-dim`). Avoid pure white text on dark — use `#c9e0ff`-ish to reduce
  glare.
- **Loading a webfont in Slidev** — either via headmatter:
  ```yaml
  fonts:
    sans: 'Source Han Sans SC'
    # Slidev fetches Google Fonts automatically for known families
  ```
  or `@import` in `styles/dashboard.css`:
  ```css
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');
  .dv-num { font-family: 'Orbitron', 'DIN', ui-monospace, monospace; font-variant-numeric: tabular-nums; }
  ```

## Motion (restraint)

DataV components animate by default (scroll boards cycle, rings rotate, numbers tween). That's
plenty. **Don't add Slidev click-animations to dashboard panels** — a 大屏 is "always on", not a
click-through. Keep ambient motion subtle and continuous; avoid anything that flashes or distracts
from reading values. Reserve motion spikes for genuine alarms.

## Backgrounds & depth

- Base: a subtle **radial/linear gradient** (lighter toward the focal area) over the dark base — see
  `layouts/dashboard.vue`. Avoid flat pure-black (looks dead) and avoid busy photo backgrounds.
- Optional: faint grid lines, a low-opacity world-map or hex texture, soft glows behind the hero.
- Panels float above the base via translucent fills (`--dv-panel`) + glowing DataV border boxes.

## Accessibility / readability

- Maintain strong contrast for **data**, even while text is slightly muted. Target ≥ 4.5:1 for any
  number a viewer must read.
- Don't encode meaning by hue alone (color-blind safety) — pair color with position, label, or
  shape (e.g., ▲/▼ for up/down alongside green/red).
- Test at the **real display size and distance**. What's legible on a laptop can vanish on a
  6 m video wall — bump font sizes and weights accordingly.

## Quick checklist before you ship

- [ ] Dark base + ≤ 3 hues + a separate status (R/A/G) palette
- [ ] One clear hero metric, largest, centered
- [ ] Everything on the 1920×1080 grid with equal gutters
- [ ] Numbers in a technical face; labels dimmed; nothing pure-white
- [ ] Panels balanced left/right; related items grouped
- [ ] Ambient motion only; no click-throughs on the dashboard slide
- [ ] Readable in 5 seconds from across the room
