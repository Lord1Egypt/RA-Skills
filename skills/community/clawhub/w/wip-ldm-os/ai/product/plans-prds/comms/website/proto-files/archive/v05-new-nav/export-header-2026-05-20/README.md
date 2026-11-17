# Homepage header - sprite + WIP wordmark + scroll-crossfade CTA

Drop these snippets into `wip-websites-private` / `wip.computer/`. They replace
the static WIP logo image in the header with a cycling Kaleidoscope sprite +
"WORK IN PROGRESS" wordmark, and set the bar height to 55px to match the
privacy page header.

The rest of the file (hero, letter, products, footer) is untouched.

---

## 1. HTML - `wip.computer/index.html`

Replace the existing `<header class="site-header">` block with:

```html
<header class="site-header" data-screen-label="Header">
  <div class="site-header__inner">
    <a href="/" class="site-header__brand" aria-label="WIP Computer home">
      <span class="site-header__sprite" id="brandIcon" aria-hidden="true"></span>
      <span class="site-header__wordmark" style="font-size: 12px; font-weight: 700; line-height: 1">WORK IN PROGRESS</span>
    </a>
    <div class="site-header__cta" aria-hidden="true">
      <a class="btn btn--sm" href="https://wip.computer/login?next=/demo" target="_blank" rel="noopener">
        Demo Kaleidoscope
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="7" y1="17" x2="17" y2="7"></line>
          <polyline points="7 7 17 7 17 17"></polyline>
        </svg>
      </a>
    </div>
  </div>
</header>
```

Notes:
- The `<img src="assets/wip-logo.png">` is gone.
- `#brandIcon` is the sprite slot. JS fills it.
- Wordmark uses an inline `font-size: 12px` to match the privacy page's
  visual weight. It's intentionally smaller than the sprite.

---

## 2. CSS - `wip.computer/styles.css`

Replace the existing `/* ---------- Header ---------- */` section with:

```css
/* ---------- Header ---------- */
.site-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 10;
  background: transparent;
  border-bottom: 1px solid transparent;
  transition: background 220ms ease, backdrop-filter 220ms ease, border-color 220ms ease;
}
.site-header.is-scrolled {
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom-color: rgba(0, 0, 0, 0.06);
}
.site-header__inner {
  margin: 0;
  padding: 0 20px;
  height: 55px;                       /* exact match for privacy header */
  display: flex;
  align-items: center;
  justify-content: space-between;     /* sprite hugs left, button hugs right */
  gap: 24px;
}
.site-header__brand {
  display: inline-flex; align-items: center; gap: 6px;
  flex: 0 0 auto;
  color: #1a1a1a;
  text-decoration: none;
}
.site-header__sprite {
  display: inline-block;
  width: 28px;
  height: 28px;
  overflow: hidden;
  flex: 0 0 auto;
}
.site-header__sprite > div { width: 100%; height: 100%; }
.site-header__wordmark {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  font-size: 15px;                    /* inline 12px overrides this on the page */
  font-weight: 600;
  letter-spacing: -0.02em;
  line-height: 1;
  color: #1a1a1a;
  text-transform: uppercase;
  margin-left: -2px;                  /* nudges wordmark slightly under the sprite curve */
}

@media (max-width: 720px) {
  .site-header__inner { padding: 0 16px; gap: 16px; height: 55px; }
}

.site-header__cta {
  flex: 0 0 auto;
  opacity: 0;                         /* JS animates this 0 → 1 as hero CTA scrolls past */
  pointer-events: none;
  transition: none;                   /* opacity is driven by scroll position, not CSS */
}
```

The `.site-header.is-scrolled` rule fades a translucent white background +
1px bottom border in as soon as the user scrolls past 8px. Before that the
header sits transparent on top of the bucky bg.

---

## 3. JS - `wip.computer/app.js`

### 3a. Sprite cycler (add to the top of the file, before any other code)

```js
// Brand sprite (Kaleidoscope mark) - header icon next to "wip" wordmark.
// Source sprite is served alongside the homepage at /assets/sprites.png.
(function() {
  var SPRITE_COLS = 8, SPRITE_ROWS = 3, SPRITE_TOTAL = 24;
  var idx = Math.floor(Math.random() * SPRITE_TOTAL);
  function render() {
    var el = document.getElementById('brandIcon');
    if (!el) return;
    var col = idx % SPRITE_COLS;
    var row = Math.floor(idx / SPRITE_COLS);
    var bgX = (col / (SPRITE_COLS - 1)) * 100;
    var bgY = (row / (SPRITE_ROWS - 1)) * 100;
    el.innerHTML = '<div style="background:url(assets/sprites.png);background-size:' +
      (SPRITE_COLS * 100) + '% ' + (SPRITE_ROWS * 100) + '%;background-position:' +
      bgX + '% ' + bgY + '%;"></div>';
  }
  function init() {
    render();
    setInterval(function() { idx = (idx + 1) % SPRITE_TOTAL; render(); }, 6000);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

### 3b. Header CTA crossfade (existing `initHeader()` function - keep as is)

Already present. For reference, it tracks the hero CTA's vertical position
and sets `.site-header__cta.style.opacity` between 0 and 1 as the hero
button scrolls up past the fixed-header line at y=70px:

```js
function initHeader() {
  const header = document.querySelector(".site-header");
  const cta = document.querySelector(".site-header__cta");
  if (!header || !cta) return;

  let ticking = false;
  const update = () => {
    ticking = false;
    header.classList.toggle("is-scrolled", window.scrollY > 8);

    const heroCta = document.querySelector(".hero__ctas");
    const headerBottomY = 70;
    let opacity = 0;
    if (heroCta) {
      const rect = heroCta.getBoundingClientRect();
      const height = rect.height || 1;
      if (rect.top >= headerBottomY) opacity = 0;
      else if (rect.bottom <= headerBottomY) opacity = 1;
      else opacity = (headerBottomY - rect.top) / height;
    } else if (window.scrollY > 500) {
      opacity = 1;
    }
    cta.style.opacity = String(opacity);
    cta.style.pointerEvents = opacity > 0.5 ? "auto" : "none";
    cta.setAttribute("aria-hidden", opacity > 0.5 ? "false" : "true");
  };
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  };
  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", update);
}
```

Effect: as the hero's "Demo Kaleidoscope" button scrolls upward through the
header line, the header CTA fades in proportionally. The two buttons appear
to crossfade pixel-by-pixel.

---

## 4. Asset - `wip.computer/assets/sprites.png`

The Kaleidoscope sprite sheet (8 cols × 3 rows = 24 frames). Copy it from
the demo at `hosted-mcp/src/hosted-mcp/demo/sprites.png` into
`wip-websites-private/wip.computer/assets/sprites.png` so the homepage
can serve it locally without depending on nginx routing /demo/* to the
hosted-mcp app.

Included in this bundle at `assets/sprites.png`.

---

## Behavior summary

| Element | Behavior |
|---|---|
| Sprite | 28×28 cell from the 8×3 sprite sheet. Picks a random frame on load. Advances to the next frame every 6 seconds. |
| Wordmark | "WORK IN PROGRESS", uppercase, 12px / 700 weight (inline override), system-ui sans. Sits to the right of the sprite with a tight 6px gap and -2px margin-left nudge. |
| Bar height | Fixed 55px. Matches the privacy page header exactly. |
| Background | Transparent at scroll-top. Fades to translucent white + 1px black border-bottom at ≥8px scroll. |
| Right CTA | "Demo Kaleidoscope" pill button. Hidden at scroll-top (`opacity: 0`). Crossfades to fully visible as the hero's own Demo Kaleidoscope button scrolls up past the header line. |
| Left edge | Sprite hugs left edge (20px padding desktop, 16px mobile). |
| Right edge | Button hugs right edge with matching padding. |

Nothing else on the page changed.
