# Troubleshooting: Slidev + DataV 大屏

Symptom → cause → fix. Most issues are **sizing** or **SSR**.

## Component renders blank / collapsed (0 height)

- **Cause:** the parent passed no height. DataV components are `100%` of their parent; if an ancestor
  is `height:auto` they get `0`.
- **Fix:** ensure a sized chain. The cell (`grid-row` span or fixed px) → `DashPanel` body
  (`flex:1; min-height:0`) → the component (`style="width:100%;height:100%"`). For a one-off, set
  explicit px: `style="width:320px;height:220px"`.
- **Also:** content placed *inside a border box* must be a **component**, not raw inline DOM —
  slot-mounted DOM can measure `0` in `onMounted`. `DashPanel` handles this; if you bypass it, wrap
  your chart in its own `.vue`.

## Component measured wrong after a parent resize

- **Cause:** the box cached its size and didn't observe the parent change (e.g., toggling
  presenter/overview, or a CSS change).
- **Fix:** grab the box via `ref` and call its exposed **`initWH()`** instead of re-keying it
  (re-keying destroys/re-creates inner charts and loses state).

## Chart doesn't update when data changes

- **Cause:** DataV watches the `config`/`option` **reference**; a deep mutation may not trigger.
- **Fix:** **replace** the field: `config.value = next` / `config.data = [...next]` /
  `option.series = [...]`. Make the object `reactive`. Don't push into a deeply-nested array and
  expect a redraw — reassign the array.

## `<DvXxx>` is "unknown custom element" / not registered

- **Cause:** `app.use(DataVVue3)` didn't run, or `setup/main.ts` is misplaced.
- **Fix:** confirm `setup/main.ts` exists at project root `setup/main.ts` and exports
  `defineAppSetup`. Restart `npm run dev` after adding it. Verify the import:
  `import DataVVue3 from '@kjgl77/datav-vue3'`.

## Everything is double-scaled / blurry / mispositioned

- **Cause:** using `DvFullScreenContainer` inside Slidev — it adds its own `window` scale on top of
  Slidev's canvas transform.
- **Fix:** remove `FullScreenContainer`; rely on headmatter `canvasWidth: 1920` + `aspectRatio:
  '16/9'` and lay out at 1920×1080. (FullScreenContainer is only for standalone Vue apps.)

## Layout overflows the slide / panels clipped

- **Cause:** absolute coordinates exceed 1920×1080, or grid spans sum past your `cols`/`rows`.
- **Fix:** keep all `left+width ≤ 1920`, `top+height ≤ 1080`. With `DashGrid :cols="24" :rows="12"`,
  `grid-column` ends at `25` and `grid-row` at `13` (grid lines are 1-indexed and one past the last
  track). Add `overflow:hidden` on panels to clip gracefully.

## `npm run build` / `npm run export` errors or blank panels (works in dev)

- **Cause:** SSR (build/export render on the server first) — `window`/`document` undefined for DataV.
- **Fix (combine both):**
  1. Gate heavy content: `<div v-if="mounted">…</div>` with `const mounted = ref(false);
     onMounted(() => mounted.value = true)`.
  2. Keep `ssr: { noExternal: ['@kjgl77/datav-vue3'] }` in `vite.config.ts` (in `assets/`).
- If export still blanks, prefer `npm run export` from a running build, or screenshot from
  `npm run dev` full-screen.

## `DvCharts` looks wrong / option keys ignored

- **Cause:** treating it as **ECharts**. `DvCharts` uses `@jiaminghi/charts`, a different (smaller)
  option dialect.
- **Fix:** use CRender keys — text color is `style.fill`, lines `style.stroke`; series area is
  `lineArea`, gradients `gradient`. See `components.md` → `DvCharts`, and
  http://charts.jiaminghi.com/config/. It is **not** a drop-in for ECharts options.

## Fonts not applying (numbers look like default sans)

- **Cause:** webfont not loaded, or applied to text but not DataV's canvas-drawn numbers.
- **Fix:** load the face (`@import` in `dashboard.css` or `fonts:` headmatter). For `DvDigitalFlop`,
  the numerals are SVG/canvas-styled via `config.style.fill`/`fontSize`, not CSS `font-family` — set
  size/color through `config.style`. For HTML text, apply `.dv-num { font-family: … }`.

## Flyline map is empty

- **Cause:** no `bgImgUrl`, or `points` positions not in 0–1 relative coords.
- **Fix:** supply a map image as `config.bgImgUrl`; set each point `position: [x, y]` with `x,y ∈
  [0,1]` relative to that image; enable `:dev="true"` to read coordinates while placing. No map asset
  → use `DvCharts` instead.

## Colors from CSS vars don't show inside a DataV chart

- **Cause:** DataV draws to canvas/SVG and can't read CSS custom properties.
- **Fix:** pass **literal** colors (hex/rgb) to `:color`/`:config`/`:option`. Keep a JS `palette`
  object (see `design-rules.md`) mirroring your CSS vars and feed those values to components.

## Dev server port / theme install

- `npm run dev` defaults to `http://localhost:3030`. Add `--port 4000` to change.
- First run may prompt to install the theme — accept, or pre-install
  `@slidev/theme-default` (already in the template `package.json`).
