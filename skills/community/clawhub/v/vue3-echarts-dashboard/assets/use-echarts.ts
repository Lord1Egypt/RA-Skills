import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import { onBeforeUnmount, onMounted, ref, shallowRef, type Ref } from 'vue'

export interface UseEChartsOptions {
  /** 主题名或主题对象，默认不传 */
  theme?: string | object
  /** 渲染器，默认 canvas（大数据量 / 需要导出 SVG 时改 svg） */
  renderer?: 'canvas' | 'svg'
  /** 是否用 ResizeObserver 自动 resize，默认 true */
  autoResize?: boolean
  /** 实例初始化完成后回调，适合在这里做首次渲染或绑定事件 */
  onReady?: (instance: ECharts) => void
}

/**
 * 【可选】ECharts 生命周期封装：init / setOption / resize / dispose 全部托管。
 *
 * 注意：本文件【不会】被生成器自动注入项目——生成的每个图表已把等价的
 * 生命周期内联进各自的 use<Pascal>Chart hook，做到自包含、弱耦合。
 * 仅当你想"集中治理"生命周期（多图表共用一份 init/resize/dispose）时，
 * 才手动把本文件拷进项目；届时把对应 hook 里的内联逻辑替换为
 * `import { useECharts } from '@/hooks/charts/useECharts'` 即可。
 *
 * 默认从完整包 'echarts' 引入；要做体积优化见 references/conventions.md 的 tree-shaking 段落。
 */
export function useECharts(elRef: Ref<HTMLElement | null>, options: UseEChartsOptions = {}) {
  const { theme, renderer = 'canvas', autoResize = true, onReady } = options
  const instance = shallowRef<ECharts | null>(null)
  const isReady = ref(false)
  let resizeObserver: ResizeObserver | null = null

  function initChart() {
    if (!elRef.value || instance.value) return
    instance.value = echarts.init(elRef.value, theme, { renderer })
    isReady.value = true
    onReady?.(instance.value)
  }

  function setOption(option: EChartsOption, notMerge = false) {
    instance.value?.setOption(option, notMerge)
  }

  function resize() {
    instance.value?.resize()
  }

  function clear() {
    instance.value?.clear()
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

  onMounted(() => {
    initChart()
    if (autoResize && elRef.value) {
      resizeObserver = new ResizeObserver(() => resize())
      resizeObserver.observe(elRef.value)
    }
  })

  onBeforeUnmount(dispose)

  return { instance, isReady, setOption, resize, clear, dispose, getInstance }
}
