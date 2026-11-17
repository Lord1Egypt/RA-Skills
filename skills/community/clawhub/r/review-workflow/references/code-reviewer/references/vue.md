# Vue 3 Code Review Guide

> Vue 3 Composition API 代码审查指南，覆盖响应性系统、Props/Emits、Watchers、Composables、Vue 3.5 新特性等核心主题。

## 目录

- [响应性系统](#响应性系统)
- [Props & Emits](#props--emits)
- [Vue 3.5 新特性](#vue-35-新特性)
- [Watchers](#watchers)
- [模板最佳实践](#模板最佳实践)
- [Composables](#composables)
- [性能优化](#性能优化)
- [Review Checklist](#review-checklist)

---

## 响应性系统

### ref vs reactive 选择

```vue
<!-- ✅ 现代最佳实践：全部使用 ref，保持一致性 -->
<script setup lang="ts">
const user = ref<User | null>(null)
const loading = ref(false)
const error = ref<Error | null>(null)
</script>
```

### 解构 reactive 对象

```vue
<!-- ❌ 解构 reactive 会丢失响应性 -->
<script setup lang="ts">
const state = reactive({ count: 0, name: 'Vue' })
const { count, name } = state  // 丢失响应性！
</script>

<!-- ✅ 使用 toRefs 保持响应性 -->
<script setup lang="ts">
const state = reactive({ count: 0, name: 'Vue' })
const { count, name } = toRefs(state)  // 保持响应性
</script>
```

### computed 副作用

```vue
<!-- ❌ computed 中产生副作用 -->
<script setup lang="ts">
const fullName = computed(() => {
  console.log('Computing...')  // 副作用！
  otherRef.value = 'changed'   // 修改其他状态！
  return `${firstName.value} ${lastName.value}`
})
</script>

<!-- ✅ computed 只用于派生状态 -->
<script setup lang="ts">
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`
})
</script>
```

### shallowRef 优化

```vue
<!-- ✅ 大型对象使用 shallowRef 避免深度转换 -->
<script setup lang="ts">
const largeData = shallowRef(hugeNestedObject)

// 整体替换才会触发更新
function updateData(newData) {
  largeData.value = newData  // ✅ 触发更新
}
</script>
```

---

## Props & Emits

### defineProps 类型声明

```vue
<!-- ✅ 使用类型声明 + withDefaults -->
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  items?: string[]
}
const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => []  // 对象/数组默认值需要工厂函数
})
</script>
```

### defineEmits 类型安全

```vue
<!-- ✅ 完整的类型定义 -->
<script setup lang="ts">
const emit = defineEmits<{
  update: [id: number, value: string]
  delete: [id: number]
}>()

emit('update', 1, 'new value')  // ✅
emit('update', 'wrong')  // ❌ TypeScript 报错
</script>
```

---

## Vue 3.5 新特性

### Reactive Props Destructure (3.5+)

```vue
<!-- ✅ Vue 3.5+：解构保持响应性 -->
<script setup lang="ts">
const { count, name = 'default' } = defineProps<{
  count: number
  name?: string
}>()

// count 和 name 自动保持响应性！
watch(() => count, (newCount) => {
  console.log('Count changed:', newCount)
})
</script>
```

### defineModel (3.4+)

```vue
<!-- ✅ defineModel：简洁的 v-model 实现 -->
<script setup lang="ts">
const model = defineModel<string>()

// 多个 v-model
const firstName = defineModel<string>('firstName')
const lastName = defineModel<string>('lastName')
</script>
<template>
  <input v-model="model" />
</template>
```

### useTemplateRef (3.5+)

```vue
<!-- ✅ useTemplateRef：更清晰的模板引用 -->
<script setup lang="ts">
import { useTemplateRef } from 'vue'

const input = useTemplateRef<HTMLInputElement>('my-input')

onMounted(() => {
  input.value?.focus()
})
</script>
<template>
  <input ref="my-input" />
</template>
```

### useId (3.5+)

```vue
<!-- ✅ useId：SSR 安全的唯一 ID -->
<script setup lang="ts">
import { useId } from 'vue'

const id = useId()
</script>
<template>
  <label :for="id">Name</label>
  <input :id="id" />
</template>
```

---

## Watchers

### watch vs watchEffect

```vue
<script setup lang="ts">
// ✅ watch：明确指定依赖，惰性执行
watch(
  () => props.userId,
  async (userId) => {
    user.value = await fetchUser(userId)
  }
)

// ✅ watchEffect：自动收集依赖，立即执行
watchEffect(async () => {
  user.value = await fetchUser(props.userId)
})

// 💡 选择指南：
// - 需要旧值？用 watch
// - 需要惰性执行？用 watch
// - 依赖复杂？用 watchEffect
</script>
```

### watch 清理函数

```vue
<!-- ✅ 使用 onCleanup 清理副作用 -->
<script setup lang="ts">
watch(searchQuery, async (query, _, onCleanup) => {
  const controller = new AbortController()
  onCleanup(() => controller.abort())

  try {
    const data = await fetch(`/api/search?q=${query}`, {
      signal: controller.signal
    })
    results.value = await data.json()
  } catch (e) {
    if (e.name !== 'AbortError') throw e
  }
})
</script>
```

---

## 模板最佳实践

### v-for 的 key

```vue
<!-- ❌ v-for 中使用 index 作为 key -->
<template>
  <li v-for="(item, index) in items" :key="index">
    {{ item.name }}
  </li>
</template>

<!-- ✅ 使用唯一标识作为 key -->
<template>
  <li v-for="item in items" :key="item.id">
    {{ item.name }}
  </li>
</template>
```

### v-if 和 v-for 优先级

```vue
<!-- ❌ v-if 和 v-for 同时使用 -->
<template>
  <li v-for="user in users" v-if="user.active" :key="user.id">
    {{ user.name }}
  </li>
</template>

<!-- ✅ 使用 computed 过滤 -->
<script setup lang="ts">
const activeUsers = computed(() =>
  users.value.filter(user => user.active)
)
</script>
<template>
  <li v-for="user in activeUsers" :key="user.id">
    {{ user.name }}
  </li>
</template>
```

---

## Composables

### Composable 设计原则

```typescript
// ✅ 好的 composable 设计
export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initialValue

  return {
    count: readonly(count),  // 只读防止外部修改
    increment,
    decrement,
    reset
  }
}

// ❌ 不要返回 .value
export function useBadCounter() {
  const count = ref(0)
  return {
    count: count.value  // ❌ 丢失响应性！
  }
}
```

### Props 传递给 composable

```vue
<!-- ✅ 使用 toRef 或 getter 保持响应性 -->
<script setup lang="ts">
const props = defineProps<{ userId: string }>()
const userIdRef = toRef(props, 'userId')
const { user } = useUser(userIdRef)

// ✅ Vue 3.5+：直接解构使用
const { userId } = defineProps<{ userId: string }>()
const { user } = useUser(() => userId)
</script>
```

### 异步 Composable

```typescript
// ✅ 异步 composable 模式
export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  const execute = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(toValue(url))
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      data.value = await response.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  watchEffect(() => {
    toValue(url)  // 追踪依赖
    execute()
  })

  return {
    data: readonly(data),
    error: readonly(error),
    loading: readonly(loading),
    refetch: execute
  }
}
```

---

## 性能优化

### defineAsyncComponent

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

// ✅ 懒加载组件
const HeavyChart = defineAsyncComponent(() =>
  import('./components/HeavyChart.vue')
)

// ✅ 带加载和错误状态
const AsyncModal = defineAsyncComponent({
  loader: () => import('./components/Modal.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,
  timeout: 3000
})
</script>
```

### KeepAlive + 虚拟列表

```vue
<template>
  <!-- ✅ 缓存动态组件 -->
  <KeepAlive :max="10">
    <component :is="currentTab" />
  </KeepAlive>
</template>

<script setup lang="ts">
// KeepAlive 组件的生命周期钩子
onActivated(() => {
  refreshData()
})

onDeactivated(() => {
  pauseTimers()
})
</script>
```

---

## Review Checklist

### 响应性系统
- [ ] ref 用于基本类型，或统一用 ref
- [ ] 没有解构 reactive 对象（或使用了 toRefs）
- [ ] props 传递给 composable 时保持了响应性
- [ ] shallowRef/shallowReactive 用于大型对象优化
- [ ] computed 中没有副作用

### Props & Emits
- [ ] defineProps 使用 TypeScript 类型声明
- [ ] 复杂默认值使用 withDefaults + 工厂函数
- [ ] defineEmits 有完整的类型定义
- [ ] 没有直接修改 props
- [ ] 考虑使用 defineModel 简化 v-model（Vue 3.4+）

### Vue 3.5 新特性（如适用）
- [ ] 使用 Reactive Props Destructure 简化 props 访问
- [ ] 使用 useTemplateRef 替代 ref 属性
- [ ] 表单使用 useId 生成 SSR 安全的 ID

### Watchers
- [ ] watch/watchEffect 有适当的清理函数
- [ ] 异步 watch 处理了竞态条件
- [ ] 避免过度使用 watcher（优先用 computed）

### 模板
- [ ] v-for 使用唯一且稳定的 key
- [ ] v-if 和 v-for 没有在同一元素上
- [ ] 事件处理使用方法而非内联复杂逻辑
- [ ] 大型列表使用虚拟滚动

### Composables
- [ ] 相关逻辑提取到 composables
- [ ] composables 返回响应式引用（不是 .value）
- [ ] 副作用在组件卸载时清理

### 性能
- [ ] 大型组件拆分为小组件
- [ ] 使用 defineAsyncComponent 懒加载
- [ ] v-memo 用于昂贵的列表渲染
- [ ] KeepAlive 用于缓存动态组件