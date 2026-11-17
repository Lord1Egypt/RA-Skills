import type { EChartsOption } from 'echarts'

/** 对应 public/data/pie.json */
export interface ChartItem {
  name: string
  value: number
}
export interface ChartData {
  title?: string
  data: ChartItem[]
}
export interface ChartConfig {
  /** 环形半径 [内, 外]，默认 ['45%', '70%'] */
  radius?: [string, string]
  /** 玫瑰图模式 */
  roseType?: boolean
  showLegend?: boolean
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const {
    radius = ['45%', '70%'],
    roseType = false,
    showLegend = true,
  } = config
  return {
    color: config.colors,
    tooltip: { trigger: 'item' as const, formatter: '{b}: {c} ({d}%)' },
    legend: showLegend ? { bottom: 0, left: 'center' } : undefined,
    series: [
      {
        type: 'pie' as const,
        radius,
        center: ['50%', showLegend ? '45%' : '50%'],
        roseType: roseType ? ('radius' as const) : undefined,
        avoidLabelOverlap: true,
        itemStyle: { borderWidth: 2 },
        label: { color: 'inherit', formatter: '{b} {d}%' },
        labelLine: { length: 8, length2: 8 },
        emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' as const } },
        data: data.data,
      },
    ],
  }
}
