# Modern Effects Catalogue — Native CSS

A reference library of production-usable effects. Each entry includes the mechanism, working code, browser-support notes, and — critically — the `prefers-reduced-motion` or `@supports` fallback it needs. **Use one signature effect per screen, not all of them at once** — see the restraint note in `SKILL.md`.

Full working demos of most of these are in `examples/effects-showcase.html` + `.css`.

## Glassmorphism

Frosted-glass surface: semi-transparent background + `backdrop-filter: blur()` + a thin light border to sell the "glass edge."

```css
.glass-panel {
  background: rgb(255 255 255 / 0.08);
  backdrop-filter: blur(16px) saturate(140%);
  -webkit-backdrop-filter: blur(16px) saturate(140%);
  border: 1px solid rgb(255 255 255 / 0.15);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}
```

**Support**: `backdrop-filter` has broad modern support but is genuinely expensive to composite — avoid stacking many blurred layers in a scrollable list (each one is a separate GPU compositing pass). Reserve for headers, modals, and a handful of hero cards, not every card in a grid.

**Fallback**: `@supports not (backdrop-filter: blur(1px))" { .glass-panel { background: rgb(30 30 34 / 0.92); } }` — a plain translucent panel reads fine without the blur.

## Layered / mesh gradients

A single linear gradient reads as a template default. Layering multiple radial gradients at different positions and blend modes produces a mesh-gradient look with zero images:

```css
.mesh-bg {
  background:
    radial-gradient(at 20% 20%, oklch(70% 0.15 250 / 0.6) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(75% 0.18 320 / 0.5) 0px, transparent 50%),
    radial-gradient(at 50% 100%, oklch(65% 0.16 180 / 0.4) 0px, transparent 50%),
    var(--color-bg);
}
```

Animated conic gradient border (uses the `@property` technique from `css-architecture-bem.md`):

```css
@property --angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.gradient-border {
  position: relative;
  border-radius: var(--radius-lg);
}

.gradient-border::before {
  content: "";
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: conic-gradient(from var(--angle), #3a5fff, #7c3aed, #3a5fff);
  z-index: -1;
  animation: spin-border 4s linear infinite;
}

@keyframes spin-border {
  to { --angle: 360deg; }
}
```

## Elevation / shadow scale

Don't invent a shadow per component — reuse the token scale from `css-architecture-bem.md` (`--shadow-xs` through `--shadow-lg`), reserving the larger values for genuinely floating elements (modals, dropdowns, popovers). Colored shadows (shadow tinted toward the element's own hue rather than pure black) read as more polished for brand-forward cards:

```css
.card--branded {
  box-shadow: 0 8px 24px oklch(55% 0.2 265 / 0.25);
}
```

## Scroll-driven animations (native, no JS/library)

`animation-timeline: scroll()` and `view()` drive an animation's progress directly from scroll position — no `IntersectionObserver`, no scroll-linked JS needed for the common cases.

**Reveal-on-scroll** (element fades/slides in as it enters the viewport):

```css
.reveal {
  opacity: 0;
  transform: translateY(24px);
  animation: reveal-in linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}

@keyframes reveal-in {
  to { opacity: 1; transform: translateY(0); }
}
```

**Progress indicator tied to page scroll**:

```css
.scroll-progress {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  background: var(--color-primary);
  transform-origin: left;
  animation: grow-progress linear;
  animation-timeline: scroll(root);
}

@keyframes grow-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

**Support**: `animation-timeline` is Chromium-first with growing but not universal support. Always pair with a fallback so content isn't invisible on unsupported browsers:

```css
@supports not (animation-timeline: view()) {
  .reveal { opacity: 1; transform: none; animation: none; }
}
```

**Required guard** — scroll-driven and parallax effects are exactly the ones most likely to trigger motion discomfort:

```css
@media (prefers-reduced-motion: reduce) {
  .reveal, .scroll-progress, .parallax-layer {
    animation: none !important;
    opacity: 1;
    transform: none;
  }
}
```

## Parallax

CSS-only parallax via `perspective` + `translateZ`, no JS scroll listener (which is expensive and jank-prone compared to letting the compositor handle it):

```css
.parallax-container {
  perspective: 1px;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
}

.parallax-layer {
  position: relative;
  transform-style: preserve-3d;
}

.parallax-layer--back {
  transform: translateZ(-1px) scale(2); /* moves slower than scroll */
}

.parallax-layer--base {
  transform: translateZ(0);
}
```

Use sparingly — parallax is exactly the kind of effect that reads as a tech demo if applied to more than one section per page, and is a common `prefers-reduced-motion` violation if not guarded.

## Micro-interactions

The difference between a UI that feels "alive" and one that feels inert is almost entirely in hover/focus/active transitions on small, frequent interactions — not big showcase animations.

```css
.button {
  transition: transform var(--duration-fast) var(--ease-standard),
              box-shadow var(--duration-fast) var(--ease-standard),
              background-color var(--duration-fast) var(--ease-standard);
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.button:active {
  transform: translateY(0);
  transition-duration: 50ms;
}

.button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

Keep these fast (`--duration-fast`, 100–200ms) — a micro-interaction that takes 400ms+ feels laggy rather than responsive. Reserve `--duration-slow` for larger state changes (panel open/close, page transitions).

## 3D transforms

Tilt-on-hover card, a common signature-moment effect for a single hero element:

```css
.tilt-card {
  transform-style: preserve-3d;
  transition: transform var(--duration-base) var(--ease-standard);
  will-change: transform;
}

.tilt-card:hover {
  transform: perspective(800px) rotateX(6deg) rotateY(-6deg) scale(1.02);
}
```

For a mouse-tracked tilt (rotation follows cursor position rather than a fixed hover angle), a small amount of JS is required — CSS alone can't read pointer coordinates:

```js
const card = document.querySelector(".tilt-card");
card.addEventListener("pointermove", (e) => {
  const rect = card.getBoundingClientRect();
  const x = (e.clientX - rect.left) / rect.width - 0.5;
  const y = (e.clientY - rect.top) / rect.height - 0.5;
  card.style.setProperty("--rx", `${y * -12}deg`);
  card.style.setProperty("--ry", `${x * 12}deg`);
});
card.addEventListener("pointerleave", () => {
  card.style.setProperty("--rx", "0deg");
  card.style.setProperty("--ry", "0deg");
});
```

```css
.tilt-card {
  transform: perspective(800px) rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg));
}
```

## Complex multi-stage `@keyframes`

Beyond a simple two-state fade, multi-stage keyframes let a single animation carry a full narrative beat (useful for a signature loading state or an empty-state illustration):

```css
@keyframes pulse-and-settle {
  0%   { transform: scale(0.9); opacity: 0; }
  40%  { transform: scale(1.05); opacity: 1; }
  70%  { transform: scale(0.98); }
  100% { transform: scale(1); }
}

.badge--new {
  animation: pulse-and-settle 600ms var(--ease-standard) both;
}
```

For looping ambient motion (e.g. a subtle floating illustration), keep the amplitude small and the duration long — fast, large-amplitude looping motion reads as distracting rather than ambient:

```css
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.illustration--ambient {
  animation: float 6s ease-in-out infinite;
}
```

## CSS Houdini

### `@property` — use freely, excellent support

Already covered in `css-architecture-bem.md`. This is the workhorse Houdini feature for production use: it's what makes animating gradient angles, custom-property-driven color transitions, and similar effects actually interpolate instead of snapping.

### Paint API — Chromium-first, needs a fallback

Lets you write a JS worklet that paints directly into an element's background/border, generating patterns without images or extra DOM nodes.

```js
// dotted-pattern.js — registered as a paint worklet
class DottedPattern {
  static get inputProperties() { return ["--dot-color", "--dot-size"]; }
  paint(ctx, size, props) {
    const color = props.get("--dot-color").toString().trim() || "#000";
    const dotSize = parseFloat(props.get("--dot-size").toString()) || 2;
    const gap = dotSize * 4;
    ctx.fillStyle = color;
    for (let x = 0; x < size.width; x += gap) {
      for (let y = 0; y < size.height; y += gap) {
        ctx.beginPath();
        ctx.arc(x, y, dotSize, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
}
registerPaint("dottedPattern", DottedPattern);
```

```js
// main.js
if ("paintWorklet" in CSS) {
  CSS.paintWorklet.addModule("/dotted-pattern.js");
}
```

```css
.dotted-bg {
  --dot-color: var(--color-border);
  --dot-size: 1.5px;
  background-image: paint(dottedPattern);
}

/* Fallback for browsers without Paint API support (Firefox, older Safari) */
@supports not (background: paint(dottedPattern)) {
  .dotted-bg {
    background-image: radial-gradient(var(--color-border) 1px, transparent 1px);
    background-size: 12px 12px;
  }
}
```

Note the fallback above actually achieves a near-identical dotted pattern with a plain `radial-gradient` — a good illustration that Paint API is often a "nicer mechanism," not the only way to get an effect. Reach for it when the pattern genuinely needs procedural/parametric generation (irregular, data-driven, or interactive patterns), not for anything a gradient can already do.

## Checklist before shipping an effects-heavy screen

- [ ] Exactly one signature effect anchors this screen — everything else is quiet
- [ ] Every scroll-driven, parallax, or large-motion effect has a `prefers-reduced-motion` fallback
- [ ] Every Chromium-first feature (Paint API, some `animation-timeline` usage) has an `@supports` fallback that still looks intentional, not broken
- [ ] `backdrop-filter` usage is limited to a few elements at a time, not stacked across a scrollable list
- [ ] Micro-interaction durations are fast (100–200ms); only intentional showcase animations run longer
