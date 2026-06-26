---
name: vue-composition-api-best-practices
description: "Vue 3 组合式 API 与 <script setup> 最佳实践。涵盖代码组织、useXxx 模式、组合式函数设计、Store 集成、响应性优化及功能提取。"
license: MIT
metadata:
  author: github.com/acanzaima
  version: 1.0.0
  tags: [vue3, composition-api, script-setup, typescript, pinia, composables, reactivity, performance]
---

Vue 3 组合式 API 与 `<script setup>`、TypeScript 集成及代码组织模式的最佳实践。

## 版本兼容性

本技能面向 **Vue 3.3+**，部分功能需要更高的次版本号：

| 特性 | 最低版本 | 参考 |
|---------|:---:|---|
| `defineOptions` | 3.3+ | [script-setup](reference/script-setup-best-practices.md) |
| `toValue()` | 3.3+ | [script-setup](reference/script-setup-best-practices.md) |
| `defineModel` | 3.4+ | [script-setup](reference/script-setup-best-practices.md) |
| `watch` 搭配 `once` 选项 | 3.4+ | [reactivity](reference/reactivity-performance.md) |
| `useTemplateRef()` | 3.5+ | [script-setup](reference/script-setup-best-practices.md) |
| `useId()` | 3.5+ | [script-setup](reference/script-setup-best-practices.md) |
| `onWatcherCleanup()` | 3.5+ | [reactivity](reference/reactivity-performance.md) |

## 快速决策表

| 问题 | 参考阅读 |
|---------|-------------|
| 我的 `<script setup>` 很乱，难以浏览 | [SFC 代码组织](reference/sfc-code-organization.md) |
| 某个功能的逻辑分散在很多行中 | [useXxx 函数模式](reference/use-function-pattern.md) |
| 相同逻辑在多个组件中重复 | [功能提取](reference/feature-extraction.md) |
| 两个功能相互影响，但不知道正确的处理模式 | [跨功能依赖](reference/cross-feature-dependencies.md) |
| Props/emits 类型安全、`defineModel` 使用 | [script setup 最佳实践](reference/script-setup-best-practices.md) |
| 在 hooks/工具函数/插件中无法访问 Store | [组件外 Store 访问](reference/store-without-pattern.md) |
| 如何组织新的组合式函数文件 | [组合式函数设计模式](reference/composable-design-patterns.md) |
| 页面感觉慢，可能是响应性问题 | [响应性与性能](reference/reactivity-performance.md) |
| 如何测试组合式函数 | [组合式函数测试](reference/composable-design-patterns.md#9-testing-composables) |
| 类型安全的 `provide`/`inject` | [script setup - Provide/Inject](reference/script-setup-best-practices.md#provideinject-with-typescript) |

### 代码组织
- SFC 代码缺乏清晰的组织结构 → 参见 [sfc-code-organization](reference/sfc-code-organization.md)
- 功能逻辑分散在脚本各处 → 参见 [use-function-pattern](reference/use-function-pattern.md)
- 需要将可复用逻辑提取为组合式函数 → 参见 [feature-extraction](reference/feature-extraction.md)
- 跨功能依赖导致混乱 → 参见 [cross-feature-dependencies](reference/cross-feature-dependencies.md)

### TypeScript 与 Script Setup
- 需要 script setup 的 TypeScript 最佳实践 → 参见 [script-setup-best-practices](reference/script-setup-best-practices.md)

### Store 集成
- 在 Vue 组件外部访问 Pinia store → 参见 [store-without-pattern](reference/store-without-pattern.md)

### 组合式函数设计
- 设计健壮、可复用的组合式函数 → 参见 [composable-design-patterns](reference/composable-design-patterns.md)

### 响应性与性能
- 优化响应性以获得更好性能 → 参见 [reactivity-performance](reference/reactivity-performance.md)

### 测试
- 使用 Vitest 测试组合式函数 → 参见 [composable-design-patterns](reference/composable-design-patterns.md#9-testing-composables)

---

## 速查表

### SFC 代码组织顺序（11 步）

```
1. defineOptions     → 组件名称
2. defineProps       → Props 类型声明
3. defineModel       → 双向绑定（3.4+）
4. inject            → 注入依赖
5. defineEmits       → 事件类型声明
6. Store 声明         → useXxxStore()
7. 外部 hooks         → useI18n()、useDesign() 等
8. 功能声明           → const { ... } = useFeature()
9. provide           → 提供依赖
10. defineExpose     → 暴露公共 API
11. 功能实现          → function useFeature() {}
```

### 响应式 API 选择

```
基本类型       → ref
需要深层响应    → ref
大型对象/动态组件 → shallowRef
不需要重新赋值   → reactive（谨慎使用）
永不响应式      → markRaw + shallowRef
```

### Store 访问规则

```
组件内 (<script setup>)  → useAppStore()
组件外 (hooks/utils/plugins) → useAppStoreWithOut()
解构保持响应式            → storeToRefs(store)
```

### 反模式 TOP 5

| # | 反模式 | 正确做法 |
|---|--------|---------|
| 1 | 解构 props → 丢失响应式 | `toRefs(props)` 或直接用 `props.xxx` |
| 2 | 组件外用 `useXxxStore()` | 用 `useXxxStoreWithOut()` |
| 3 | `ref` 用于动态组件/大对象 | 用 `shallowRef` |
| 4 | 混用 Options API + script setup | 只选一种风格 |
| 5 | 事件监听不清理 | `onUnmounted` 中移除 / 使用 VueUse 的 `useEventListener` |

### 依赖模式速查

| 场景 | 推荐模式 |
|------|---------|
| 父子组件通信 | Props + Emits |
| 兄弟功能交互 | 回调参数（`onXxxChange`） |
| 跨层级多对多 | 事件总线（`useEmitt`） |
| 共享状态 | Store 桥接组合式函数 |
| 功能编排 | 组合式函数编排模式 |
