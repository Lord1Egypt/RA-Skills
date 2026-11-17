/** 大屏数据契约（与 public/data/*.json 一一对应） */

/** KPI 数字翻牌卡 */
export interface KpiItem {
  label: string
  value: number
  suffix?: string
  separator?: string
  decimal?: string
  toFixedNum?: number
  delta?: string
}

/** 折线/柱状类：分类 + 单序列 */
export interface CategorySeries {
  name: string
  unit: string
  categories: string[]
  values: number[]
}

/** 饼图/环形图 */
export interface PieData {
  unit: string
  items: Array<{ name: string; value: number }>
}

/** 雷达图 */
export interface RegionData {
  name: string
  indicators: Array<{ name: string; max: number }>
  values: number[]
}

/** 漏斗图 */
export interface FunnelData {
  name: string
  unit: string
  items: Array<{ name: string; value: number }>
}

/** 仪表盘 */
export interface GaugeData {
  name: string
  value: number
  max: number
  unit: string
}

/** 散点图 */
export interface ScatterPoint {
  x: number
  y: number
}
export interface ScatterData {
  name: string
  xName: string
  yName: string
  points: ScatterPoint[]
}

/** 旭日图（层级结构） */
export interface SunburstDatum {
  name: string
  value: number
  children?: SunburstDatum[]
}
export interface SunburstData {
  name: string
  unit: string
  items: SunburstDatum[]
}

/** 桑基图 */
export interface SankeyNode {
  name: string
}
export interface SankeyLink {
  source: string
  target: string
  value: number
}
export interface SankeyData {
  name: string
  nodes: SankeyNode[]
  links: SankeyLink[]
}

/** 树图（结构与旭日图同源） */
export interface TreeData {
  name: string
  unit: string
  items: SunburstDatum
}

/** 热力图（x=列索引，y=行索引，value=数值） */
export interface HeatmapCell {
  x: number
  y: number
  value: number
}
export interface HeatmapData {
  name: string
  unit: string
  series: string[]
  categories: string[]
  values: HeatmapCell[]
}

/** 地图（省级 name 与 geoJSON 的 properties.name 对应） */
export interface MapData {
  name: string
  unit: string
  items: Array<{ name: string; value: number }>
}

/** 词云 */
export interface WordcloudData {
  name: string
  items: Array<{ name: string; value: number }>
}

/** 大屏全部初始化数据 */
export interface DashboardData {
  kpis: KpiItem[]
  trend: CategorySeries
  product: PieData
  channel: CategorySeries
  profit: CategorySeries
  region: RegionData
  funnel: FunnelData
  gauge: GaugeData
  scatter: ScatterData
  sunburst: SunburstData
  sankey: SankeyData
  tree: TreeData
  heatmap: HeatmapData
  map: MapData
  wordcloud: WordcloudData
}
