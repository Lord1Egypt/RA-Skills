import type { EChartsOption } from 'echarts'

/** 对应 public/data/gauge.json */
export interface ChartData {
  title?: string
  name?: string
  value: number
  max?: number
  unit?: string
}
export interface ChartConfig {
  /** 进度条颜色分段，默认 [[0.6,'#3fb1e3'],[0.8,'#37a2da'],[1,'#00eaff']] */
  axisColors?: [number, string][]
  colors?: string[]
  /** 数值小数位，默认 1 */
  precision?: number
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { precision = 1 } = config
  const main = config.colors?.[0] ?? '#00eaff'
  const axisColors = config.axisColors ?? [
    [0.6, '#3fb1e3'],
    [0.8, '#37a2da'],
    [1, main],
  ]
  return {
    color: config.colors,
    series: [
      {
        type: 'gauge' as const,
        center: ['50%', '55%'],
        radius: '82%',
        min: 0,
        max: data.max ?? 100,
        startAngle: 210,
        endAngle: -30,
        progress: { show: true, width: 12, itemStyle: { color: main } },
        axisLine: { lineStyle: { width: 12, color: axisColors } },
        axisTick: { distance: -18, length: 6, lineStyle: { color: 'auto', width: 1 } },
        splitLine: { distance: -22, length: 12, lineStyle: { color: 'auto', width: 2 } },
        axisLabel: { distance: 22, color: 'inherit', fontSize: 10 },
        pointer: { icon: 'triangle', width: 8, length: '55%', offsetCenter: [0, '5%'], itemStyle: { color: main } },
        anchor: { show: true, size: 12, itemStyle: { color: main } },
        title: { offsetCenter: [0, '32%'], fontSize: 12, color: 'inherit' },
        detail: {
          valueAnimation: true,
          offsetCenter: [0, '-8%'],
          fontSize: 26,
          fontWeight: 'bold' as const,
          color: main,
          formatter: (v: number) => `${v.toFixed(precision)}${data.unit ?? ''}`,
        },
        data: [{ value: data.value, name: data.name ?? data.title ?? '' }],
      },
    ],
  }
}
