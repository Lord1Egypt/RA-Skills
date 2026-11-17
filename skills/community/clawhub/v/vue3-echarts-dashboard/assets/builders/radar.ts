import type { EChartsOption } from 'echarts'

/** 对应 public/data/radar.json */
export interface ChartIndicator {
  name: string
  max?: number
}
export interface ChartSeries {
  name: string
  data: number[]
}
export interface ChartData {
  title?: string
  indicator: ChartIndicator[]
  series: ChartSeries[]
}
export interface ChartConfig {
  showLegend?: boolean
  /** 填充透明度，默认 0.25 */
  areaOpacity?: number
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { showLegend = true, areaOpacity = 0.25 } = config
  return {
    color: config.colors,
    tooltip: { trigger: 'item' as const },
    legend: showLegend ? { data: data.series.map((s) => s.name), bottom: 0 } : undefined,
    radar: {
      indicator: data.indicator,
      center: ['50%', '52%'],
      radius: '65%',
      splitNumber: 4,
      axisName: { color: 'inherit' },
    },
    series: [
      {
        type: 'radar' as const,
        areaStyle: { opacity: areaOpacity },
        emphasis: { focus: 'series' as const },
        data: data.series.map((s) => ({ name: s.name, value: s.data })),
      },
    ],
  }
}
