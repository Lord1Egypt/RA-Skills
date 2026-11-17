import type { EChartsOption } from 'echarts'

/** 对应 public/data/funnel.json */
export interface ChartItem {
  name: string
  value: number
}
export interface ChartData {
  title?: string
  data: ChartItem[]
}
export interface ChartConfig {
  /** 排序：'descending' | 'ascending' | 'none'，默认 none（按数据顺序） */
  sort?: 'descending' | 'ascending' | 'none'
  /** 是否显示转化率标签，默认 true */
  showLabel?: boolean
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { sort = 'none', showLabel = true } = config
  return {
    color: config.colors,
    tooltip: { trigger: 'item' as const, formatter: '{b}: {c}' },
    legend: { bottom: 0, data: data.data.map((d) => d.name) },
    series: [
      {
        type: 'funnel' as const,
        top: '8%',
        bottom: '16%',
        left: '10%',
        width: '80%',
        minSize: '20%',
        sort,
        gap: 2,
        label: showLabel ? { position: 'inside' as const, formatter: '{b}: {c}' } : undefined,
        itemStyle: { borderWidth: 0 },
        emphasis: { label: { fontSize: 14 } },
        data: data.data,
      },
    ],
  }
}
