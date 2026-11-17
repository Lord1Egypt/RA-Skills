import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import { onBeforeUnmount, onMounted, ref, shallowRef, type Ref } from 'vue'
import {
  buildOption as build{{PASCAL}}Option,
  type ChartData as {{PASCAL}}ChartData,
  type ChartConfig as {{PASCAL}}ChartConfig,
} from '@/hooks/charts/builders/{{KEBAB}}'

export interface {{PASCAL}}ChartOptions {
  renderer?: 'canvas' | 'svg'
  theme?: string | object
  autoResize?: boolean
  /** 地图 geoJSON 地址，默认 /geo/china.json */
  geoUrl?: string
}

const BASE_CONFIG: Partial<{{PASCAL}}ChartConfig> = {{BASE_CONFIG}}

/**
 * {{PASCAL}} 地图图表。与通用 hook 的唯一差别：init 之前必须先 registerMap，
 * 因此这里内置了 geoJSON 的懒加载（同名的重复注册只拉取一次）。
 * 其余生命周期（resize / dispose）与通用 hook 完全一致，依旧自包含。
 */
let geoReady: Promise<void> | null = null

function ensureGeo(mapName: string, geoUrl: string): Promise<void> {
  if (!geoReady) {
    geoReady = fetch(geoUrl)
      .then((r) => r.json())
      .then((geo) => {
        echarts.registerMap(mapName, geo)
      })
  }
  return geoReady
}

export function use{{PASCAL}}Chart(
  elRef: Ref<HTMLElement | null>,
  initialData?: {{PASCAL}}ChartData,
  config?: {{PASCAL}}ChartConfig,
  chartOptions?: {{PASCAL}}ChartOptions,
) {
  const {
    renderer = 'canvas',
    theme = {{DEFAULT_THEME}},
    autoResize = true,
    geoUrl = '/geo/china.json',
  } = chartOptions ?? {}
  const instance = shallowRef<ECharts | null>(null)
  const isReady = ref(false)
  let resizeObserver: ResizeObserver | null = null

  function setOption(option: EChartsOption, notMerge = false) {
    instance.value?.setOption(option, notMerge)
  }

  function render(data: {{PASCAL}}ChartData) {
    setOption(build{{PASCAL}}Option(data, { ...BASE_CONFIG, ...config }))
  }

  function resize() {
    instance.value?.resize()
  }

  function getInstance() {
    return instance.value
  }

  function dispose() {
    resizeObserver?.disconnect()
    resizeObserver = null
    instance.value?.dispose()
    instance.value = null
    isReady.value = false
  }

  onMounted(async () => {
    if (!elRef.value) return
    const mapName = (initialData as { mapName?: string } | undefined)?.mapName ?? 'china'
    await ensureGeo(mapName, geoUrl)
    if (!elRef.value) return
    instance.value = echarts.init(elRef.value, theme, { renderer })
    isReady.value = true
    if (autoResize) {
      resizeObserver = new ResizeObserver(() => resize())
      resizeObserver.observe(elRef.value)
    }
    if (initialData) render(initialData)
  })

  onBeforeUnmount(dispose)

  return { render, resize, getInstance, isReady, dispose }
}
