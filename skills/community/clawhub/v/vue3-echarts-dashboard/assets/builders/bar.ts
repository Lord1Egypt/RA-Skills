import type { EChartsOption } from 'echarts'

/** 对应 public/data/bar.json（纵向多系列柱状） */
export interface ChartSeries {
  name: string
  data: number[]
}
export interface ChartData {
  title?: string
  categories: string[]
  series: ChartSeries[]
}
export interface ChartConfig {
  stack?: boolean
  showLegend?: boolean
  /** 圆角，默认 [4, 4, 0, 0] */
  radius?: number | number[]
  /** 横向柱状（类目轴放 Y 轴），默认 false */
  horizontal?: boolean
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { stack = false, showLegend = true, horizontal = false, radius = [4, 4, 0, 0] } = config
  const catAxis = { type: 'category' as const, data: data.categories }
  const valAxis = { type: 'value' as const }
  return {
    color: config.colors,
    tooltip: { trigger: 'axis' as const, axisPointer: { type: 'shadow' as const } },
    legend: showLegend ? { data: data.series.map((s) => s.name) } : undefined,
    grid: { left: '3%', right: '4%', bottom: '3%', top: showLegend ? '14%' : '8%', containLabel: true },
    xAxis: horizontal ? valAxis : catAxis,
    yAxis: horizontal ? catAxis : valAxis,
    series: data.series.map((s) => ({
      name: s.name,
      type: 'bar' as const,
      stack: stack ? 'total' : undefined,
      barMaxWidth: 24,
      itemStyle: { borderRadius: horizontal ? [0, 4, 4, 0] : radius },
      emphasis: { focus: 'series' as const },
      data: s.data,
    })),
  }
}
