# Layout Patterns — Native CSS

Structural patterns for the pieces almost every production UI needs. Adapt, don't paste verbatim — see the worked full examples in `examples/header.html`/`.css` and `examples/dashboard.html`/`.css` for complete, working versions of the header and dashboard patterns below.

## Sticky, blurred header

The most common production header pattern: sticky on scroll, translucent with backdrop blur once content scrolls beneath it, mobile nav collapses to a toggled panel.

```css
.header {
  position: sticky;
  top: 0;
  z-index: 40;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
  padding-inline: var(--space-6);
  background: color-mix(in srgb, var(--color-bg) 80%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
}

.header__nav {
  display: none;
  gap: var(--space-8);
}

@media (min-width: 768px) {
  .header__nav { display: flex; }
  .header__mobile-toggle { display: none; }
}
```

Mobile nav panel (togglable, no JS framework required — a checkbox hack or ~10 lines of vanilla JS toggling a class both work; prefer the JS toggle for correct `aria-expanded` state):

```html
<button class="header__mobile-toggle" aria-expanded="false" aria-controls="mobile-nav">
  <span class="sr-only">Toggle menu</span>
  <svg aria-hidden="true"><!-- hamburger icon --></svg>
</button>
<nav id="mobile-nav" class="mobile-nav" data-open="false">
  <a class="mobile-nav__link" href="#features">Features</a>
  <a class="mobile-nav__link" href="#pricing">Pricing</a>
</nav>
```

```js
const toggle = document.querySelector(".header__mobile-toggle");
const nav = document.querySelector(".mobile-nav");
toggle.addEventListener("click", () => {
  const isOpen = nav.dataset.open === "true";
  nav.dataset.open = String(!isOpen);
  toggle.setAttribute("aria-expanded", String(!isOpen));
});
```

## Dashboard shell (sidebar + topbar)

CSS Grid template areas give a dashboard shell that's readable at a glance and trivially reflows for mobile — no wrapper-div nesting needed.

```css
.dashboard {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: 3.5rem 1fr;
  grid-template-areas:
    "sidebar topbar"
    "sidebar main";
  min-height: 100svh;
}

.dashboard__sidebar { grid-area: sidebar; border-right: 1px solid var(--color-border); }
.dashboard__topbar { grid-area: topbar; border-bottom: 1px solid var(--color-border); }
.dashboard__main { grid-area: main; overflow-y: auto; padding: var(--space-6); }

/* Collapse to a slide-over sidebar under 768px rather than squeezing columns */
@media (max-width: 767px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-areas:
      "topbar"
      "main";
  }
  .dashboard__sidebar {
    position: fixed;
    inset: 0 25% 0 0;
    transform: translateX(-100%);
    transition: transform var(--duration-base) var(--ease-standard);
    z-index: 50;
  }
  .dashboard__sidebar[data-open="true"] { transform: translateX(0); }
}
```

## Responsive card grid with container queries

Container queries respond to the *parent's* width, not the viewport — correct for a card grid that might sit in a full-width page or a narrow sidebar. No plugin needed; this is a native browser feature.

```css
.card-grid {
  container-type: inline-size;
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr;
}

@container (min-width: 480px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}

@container (min-width: 768px) {
  .card-grid { grid-template-columns: repeat(3, 1fr); }
}
```

## Landing hero rhythm

```css
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-6);
  max-width: 48rem;
  margin-inline: auto;
  padding-block: var(--space-16);
}

.hero__title {
  font-family: var(--font-display);
  font-size: clamp(var(--text-3xl), 5vw, var(--text-5xl));
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
```

`clamp()` for hero type is worth using deliberately: it fluidly scales between a mobile floor and a desktop ceiling without a media-query staircase, and reads as more considered than a hard breakpoint jump.

## Sticky footer pattern (footer stays at bottom on short pages)

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100svh;
}
main { flex: 1; }
```

## Checklist

- [ ] Header behavior (sticky, blur) tested with real scrollable content, not just at the top of the page
- [ ] Mobile nav toggle sets `aria-expanded` correctly, not just a visual class swap
- [ ] Dashboard sidebar collapse tested at 767px and 360px specifically, not just "resized until it looked okay"
- [ ] Card grids use container queries where the component's context width varies (sidebar-adjacent placement), viewport media queries where it doesn't
