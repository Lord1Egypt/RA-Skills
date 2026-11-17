import type { EChartsOption } from 'echarts'

/** 层级数据节点，tree / treemap / sunburst 共用 */
export interface TreeNode {
  name: string
  value?: number
  children?: TreeNode[]
}
/** 对应 public/data/tree.json */
export interface ChartData {
  title?: string
  data: TreeNode
}
export interface ChartConfig {
  /** 布局方向：LR 横向 / TB 纵向，默认 LR */
  orient?: 'LR' | 'TB'
  /** 展开层级，默认全部展开 */
  initialTreeDepth?: number
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { orient = 'LR' } = config
  return {
    color: config.colors,
    tooltip: { trigger: 'item' as const, formatter: '{b}: {c}' },
    series: [
      {
        type: 'tree' as const,
        data: [data.data],
        left: '8%',
        right: '12%',
        top: '10%',
        bottom: '10%',
        orient,
        symbol: 'emptyCircle',
        symbolSize: 7,
        initialTreeDepth: config.initialTreeDepth ?? -1,
        expandAndCollapse: true,
        roam: false,
        label: { position: orient === 'LR' ? ('left' as const) : ('top' as const), color: 'inherit', fontSize: 11 },
        leaves: { label: { position: orient === 'LR' ? ('right' as const) : ('bottom' as const) } },
        emphasis: { focus: 'descendant' as const },
        animationDuration: 550,
      },
    ],
  }
}
