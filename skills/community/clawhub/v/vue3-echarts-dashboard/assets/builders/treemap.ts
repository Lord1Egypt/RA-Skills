import type { EChartsOption } from 'echarts'

/** 层级数据节点，与 tree / sunburst 共用同一结构 */
export interface TreeNode {
  name: string
  value?: number
  children?: TreeNode[]
}
export interface ChartData {
  title?: string
  data: TreeNode
}
export interface ChartConfig {
  /** 是否开启上钻 */
  roam?: boolean
  /** 面包屑导航，默认显示 */
  breadcrumb?: boolean
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { roam = false, breadcrumb = true } = config
  return {
    color: config.colors,
    tooltip: { formatter: '{b}: {c}' },
    series: [
      {
        type: 'treemap' as const,
        data: [data.data],
        roam,
        breadcrumb: breadcrumb ? { show: true, bottom: 0 } : { show: false },
        nodeClick: 'zoomToNode' as const,
        leafDepth: 1,
        visibleMin: 0,
        label: { show: true, formatter: '{b}', fontSize: 11 },
        upperLabel: { show: true, height: 20, color: 'inherit' },
        itemStyle: { borderColor: 'rgba(0,0,0,0.25)', borderWidth: 1, gapWidth: 1 },
        levels: [
          { itemStyle: { borderWidth: 0, gapWidth: 4 } },
          { itemStyle: { gapWidth: 1 }, colorSaturation: [0.32, 0.55] },
        ],
        animationDuration: 400,
      },
    ],
  }
}
