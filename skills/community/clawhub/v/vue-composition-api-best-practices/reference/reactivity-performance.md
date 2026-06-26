# 响应性与性能

Vue 3 Composition API 响应式与性能优化最佳实践。

---

## 1. ref vs shallowRef vs reactive

### 选择决策树

```
需要响应式？
├── 是 → 数据是基本类型？
│        ├── 是 → ref
│        └── 否 → 数据层级深？
│                 ├── 浅层即可 → shallowRef
│                 └── 需要深层 → ref（或 reactive）
└── 否 → 不需要响应式 → 普通变量 / shallowRef
```

### 对比表

| API | 响应深度 | 触发更新方式 | 适用场景 |
|-----|---------|-------------|---------|
| `ref` | 深层 | 自动 | 通用场景，对象属性变更需触发更新 |
| `shallowRef` | 浅层（.value） | 手动 `triggerRef` | 大型对象、动态组件、性能敏感场景 |
| `reactive` | 深层 | 自动 | 不需要重新赋值的对象 |

### ⚠️ reactive 的局限性

虽然 `reactive` 在某些场景下很方便，但 Vue 3 官方更推荐用 `ref` 作为主要响应式 API：

```typescript
// ❌ 1. 不能重新赋值 -- 整个替换会丢失响应式
let state = reactive({ count: 0 })
state = reactive({ count: 1 }) // 响应式连接断开！

// ✅ 用 ref 没问题
const state = ref({ count: 0 })
state.value = { count: 1 } // 正常触发更新

// ❌ 2. 解构丢失响应式
const { count } = reactive({ count: 0 }) // count 变成了普通数字

// ✅ 用 toRefs 保持响应式
const { count } = toRefs(reactive({ count: 0 }))

// ❌ 3. 不支持基本类型
const count = reactive(0) // 类型错误！

// ✅ 基本类型用 ref
const count = ref(0)
```

**经验法则：** 新代码优先使用 `ref`，仅在明确需要"对象属性级响应式且确定不会重新赋值"时使用 `reactive`。

### 实际案例：动态组件切换

```typescript
// ✅ GOOD: 使用 shallowRef 避免组件对象的深层响应式开销
function usePage() {
  const activeCom = shallowRef()
  const isPure = computed(() => appStore.pure)

  watchEffect(() => {
    // 组件对象不需要深层响应式，shallowRef 足矣
    activeCom.value = isPure.value ? PureMode : HomeMode
  })

  return { activeCom }
}
```

```typescript
// ❌ BAD: 使用 ref 对组件对象做深层响应式，无意义且浪费性能
function usePage() {
  const activeCom = ref()  // 会递归遍历组件对象的所有属性
  // ...
}
```

### shallowRef 手动触发更新

```typescript
const list = shallowRef<string[]>(['a', 'b', 'c'])

// ❌ 不会触发更新：修改数组内部不会被追踪
list.value.push('d')

// ✅ 触发更新：替换整个 .value
list.value = [...list.value, 'd']

// ✅ 触发更新：使用 triggerRef
list.value.push('d')
triggerRef(list)
```

### markRaw — 标记对象永不转为响应式

当确定某个对象不需要响应式时（如第三方库实例、大型静态数据），用 `markRaw` 标记它。这可以防止 Vue 的响应式系统意外地将其深层代理，避免性能浪费：

```typescript
import { markRaw, reactive, shallowRef } from 'vue'

// ❌ BAD: 第三方库实例被意外代理
const mapInstance = new Map() // 被 reactive 包装，产生大量 proxy 开销

// ✅ GOOD: 标记为永不代理
const mapInstance = markRaw(new Map())
const state = reactive({
  map: mapInstance // map 本身不会被代理
})

// ✅ GOOD: 标记大型静态数据
const largeStaticConfig = markRaw({
  // 数千行配置数据...
})
const appState = shallowRef({
  config: largeStaticConfig // config 不会被 deep-track
})
```

**何时使用 `markRaw`：**
- 第三方库实例（如 Leaflet 地图、Monaco Editor、ECharts 实例）
- 大型静态数据对象（如国家/地区列表、字典数据）
- 已经冻结的数据（`Object.freeze`）
- 在 `pinia` persist 中不需要持久化的运行时对象

**⚠️ 注意：** `markRaw` 是永久性的，标记后无法撤销。被标记的对象在 `reactive`/`ref` 中会被视为非响应式。

---

## 2. computed 缓存优化

### computed 的缓存特性

- 只在依赖变化时重新计算
- 多次访问只计算一次
- 适合派生状态和昂贵计算

### 何时用 computed vs 方法

```typescript
// ✅ GOOD: 派生状态用 computed，有缓存
const filteredList = computed(() =>
  list.value.filter(item => item.active)
)

// ❌ BAD: 用方法返回派生值，每次调用都重新计算
function getFilteredList() {
  return list.value.filter(item => item.active)
}
```

### computed 写入（双向绑定）

```typescript
const keyword = computed({
  get: () => searchStore.keyword,
  set: (val: string) => { searchStore.keyword = val }
})
```

### 避免在 computed 中产生副作用

```typescript
// ❌ BAD: computed 中有副作用
const userInfo = computed(() => {
  fetchUserInfo()  // 每次依赖变化都会请求
  return userStore.info
})

// ✅ GOOD: 用 watch 处理副作用
const userInfo = computed(() => userStore.info)
watch(userId, (newId) => {
  fetchUserInfo(newId)
}, { immediate: true })
```

---

## 3. watch 优化

### watch vs watchEffect

| API | 依赖追踪 | 访问旧值 | 精确控制 | 适用场景 |
|-----|---------|---------|---------|---------|
| `watch` | 显式指定 | ✅ | ✅ | 需要旧值对比、精确监听 |
| `watchEffect` | 自动追踪 | ❌ | ❌ | 副作用与响应式源直接关联 |

### watch 的精确控制

```typescript
// ✅ GOOD: 精确监听特定属性
watch(
  () => appStore.theme,
  (newTheme) => { applyTheme(newTheme) }
)

// ❌ BAD: 监听整个 store，任何变化都触发
watch(
  () => appStore,
  () => { applyTheme(appStore.theme) },
  { deep: true }  // 深层监听开销大
)
```

### 常用选项

```typescript
watch(source, callback, {
  immediate: true,  // 创建时立即执行一次
  deep: false,      // 避免深层监听（默认 false）
  once: true,       // 只触发一次后自动停止（Vue 3.4+）
  flush: 'post',    // DOM 更新后执行（需要访问更新后的 DOM 时使用）
})
```

### watch 中清理副作用

```typescript
watch(id, (newId, oldId, onCleanup) => {
  const controller = new AbortController()

  fetch(`/api/user/${newId}`, { signal: controller.signal })
    .then(res => res.json())
    .then(data => { user.value = data })

  // id 变化时取消上一次请求
  onCleanup(() => controller.abort())
})
```

### onWatcherCleanup (Vue 3.5+)

**Vue 3.5 引入了 `onWatcherCleanup()`** — 可以在 `watchEffect` 内部调用的清理函数（之前 `watchEffect` 不支持 `onCleanup` 回调参数）：

```typescript
import { watchEffect, onWatcherCleanup } from 'vue'

// ✅ Vue 3.5+: watchEffect 内部也能注册清理函数
watchEffect(() => {
  const controller = new AbortController()

  fetch(`/api/user/${userId.value}`, { signal: controller.signal })
    .then(res => res.json())
    .then(data => { user.value = data })

  // userId 变化或组件卸载时自动取消请求
  onWatcherCleanup(() => controller.abort())
})
```

**对比 `watch` 的 `onCleanup` 参数：**

| 特性 | `watch(fn, (_, __, onCleanup) => {})` | `watchEffect(() => { onWatcherCleanup(...) })` |
|------|--------------------------------------|----------------------------------------------|
| 可用性 | Vue 3.0+ | Vue 3.5+ |
| 清理触发时机 | 下次执行前 + 卸载时 | 下次执行前 + 卸载时 |
| 使用方式 | 回调参数 | 独立函数调用 |
| 适用场景 | 精确监听 + 清理 | 自动追踪 + 清理 |

**为什么需要 `onWatcherCleanup`：** 之前 `watchEffect` 无法注册清理函数，导致在 effect 中发起的异步请求无法在新请求发起前自动取消，容易产生竞态条件。

---

## 4. 事件监听清理

### 组件级自动清理

```typescript
// ✅ GOOD: 在 composable 中使用生命周期钩子自动清理
import { onUnmounted } from 'vue'
import { mittBus } from '@/utils/mitt'

export function useEmitt() {
  const listeners: Array<{ event: string; handler: Function }> = []

  function on(event: string, handler: Function) {
    mittBus.on(event, handler as any)
    listeners.push({ event, handler })
  }

  onUnmounted(() => {
    listeners.forEach(({ event, handler }) => {
      mittBus.off(event, handler as any)
    })
    listeners.length = 0
  })

  return { on, emit: mittBus.emit }
}
```

> 另见：[组合式函数设计模式 - 模式 3](composable-design-patterns.md#模式-3生命周期感知) 和 [跨功能依赖 - 模式 4](cross-feature-dependencies.md#模式-4事件总线模式适用于复杂的多对多场景) 了解 `useEmitt` 的更多使用场景。

### DOM 事件清理

```typescript
// ✅ 使用 VueUse 的 useEventListener 自动清理
import { useEventListener } from '@vueuse/core'

export function useNetwork() {
  const isOnline = ref(navigator.onLine)
  // 自动在卸载时移除监听
  useEventListener(window, 'online', () => (isOnline.value = true))
  useEventListener(window, 'offline', () => (isOnline.value = false))
  return { isOnline }
}
```

### 手动清理模式

```typescript
// 对于不支持生命周期钩子的场景，提供 stop 函数
export function useInterval(fn: () => void, delay: number) {
  let timer: ReturnType<typeof setInterval> | null = null

  function start() {
    stop()
    timer = setInterval(fn, delay)
  }

  function stop() {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  onUnmounted(stop)

  return { start, stop }
}
```

---

## 5. 组件懒加载

### defineAsyncComponent

```typescript
import { defineAsyncComponent } from 'vue'

// ✅ GOOD: 懒加载重型组件
const HeavyChart = defineAsyncComponent(() =>
  import('@/components/Chart/src/HeavyChart.vue')
)
```

### 动态 import + shallowRef

```typescript
// ✅ GOOD: 条件加载组件
const activeCom = shallowRef<Component>()

watchEffect(async () => {
  if (condition.value) {
    const mod = await import('./HeavyComponent.vue')
    activeCom.value = mod.default
  } else {
    activeCom.value = LightComponent
  }
})
```

### Suspense 配合

```vue
<template>
  <Suspense>
    <template #default>
      <AsyncComponent />
    </template>
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>
```

---

## 6. v-once 与 v-memo

### v-once：只渲染一次

```vue
<template>
  <!-- 只在首次渲染时求值，后续更新跳过 -->
  <div v-once>{{ staticContent }}</div>
</template>
```

### v-memo：条件记忆

```vue
<template>
  <!-- 仅当 item.id 变化时重新渲染 -->
  <div v-memo="[item.id]">
    <ExpensiveComponent :item="item" />
  </div>
</template>
```

---

## 7. 列表渲染优化

### key 的正确使用

```vue
<!-- ✅ GOOD: 使用唯一 ID -->
<div v-for="item in list" :key="item.id">

<!-- ❌ BAD: 使用 index -->
<div v-for="(item, index) in list" :key="index">
```

### 虚拟列表

当列表项超过 100 个时，使用虚拟滚动：

```typescript
// 推荐 vueuse/useVirtualList 或第三方库
import { useVirtualList } from '@vueuse/core'

const { list, containerProps, wrapperProps } = useVirtualList(
  largeList,
  { itemHeight: 48, overscan: 10 }
)
```

---

## 8. 响应式解包注意事项

### 模板自动解包

在模板中，`ref` 自动解包，不需要 `.value`：

```vue
<template>
  <!-- ✅ 自动解包 -->
  <div>{{ count }}</div>

  <!-- ❌ 不需要 .value -->
  <div>{{ count.value }}</div>
</template>
```

### reactive 内的 ref 自动解包

```typescript
const state = reactive({
  count: ref(0),
  name: 'test'
})

// ✅ reactive 对象中 ref 自动解包
console.log(state.count) // 0，不需要 state.count.value
```

### 非响应式对象中的 ref 不解包

```typescript
const map = new Map<string, Ref<number>>()
map.set('a', ref(1))

// ❌ 非 reactive 对象，不会自动解包
console.log(map.get('a')) // Ref 对象，需要 .value
console.log(map.get('a')!.value) // 1
```

---

## 9. effectScope — 管理多个 Composable 的生命周期

当多个 composable 需要同时创建和销毁时，`effectScope` 可以批量管理它们的响应式 effect：

### 基础用法

```typescript
import { effectScope, ref, watchEffect, onScopeDispose } from 'vue'

// 创建独立作用域
const scope = effectScope()

scope.run(() => {
  // 在这个作用域内创建的所有 effect、watch、computed
  // 都会关联到此 scope
  const count = ref(0)

  watchEffect(() => {
    console.log(`Count: ${count.value}`)
  })

  // 注册作用域销毁时的清理函数
  onScopeDispose(() => {
    console.log('Scope disposed')
  })
})

// 一次性停止作用域内的所有 effect
scope.stop()
// 输出: "Scope disposed"
// 所有 watchEffect 停止
```

### 实际场景：Composable 工厂

```typescript
// hooks/web/useControlledEffects.ts
import { effectScope, ref, watch } from 'vue'

export function useControlledEffects() {
  let scope: ReturnType<typeof effectScope> | null = effectScope()
  const isActive = ref(true)

  function run(setup: () => void) {
    scope?.run(() => {
      setup()
    })
  }

  function restart() {
    scope?.stop()
    scope = effectScope()
    isActive.value = false
    nextTick(() => (isActive.value = true))
  }

  onBeforeUnmount(() => {
    scope?.stop()
    scope = null
  })

  return { run, restart, isActive }
}
```

**何时使用 `effectScope`：**
- 需要在组件外手动管理多个 effect 的生命周期（如插件、指令）
- 实现"批量创建/销毁"模式（如路由切换时清理上一页所有 effect）
- 编写 composable 测试时隔离 effect

**何时不需要：**
- 直接在组件内使用 composable — 组件卸载时自动清理
- 单个 `watch` / `watchEffect` — 返回的 `stop` 函数足矣

> 另见：[组合式函数测试](composable-design-patterns.md#9-测试-composable) 了解如何在测试中使用 `effectScope` 隔离 effect。

---

## 10. Store 性能优化

### storeToRefs 避免额外响应式

```typescript
import { storeToRefs } from 'pinia'

const store = useAppStore()

// ✅ GOOD: storeToRefs 只提取响应式属性，不触发额外响应式包装
const { theme, pure } = storeToRefs(store)

// ❌ BAD: 解构丢失响应式
const { theme, pure } = store // 失去响应式

// ❌ BAD: toRefs 对 store 实例做额外包装
const { theme, pure } = toRefs(store) // 不必要，用 storeToRefs
```

### 按需访问 Store 属性

```typescript
// ✅ GOOD: computed 精确追踪
const theme = computed(() => appStore.theme)

// ❌ BAD: 解构整个 store 导致所有属性变化都触发重渲染
const store = useAppStore()
const { theme, pure, layout, ... } = storeToRefs(store) // 过度解构
```

---

## 11. 性能检查清单

### 组件级

- [ ] 大型数据使用 `shallowRef` 而非 `ref`
- [ ] 动态组件使用 `shallowRef`
- [ ] 派生状态用 `computed`，不用方法
- [ ] 避免在 `computed` 中产生副作用
- [ ] 列表使用唯一 `key`
- [ ] 重型组件懒加载
- [ ] 非响应式对象使用 `markRaw` 标记

### 副作用清理

- [ ] 事件监听器在 `onUnmounted` 中移除
- [ ] 定时器在 `onUnmounted` 中清除
- [ ] JSONP 脚本在完成/超时后移除
- [ ] `watch` 返回的 `stop` 函数在适当时机调用
- [ ] `watchEffect` 中使用 `onWatcherCleanup()` 清理异步请求（3.5+）

### Store 使用

- [ ] 组件内用 `useXxxStore()`，组件外用 `useXxxStoreWithOut()`
- [ ] 解构 store 用 `storeToRefs`
- [ ] 避免深层 `watch` store
- [ ] 不暴露整个 store 实例

### 响应式选择

- [ ] 基本类型用 `ref`
- [ ] 不需要深层响应的大型对象用 `shallowRef`
- [ ] 需要旧值对比用 `watch`，否则用 `watchEffect`
- [ ] 模板中不加 `.value`
- [ ] 多个 composable 需统一生命周期管理时考虑 `effectScope`
