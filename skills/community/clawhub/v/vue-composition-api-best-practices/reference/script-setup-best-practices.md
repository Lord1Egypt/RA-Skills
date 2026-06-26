---
title: script setup Best Practices
impact: HIGH
impactDescription: 滥用 script setup 特性会导致类型安全问题、运行时错误以及更难维护的代码
type: best-practice
tags: [vue3, composition-api, script-setup, typescript, best-practices]
---

# script setup 最佳实践

**影响程度：高** — `<script setup>` 是编写 Vue 3 组件的推荐方式。理解其模式可确保类型安全和可维护性。

## 任务清单

- [ ] 使用 `<script setup lang="ts">` 以支持 TypeScript
- [ ] 使用 `defineOptions` 设置组件名称（Vue 3.3+）—— 务必始终使用
- [ ] 使用类型声明式的 `defineProps` 和 `defineEmits`
- [ ] 使用 `defineModel` 实现双向绑定（Vue 3.4+）
- [ ] 使用 `useTemplateRef()` 获取类型安全的模板引用（Vue 3.5+）
- [ ] 使用 `useId()` 生成无障碍友好的唯一 ID（Vue 3.5+）
- [ ] 优先使用 `toValue()` 而非 `unref()` 来解包 MaybeRef（Vue 3.3+）
- [ ] 使用 `InjectionKey` 为 `provide`/`inject` 添加类型
- [ ] 避免将 `<script setup>` 与 Options API 混用
- [ ] 在组件内和组件外使用正确的 Store 访问模式

## 问题所在

使用 `<script setup>` 时的常见错误可能导致类型问题、响应性丢失或令人困惑的代码模式。

## defineOptions — 务必始终使用

`defineOptions` 对于 DevTools 识别、`keep-alive` 的 include/exclude 以及递归组件至关重要：

```vue
<script setup lang="ts">
// ✅ Good - 始终设置组件名称
defineOptions({
  name: 'MiSearch'
})
</script>
```

**在真实项目中的重要性：**
- Vue DevTools 显示组件名称而非 `<Anonymous>`
- `<keep-alive :include="['MiSearch']">` 可以正常工作
- 递归组件可以引用自身
- 调试堆栈信息具有可读性
- 更易于在代码库中按组件名称搜索

## TypeScript 集成

### 带类型的 Props

**BAD — 运行时声明：**

```vue
<script setup lang="ts">
// props 使用时没有类型推导
const props = defineProps({
  title: String,
  count: {
    type: Number,
    default: 0
  }
})
// props.title 的类型是 string | undefined，而不是 string
</script>
```

**GOOD — 基于类型的声明：**

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

// props.title 的类型是 string（必填、已定义）
// props.count 的类型是 number（可选、有默认值）
</script>
```

### 带类型的 Emits

**BAD — 无类型安全：**

```vue
<script setup lang="ts">
const emit = defineEmits(['update', 'delete'])
// 没有参数类型检查
emit('update', { any: 'thing' })
</script>
```

**GOOD — 类型安全的 emits：**

```vue
<script setup lang="ts">
interface Emits {
  update: [value: { id: string; name: string }]
  delete: [id: string]
}

const emit = defineEmits<Emits>()

// 类型检查！
emit('update', { id: '1', name: 'Test' }) // ✅
emit('update', { wrong: 'type' }) // ❌ Error
emit('delete', '123') // ✅
</script>
```

## defineModel 实现双向绑定

**Vue 3.4+ 特性：**

```vue
<script setup lang="ts">
// 简单 model
const model = defineModel<string>()
model.value = 'new value' // 更新父组件

// 带选项
const count = defineModel<number>({
  default: 0,
  required: true
})

// 命名 model
const title = defineModel<string>('title')
const description = defineModel<string>('description')

// 带校验器
const email = defineModel<string>({
  default: '',
  validator: (value) => value.includes('@')
})
</script>

<template>
  <input v-model="model" />
  <input v-model:title="title" v-model:description="description" />
</template>
```

**Vue 3.4 之前（手动实现）：**

```vue
<script setup lang="ts">
const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script>
```

## Store 访问模式

### 在 Vue 组件内 — 使用 `useXxxStore()`

```vue
<script setup lang="ts">
// ✅ Good - 在组件内，使用标准的 store 访问方式
const appStore = useAppStore()
const businessStore = useBusinessStore()

// 在组件中直接访问
const isDark = computed(() => appStore.getIsDark)
</script>
```

### 在 Vue 组件外 — 使用 `useXxxStoreWithOut()`

```typescript
// ✅ Good - 在 utils、hooks、plugins 中使用 WithOut 版本
import { useAppStoreWithOut } from '@/store/modules/app'

export const useEngine = () => {
  const appStore = useAppStoreWithOut() // 传入全局 pinia 实例
  // ...
}
```

```typescript
// ✅ Good - 在 utils/migration.ts 中
import { useAppStoreWithOut } from '@/store/modules/app'

export async function migrateOnlineIcons() {
  const appStore = useAppStoreWithOut()
  // 可以在组件上下文之外访问 store
}
```

```typescript
// ✅ Good - 在 plugins/vue-i18n/index.ts 中
import { useLocaleStoreWithOut } from '@/store/modules/locale'

export async function setupI18n(app: App) {
  const localeStore = useLocaleStoreWithOut()
  // ...
}
```

**区分两者的原因：**
- `useXxxStore()` 依赖 Vue 的 `inject`/`provide`，仅在组件上下文中可用
- `useXxxStoreWithOut(store)` 显式传入 pinia 实例，可在任意位置使用
- 使用错误会导致运行时错误：`getActivePinia was called with no active Pinia`

详见 [store-without-pattern](store-without-pattern.md)。

## 常见模式

### 带默认值的响应式 Props

```vue
<script setup lang="ts">
interface Props {
  items: string[]
  pageSize?: number
}

const props = withDefaults(defineProps<Props>(), {
  pageSize: 10
})

// 使用 toRefs 获取响应式 props
const { pageSize } = toRefs(props)

// 或使用 computed 获取派生值
const totalPages = computed(() =>
  Math.ceil(props.items.length / pageSize.value)
)
</script>
```

### 暴露组件方法

```vue
<script setup lang="ts">
const inputRef = ref<HTMLInputElement | null>(null)

const focus = () => {
  inputRef.value?.focus()
}

const clear = () => {
  inputRef.value!.value = ''
}

// 暴露方法供父组件调用
defineExpose({
  focus,
  clear
})
</script>
```

### 模板引用

```vue
<script setup lang="ts">
// 元素引用
const inputRef = ref<HTMLInputElement | null>(null)

// 组件引用
const componentRef = ref<InstanceType<typeof MyComponent> | null>(null)

// v-for 中的引用数组
const itemRefs = ref<HTMLDivElement[]>([])

onMounted(() => {
  inputRef.value?.focus()
})
</script>

<template>
  <input ref="inputRef" />
  <MyComponent ref="componentRef" />
  <div v-for="item in items" :key="item.id" ref="itemRefs">
    {{ item.name }}
  </div>
</template>
```

### useTemplateRef（Vue 3.5+）

**Vue 3.5 引入了 `useTemplateRef()`** — 一种类型安全的替代方案，用于替代普通的 `ref()` 来获取模板引用。它解决了尴尬的 `null` 初始化问题，并提供更好的类型推导：

```vue
<script setup lang="ts">
// ✅ Vue 3.5+：无需 null 初始值，类型从模板中推导
const inputRef = useTemplateRef<HTMLInputElement>('inputRef')
const componentRef = useTemplateRef<InstanceType<typeof MyComponent>>('componentRef')

onMounted(() => {
  inputRef.value?.focus() // HTMLInputElement | undefined
})
</script>

<template>
  <input ref="inputRef" />
  <MyComponent ref="componentRef" />
</template>
```

**与 `ref<T | null>` 的关键区别：**

| 特性 | `ref<T \| null>` | `useTemplateRef<T>()` |
|---------|-------------------|-----------------------|
| 初始值 | 必须指定 `null` | 自动推导，无需手动设置 null |
| 挂载后的类型 | `T \| null` | `T \| undefined` |
| 需要 ref 名称匹配 | 手动（靠约定） | 通过字符串参数强制匹配 |
| 支持 v-for | ✅ `ref<T[]>([])` | ✅ `useTemplateRef<T[]>('list')` |

### useId（Vue 3.5+）

**Vue 3.5 引入了 `useId()`**，用于生成唯一的、SSR 安全的 ID。对于无障碍访问（`aria-labelledby`、`for`/`id` 关联）和避免 ID 冲突至关重要：

```vue
<script setup lang="ts">
const inputId = useId()
const labelId = useId()
</script>

<template>
  <label :for="inputId" :id="labelId">Email</label>
  <input :id="inputId" :aria-labelledby="labelId" />
</template>
```

**为什么不使用 `Math.random()` 或计数器？**
- `useId()` 是 SSR 安全的 — 服务端和客户端生成匹配的 ID
- 不会在组件实例之间产生冲突
- 在客户端导航（SPA 路由切换）之间会清除

### Provide/Inject 与 TypeScript

`provide`/`inject` 是避免 props 逐层传递的强大工具，但类型安全需要明确的模式：

**步骤 1：定义 `InjectionKey`**

```typescript
// types/injection-keys.ts
import type { InjectionKey, Ref } from 'vue'

// 类型化的 injection key
export const THEME_KEY: InjectionKey<Ref<'light' | 'dark'>> = Symbol('theme')
export const CONFIG_KEY: InjectionKey<AppConfig> = Symbol('config')
```

**步骤 2：带类型安全地 provide**

```vue
<script setup lang="ts">
import { provide } from 'vue'
import { THEME_KEY, CONFIG_KEY } from '@/types/injection-keys'

const theme = ref<'light' | 'dark'>('light')
const appConfig = { apiUrl: 'https://api.example.com', timeout: 5000 }

provide(THEME_KEY, theme)  // ✅ 类型检查通过
provide(CONFIG_KEY, appConfig)  // ✅ 类型检查通过

// ❌ Error：类型错误
provide(THEME_KEY, 'blue')
</script>
```

**步骤 3：带类型安全地 inject**

```vue
<script setup lang="ts">
import { inject } from 'vue'
import { THEME_KEY, CONFIG_KEY } from '@/types/injection-keys'

// ✅ 使用 InjectionKey — 完全类型化，无需默认值
const theme = inject(THEME_KEY) // Ref<'light' | 'dark'>

// ✅ 带默认值 — 类型推导，不会是 undefined
const config = inject(CONFIG_KEY, { apiUrl: '/fallback', timeout: 3000 })

// ⚠️ 不使用 key 或默认值 — 返回 T | undefined
const maybeConfig = inject<AppConfig>('config') // AppConfig | undefined
</script>
```

| 模式 | 返回类型 | 使用场景 |
|---------|------------|-------------|
| `inject(key)` 配合 `InjectionKey` | `T`（不可为 null） | 祖先组件中存在 provider |
| `inject(key, default)` | `T`（不可为 null） | provider 可能不存在 |
| `inject<string>('key')` | `T \| undefined` | 旧的字符串 key 模式 |

**⚠️ 在 TypeScript 中不要使用纯字符串进行 provide/inject** — 你会失去所有类型安全和 IDE 自动补全。

### toValue() vs unref()

**Vue 3.3 引入了 `toValue()`**，作为解包 "MaybeRef" 值的首选方式：

```typescript
import { toValue, unref } from 'vue'
import type { MaybeRef } from 'vue'

// 两者都可以标准化 ref 和普通值
const a = ref(42)
const b = 100

toValue(a) // 42 — 解包 ref，透传普通值
toValue(b) // 100

unref(a)  // 42 — 行为相同
unref(b)  // 100

// 但 toValue() 有一个关键区别：
// toValue() 还可以解包 getter（返回值的函数）
const getter = () => 42
toValue(getter) // 42 ✅
unref(getter)   // () => 42 ❌（不会调用 getter）
```

**经验法则：**
- 如果你的组合式函数接受 `MaybeRef<T>` — 使用 `toValue()` 来标准化
- 如果你只处理 `Ref` 对象 — `unref()` 也可以
- 新代码应优先使用 `toValue()` 以保持向前兼容

## 应避免的反模式

### ❌ 不要与 Options API 混用

```vue
<!-- BAD - 混合风格 -->
<script>
export default {
  data() {
    return {
      count: 0
    }
  }
}
</script>

<script setup lang="ts">
// 无法在这里访问 Options API 的 data！
const double = computed(() => this.count * 2) // Error!
</script>
```

### ❌ 不要解构 Props

```vue
<script setup lang="ts">
const props = defineProps<{ count: number }>()

// BAD - 丢失响应性
const { count } = props

// GOOD - 使用 toRefs
const { count } = toRefs(props)

// 或者直接使用 props
const double = computed(() => props.count * 2)
</script>
```

### ❌ 不要在 script setup 中使用 `this`

```vue
<script setup lang="ts">
// ❌ Error：'this' 是 undefined
console.log(this.$router)

// ✅ 改用组合式函数
import { useRouter } from 'vue-router'
const router = useRouter()
console.log(router)
</script>
```

### ❌ 不要忘记 ref 的 `.value`

```vue
<script setup lang="ts">
const count = ref(0)

// ❌ 不会触发响应性
count = 1

// ✅ 正确方式
count.value = 1

// 模板中不需要 .value
</script>

<template>
  <!-- 模板中自动解包 -->
  <div>{{ count }}</div>
</template>
```

### ❌ 不要在组件外使用 `useXxxStore()`

```typescript
// ❌ Bad - 在 utils/hooks/plugins 中会抛出错误
import { useAppStore } from '@/store/modules/app'
export function someUtil() {
  const store = useAppStore() // Error: pinia is not defined
}

// ✅ Good - 使用 WithOut 版本
import { useAppStoreWithOut } from '@/store/modules/app'
export function someUtil() {
  const store = useAppStoreWithOut() // 正常工作！
}
```

## 性能提示

### 对大型对象和动态组件使用 shallowRef

```vue
<script setup lang="ts">
// 动态组件切换 — 使用 shallowRef 避免深层响应性
const activeCom = shallowRef()
watchEffect(() => {
  activeCom.value = isPure.value ? PureMode : HomeMode
})

// 大型数据对象 — 替换整个值时使用 shallowRef
const largeData = shallowRef<BigObject>({})
largeData.value = { /* 新对象 */ } // 仅在引用变化时触发更新
</script>
```

### 对派生状态使用 computed

```vue
<script setup lang="ts">
const items = ref<string[]>([])

// ✅ 高效 - 缓存直到 items 变化
const sortedItems = computed(() =>
  [...items.value].sort()
)

// ❌ 低效 - 每次渲染都重新创建
const getSortedItems = () => [...items.value].sort()
</script>
```

## 参考资料

- [Vue.js script setup](https://vuejs.org/api/sfc-script-setup.html)
- [Vue.js TypeScript with Composition API](https://vuejs.org/guide/typescript/composition-api.html)
- [Vue.js defineModel](https://vuejs.org/api/sfc-script-setup.html#definemodel)
- [Vue.js defineOptions](https://vuejs.org/api/sfc-script-setup.html#defineoptions)
- [Vue.js useTemplateRef](https://vuejs.org/api/composition-api-helpers.html#usetemplateref)
- [Vue.js useId](https://vuejs.org/api/composition-api-helpers.html#useid)
- [Vue.js provide/inject](https://vuejs.org/guide/components/provide-inject.html#working-with-reactivity)
- [Vue.js toValue](https://vuejs.org/api/reactivity-utilities.html#tovalue)
