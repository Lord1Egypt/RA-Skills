import type { EChartsOption } from 'echarts'

export interface ChartData {
  /** 趋势序列（sparkline），如近 N 天的值 */
  trend: number[]
  /** 主指标值（大数字，可字符串如 '1.2w'） */
  value?: number | string
  /** 指标名称 */
  name?: string
  /** 目标值（仅作占位，可与 value 一起由页面展示） */
  target?: number
}
export interface ChartConfig {
  area?: boolean
  color?: string
  showTrend?: boolean
}

/**
 * KPI 卡片图：大数字（title）+ 迷你趋势线（sparkline）。
 * 与 funnel / sunburst / sankey / heatmap 共享同一业务数据集时可互相印证：
 * value 取漏斗顶层、trend 取该指标时间序列。
 */
export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { area = true, color = '#409EFF', showTrend = true } = config
  const hasTrend = showTrend && data.trend.length > 0
  return {
    title: data.name
      ? {
          text: String(data.value ?? ''),
          subtext: data.name,
          left: hasTrend ? 'left' : 'center',
          top: hasTrend ? '12%' : 'center',
          textStyle: { fontSize: hasTrend ? 28 : 36, fontWeight: 'bold', color },
          subtextStyle: { fontSize: 13, color: '#909399' },
        }
      : undefined,
    grid: hasTrend ? { left: 0, right: 0, top: '55%', bottom: 0 } : undefined,
    xAxis: hasTrend ? { type: 'category', show: false, boundaryGap: false } : undefined,
    yAxis: hasTrend ? { type: 'value', show: false } : undefined,
    series: hasTrend
      ? [
          {
            type: 'line',
            data: data.trend,
            showSymbol: false,
            smooth: true,
            lineStyle: { color, width: 2 },
            areaStyle: area ? { color, opacity: 0.15 } : undefined,
          },
        ]
      : [],
  }
}
