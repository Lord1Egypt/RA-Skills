import type { EChartsOption } from 'echarts'

/** 对应 public/data/category.json（单系列横向柱状，常用于渠道/排行对比） */
export interface ChartData {
  title?: string
  categories: string[]
  data: number[]
}
export interface ChartConfig {
  showLabel?: boolean
  colors?: string[]
  /** 主色，用于渐变条（缺省取 colors[0]） */
  primary?: string
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { showLabel = true } = config
  const primary = config.primary ?? config.colors?.[0] ?? '#00eaff'
  return {
    color: config.colors,
    tooltip: { trigger: 'axis' as const, axisPointer: { type: 'shadow' as const } },
    grid: { left: '3%', right: '10%', top: '6%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value' as const },
    yAxis: {
      type: 'category' as const,
      data: data.categories,
      inverse: true,
      axisLine: { show: false },
      axisTick: { show: false },
    },
    series: [
      {
        type: 'bar' as const,
        barMaxWidth: 18,
        showBackground: true,
        backgroundStyle: { color: 'rgba(255,255,255,0.04)' },
        label: showLabel ? { show: true, position: 'right' as const, color: primary } : undefined,
        itemStyle: {
          borderRadius: [0, 4, 4, 0],
          color: {
            type: 'linear' as const,
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: 'rgba(255,255,255,0.08)' },
              { offset: 1, color: primary },
            ],
          },
        },
        data: data.data,
      },
    ],
  }
}
