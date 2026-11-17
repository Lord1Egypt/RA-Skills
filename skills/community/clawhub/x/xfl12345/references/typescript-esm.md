---
name: typescript-esm
description: 打包器项目（Vite / webpack 等——模块说明符由打包器解析）的模块导入规范——TypeScript ESM 导入的完整约定，与 typescript.md 配套。凡在打包器项目中写、改、审任何 import 语句时触发；不覆盖纯 Node 原生环境（node 解释器直接执行 .ts：type stripping / nodenext），那套后缀规范与之相反。
---

# TypeScript × ESM

> **适用**：源码由打包器消费的项目（Vite / webpack 等）。  
> **不适用**：纯 Node 原生环境——node 直接执行 `.ts`（type stripping / nodenext），其后缀规范与本文相反。
>
> 核心心智模型：**导入的是模块说明符，不是文件路径**。解析由打包器完成，任何「替它省事」的写法都是多余的。

## 模块导入

**通用原则**（适用任何使用路径别名的项目；为避免循环引用，内部资源导入**必须**具体——即准确到文件或目录，各场景走法见下述条目）：

- TS 上下文导入 TS 文件应当省略 `.ts` 后缀：

  ```typescript
  // ❌ BAD: TS 上下文里导入 TS 文件带 `.ts` 后缀
  import { foo } from './utils/helper.ts'
  import type { User } from './types/user.ts'

  // ✅ GOOD: 省略后缀
  import { foo } from './utils/helper'
  import type { User } from './types/user'
  ```

- 导入 `index.ts` 只引用到目录名（如 `./api/common`、`./api`）：

  ```typescript
  // ❌ BAD: 把目录别名写全，噪音
  import { listUsers } from './api/users/index'

  // ✅ GOOD: 只引用到目录名
  import { listUsers } from './api/users'
  ```

- 对 常量 / 通用模型 的引用准确到文件（如 `./api/common/TheConst`、`./model/BroadcastContext`）
- 目录级资源以 `index.ts` 作 barrel 对外统一导出；该目录有类型定义时配套 `types.ts`
  - 走法分工按资源领域划：常量 / 通用模型 / class 一律按前述规则直达文件；Vue 组件则一律经目录 index / barrel 汇总消费，细则见 [vue-component-directory-structure.md](./vue-component-directory-structure.md)
  - 消费者必须从顶层 barrel 导入、禁止绕行直取 `.vue`
  - re-export 类型必须显式 type 标注（如 `export type * as XxxTypes from './types'`；`isolatedModules` / `verbatimModuleSyntax` 下与值导出混写直接编译报错）
- 同一文件的值导入 + 类型导入写成一条语句，用内联 `type` 修饰符；仅当 value / type 混杂且超出可读阈值时（经验值：type 条目 >2）才拆成「值导入」+「类型导入」两条：

  ```typescript
  // ❌ BAD: 能合成一条却拆成两条
  import { foo } from './module'
  import type { Bar } from './module'

  // ✅ GOOD: 一条搞定，内联 type 修饰符（TS 4.5+）
  import { foo, type Bar } from './module'

  // ❌ BAD: value / type 混杂、数量又多，硬塞一条，读起来跳
  import {
    connect,
    disconnect,
    type ChannelConfig,
    ChannelContext,
    type ChannelEvent,
    type ChannelStatus,
    TheConst,
  } from './model/broadcast/channel'

  // ✅ GOOD: 拆成「值导入」+「类型导入」两条，各归各
  import {
    connect,
    disconnect,
    ChannelContext,
    TheConst,
  } from './model/broadcast/channel'
  import type {
    ChannelConfig,
    ChannelEvent,
    ChannelStatus,
  } from './model/broadcast/channel'
  ```

- 文件引用 <2 级用相对（`./types`、`../common`）
  - 级数 = 路径里 `../` 的层数（`./` 不计层级，只是「当前目录内」）：
  - 级数 ≥2 应转用绝对

  ```typescript
  // src/components/chat/Chat.vue

  // ✅ GOOD: 0 级（同目录 ./）
  import { foo } from './ChatInput'
  import type { Msg } from './types'

  // ✅ GOOD: 1 级（一个 ../）
  // 无论 shared 是 shared.ts 还是 shared/index.ts
  // 只要能写成单个 '../' 且不再有更多的 '/' 就可以
  import { bar } from '../shared'

  // ❌ BAD: 凑不出「单个 '../' + 名称」的形态，路径引用绕，不利于判断引用来源，可读性差
  import { User } from '../../model'                        // 2 个 ../ → 超阈值
  import { fmt } from '../shared/format'                    // 名称后还挂 '/' → 不合形态
  import { API_BASE_PATH } from '../../api/common/TheConst' // 2 个 ../ → 超阈值，名称后还挂 '/' → 不合形态

  // ✅ GOOD: 转绝对别名（@ 指向 src）
  import { User } from '@/model'
  import { fmt } from '@/components/shared/format'
  import { API_BASE_PATH } from '@/api/common/TheConst'
  ```

- 组件引用（相对路径的参照：src 根一级文件，如 `src/router/index.ts`、`src/App.vue`）
  - 跨树导入 vue 组件一律走组件顶层 barrel `@/components/ChatButton`
  - 邻里（文件引用 <2 级）引用准确到目录：`import { ChatButton } from '../ChatButton'`，即其 index 入口
