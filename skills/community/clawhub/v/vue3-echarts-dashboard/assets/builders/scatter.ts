import type { EChartsOption } from 'echarts'

/** 散点图：series 每项的 data 为 [x, y] 或 [x, y, size] */
export interface ChartSeries {
  name: string
  data: (number[])[]
}
export interface ChartData {
  title?: string
  series: ChartSeries[]
}
export interface ChartConfig {
  showLegend?: boolean
  symbolSize?: number
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { showLegend = true, symbolSize = 10 } = config
  return {
    color: config.colors,
    tooltip: { trigger: 'item' as const },
    legend: showLegend ? { data: data.series.map((s) => s.name), bottom: 0 } : undefined,
    grid: { left: '6%', right: '8%', top: '10%', bottom: '14%', containLabel: true },
    xAxis: { type: 'value' as const, scale: true },
    yAxis: { type: 'value' as const, scale: true },
    series: data.series.map((s) => ({
      name: s.name,
      type: 'scatter' as const,
      symbolSize,
      emphasis: { focus: 'series' as const },
      data: s.data,
    })),
  }
}
