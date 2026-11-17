import type { EChartsOption } from 'echarts'

/** 对应 public/data/wordcloud.json（需安装 echarts-wordcloud 并在入口 import） */
export interface ChartItem {
  name: string
  value: number
}
export interface ChartData {
  title?: string
  data: ChartItem[]
}
export interface ChartConfig {
  /** 词形，默认 'circle'，可选 cardioid / diamond / square / triangle */
  shape?: string
  sizeRange?: [number, number]
  rotationRange?: [number, number]
  colors?: string[]
}

/**
 * echarts-wordcloud 未内置类型声明，series 用 Record 承载后整体断言。
 * 用法：npm i echarts-wordcloud，并在入口 `import 'echarts-wordcloud'`。
 */
export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const {
    shape = 'circle',
    sizeRange = [12, 42],
    rotationRange = [-45, 45],
  } = config
  const series: Record<string, unknown> = {
    type: 'wordCloud',
    shape,
    left: 'center',
    top: 'center',
    width: '96%',
    height: '92%',
    sizeRange,
    rotationRange,
    rotationStep: 15,
    gridSize: 8,
    drawOutOfBound: false,
    textStyle: {
      fontFamily: 'sans-serif',
      fontWeight: 'bold',
      color: () => {
        const palette = config.colors ?? ['#00eaff', '#37d0f0', '#7ff5ff', '#1890ff', '#69c0ff']
        return palette[Math.floor(Math.random() * palette.length)]
      },
    },
    emphasis: { textStyle: { color: '#fff' } },
    data: data.data,
  }
  return {
    tooltip: { formatter: '{b}: {c}' },
    series: [series],
  } as unknown as EChartsOption
}
