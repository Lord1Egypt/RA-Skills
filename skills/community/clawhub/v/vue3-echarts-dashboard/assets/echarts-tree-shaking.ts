/**
 * ECharts 体积优化版（tree-shaking）。
 * 完整包 'echarts' 约 1MB+；按需引入可砍到几十 KB。
 *
 * 用法：
 *   1. 在 main.ts 或单独的 echarts-setup.ts 里调用一次 use([...]) 注册用到的模块。
 *   2. 把 use-echarts.ts 顶部的 `import * as echarts from 'echarts'`
 *      改为 `import { init } from 'echarts/core'`，类型从 'echarts/core' 取。
 *   3. 业务 builder 里用 `ECOption` 替代 `EChartsOption`。
 *
 * 注意：新增图表类型 / 组件时，记得在下面 use([...]) 同步注册，否则会报
 * "Component xxx is used but not imported." 或图表空白。
 *
 * 插件型图表（不走本文件注册，需单独安装并全量引入）：
 *   npm i echarts-wordcloud echarts-liquidfill
 *   import 'echarts-wordcloud'    // 挂载 wordCloud series
 *   import 'echarts-liquidfill'   // 挂载 liquidFill series
 * 两者内部自带注册逻辑，import 一次即可；不要与下面的 use([...]) 混用。
 * map 类型已按内置图表注册（MapChart），但地图 geoJSON 数据需自行 registerMap。
 */
import { use } from 'echarts/core'
import { CanvasRenderer, SVGRenderer } from 'echarts/renderers'
import {
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  RadarChart,
  GaugeChart,
  FunnelChart,
  HeatmapChart,
  SankeyChart,
  TreemapChart,
  SunburstChart,
  MapChart,
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  RadarComponent,
  VisualMapComponent,
} from 'echarts/components'
import type { ComposeOption } from 'echarts/core'
import type {
  LineSeriesOption,
  BarSeriesOption,
  PieSeriesOption,
  ScatterSeriesOption,
  RadarSeriesOption,
  GaugeSeriesOption,
  FunnelSeriesOption,
  HeatmapSeriesOption,
  SankeySeriesOption,
  TreemapSeriesOption,
  SunburstSeriesOption,
} from 'echarts/charts'
import type {
  TitleComponentOption,
  TooltipComponentOption,
  GridComponentOption,
  LegendComponentOption,
  DataZoomComponentOption,
  RadarComponentOption,
  VisualMapComponentOption,
} from 'echarts/components'

use([
  CanvasRenderer,
  SVGRenderer,
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  RadarChart,
  GaugeChart,
  FunnelChart,
  HeatmapChart,
  SankeyChart,
  TreemapChart,
  SunburstChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  RadarComponent,
  VisualMapComponent,
])

export type ECOption = ComposeOption<
  | LineSeriesOption
  | BarSeriesOption
  | PieSeriesOption
  | ScatterSeriesOption
  | RadarSeriesOption
  | GaugeSeriesOption
  | FunnelSeriesOption
  | HeatmapSeriesOption
  | SankeySeriesOption
  | TreemapSeriesOption
  | SunburstSeriesOption
  | MapSeriesOption
  | TitleComponentOption
  | TooltipComponentOption
  | GridComponentOption
  | LegendComponentOption
  | DataZoomComponentOption
  | RadarComponentOption
  | VisualMapComponentOption
>
