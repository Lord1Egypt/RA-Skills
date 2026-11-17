// 大屏各接口的响应数据类型定义

export interface Metric {
  key: string
  label: string
  value: number
  unit?: string
  prefix?: string
}

export interface OverviewResp {
  updatedAt: string
  metrics: Metric[]
}

export interface TrendSeries {
  name: string
  data: number[]
}

export interface TrendResp {
  title: string
  xAxis: string[]
  series: TrendSeries[]
}

export interface CategoryResp {
  title: string
  categories: string[]
  data: number[]
}

export interface PieItem {
  name: string
  value: number
}

export interface PieResp {
  title: string
  data: PieItem[]
}

export interface RankingResp {
  title: string
  list: PieItem[]
}

// 仪表盘（单指标完成率）
export interface GaugeResp {
  title: string
  name: string
  value: number
  max: number
  unit?: string
}

// 雷达图
export interface RadarIndicator {
  name: string
  max: number
}
export interface RadarSeries {
  name: string
  data: number[]
}
export interface RadarResp {
  title: string
  indicator: RadarIndicator[]
  series: RadarSeries[]
}

// 漏斗图
export interface FunnelResp {
  title: string
  data: PieItem[]
}

// 柱状图（可多系列，纵向）
export interface BarSeries {
  name: string
  data: number[]
}
export interface BarResp {
  title: string
  categories: string[]
  series: BarSeries[]
}

// 热力图（天 × 时段 活跃度矩阵）
export interface HeatmapResp {
  title: string
  xAxis: string[] // 横轴（时段）
  yAxis: string[] // 纵轴（星期）
  data: number[][] // 与 xAxis/yAxis 对齐的二维矩阵
}

// 桑基图
export interface SankeyNode {
  name: string
}
export interface SankeyLink {
  source: string
  target: string
  value: number
}
export interface SankeyResp {
  title: string
  nodes: SankeyNode[]
  links: SankeyLink[]
}

// 树图 / 旭日图共用的层级结构
export interface TreeData {
  name: string
  value?: number
  children?: TreeData[]
}
export interface TreeResp {
  title: string
  data: TreeData
}
export interface SunburstResp {
  title: string
  data: TreeData
}

// 地图（ECharts 内置 map 系列 + 本地 geoJSON）
export interface MapItem {
  name: string
  value: number
}
export interface MapResp {
  title: string
  mapName: string // 与 echarts.registerMap 注册的名称一致
  data: MapItem[]
}

// 词云
export interface WordCloudResp {
  title: string
  data: MapItem[]
}

// 水球图（value 为 0~1 的比例）
export interface LiquidFillResp {
  title: string
  name: string
  value: number
}
