# 2026-05-18 Mobile Layout Overflow Repair Pattern

## Trigger

After the PC/m top-navigation fixes, the user reported that `https://m.900az.com/` looked bad on mobile. Initial screenshots showed:

- top navigation visually clipped when dynamic menu items exceeded the viewport;
- `每日推荐` two-column cards clipped on the right;
- `攻略` two-card row clipped on the right;
- app/game list text areas at risk of pushing download buttons or overflowing.

## Durable Lesson

For xz01 mobile visual QA, do not stop at ordinary headless `--window-size` screenshots. They can misrepresent mobile layout when the browser is not truly in mobile device mode. Use Chrome DevTools Protocol (CDP) device emulation for final validation:

```text
Emulation.setDeviceMetricsOverride({ width: 360/390/430, height: ..., deviceScaleFactor: 2, mobile: true })
Network.setUserAgentOverride(real iPhone/Android UA)
Page.captureScreenshot(...)
```

Pair screenshot review with runtime layout probes:

```js
document.documentElement.clientWidth
document.documentElement.scrollWidth
document.body.scrollWidth
```

Then enumerate body elements whose bounding boxes exceed the viewport, excluding intended internal scrollers such as `.xz-m-nav`.

## CSS Repair Pattern

Use a small, explicit mobile-only CSS override at the end of the mobile stylesheet. Prefer fixing layout constraints over hiding overflow globally.

Key rules:

1. Header nav with many dynamic menu items should be an internal horizontal scroller:
   - `.xz-m-nav { overflow-x:auto; flex-wrap:nowrap; }`
   - `.xz-m-nav a { flex:0 0 auto; white-space:nowrap; }`
   - hide scrollbar if desired;
   - body/page `scrollWidth` must still equal `clientWidth`.
2. Two-column mobile modules must be true responsive grids:
   - `.xz-m-recom-grid`, `.xz-m-strategy-top`, `.xz-m-album-grid`
   - `display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:...; min-width:0; max-width:100%;`
3. Card children must be shrink-safe:
   - `.xz-m-recom-card`, `.xz-m-strategy-top a`, `.xz-m-album-card { min-width:0; max-width:100%; overflow:hidden; }`
   - long text should use ellipsis.
4. List rows must not let text push buttons out:
   - row container `display:flex; min-width:0; overflow:hidden;`
   - icon/button `flex:0 0 auto;`
   - info text area `flex:1; min-width:0;`
   - title/desc/meta ellipsis.
5. Decorative hero/orbit pseudo-elements must not create horizontal overflow.

## Validation Gate

For mobile homepage layout fixes, pass requires all of the following:

- CDP mobile-mode screenshots at least 390px; preferably also 360px and 430px.
- AI visual review of first viewport and long screenshot.
- Runtime widths show no page-level horizontal overflow:
  - `documentElement.scrollWidth === documentElement.clientWidth`
  - `body.scrollWidth === documentElement.clientWidth`
- Overflow probe finds zero non-nav elements outside the viewport.
- Internal `.xz-m-nav` horizontal overflow is acceptable only when it is intentional and scrollable.

## Pitfall

A screenshot captured with only `chromium --headless --window-size=390,...` can make a fixed/desktop viewport behave differently from a real mobile viewport. If it contradicts CDP mobile-mode metrics, trust CDP mobile-mode plus runtime layout probes for final mobile acceptance.
