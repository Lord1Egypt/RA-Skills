/// <reference types="vite/client" />

// 让 TypeScript 识别 .vue 单文件组件
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>
  export default component
}

// vue3-digital-flop 未自带类型声明，这里补一份，避免编辑器/tsc 报找不到模块
declare module 'vue3-digital-flop' {
  import type { App, DefineComponent } from 'vue'
  export const VueDigitalFlop: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>
  const plugin: { install: (app: App) => void }
  export default plugin
}

// 全局注册的组件（naive-ui / vue3-digital-flop 通过 app.use 注册）放开类型检查，
// 避免 vue-tsc 对 <n-card> / <vue-digital-flop> 等报 “找不到名称”。
declare module 'vue' {
  interface GlobalComponents {
    [name: string]: unknown
  }
}
