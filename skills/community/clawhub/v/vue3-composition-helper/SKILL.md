---
name: vue3-composition-helper
description: Vue3 Composition API 速查与最佳实践。当使用Vue3 + TypeScript + <script setup>语法开发时使用。包含常用组合式函数模式、VueUse推荐用法、响应式陷阱避坑、性能优化技巧。所有代码默认使用<script setup>+TypeScript。

**使用时机**：
(1) 用户问Vue3写法、Composition API用法
(2) 需要ref/reactive/computed/watch的正确模式
(3) VueUse函数选择和用法
(4) 组件通信(props/emit/provide/inject)
(5) 用户提到"Vue3"、"script setup"、"Composition API"
---

# Vue3 Composition API 助手

## 基本原则

- **所有代码使用 `<script setup lang="ts">`**
- **优先 VueUse**，不重复造轮子
- **ref 用于基础类型，reactive 用于对象**（避免 reactive 解构丢失响应性）

## 响应式速查

```typescript
import { ref, reactive, computed, watch, watchEffect } from 'vue'
import { useStorage, useDebounceFn, useWindowSize } from '@vueuse/core'

// ref - 基础类型
const count = ref(0)
const user = ref<User | null>(null)

// reactive - 对象（⚠️ 不要解构，会丢失响应性）
const state = reactive({
  loading: false,
  data: [] as Item[],
  error: null as string | null,
})

// computed - 派生状态
const filteredList = computed(() =>
  state.data.filter(item => item.active)
)

// watch - 副作用
watch(count, (newVal) => {
  console.log('count changed:', newVal)
}, { immediate: false })

// watchEffect - 自动追踪依赖
watchEffect(() => {
  console.log('data length:', state.data.length)
})
```

## VueUse 常用函数

```typescript
import {
  useStorage,        // localStorage 响应式绑定
  useDebounceFn,     // 防抖
  useThrottleFn,     // 节流
  useWindowSize,     // 窗口尺寸
  useMouse,          // 鼠标位置
  useEventListener,  // 事件监听（自动清理）
  useIntersectionObserver, // 元素可见性
  useClipboard,      // 剪贴板
  useTitle,          // 页面标题
  useAsyncState,     // 异步状态管理
} from '@vueuse/core'

// localStorage 持久化（替代 ref + onMounted 写入）
const theme = useStorage('theme', 'dark')

// 防抖搜索
const debouncedSearch = useDebounceFn((query: string) => {
  fetchResults(query)
}, 300)

// 异步状态（替代 loading + error 手动管理）
const { state, isLoading, error } = useAsyncState(
  fetchItems(),
  { items: [] as Item[] },
)
```

## 组件通信

```typescript
// Props（带类型）
interface Props {
  title: string
  count?: number  // 可选
  items: Item[]
}
const props = withDefaults(defineProps<Props>(), {
  count: 0,
})

// Emit（带类型）
interface Emits {
  change: [value: string]
  update: [id: string, data: Partial<Item>]
}
const emit = defineEmits<Emits>()

// 跨层级通信
// 祖先组件
provide('config', { theme: 'dark', locale: 'zh-CN' })
// 后代组件
const config = inject<Config>('config')!
```

## 生命周期（Composition API 风格）

```typescript
import { onMounted, onUnmounted, onBeforeUnmount } from 'vue'

onMounted(() => {
  // 初始化
})

// 用 useEventListener 自动清理，比手动 onUnmounted 更优雅
useEventListener(window, 'resize', handleResize)
```

## 性能陷阱

```typescript
// ❌ 陷阱1：reactive 解构丢失响应性
const { name, age } = reactive(user) // name/age 不是响应式的！

// ✅ 正确：toRefs 或直接使用
import { toRefs } from 'vue'
const { name, age } = toRefs(reactive(user))

// ❌ 陷阱2：v-for 中使用复杂表达式
<div v-for="item in list" :key="item.id">
  {{ heavyCompute(item) }}  <!-- 每次渲染都计算 -->
</div>

// ✅ 正确：computed 缓存
const computedList = computed(() =>
  list.value.map(item => ({ ...item, result: heavyCompute(item) }))
)

// ❌ 陷阱3：不必要的响应式
const config = reactive({ apiUrl: 'https://...' }) // 不会变的数据不需要响应式

// ✅ 正确：用普通常量
const CONFIG = { apiUrl: 'https://...' } as const
```

## 通用组件模式

```typescript
// 可控/非可控组件
interface Props {
  modelValue: string
}
const props = defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()
const internal = ref(props.modelValue)

watch(() => props.modelValue, (v) => { internal.value = v })
watch(internal, (v) => { emit('update:modelValue', v) })

// 列表+虚拟滚动
import { useVirtualList } from '@vueuse/core'
const { list, containerProps, wrapperProps } = useVirtualList(
  largeDataSource,
  { itemHeight: 48, overscan: 5 }
)
```
