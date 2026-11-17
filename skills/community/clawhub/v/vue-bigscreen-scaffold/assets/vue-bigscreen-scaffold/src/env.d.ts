/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

/** vue3-digital-flop 未提供类型声明，这里给出最小类型 */
declare module 'vue3-digital-flop' {
  import type { DefineComponent } from 'vue'
  export const VueDigitalFlop: DefineComponent<
    {
      start?: number
      end?: number
      duration?: number
      separator?: string
      decimal?: string
      prefix?: string
      suffix?: string
      toFixedNum?: number
    },
    {},
    any
  >
  const _default: { install: (app: unknown) => void }
  export default _default
}

/** ECharts 插件（词云/水球）无完整类型声明，按副作用导入 */
declare module 'echarts-wordcloud' {
  const _default: unknown
  export default _default
}

declare module 'echarts-liquidfill' {
  const _default: unknown
  export default _default
}
