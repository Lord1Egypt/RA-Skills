import type { EChartsOption } from 'echarts'

/** 对应 public/data/heatmap.json（x 轴=时段，y 轴=星期，data 为二维数值矩阵） */
export interface ChartData {
  title?: string
  xAxis: string[]
  yAxis: string[]
  data: number[][]
}
export interface ChartConfig {
  min?: number
  max?: number
  /** 是否在格子内显示数值 */
  showLabel?: boolean
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { showLabel = false } = config
  const flat = data.data.flat()
  const min = config.min ?? Math.min(...flat)
  const max = config.max ?? Math.max(...flat)
  const cells: [number, number, number][] = []
  data.data.forEach((row, y) => row.forEach((v, x) => cells.push([x, y, v])))
  return {
    tooltip: {
      position: 'top',
      formatter: (p: unknown) => {
        const q = p as { data: [number, number, number] }
        return `${data.yAxis[q.data[1]]} · ${data.xAxis[q.data[0]]}<br/>活跃量：${q.data[2]}`
      },
    },
    grid: { left: '8%', right: '6%', top: '8%', bottom: '14%', containLabel: true },
    xAxis: { type: 'category', data: data.xAxis, splitArea: { show: true } },
    yAxis: { type: 'category', data: data.yAxis, splitArea: { show: true } },
    visualMap: {
      min,
      max,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      itemWidth: 10,
      itemHeight: 80,
      inRange: { color: config.colors ?? ['#0a2a4a', '#1565a8', '#1e9bd6', '#37d0f0', '#7ff5ff'] },
    },
    series: [
      {
        type: 'heatmap',
        data: cells,
        label: showLabel ? { show: true, fontSize: 9 } : undefined,
        emphasis: { itemStyle: { borderColor: '#fff', borderWidth: 1 } },
      },
    ],
  }
}
