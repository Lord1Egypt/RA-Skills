---
name: vue-component-directory-structure
description: 在项目中组织 Vue 3 SFC 组件时使用——决定哪些组件采用带 types.ts 的目录结构、如何命名和导出类型、如何做 barrel 逐级导出。创建新组件、重构组件目录、或搭建 Vue 组件架构时触发。
---

# Vue 组件目录结构与类型导出工程规范

## 核心原则

**只有对外有数据传递（props / emits / model / slots 暴露复杂类型）的组件才进目录。无外部接口的组件保持扁平单文件。**

一致性比「性价比」重要。规则不按复杂度设门槛，不给判断留余地。

## 目录结构判定

```
有 defineProps / defineEmits / defineModel / defineSlots？
├─ 是 → 目录结构（ComponentName/）
│       ├── index.ts
│       ├── types.ts
│       ├── TheConst.ts（可选，运行时枚举 / 常量）
│       └── ComponentName.vue
└─ 否 → 扁平文件（ComponentName.vue）
```

无外部接口的组件：纯布局容器、纯展示、只消费 store/路由的页面级组件。

## types.ts 规范

### 用途

只放纯类型，运行时值（枚举 / 常量）见下文 [运行时常量处理办法](#运行时常量处理办法) 一节。

#### 单组件接口

组件对外暴露的 `Props` / `Emits` / `ModelValue`（默认 `v-model`）/ `Xxx`（具名 `v-model:xxx`，绑定名首字母大写作为类型名）/ `Slots` 等 TS 类型——外界必须遵守的数据交换约定

#### 目录级共享

同一目录多个组件确实需要复用一个通用类型时，在目录的 types.ts 里定义它，各组件 `import` 复用。

> **何时该建 / 不该建目录级 types.ts：**

```typescript
// ❌ BAD: 只为转发子组件类型而建目录级 types.ts——冗余环路
export type * from './Child'
// barrel 的 export * 是传递性的，someDir/index.ts 里一句
// `export * from './Child'` 已把 ChildTypes 一路带向顶层，
// 再加这层转发是重复导出。如果仅有这种 re-export 用途，直接删掉这个文件。

// ✅ GOOD: 同一目录多个组件确实需要复用一个通用类型时，在目录的 types.ts 里定义它
export interface SharedState {        // 不是转发，是新定义
  id: number
  label: string
}
```

### 规范

- 接口名统一叫 `Props`，有 emit 加 `Emits`，有默认 `v-model` 加 `ModelValue`，有 slot 加 `Slots`（含各 slot 的 scoped props 类型），都不加组件名前缀
- 具名 `v-model:xxx` 加绑定名首字母大写的类型名（如 `Count`）

```typescript
// types.ts
import type { VNode } from 'vue'

// ❌ BAD：加前缀，冗余
export interface CircleProgressBarProps { ... }
export interface CircleProgressBarEmits { ... }
export interface CircleProgressBarSlots { ... }

// ✅ GOOD：统一 Props / Emits / ModelValue / Slots（具名 v-model:count 见 Count 示例）
export interface Props {
  progressMax: number
  progress: number
  // ...
}

export interface Emits {
  updateProgress: [value: number]    // 有参数：元组语法
  reset: []                           // 无参数：空元组
}

// 默认 v-model
export type ModelValue = string

// 具名 model 示例：v-model:count 对应类型 Count
export type Count = number

// 各 slot 的 scoped props 类型——返回渲染内容 VNode[]，勿用 any（slot 调用返回 children 数组，纯文本也会被规范化为 VNode）
export interface Slots {
  default(props: { label: string }): VNode[]
  item(props: { id: number; label: string }): VNode[]
}
```

辅助类型里的**纯类型**放 types.ts  
枚举和常量按 [运行时常量处理办法](#运行时常量处理办法) 从 TheConst.ts 取类型：

```typescript
// types.ts —— CircleProgressBar 的进度条刻度
export interface TickMark {
  value: number
  label: string
  major?: boolean
}

export interface Props {
  ticks?: TickMark[]
  // ...
}
```

### 运行时常量处理办法

枚举和常量都放 TheConst.ts，不放 types.ts

缘由：`enum`、`const` 对象带运行时值，放 types.ts 会踩雷——barrel 用 `export type * as XxxTypes` 只导出类型会导致无法取值（`Object.values(XxxTypes.SomeEnum)` TS 编译报错）。  
规则：运行时值放组件同级的 `TheConst.ts`，types.ts 只取它的类型，index.ts 把值用「组件名 + 枚举名」命名导出。

```typescript
// TheConst.ts —— 运行时值在这里
export enum ViewMode {
  List = 'list',
  Grid = 'grid',
}

// types.ts
import type { ViewMode } from './TheConst'        // 本文件用
export type * from './TheConst'                   // 把类型转发给 barrel 命名空间

export interface Props {
  viewMode?: ViewMode              // prop 直接引用枚举类型，消费者可传枚举值
  // ...
}

// index.ts
export { default as DataViewer } from './DataViewer.vue'
export type * as DataViewerTypes from './types'
export { ViewMode as DataViewerViewMode } from './TheConst'   // 在原有两条基础上加一行，把枚举值按「组件名 + 枚举名」导出
```

消费者：类型走命名空间 `DataViewerTypes.ViewMode`；运行时值用 `DataViewerViewMode`。prop 类型直接是枚举，所以可以把枚举值安全地传进去：

```vue
<script setup lang="ts">
import { DataViewer, DataViewerViewMode } from '@/components'
import type { DataViewerTypes } from '@/components'

// 运行时迭代枚举值
for (const mode of Object.values(DataViewerViewMode)) {
  console.log(mode) // 'list' | 'grid'
}
</script>

<template>
  <!-- 类型安全：枚举值可赋给 viewMode（因为 prop 类型就是 ViewMode） -->
  <DataViewer :view-mode="DataViewerViewMode.Grid" />
</template>
```

## index.ts 规范

两条语句：默认导出组件 + 命名空间导出类型。

```typescript
export { default as CircleProgressBar } from './CircleProgressBar.vue'
export type * as CircleProgressBarTypes from './types'
```

**为什么用 `export type * as XxxTypes` 而不是逐个 export：**
- 避免多个组件的 `Props` 类型命名冲突
- 消费者写 `CircleProgressBarTypes.Props`，可搜索、可区分
- 新增类型时只需改 types.ts，index.ts 不用动

## 组件内引用常量与类型

- `defineProps` / `defineEmits` / `defineModel` / `defineSlots` 必须引用同目录的 `types.ts`，保证唯一真相源
- 运行时常量 / 枚举值引用同目录的 `TheConst.ts`

```vue
<script setup lang="ts">
import type { Count, Emits, ModelValue, Props, Slots } from './types'
import { ViewMode } from './TheConst'

// 默认 v-model + 具名 v-model:count
const modelValue = defineModel<ModelValue>()
const count = defineModel<Count>('count')

const props = withDefaults(defineProps<Props>(), {
  viewMode: ViewMode.List,
  // ...
})

// 声明插槽及其 scoped props 类型
const slots = defineSlots<Slots>()

const emit = defineEmits<Emits>()
</script>
```

## Barrel Exports（逐层汇总）

每一层目录的 index.ts 用 `export *` 透传目录，扁平 `.vue` 用命名默认导出汇入：

```typescript
// components/common/index.ts —— 目录组件透传
export * from './CenterBox'
export * from './CircleProgressBar'
export * from './SvgRightPicturePath'

// components/index.ts —— 扁平文件 + 目录透传
export { default as HelloWorld } from './HelloWorld.vue'
export * from './common'
export * from './lab'
```

中间层 barrel（如 `lab/blob_url/`）同理，把同目录扁平文件汇入后再被上层 `export *` 透传：

```typescript
// lab/blob_url/index.ts —— 扁平文件 + 目录透传
export { default as ConvertImgDataToDataUrlTestPage } from './ConvertImgDataToDataUrlTestPage.vue'
export * from './CopyButtonWithFeedback'
```

非 components 区的消费者统一从顶层导入：

```typescript
// ❌ BAD：绕过 barrel，耦合内部路径
import CenterBox from '@/components/common/CenterBox/CenterBox.vue'
import HelloWorld from '@/components/HelloWorld.vue'

// ✅ GOOD
import { CenterBox, CircleProgressBar, HelloWorld } from '@/components'
```

## 完整示例

```
components/
├── index.ts                              # 顶层 barrel
├── HelloWorld.vue                        # 无 props，扁平
├── common/
│   ├── index.ts                          # export * 汇总
│   ├── CenterBox/
│   │   ├── index.ts
│   │   ├── types.ts
│   │   └── CenterBox.vue
│   ├── CircleProgressBar/
│   │   ├── index.ts
│   │   ├── types.ts
│   │   └── CircleProgressBar.vue
│   └── DataViewer/
│       ├── index.ts
│       ├── types.ts
│       ├── TheConst.ts                # 运行时枚举（ViewMode）
│       └── DataViewer.vue
└── lab/
    ├── index.ts
    ├── blob_url/
    │   ├── index.ts
    │   ├── ConvertImgDataToDataUrlTestPage.vue   # 无 props，扁平
    │   └── CopyButtonWithFeedback/
    │       ├── index.ts
    │       ├── types.ts
    │       └── CopyButtonWithFeedback.vue
    └── font_support/
        ├── index.ts
        ├── TestFontSupport.vue           # 无对外 props，扁平
        └── BenchMarkResult/
            ├── index.ts
            ├── types.ts
            └── BenchMarkResult.vue
```

## Anti-Patterns

| Anti-Pattern | 问题 | 修正 |
|---|---|---|
| 所有组件都进目录 | 无 props 的组件白赚 2-3 个文件 | 只有有 props/emits/model/slots 的才进 |
| types.ts 接口加前缀 `XxxProps` | 命名空间导出已经消除了冲突 | 统一叫 `Props` |
| 消费者直接 import `.vue` 文件 | 绕过 barrel，耦合内部路径 | 从 `@/components` 导入 |
| 手写 Props 接口又手写 defineProps | 两处维护，容易 drift | defineProps 引用 types.ts |
| 扁平组件也建目录 + index.ts | 无收益的样板代码 | 扁平组件就是单文件 |
| 目录级 types.ts 只做 `export type * from './子组件'` 转发 | barrel 的 `export *` 已传递性带出子组件类型，转发层是冗余环路 | 删掉该文件；需共享时定义新的通用类型，不要转发子组件类型 |
