import type { EChartsOption } from 'echarts'

/** 对应 public/data/trend.json */
export interface ChartSeries {
  name: string
  data: number[]
}
export interface ChartData {
  title?: string
  xAxis: string[]
  series: ChartSeries[]
}
export interface ChartConfig {
  smooth?: boolean
  area?: boolean
  stack?: boolean
  showLegend?: boolean
  /** 调色板，覆盖整套系列色 */
  colors?: string[]
  /** 主色，用于面积渐变（缺省取 colors[0]） */
  primary?: string
}

function withAlpha(color: string, alpha: number): string {
  if (!color.startsWith('#')) return color
  const hex = color.slice(1)
  const full =
    hex.length === 3
      ? hex
          .split('')
          .map((c) => c + c)
          .join('')
      : hex
  const num = parseInt(full, 16)
  const r = (num >> 16) & 255
  const g = (num >> 8) & 255
  const b = num & 255
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { smooth = true, area = false, stack = false, showLegend = true } = config
  const primary = config.primary ?? config.colors?.[0] ?? '#00eaff'
  return {
    color: config.colors,
    tooltip: { trigger: 'axis' },
    legend: showLegend ? { data: data.series.map((s) => s.name) } : undefined,
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: showLegend ? '16%' : '8%',
      containLabel: true,
    },
    xAxis: { type: 'category', boundaryGap: !area, data: data.xAxis },
    yAxis: { type: 'value' },
    series: data.series.map((s, i) => {
      const c = config.colors?.[i] ?? (i === 0 ? primary : undefined)
      return {
        name: s.name,
        type: 'line' as const,
        smooth,
        showSymbol: !area,
        stack: stack ? 'total' : undefined,
        emphasis: { focus: 'series' as const },
        lineStyle: c ? { width: 2, color: c } : undefined,
        itemStyle: c ? { color: c } : undefined,
        areaStyle: area
          ? {
              opacity: 0.18,
              color: {
                type: 'linear' as const,
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: withAlpha(primary, 0.45) },
                  { offset: 1, color: withAlpha(primary, 0) },
                ],
              },
            }
          : undefined,
        data: s.data,
      }
    }),
  }
}
