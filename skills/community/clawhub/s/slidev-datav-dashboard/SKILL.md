---
name: slidev-datav-dashboard
description: >-
  Build large-screen data-visualization dashboards (大屏 / 数据大屏 / 可视化大屏) as Slidev
  presentations using the datav-vue3 (DataV) component library. Use when the user wants a
  data dashboard, monitoring/command-center screen, or visualization deck built with Slidev —
  covers all 39 DataV components (border-boxes, decorations, ScrollBoard, DigitalFlop, Charts,
  ActiveRingChart, WaterLevelPond, etc.), dark-theme 大屏 design rules, 1920×1080 canvas
  scaling, ready-to-use layout/panel assets, a worked example deck, and a one-command scaffold.
---

# Slidev × DataV 大屏 (Large-Screen Dashboard) Skill

Build a sci-fi / command-center **data dashboard ("大屏")** as a **Slidev** deck, using
**`@kjgl77/datav-vue3`** — the maintained Vue 3 port of the classic [DataV](http://datav.jiaminghi.com/)
component library (border boxes, decorations, scroll boards, digital flops, gauges, water-level
pools, flyline maps, …).

## What this produces

A Slidev project whose slides are full-screen dark dashboards: glowing DataV border-box panels
arranged on a 1920×1080 grid, filled with live-updating DataV charts and indicators, that you can
present, export to PDF/PNG, or build to a static SPA.

## When to use

Trigger on requests like: "用 slidev 做一个 datav 大屏", "make a data dashboard / 数据大屏 / 监控大屏",
"command-center visualization screen", "DataV border box + charts deck", "可视化大屏 with Slidev".

## ⚠️ The one rule that makes Slidev + DataV work

DataV's `FullScreenContainer` scales itself to `window` and **fights Slidev's own canvas
transform** — never use it inside a slide. Instead, let **Slidev** do the scaling:

```yaml
# deck headmatter (first slide)
canvasWidth: 1920      # design at 1920 px wide …
aspectRatio: '16/9'    # … → 1080 px tall; Slidev auto-fits it to any screen
```

Then design every panel against **1920×1080 absolute coordinates** (a grid or absolute
positioning) on a dark, full-bleed `layout`. Slidev rescales the whole canvas to fit the viewport
on present/export. See `references/slidev-integration.md`.

The second rule: **every DataV component needs an explicit width & height** from its container
(`style="width:100%;height:100%"` inside a sized panel, or explicit px). A box with no height
renders blank.

## Workflow

1. **Scaffold** a pre-wired Slidev project:
   `bash scripts/init-dashboard.sh my-dashboard` → `cd my-dashboard && npm run dev`.
   (This copies the `assets/` wiring + the example deck and runs `npm install`.)
2. **Pick a palette + layout archetype** from `references/design-rules.md` (dark base, 60/30/10
   color split, center-focus / three-column). Set CSS vars in `styles/dashboard.css`.
3. **Place panels** on the `DashGrid` using the `DashPanel` wrapper (a titled DataV border box).
   Choose border boxes & decorations from `references/components.md`.
4. **Bind data**: give each DataV chart its `:config` / `:option` reactive object (verified
   shapes in `references/components.md`). Update data by *replacing* the object/array, not mutating.
5. **Preview & export**: `npm run dev` to iterate; `npm run export` (PDF/PNG) or `npm run build`
   (static SPA). See troubleshooting for crisp exports & SSR notes.

## Quick start (manual, without the script)

```bash
npm init slidev@latest        # or: npm i -D @slidev/cli @slidev/theme-default vue
npm i @kjgl77/datav-vue3
# then copy these from this skill's assets/ into the project:
#   assets/setup/main.ts        -> setup/main.ts        (registers DataV globally + loads CSS)
#   assets/vite.config.ts       -> vite.config.ts       (optimizeDeps / SSR for DataV)
#   assets/layouts/dashboard.vue.md-> layouts/dashboard.vue.md (dark full-bleed layout)
#   assets/styles/dashboard.css -> styles/dashboard.css  (palette vars + panel styling)
#   assets/components/*.vue.md     -> components/           (DashPanel, DashGrid)
# set headmatter: canvasWidth: 1920, aspectRatio: '16/9', then build slides.md
```

Global registration (already in `assets/setup/main.ts`):

```ts
import { defineAppSetup } from '@slidev/types'
import DataVVue3 from '@kjgl77/datav-vue3'
import '../styles/dashboard.css'

export default defineAppSetup(({ app }) => {
  app.use(DataVVue3)   // registers DvBorderBox1…13, DvDecoration1…12, DvScrollBoard, DvCharts, …
})
```

## Files in this skill

| Path | Read it when you need… |
| --- | --- |
| `references/components.md` | The full catalog of all **39 DataV components** — tag names, props, `config`/`option` shapes, copy-paste examples, and which one to pick. |
| `references/design-rules.md` | 大屏 **design spec**: dark theme, 60/30/10 color rule, 3 ready palettes, layout archetypes + wireframes, typography (numeric fonts), grid & spacing. |
| `references/slidev-integration.md` | **Wiring & scaling recipe**: headmatter, `setup/main.ts`, custom layout, grid vs absolute placement, exporting, SSR/`onMounted` notes, the FullScreenContainer gotcha. |
| `references/troubleshooting.md` | Symptom → fix table: blank/0-height components, charts not updating, fonts, build/SSR errors, blurry exports, overflow. |
| `assets/` | Copy-paste-ready project files: `setup/main.ts`, `vite.config.ts`, `layouts/dashboard.vue.md`, `styles/dashboard.css`, `components/DashPanel.vue.md`, `components/DashGrid.vue.md`. |
| `templates/slides.example.md` | A complete, runnable **"城市运营监控大屏"** deck — the reference example to copy and adapt. |
| `templates/package.json` | Dependency + scripts template (`dev` / `build` / `export`). |
| `scripts/init-dashboard.sh` | One command that assembles all of the above into a fresh, runnable Slidev project. |

## Component cheat-sheet (full details in `references/components.md`)

All components are registered globally with a `Dv` prefix; kebab-case (`<dv-border-box-13>`) and
PascalCase (`<DvBorderBox13>`) both resolve.

- **Border (13):** `DvBorderBox1` … `DvBorderBox13` — props `:color="[main, sub]"`, `backgroundColor`.
- **Decoration (12):** `DvDecoration1` … `DvDecoration12` — props `:color`, some `reverse` / `dur`.
- **Data / charts (Other):** `DvDigitalFlop` (翻牌器), `DvScrollBoard` (轮播表), `DvScrollRankingBoard`
  (排名), `DvCapsuleChart` (胶囊柱), `DvActiveRingChart` (动态环), `DvWaterLevelPond` (水位),
  `DvPercentPond` (进度池), `DvConicalColumnChart` (锥形柱), `DvCharts` (通用图表，传 `:option`),
  `DvFlylineChart` / `DvFlylineChartEnhanced` (飞线地图), `DvLoading`, `DvButton`,
  `DvFullScreenContainer` (⚠️ standalone apps only — **not** inside Slidev slides).
