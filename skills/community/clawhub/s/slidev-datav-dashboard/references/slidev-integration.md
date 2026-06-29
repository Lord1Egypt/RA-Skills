# Wiring DataV into Slidev (and making it scale)

How the pieces fit, why, and the gotchas. Slidev is Vue 3 + Vite under the hood, so DataV (a Vue 3
library) drops in cleanly — the only real work is **registration**, **scaling**, and a **dark
layout**.

## Project layout (what the scaffold creates)

```
my-dashboard/
├── slides.md              # the deck (headmatter + slides)
├── package.json           # @slidev/cli + @kjgl77/datav-vue3 + scripts
├── vite.config.ts         # optimizeDeps / SSR tweaks for DataV
├── setup/
│   └── main.ts            # app.use(DataVVue3) + import dashboard.css   ← registers all Dv* tags
├── layouts/
│   └── dashboard.vue      # full-bleed dark layout (layout: dashboard)
├── styles/
│   └── dashboard.css      # palette CSS vars + panel/scrollbar styling
└── components/            # auto-imported by Slidev (no import needed in slides)
    ├── DashPanel.vue      # titled DataV border-box wrapper
    └── DashGrid.vue       # 1920×1080 CSS grid
```

Slidev auto-registers everything in `components/`, runs `setup/main.ts` before the app mounts, picks
up `layouts/*.vue` as named layouts, and merges your `vite.config.ts`.

## 1. Register DataV globally — `setup/main.ts`

```ts
import { defineAppSetup } from '@slidev/types'
import DataVVue3 from '@kjgl77/datav-vue3'
import '../styles/dashboard.css'

export default defineAppSetup(({ app }) => {
  app.use(DataVVue3)          // now <DvBorderBox13>, <DvScrollBoard>, … work in every slide
})
```

`defineAppSetup` runs **client-side**, which suits DataV (it touches the DOM/canvas). Importing the
CSS here makes the palette vars + styles global.

## 2. Make it scale — headmatter (THE key step)

Put this in the **first slide's headmatter**. It sets the design coordinate system and lets Slidev
fit the canvas to any screen:

```yaml
---
theme: default
title: 城市运营监控大屏
canvasWidth: 1920        # design width in px
aspectRatio: '16/9'      # → canvas is 1920×1080; Slidev scales it to fit the viewport
class: text-left
fonts:
  sans: Source Han Sans SC
  mono: Fira Code
---
```

Now `1px` in your CSS == `1px` on the 1920-wide canvas, regardless of the real display. Slidev
applies a single CSS `transform: scale()` to the whole slide on present/export — your job is just to
lay out at 1920×1080.

### ⚠️ Do NOT use `DvFullScreenContainer` inside Slidev

`FullScreenContainer` reads `window.innerWidth/Height` and applies its **own** `scale` transform to
hit 1920×1080. Inside Slidev that stacks on top of Slidev's transform → double-scaling, wrong sizes,
blur, mispositioned content. Slidev's `canvasWidth`/`aspectRatio` already does exactly what
FullScreenContainer does for standalone apps. Use one or the other — in Slidev, always Slidev's.

## 3. A dark, full-bleed layout — `layouts/dashboard.vue`

The default theme adds padding and a light background. The `dashboard` layout (provided in
`assets/`) makes the slide an edge-to-edge dark canvas with a gradient, and exposes a `slot` for your
grid. Use it per slide:

```md
---
layout: dashboard
---
```

## 4. Place panels — grid vs absolute

**Grid (recommended)** — `DashGrid` is a `display:grid` filling the slide; children pick cells with
`grid-column` / `grid-row`:

```html
<DashGrid :cols="24" :rows="12" gap="14px">
  <header style="grid-column:1/25; grid-row:1/2"> … title + clock … </header>
  <DashPanel title="趋势" style="grid-column:8/18; grid-row:3/9"> … </DashPanel>
</DashGrid>
```

**Absolute** — for pixel-perfect / overlapping art, position children against the 1920×1080 canvas:

```html
<div style="position:absolute; left:40px; top:120px; width:520px; height:300px"> … </div>
```

Grid is easier to keep balanced; absolute gives full control. You can mix (absolute children inside
a grid cell).

## 5. Give every DataV component a height

A grid/flex cell must pass a real height down. `DashPanel`'s body is `flex:1; min-height:0`, and you
put `style="width:100%;height:100%"` on the DataV component inside. If a chart is blank, 90% of the
time a parent has `height:auto`/0 — see `troubleshooting.md`.

## 6. Reactive data & updates

Define `reactive`/`ref` data in a **single `<script setup>` block** in `slides.md` (Slidev hoists one
per deck) or inside a component. Update charts by **replacing** the watched field:

```ts
import { reactive, ref, onMounted } from 'vue'
const flop = reactive({ number: [0], content: '{nt}' })
onMounted(() => { setInterval(() => { flop.number = [Math.round(Math.random()*9999)] }, 2000) })
```

## 7. SSR / build safety

`npm run dev` renders purely client-side → DataV always works. `npm run build` (static SPA) and
`npm run export` (PDF/PNG) do a **server render first**, where `window` doesn't exist and DataV can
throw or render empty. Two defenses (the example uses the first):

- **Gate with `onMounted`:** wrap dashboard content in `<div v-if="mounted">` and set
  `mounted=true` in `onMounted`. Skips SSR for the heavy bits; they hydrate on the client.
- **`vite.config.ts` ssr.noExternal:** bundle DataV for SSR so its ESM resolves
  (provided in `assets/vite.config.ts`). Combine both for robust builds.

## 8. Export & present

```bash
npm run dev            # localhost:3030, live reload — primary authoring loop
npm run export         # slidev export → PDF (add --format png for images)
npm run export -- --scale 2   # 2× for crisp big-screen PDFs/PNGs
npm run build          # static SPA in dist/ → host on any static server / video-wall browser
```

Presenter view (`P`), overview (`O`), and dark mode are built in. For a real video wall, open the
`build` output full-screen in a kiosk browser — `canvasWidth`/`aspectRatio` keeps it pixel-correct.

## 9. Multiple dashboards in one deck

Each slide is independent. Make a deck of screens (overview → drill-down → detail) by repeating
`layout: dashboard` slides separated by `---`. Navigate with arrow keys, or `clicks`/`v-click` if
you want progressive reveal *within* a screen (use sparingly — see design rules on motion).

## Reference

- Slidev — configure Vue app: https://sli.dev/custom/config-vue
- Slidev — components in slides: https://sli.dev/guide/component
- Slidev — Vite config: https://sli.dev/custom/config-vite
- DataV Vue3 docs: https://datav-vue3.netlify.app
