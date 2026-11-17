import type { EChartsOption } from 'echarts'

/** 对应 public/data/liquidfill.json（value 取值 0~1，需安装 echarts-liquidfill） */
export interface ChartData {
  title?: string
  name?: string
  value: number
}
export interface ChartConfig {
  /** 波纹数量，默认 3 */
  waveCount?: number
  /** 外圈边框宽度 */
  outlineWidth?: number
  colors?: string[]
  /** 数值小数位，默认 1（显示为百分比） */
  precision?: number
}

/**
 * echarts-liquidfill 未内置类型声明，series 用 Record 承载后整体断言。
 * 用法：npm i echarts-liquidfill，并在入口 `import 'echarts-liquidfill'`。
 */
export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { waveCount = 3, outlineWidth = 2, precision = 1 } = config
  const palette = config.colors ?? ['#00eaff', '#37d0f0', '#1890ff']
  const series: Record<string, unknown> = {
    type: 'liquidFill',
    radius: '88%',
    center: ['50%', '50%'],
    amplitude: 8,
    waveAnimation: true,
    animationDuration: 1200,
    outline: {
      show: true,
      borderDistance: 4,
      itemStyle: { borderColor: palette[0], borderWidth: outlineWidth },
    },
    backgroundStyle: { color: 'rgba(255,255,255,0.04)' },
    color: Array.from({ length: waveCount }, (_, i) => palette[i % palette.length]),
    label: {
      formatter: () => `${(data.value * 100).toFixed(precision)}%`,
      fontSize: 28,
      fontWeight: 'bold',
      color: palette[0],
      insideColor: '#fff',
    },
    data: [
      { value: data.value, name: data.name ?? data.title ?? '' },
      ...Array.from({ length: Math.max(0, waveCount - 1) }, (_, i) => ({
        value: Math.max(0, data.value - 0.03 * (i + 1)),
      })),
    ],
  }
  return { series: [series] } as unknown as EChartsOption
}
