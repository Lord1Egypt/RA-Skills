import type { EChartsOption } from 'echarts'

// 自定义图表模板：按 ECharts 官方 option 文档实现 buildOption 即可。
// 文档：https://echarts.apache.org/zh/option.html
export interface ChartData {
  // TODO: 定义你的数据结构
  [key: string]: unknown
}
export interface ChartConfig {
  // TODO: 定义你的配置项
  [key: string]: unknown
}

export function buildOption(_data: ChartData, _config: ChartConfig = {}): EChartsOption {
  // TODO: 返回 ECharts option
  return {}
}
