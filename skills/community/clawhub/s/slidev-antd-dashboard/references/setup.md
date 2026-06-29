# Setup: ant-design-vue in Slidev

Tested against **Slidev v52+**, **ant-design-vue v4.2.x**, **Vue 3**, Node ≥ 18.

## 1. Create / have a Slidev project

```bash
npm init slidev@latest        # scaffolds a Slidev project
cd my-slides
```

A Slidev project has `slides.md` at its root, plus optional `setup/`, `components/`, `styles/` directories that Slidev auto-discovers.

## 2. Install dependencies

```bash
npm i ant-design-vue@^4.2.6 @ant-design/icons-vue
npm i echarts vue-echarts          # charts — see §Charts
# optional, only if you want AntV's Ant-Design-styled plots instead of ECharts:
# npm i @antv/g2plot
```

## 3. Register the plugin: `setup/main.ts`

Slidev runs your Vue app; extend it with `defineAppSetup`. Copy `assets/main.ts` to `setup/main.ts`. It does three things:

```ts
import { defineAppSetup } from '@slidev/types'
import Antd from 'ant-design-vue'
import * as Icons from '@ant-design/icons-vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart, GaugeChart } from 'echarts/charts'
import {
  GridComponent, TooltipComponent, LegendComponent, TitleComponent, DatasetComponent,
} from 'echarts/components'

use([
  CanvasRenderer, BarChart, LineChart, PieChart, GaugeChart,
  GridComponent, TooltipComponent, LegendComponent, TitleComponent, DatasetComponent,
])

export default defineAppSetup(({ app }) => {
  app.use(Antd)                                   // all <a-*> components
  Object.entries(Icons).forEach(([n, c]) => app.component(n, c as any)) // all icons globally
  app.component('VChart', VChart)                 // <v-chart :option="..."/>
})
```

> **Why register everything globally?** These slides are local artifacts — bundle size is irrelevant. Global registration means any slide can use any `<a-*>`, any `<icon-outlined>`, and `<v-chart>` with no per-slide `import`. (For a production app you'd import per-component instead.)

### Do NOT globally import `reset.css`

ant-design-vue v4 injects component styles via **CSS-in-JS** automatically — components look correct with no CSS import. The bundled `ant-design-vue/dist/reset.css` is a global *preflight* (resets `h1`, `p`, `a`, `body`, etc.) that **will override Slidev's slide typography and theme**. Leave it out. If a specific antd component looks unstyled (rare), import its reset locally and scope it; do not import it globally in `setup/`.

## 4. Theme + dark-mode wrapper: `components/AntdThemeProvider.vue`

Copy `assets/AntdThemeProvider.vue` to `components/`. It wraps content in `<a-config-provider>`, sets design tokens (primary color, radius), default component size, and **syncs antd's dark algorithm to Slidev's dark mode**. Wrap every dashboard slide's content in it:

```html
<AntdThemeProvider>
  <!-- dashboard here -->
</AntdThemeProvider>
```

## 5. Headmatter: give dashboards room

A Slidev slide is a fixed canvas; the default `canvasWidth: 980` is too narrow for desktop-density dashboards. Render at a wider canvas and let Slidev scale the whole slide to the viewport. In `slides.md` headmatter (the first frontmatter block):

```yaml
---
theme: default
canvasWidth: 1280     # 1280 or 1440 for dashboards; Slidev scales to fit
aspectRatio: 16/9
---
```

For one-off slides that need more room, use a per-slide `zoom`:

```yaml
---
layout: full
zoom: 0.85
---
```

See [dashboard-rules.md](dashboard-rules.md#fitting-a-dashboard-onto-a-slide) for the full sizing strategy.

## Using components in a slide

In Slidev markdown you write Vue directly. Reactive data goes in a `<script setup>` block at the **top of that slide**:

```md
---
layout: full
---

<script setup>
import { ref } from 'vue'
const selectedKeys = ref(['1'])
const data = [{ key: 1, name: 'Acme', mrr: 4200, status: 'active' }]
const columns = [
  { title: 'Account', dataIndex: 'name', key: 'name' },
  { title: 'MRR', dataIndex: 'mrr', key: 'mrr' },
  { title: 'Status', key: 'status' },
]
</script>

<AntdThemeProvider>
  <a-table :columns="columns" :data-source="data" size="small" :pagination="false">
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'status'">
        <a-tag :color="record.status === 'active' ? 'green' : 'default'">{{ record.status }}</a-tag>
      </template>
    </template>
  </a-table>
</AntdThemeProvider>
```

## Charts

Ant Design has no chart components. Two good options for Slidev:

### A) ECharts via `vue-echarts` (recommended)

Most robust, dashboard-standard, great defaults, easy theming. `<v-chart>` is registered globally in `main.ts`. In a slide:

```md
<script setup>
const revenue = {
  tooltip: { trigger: 'axis' },
  grid: { left: 40, right: 16, top: 24, bottom: 24 },
  xAxis: { type: 'category', data: ['Jan','Feb','Mar','Apr','May','Jun'] },
  yAxis: { type: 'value' },
  series: [{ type: 'line', smooth: true, data: [820,932,901,934,1290,1330], areaStyle: {} }],
}
</script>

<v-chart :option="revenue" style="height: 240px" autoresize />
```

Always give `<v-chart>` an explicit pixel **height** (it has none by default). Add chart/component modules to the `use([...])` list in `main.ts` as you need them (e.g. `ScatterChart`, `RadarChart`, `MarkLineComponent`).

### B) AntV `@antv/g2plot` (matches Ant Design visuals)

Framework-agnostic; mount into a `ref` in `onMounted`. Use when you want pixel-matched Ant Design chart styling. Heavier to wire than ECharts.

> Skip the community `ant-design-charts-vue` wrapper unless you specifically need it — it lags the React original and is less maintained.

## React `antd` → `ant-design-vue` translation

If you're porting a React `antd` design, apply these mechanical changes:

| React `antd` | `ant-design-vue` |
|---|---|
| `<Button type="primary">` | `<a-button type="primary">` (all components gain the `a-` prefix) |
| `import { Button } from 'antd'` | nothing — registered globally as `<a-button>` |
| `onChange={fn}` / `onClick` | `@change="fn"` / `@click` (Vue events) |
| controlled `value` + `onChange` | `v-model:value="x"` (Input/Select/DatePicker) |
| controlled `checked` | `v-model:checked="x"` (Switch/Checkbox) |
| `<Menu selectedKeys>` | `v-model:selectedKeys` / `v-model:openKeys` |
| `dataSource={data}` | `:data-source="data"` |
| `columns={[{ render: (v,r)=>… }]}` | `#bodyCell` slot (`<template #bodyCell="{ column, record }">`) |
| `title={<X/>}` (render prop) | named slot (`<template #title>…</template>`) |
| `<ConfigProvider theme={{token}}>` | `<a-config-provider :theme="{ token }">` |
| `message.success()` / `Modal.confirm()` | same imperative API: `import { message, Modal } from 'ant-design-vue'` |
| `theme.darkAlgorithm` | `import { theme } from 'ant-design-vue'` → `theme.darkAlgorithm` |
| icons `import { UserOutlined } from '@ant-design/icons'` | `@ant-design/icons-vue`, used as `<user-outlined />` (registered globally) |

## Pitfalls

- **Wrong prefix.** It's `<a-table>`, not `<Table>`. Global registration adds `a-`.
- **No chart height.** `<v-chart>` collapses to 0 px without an explicit height.
- **Imported reset.css.** Breaks Slidev typography — don't (see §3).
- **Wiring `a-menu` to Slidev's router.** Slidev owns routing (slide nav). Keep dashboard menus on local `ref` state (`v-model:selectedKeys`) — they're mockups, not a real router.
- **Dashboard too small / cramped.** Raise `canvasWidth` (1280–1440) and/or use `componentSize="small"`; don't shrink fonts manually. See dashboard-rules.md.
- **Interactivity in PDF export.** Live slides are interactive (tabs, dropdowns, sortable tables work). `slidev export` to PDF freezes them in their default state — set the state you want to show as the default.
- **Icons not found.** They live in `@ant-design/icons-vue` (note the `-vue`), not `@ant-design/icons`.
- **Modals/drawers/overlays** render to `document.body` by default and can escape the scaled slide canvas. Pass `:get-popup-container` / `:get-container` to anchor them inside the slide if positioning looks off.
