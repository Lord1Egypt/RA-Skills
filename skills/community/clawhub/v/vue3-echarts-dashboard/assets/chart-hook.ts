import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import { onBeforeUnmount, onMounted, ref, shallowRef, type Ref } from 'vue'
{{PLUGIN_IMPORTS}}import {
  buildOption as build{{PASCAL}}Option,
  type ChartData as {{PASCAL}}ChartData,
  type ChartConfig as {{PASCAL}}ChartConfig,
} from '@/hooks/charts/builders/{{KEBAB}}'

export interface {{PASCAL}}ChartOptions {
  /** 渲染器，默认 canvas */
  renderer?: 'canvas' | 'svg'
  /** 主题：已通过 echarts.registerTheme 注册的名称，或直接传主题对象（init 时生效） */
  theme?: string | object
  /** 是否用 ResizeObserver 自动跟随容器尺寸，默认 true */
  autoResize?: boolean
}

/**
 * 图表默认配置（生成器按主题注入：大屏模式带调色板，单图表模式为空对象）。
 * 调用方传入的 config 优先级更高。
 */
const BASE_CONFIG: Partial<{{PASCAL}}ChartConfig> = {{BASE_CONFIG}}

/**
 * {{PASCAL}} 图表组合式函数（自包含，不依赖共享 composable）。
 * ECharts 生命周期（init / setOption / resize / dispose）全部托管在这里，
 * 因此生成的图表是独立可拖拽单元——只依赖本文件 + builders/<kebab>.ts，
 * 放进任意 Vue3 项目即可用，不会被某个共享 useECharts.ts 绑死。
 *
 * 返回：
 *  - render(data)  更新图表数据
 *  - resize()      手动重绘（容器尺寸变化但 ResizeObserver 没捕获时）
 *  - getInstance() 拿原生 ECharts 实例，用于绑定 click 等事件
 *  - isReady       实例是否已初始化
 */
export function use{{PASCAL}}Chart(
  elRef: Ref<HTMLElement | null>,
  initialData?: {{PASCAL}}ChartData,
  config?: {{PASCAL}}ChartConfig,
  chartOptions?: {{PASCAL}}ChartOptions,
) {
  const { renderer = 'canvas', theme = {{DEFAULT_THEME}}, autoResize = true } = chartOptions ?? {}
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

  onMounted(() => {
    if (!elRef.value) return
    instance.value = echarts.init(elRef.value, theme, { renderer })
    isReady.value = true
    if (autoResize) {
      resizeObserver = new ResizeObserver(() => resize())
      resizeObserver.observe(elRef.value)
    }
    // 实例就绪后再做首次渲染，避免 setOption 时实例还未 init
    if (initialData) render(initialData)
  })

  onBeforeUnmount(dispose)

  return { render, resize, getInstance, isReady, dispose }
}
