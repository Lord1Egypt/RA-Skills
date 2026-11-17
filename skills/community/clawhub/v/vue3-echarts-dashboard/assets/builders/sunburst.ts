import type { EChartsOption } from 'echarts'

/** 层级数据节点，与 tree / treemap 共用同一结构 */
export interface TreeNode {
  name: string
  value?: number
  children?: TreeNode[]
}
/** 对应 public/data/sunburst.json */
export interface ChartData {
  title?: string
  data: TreeNode
}
export interface ChartConfig {
  /** 圆心，默认 ['50%','52%'] */
  center?: [string, string]
  /** 半径，默认 ['18%','78%'] */
  radius?: [string, string]
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { center = ['50%', '52%'], radius = ['18%', '78%'] } = config
  return {
    color: config.colors,
    tooltip: { formatter: '{b}: {c}' },
    series: [
      {
        type: 'sunburst' as const,
        data: data.data.children ?? [data.data],
        radius,
        center,
        sort: undefined,
        emphasis: { focus: 'ancestor' as const },
        label: { rotate: 'tangential' as const, fontSize: 10, minAngle: 12, color: 'inherit' },
        levels: [
          {},
          { r0: radius[0], r: '38%', itemStyle: { borderWidth: 2 }, label: { rotate: 'tangential' as const } },
          { r0: '38%', r: '58%', label: { align: 'right' as const } },
          { r0: '58%', r: radius[1], label: { position: 'outside' as const, padding: 3, silent: false } },
        ],
      },
    ],
  }
}
