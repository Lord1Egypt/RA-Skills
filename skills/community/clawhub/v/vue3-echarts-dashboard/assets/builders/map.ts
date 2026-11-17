import type { EChartsOption } from 'echarts'

/** 对应 public/data/map.json（需先 registerMap，geoJSON 见 public/geo/china.json） */
export interface ChartItem {
  name: string
  value: number
}
export interface ChartData {
  title?: string
  /** registerMap 时使用的名字，默认 'china' */
  mapName?: string
  data: ChartItem[]
}
export interface ChartConfig {
  /** 是否开启缩放漫游 */
  roam?: boolean
  min?: number
  max?: number
  colors?: string[]
}

export function buildOption(data: ChartData, config: ChartConfig = {}): EChartsOption {
  const { roam = false } = config
  const values = data.data.map((d) => d.value)
  const min = config.min ?? Math.min(...values)
  const max = config.max ?? Math.max(...values)
  const mapName = data.mapName ?? 'china'
  return {
    tooltip: {
      trigger: 'item' as const,
      formatter: (p: unknown) => {
        const q = p as { name: string; value: unknown }
        const v = Array.isArray(q.value) ? q.value[2] : q.value
        return `${q.name}：${v ?? '-'}`
      },
    },
    visualMap: {
      min,
      max,
      left: 16,
      bottom: 16,
      calculable: true,
      text: ['高', '低'],
      inRange: { color: config.colors ?? ['#0d2b4d', '#1565a8', '#1e9bd6', '#37d0f0', '#9ff8ff'] },
      itemWidth: 10,
      itemHeight: 70,
    },
    series: [
      {
        type: 'map' as const,
        map: mapName,
        roam,
        zoom: 1.18,
        layoutCenter: ['50%', '52%'],
        layoutSize: '118%',
        nameProperty: 'name',
        label: { show: false },
        itemStyle: {
          areaColor: '#0b1f3a',
          borderColor: 'rgba(120, 220, 255, 0.45)',
          borderWidth: 0.6,
        },
        emphasis: {
          label: { show: true, color: '#fff', fontSize: 11 },
          itemStyle: { areaColor: '#1e9bd6' },
        },
        data: data.data,
      },
    ],
  }
}
