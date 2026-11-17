# 示范

和 [SKILL.md](SKILL.md) 配套。复制时改 id、类型、接口即可。

---

## Pinia setup（默认）

新 store 用这个。和本仓库 `src/stores/counter.ts` 同一写法。

```ts
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const title = ref('demo')

  const doubleCount = computed(() => count.value * 2)
  const label = computed(() => `${title.value}: ${doubleCount.value}`)

  const increment = () => {
    count.value++
  }

  const setCount = (n: number) => {
    count.value = n
  }

  const plusAfter = async (ms: number) => {
    await sleep(ms)
    increment()
  }

  const reset = () => {
    count.value = 0
    title.value = 'demo'
  }

  return { count, title, doubleCount, label, increment, setCount, plusAfter, reset }
})

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))
```

没有 `$reset`，要还原自己写 `reset`。`return` 漏了的，外面拿不到。

---

## 候补：Pinia 选项式

只改存量选项式文件，或确实要 `$reset` / `$patch`。新文件不要用。

```ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    title: 'demo',
  }),
  getters: {
    doubleCount: (state) => state.count * 2,
    label(): string {
      return `${this.title}: ${this.doubleCount}`
    },
  },
  actions: {
    increment() {
      this.count++
    },
    setCount(n: number) {
      this.count = n
    },
    async plusAfter(ms: number) {
      await sleep(ms)
      this.increment()
    },
  },
})
```

---

## Pinia 组件调用、解构

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

// state、getter 用storeToRefs 保留 state 的响应式
const { count, doubleCount, label } = storeToRefs(store)

// action 可以直接解构，this 不会丢
const { increment, setCount } = store

const onSubmit = (n: number) => {
  setCount(n)
}
</script>

<template>
  <p>{{ label }}</p>
  <button @click="increment">{{ count }} / {{ doubleCount }}</button>
</template>
```

```ts
// 错：count 变成普通 number，改了页面不更新
const { count } = useCounterStore()

// 错：把 store 结构开以后当普通对象传
const snap = { ...store }

// 对：模板直接用 store.count，不必解构
```

`s1.vue` / `s2.vue` 已经是这个用法：两个组件 `useCounterStore()` 拿到的是同一份状态。

---

## store 调 store 用法

单向：`cart` → `user`。`user` 不 import `cart`。默认 setup。

```ts
// src/stores/user.ts
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const id = ref(0)
  const token = ref('')
  const name = ref('')

  const isLogin = computed(() => Boolean(token.value))

  const logout = () => {
    id.value = 0
    token.value = ''
    name.value = ''
  }

  return { id, token, name, isLogin, logout }
})
```

```ts
// src/stores/cart.ts
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from './user'
import { createOrder } from '@/api/order'

export const useCartStore = defineStore('cart', () => {
  const user = useUserStore()
  const items = ref<{ id: number; qty: number }[]>([])

  const totalQty = computed(() => items.value.reduce((n, i) => n + i.qty, 0))

  const add = (id: number) => {
    const row = items.value.find((i) => i.id === id)
    if (row) row.qty++
    else items.value.push({ id, qty: 1 })
  }

  const checkout = async () => {
    if (!user.isLogin) throw new Error('未登录')
    await createOrder({ uid: user.id, items: items.value })
    items.value = []
  }

  return { items, totalQty, add, checkout }
})
```

编排放 order，避免 user ↔ cart 循环：

```ts
// src/stores/order.ts
import { defineStore } from 'pinia'
import { useUserStore } from './user'
import { useCartStore } from './cart'

export const useOrderStore = defineStore('order', () => {
  const submit = async () => {
    const user = useUserStore()
    const cart = useCartStore()
    if (!user.isLogin) throw new Error('未登录')
    await cart.checkout()
  }

  return { submit }
})
```

`useXxxStore()` 写在 factory / 函数体内，不要写在模块顶层。

候补（选项式互调）：

```ts
export const useCartStore = defineStore('cart', {
  actions: {
    async checkout() {
      const user = useUserStore()
      if (!user.isLogin) throw new Error('未登录')
    },
  },
})
```

---

## 普通函数 / 拦截器 / 守卫里取 store

```ts
// src/utils/auth.ts
import { useUserStore } from '@/stores/user'

export const getToken = () => useUserStore().token
```

```ts
// src/api/http.ts（拦截器）
http.interceptors.request.use((config) => {
  const token = useUserStore().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
```

```ts
// router
router.beforeEach((to) => {
  const user = useUserStore()
  if (to.meta.auth && !user.isLogin) return { name: 'login' }
})
```

```ts
// 错：main.ts 里 createPinia 之前
const user = useUserStore() // 炸

// 错：模块加载时就执行
export const token = useUserStore().token
```

`src/views/store/test.ts` 那种写法，函数要在组件/点击/请求之后再跑，不能在 import 时立刻调。

---

## 项目 store 划分和导出

```
src/stores/
  index.ts
  user.ts
  cart.ts
  order.ts
  app.ts
src/types/
  user.ts
  order.ts
```

```ts
// src/stores/index.ts
export { useUserStore } from './user'
export { useCartStore } from './cart'
export { useOrderStore } from './order'
export { useAppStore } from './app'
```

```ts
// src/stores/app.ts —— 只有壳层 UI
export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const theme = ref<'light' | 'dark'>('light')

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return { sidebarCollapsed, theme, toggleSidebar }
})
```

| 数据 | 放哪 |
|------|------|
| 输入框、本页弹窗、本页 loading（不属于任何共享对象） | 组件 `ref` |
| 同一对象：部分字段仅本组件、部分给其他组件 | 整份 Pinia，不要拆 |
| 列表页筛选，3 层子组件要读 | 页根 `provide` 或页级 composable |
| token、用户资料、权限 | `user` |
| 购物车行 | `cart` |
| 订单提交过程 | `order`（编排 cart + user） |
| 主题、侧栏 | `app` |
| 接口列表的缓存 | 先别放 store，需要再加；能请求库缓存就别手写一份 |

```ts
// user.name / token 别处要用；lastOpenedTab 只给 UserCard
// 整份放 user store，不要 lastOpenedTab 单独 ref
```

组件用法：

```ts
import { useUserStore, useCartStore } from '@/stores'
```

不要：

```
stores/state.ts + stores/getters.ts + stores/actions.ts
stores/useXxx.ts 里面再 defineStore 三个
App.vue provide 一份 user，Pinia 再存一份
```

---

## 组件内 ref

单值：

```vue
<script setup lang="ts">
const open = ref(false)
</script>
```

一组表单（整体替换、提交拷贝）：

```ts
const form = ref({ name: '', age: 0 })

const submit = () => {
  postUser({ ...form.value })
}

const reset = () => {
  form.value = { name: '', age: 0 }
}
```

列表 + 筛选（派生用 computed）：

```ts
const keyword = ref('')
const list = ref<Item[]>([])

const filtered = computed(() => {
  const k = keyword.value.trim()
  if (!k) return list.value
  return list.value.filter((i) => i.name.includes(k))
})
```

```ts
// 别这样：watch 同步第二份
const filtered = ref<Item[]>([])
watch([keyword, list], () => {
  filtered.value = list.value.filter(...)
})
```

子组件要改父状态：emit / v-model，不要 provide，更不要 Pinia。

```vue
<SearchInput v-model="keyword" />
```

```ts
// SearchInput.vue
const keyword = defineModel<string>({ default: '' })
```

---

## props

父 → 子只读：

```vue
<UserCard :user="user" />
```

```ts
defineProps<{ user: User }>()
```

子改父：

```vue
<UserCard :user="user" @update:name="user.name = $event" />
```

多层仍是同一页、每层都在转手同一个 `user`：不要 props 钻 4 层，改 provide，或把中间层做成只负责 layout、数据在页根 provide。

对象 props 是引用。子组件里改 `props.user.name` 能改到父数据，但这是暗改，后续难查。要改就 emit 或 v-model。

---

## provide / inject

```ts
// src/views/order/keys.ts
import type { InjectionKey, Ref } from 'vue'

export interface OrderFilter {
  keyword: string
  status: 'all' | 'pending' | 'done'
}

export const OrderFilterKey: InjectionKey<Ref<OrderFilter>> = Symbol('order-filter')
```

```vue
<!-- views/order/index.vue 页根 -->
<script setup lang="ts">
import { OrderFilterKey } from './keys'
import FilterBar from './FilterBar.vue'
import OrderTable from './OrderTable.vue'

const filter = ref({ keyword: '', status: 'all' as const })
provide(OrderFilterKey, filter)
</script>

<template>
  <FilterBar />
  <OrderTable />
</template>
```

```vue
<!-- FilterBar.vue，中间隔了几层 layout 也能 inject -->
<script setup lang="ts">
import { OrderFilterKey } from './keys'

const filter = inject(OrderFilterKey)
if (!filter) throw new Error('OrderFilterKey missing')

const reset = () => {
  filter.value = { keyword: '', status: 'all' }
}
</script>

<template>
  <input v-model="filter.keyword" />
  <button @click="reset">清空</button>
</template>
```

页根自己改同一份 ref，子组件也会更新，不用再 provide：

```ts
const filter = ref({ keyword: '', status: 'all' as const })
provide(OrderFilterKey, filter)

const applyStatus = (status: 'all' | 'pending' | 'done') => {
  filter.value = { ...filter.value, status }
}
```

```ts
// 错：重新 provide，已经 inject 的组件拿不到新值
provide(OrderFilterKey, ref({ keyword: '', status: 'all' }))
```

```ts
// 错：丢响应
provide('count', count.value)

// 错：字符串 key，重构搜不到，类型丢失
provide('order-filter', filter)
inject('order-filter')

// 错：把登录用户 provide 到 App，当全局 store 用
```

默认值：可选依赖才写 `inject(Key, default)`。业务数据缺了就该扔错，别默默给一份空对象。

---

## 同一页里三种一起用

订单页：筛选在页内共享，用户在全局，行选择只在表格。

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { OrderFilterKey } from './keys'

const userStore = useUserStore()
const { name } = storeToRefs(userStore)

const filter = ref({ keyword: '', status: 'all' as const })
provide(OrderFilterKey, filter)

const selectedIds = ref<number[]>([])
</script>
```

- `user`：别的页也要，Pinia
- `filter`：本页树内多层，provide
- `selectedIds`：表格自己的，ref
