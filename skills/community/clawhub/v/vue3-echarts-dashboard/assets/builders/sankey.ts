import type { EChartsOption } from 'echarts'

/** 对应 public/data/sankey.json */
export interface ChartNode {
  name: string
}
export interface ChartLink {
  source: string
  target: string
  value: number
}
export interface ChartData {
  title?: string
  nodes: ChartNode[]
  links: ChartLink[]
}
export interface ChartConfig {
  /** 节点对齐方式 */
  nodeAlign?: 'justify' | 'left' | 'right'
  nodeGap?: number
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { nodeAlign = 'justify', nodeGap = 8 } = config
  return {
    color: config.colors,
    tooltip: { trigger: 'item' as const, triggerOn: 'mousemove' as const },
    series: [
      {
        type: 'sankey' as const,
        left: 8,
        right: 8,
        top: 12,
        bottom: 12,
        nodeAlign,
        nodeGap,
        nodeWidth: 12,
        draggable: false,
        emphasis: { focus: 'adjacency' as const },
        label: { color: 'inherit', fontSize: 11 },
        lineStyle: { color: 'gradient' as const, opacity: 0.35, curveness: 0.5 },
        data: data.nodes,
        links: data.links,
      },
    ],
  }
}
