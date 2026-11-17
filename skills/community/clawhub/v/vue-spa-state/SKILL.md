---
name: vue-spa-state
description: >-
  按作用域为 Vue 3 SPA 选择并落地状态。仅本组件：ref/computed。父子 1～2 层：props/emit、
  v-model。同一页 3+ 层：provide/inject（InjectionKey；改同一份 ref，不要重新 provide）。
  跨路由、跨模块、登录态，或同一对象部分字段仅本组件、部分给其他组件：整份进 Pinia。
  新 store 用 setup + 箭头函数；选项式只改存量或需要 $reset。含 storeToRefs、store
  单向互调、普通函数/守卫/拦截器在 pinia 安装后取 store、按业务域拆分与导出。
  在新增或修改 Vue 状态、Pinia、provide/inject、状态管理、跨组件传值，
  或判断该用 ref、props 还是 Pinia 时使用。
---

# Vue SPA 状态管理

按作用域选方案(按照状态复杂度评估)
- 组件里 - ref内部状态;
- 父子组件 用props管理简单状态;
- 简单的跨多层级组件状态，考虑用 provide;
- 其他一律用 pinia store;

写状态相关代码时：先定作用域，再抄对应模板。完整示范见 [examples.md](examples.md)。

## 选型

```
当前组件用          → ref / computed（必要时 reactive）
父子、隔 1～2 层         → props down + emit up；双向用 v-model
简单同一功能树、隔 3+ 层     → provide / inject（带 InjectionKey）
跨路由 / 跨模块 / 登录态 → Pinia
```

模块级 `ref` 再 export，效果像全局 store，但没有 devtools、没有 `$reset`、HMR 行为差。正式业务不要用。

## 硬规则

1. 解构 Pinia 的 state / getter 必须 `storeToRefs`。action 直接 `store.xxx()`，或解构 action（Pinia 已绑定 this）。
2. store 调 store：在 **action / setup 函数体内** 调 `useXxxStore()`，不要在模块顶层执行。store 之间单向依赖，禁止 A↔B 互相 import。
3. 普通 ts 函数里可以 `useXxxStore()`，但必须发生在 `app.use(pinia)` 之后。不要写在模块顶层。
4. 一个文件一个 store，`id` 全局唯一。`stores/index.ts` 只做 re-export。
5. 按业务域拆（user / cart / order），不要按 state/getters/actions 拆文件，也不要一个 `appStore` 塞全部。
6. 源数据只存一份。能 computed 出来的不要再存一份再手动同步。同一对象不要按字段拆成「一半 ref、一半 store」。
7. 真正只属于本组件、且不属于任何共享对象的 UI（弹窗、输入框、临时 loading）放组件；对象上只要有字段被其他组件用，整份进 Pinia。
8. 函数写成 `const xxx = () => {}`，不要 `function` 声明。选项式 actions 例外（要 `this`）。

默认 **setup store**（与 `src/stores/counter.ts` 一致）。新文件一律 setup，同一文件不要混选项式。选项式只改存量、或明确需要 `$reset` 时用。

---

## 1. Pinia setup（默认）

```ts
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Item } from '@/types/item'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const list = ref<Item[]>([])
  const loading = ref(false)

  const doubleCount = computed(() => count.value * 2)
  const doublePlusOne = computed(() => doubleCount.value + 1)
  const itemById = (id: number) => list.value.find((i) => i.id === id)

  const increment = () => {
    count.value++
  }

  const fetchList = async () => {
    loading.value = true
    try {
      list.value = await getList()
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    count.value = 0
    list.value = []
    loading.value = false
  }

  return { count, list, loading, doubleCount, doublePlusOne, itemById, increment, fetchList, reset }
})
```

- `ref` = state，`computed` = getter，函数 = action。和组件 `<script setup>` 同一套。
- `return` 漏了的，外面拿不到。
- 没有 `$reset`，要还原自己写 `reset()`。
- 带参查询写成函数（如 `itemById`），没有 computed 缓存。

### 候补：选项式

只用于改已有选项式文件，或确实要 `$reset` / `$patch`。新 store 不要用。完整示例见 examples.md。

```ts
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++
    },
  },
})
```

- `state` 必须是工厂函数。
- 自带 `$reset()`。批量改：`this.$patch({ count: 0 })` 或 `$patch((s) => { s.list.push(x) })`。

---

## 2. 组件里怎么用

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const { count, doubleCount } = storeToRefs(store)

store.increment()
</script>

<template>
  <button @click="store.increment">{{ count }} / {{ doubleCount }}</button>
</template>
```

```ts
// 丢响应
const { count } = store

// 对
const { count } = storeToRefs(store)
store.increment()
```

模板里可以直接 `store.count`，不必解构。只在 script 里要单独用响应式值时才 `storeToRefs`。

### store 调另一个 store

```ts
// cart.ts —— 可以依赖 user；user 不要再 import cart
import { useUserStore } from './user'

export const useCartStore = defineStore('cart', () => {
  const user = useUserStore()

  const checkout = () => {
    if (!user.isLogin) return
    // ...
  }

  return { checkout }
})
```

协调两个 store 的流程（下单 = 读 user + 清 cart + 写 order）放到 **调用方或专门的 order store**，不要让 user 去清 cart。

### 普通函数里调

```ts
// utils/tracker.ts
import { useUserStore } from '@/stores/user'

export const trackEvent = (name: string) => {
  const user = useUserStore()
  send({ name, uid: user.id })
}
```

路由守卫、axios 拦截器同样：在回调里取 store，不要在 `router/index.ts` 顶层取。

---

## 3. 多 store 怎么拆、怎么导出

```
src/stores/
  index.ts      # 只 re-export
  user.ts       # 登录、资料、权限码
  cart.ts
  order.ts
  app.ts        # 主题、侧栏折叠（壳层，不是业务垃圾桶）
```

```ts
// stores/index.ts
export { useUserStore } from './user'
export { useCartStore } from './cart'
export { useOrderStore } from './order'
export { useAppStore } from './app'
```

组件：`import { useUserStore } from '@/stores/user'` 或从 `@/stores`。不要从组件里深挖 `stores/user/actions.ts`。

复杂状态怎么组合：

- **源在 user，cart 只读**：cart 的 action 里 `useUserStore()`，不要把 `userId` 再拷进 cart。
- **跨域流程**：新建 `order` store 编排，或页面里依次调，不要循环依赖。
- **复用逻辑**：抽 composable（`usePagination`），store 里调用；composable 不要自己再搞一份全局状态。
- **需要刷新还原**：setup 自己写 `reset()`。不要为了 `$reset` 把新模块写成选项式。
- **要记住的**（token、主题）：persist 插件或自己读 `localStorage`，只持久化最小字段。

什么进 Pinia、什么不进：见 examples.md 划分表。

---

## 4. 组件内部：单个 ref

```vue
<script setup lang="ts">
const open = ref(false)
const keyword = ref('')
const list = ref<Item[]>([])

const filtered = computed(() =>
  list.value.filter((i) => i.name.includes(keyword.value)),
)

const toggle = () => {
  open.value = !open.value
}
</script>
```

- 一个值一个 `ref`。对象要整体替换也用 `ref`。只有一堆字段要一起改、且不想写 `.value` 时才 `reactive`。
- 派生数据用 `computed`，不要 `watch` 里手动同步第二份。
- 本页 loading / 表单 / 弹窗开关：全放这里。子组件要改，用 emit 或 v-model，不要为这个建 store。

---

## 5. 简单跨组件：props vs provide

**1～2 层：props**

```vue
<!-- 父 -->
<UserCard :user="user" @rename="user.name = $event" />
<SearchInput v-model="keyword" />
```

```ts
const user = defineProps<{ user: User }>()
const emit = defineEmits<{ rename: [name: string] }>()
const keyword = defineModel<string>()
```

**3+ 层、同一功能树：provide / inject**

只在这棵树有效。页根 provide 一份 `ref`，深层 inject。跨路由 / 登录态用 Pinia。

```ts
export const OrderFilterKey: InjectionKey<Ref<OrderFilter>> = Symbol('order-filter')

const filter = ref<OrderFilter>({ keyword: '', status: 'all' })
provide(OrderFilterKey, filter)

const filter = inject(OrderFilterKey)
if (!filter) throw new Error('OrderFilterKey missing')

filter.value.keyword = 'vue' // 改同一份，不要再 provide
```

- provide `ref` / `reactive` 本身，不要 `.value`；key 用 `InjectionKey`，不要字符串。
- 子组件只读：`provide(Key, { filter: readonly(filter), setFilter })`。

---

## 落地顺序

1. 问：离开这个页面，这份数据还需要在吗？不需要 → 组件 ref。
2. 同一份对象：有的字段只给本组件、有的被其他组件用 → 整份进 Pinia，不要拆开。
3. 问：谁写、谁读？父子清晰 → props / v-model。
4. 问：中间隔了很多布局组件、数据流仍属于这一页？ → provide。
5. 其余 → Pinia setup store，按业务域加文件，从 `stores/index.ts` 导出。选项式只动存量。
6. 写组件时 state/getter 走 `storeToRefs`；action 走 `store.xxx`。
