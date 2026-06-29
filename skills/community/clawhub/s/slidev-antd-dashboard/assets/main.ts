// Copy to <your-slidev-project>/setup/main.ts
//
// Registers, globally for all slides:
//   - every ant-design-vue component as <a-*>
//   - every @ant-design/icons-vue icon as <icon-name-outlined /> etc.
//   - <v-chart> (ECharts) with a default set of chart + component modules
//
// ant-design-vue v4 injects component CSS automatically (CSS-in-JS), so we do
// NOT import ant-design-vue/dist/reset.css — its global preflight would clobber
// Slidev's slide typography. Theme/dark-mode is handled by AntdThemeProvider.vue.

import { defineAppSetup } from '@slidev/types'
import Antd from 'ant-design-vue'
import * as Icons from '@ant-design/icons-vue'

// --- ECharts (tree-shaken: add modules here as you need them) ---
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart, GaugeChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent,
} from 'echarts/components'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  GaugeChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent,
])

export default defineAppSetup(({ app }) => {
  app.use(Antd)

  // Register every icon globally, e.g. <user-outlined />, <dashboard-outlined />.
  // Filter to the icon components (skip helpers like setTwoToneColor / default).
  for (const [name, component] of Object.entries(Icons)) {
    if (/(Outlined|Filled|TwoTone)$/.test(name)) {
      app.component(name, component as any)
    }
  }

  app.component('VChart', VChart)
})
