---
title: Feature Extraction to Composables
impact: MEDIUM
impactDescription: 未能提取可复用逻辑将导致代码重复、组件间行为不一致以及更高的维护成本
type: best-practice
tags: [vue3, composition-api, composables, reusability, dry]
---

# 将功能提取为组合式函数

**影响等级：MEDIUM** - 将通用功能提取到外部组合式函数中可以促进代码复用、保持一致性和简化测试。

## 任务清单

- [ ] 识别多个组件中使用的逻辑
- [ ] 提取到 `composables/` 或 `hooks/` 目录
- [ ] 保持组合式函数专注于单一职责
- [ ] 使用参数进行配置和依赖注入
- [ ] 返回响应式引用和方法
- [ ] 考虑使用 Store 桥接模式抽象 store 访问

## 问题

当相似逻辑在多个组件中重复时，任何 bug 修复或功能增强都必须在多处应用，增加了维护负担和不一致的风险。

**BAD - 组件间重复的逻辑：**

```vue
<!-- ComponentA.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const width = ref(window.innerWidth)
const height = ref(window.innerHeight)

function handleResize() {
  width.value = window.innerWidth
  height.value = window.innerHeight
}

onMounted(() => window.addEventListener('resize', handleResize))
onUnmounted(() => window.removeEventListener('resize', handleResize))
</script>

<!-- ComponentB.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const width = ref(window.innerWidth)
const height = ref(window.innerHeight)

function handleResize() {
  width.value = window.innerWidth
  height.value = window.innerHeight
}

onMounted(() => window.addEventListener('resize', handleResize))
onUnmounted(() => window.removeEventListener('resize', handleResize))

// 使用 width/height 的其他逻辑...
</script>
```

**GOOD - 提取到组合式函数：**

```typescript
// hooks/web/useWindowSize.ts
import { ref, onMounted, onUnmounted } from 'vue'

export function useWindowSize() {
  const width = ref(window.innerWidth)
  const height = ref(window.innerHeight)

  function handleResize() {
    width.value = window.innerWidth
    height.value = window.innerHeight
  }

  onMounted(() => window.addEventListener('resize', handleResize))
  onUnmounted(() => window.removeEventListener('resize', handleResize))

  return { width, height }
}
```

```vue
<!-- ComponentA.vue / ComponentB.vue -->
<script setup lang="ts">
import { useWindowSize } from '@/hooks/web/useWindowSize'

const { width, height } = useWindowSize()
</script>
```

## 何时提取

| 信号 | 示例 | 操作 |
|--------|---------|--------|
| 在 2+ 组件中使用 | 窗口大小、认证状态 | 提取到组合式函数 |
| 复杂逻辑 | 表单验证、分页 | 提取以提高清晰度 |
| 需要测试 | API 调用、状态机 | 提取以实现隔离 |
| 第三方集成 | 数据分析、WebSocket | 提取以实现抽象 |
| Store 访问模式 | 页面图标、侧边栏分类 | 提取为 Store 桥接组合式函数 |
| 横切关注点 | 事件总线、网络状态 | 提取以保持一致性 |

## 提取模式

### 模式 1：简单工具组合式函数

无状态或最小状态，单一用途：

```typescript
// hooks/web/useDesign.ts
import variables from '@/styles/global.module.less'

export const useDesign = () => {
  const lessVariables = variables

  const getPrefixCls = (scope: string) => {
    return `${lessVariables.namespace}-${scope}`
  }

  return {
    variables: lessVariables,
    simplePrefixCls: lessVariables.miNamespace,
    getPrefixCls
  }
}
```

### 模式 2：Store 桥接组合式函数

将 store 访问封装在清晰的 API 之后。这是实际项目中最具影响力的提取模式：

```typescript
// hooks/web/useEngine.ts
import { useAppStoreWithOut } from '@/store/modules/app'
import { SEARCH_ENGINE_INFO, SEARCH_ENGINE_ORDER } from '@/config/setting'

export const useEngine = () => {
  const appStore = useAppStoreWithOut()

  // 当前选中搜索引擎
  const selectEngine = computed(() => appStore.selectEngine)

  // 当前设定搜索引擎列表（过滤后）
  const searchEngine = computed(() =>
    SEARCH_ENGINE_ORDER.filter((engine) => appStore.searchEngine.includes(engine))
  )

  // 当前选中搜索引擎详细信息
  const engineInfo = computed(() => SEARCH_ENGINE_INFO[selectEngine.value])

  // 更新搜索引擎
  const updateSelectEngine = (val: SearchEngine) => {
    appStore.setSelectEngine(val)
  }

  // 下一个搜索引擎
  const nextEngine = () => {
    const idx = appStore.searchEngine.indexOf(selectEngine.value)
    if (idx === appStore.searchEngine.length - 1) {
      appStore.setSelectEngine(appStore.searchEngine[0])
    } else {
      appStore.setSelectEngine(appStore.searchEngine[idx + 1])
    }
  }

  return { selectEngine, engineInfo, searchEngine, nextEngine, updateSelectEngine }
}
```

**为什么 Store 桥接很重要：**
- 组件不需要 `import { useAppStore }` 和了解 store 结构
- 业务规则（例如 `SEARCH_ENGINE_ORDER.filter`）集中在一处
- 可以轻松替换 store 实现，无需修改组件
- 通过 `useXxxStoreWithOut` 可在组件外使用

### 模式 3：基于事件的组合式函数

管理副作用并自动清理：

```typescript
// hooks/web/useNetwork.ts
import { ref, onBeforeUnmount } from 'vue'

export const useNetwork = () => {
  const online = ref(true)

  const updateNetwork = () => {
    online.value = navigator.onLine
  }

  window.addEventListener('online', updateNetwork)
  window.addEventListener('offline', updateNetwork)

  onBeforeUnmount(() => {
    window.removeEventListener('online', updateNetwork)
    window.removeEventListener('offline', updateNetwork)
  })

  return { online }
}
```

### 模式 4：参数化组合式函数

接受配置以实现灵活性：

```typescript
// hooks/web/useCoordinateArea.ts
interface Coordinate { x1: number; y1: number; x2: number; y2: number }
type DirectionX = 'ltr' | 'rtl'
type DirectionY = 'ttb' | 'btt'

export const useCoordinateArea = (
  coordinate: Coordinate,
  direction: DirectionX = 'ltr',
  directionY: DirectionY = 'ttb'
) => {
  const { width, height } = useWindowSize()
  const { x, y } = useMouse()

  const { x1, y1, x2, y2 } = coordinate

  const inCoordinateX = computed(() =>
    direction === 'ltr'
      ? x.value > x1 && x.value < x2
      : x.value > width.value - x2 && x.value < width.value - x1
  )

  const inCoordinateY = computed(() =>
    directionY === 'ttb'
      ? y.value > y1 && y.value < y2
      : y.value > height.value - y2 && y.value < height.value - y1
  )

  const inCoordinate = computed(() => inCoordinateX.value && inCoordinateY.value)

  return { inCoordinate }
}
```

### 模式 5：第三方集成组合式函数

用 Vue 友好的 API 封装第三方库：

```typescript
// hooks/web/useCache.ts
import WebStorageCacheCrypto from 'web-storage-cache-crypto'
import sm4 from '@/utils/cipher/sm4'

type CacheType = 'localStorage' | 'sessionStorage'

export const CACHE_KEY = {
  LANG: 'miao-lang',
  DICT_CACHE: 'dictCache',
  MIAOWING_APP: 'miaowing-app',
  MIAOWING_BUSINESS: 'miaowing-business'
}

export const useCache = (type: CacheType = 'localStorage', crypt: boolean = true) => {
  const wsCache = new WebStorageCacheCrypto({
    storage: type,
    crypt: Boolean(crypt),
    encrypt: sm4.encrypt,
    decrypt: sm4.decrypt
  })

  return { wsCache }
}
```

## 目录结构

```
src/
├── hooks/                     # 组合式函数目录
│   ├── event/                 # 事件相关的组合式函数
│   │   └── useScrollTo.ts     # 平滑滚动
│   └── web/                   # Web API 与业务逻辑组合式函数
│       ├── useCache.ts        # 加密存储
│       ├── useCoordinateArea.ts  # 鼠标位置检测
│       ├── useDesign.ts       # CSS 命名空间
│       ├── useEmitt.ts        # 事件总线
│       ├── useEngine.ts       # 搜索引擎（Store 桥接）
│       ├── useI18n.ts         # i18n 命名空间封装
│       ├── useLocale.ts       # 语言切换
│       ├── useLocalForage.ts  # IndexedDB 存储
│       ├── useNetwork.ts      # 网络状态
│       ├── usePageIcon.ts     # 页面图标（Store 桥接）
│       ├── useSideCategory.ts # 侧边栏分类（Store 桥接）
│       ├── useSuggestion.ts   # 搜索建议 JSONP
│       └── useTimeAgo.ts      # 相对时间
```

**命名规范：**
- 文件名与函数名一致：`useEngine.ts` → `export const useEngine = () => {}`
- 按领域分组：`event/` 用于 DOM 事件，`web/` 用于 Web API 和业务逻辑
- 每个文件一个组合式函数

## 最佳实践

### 1. 单一职责

```typescript
// ✅ 好 — 只专注一件事
export function useLocalStorage<T>(key: string, defaultValue: T) {
  const stored = localStorage.getItem(key)
  const data = ref<T>(stored ? JSON.parse(stored) : defaultValue)

  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue))
  }, { deep: true })

  return { data }
}

// ❌ 差 — 混合了多个关注点
export function useUserStorageAndAuth() {
  // 太多职责混在一起
}
```

> **注意：** 上述 `useLocalStorage` 直接使用了浏览器 API。如果你的项目需要支持 SSR，应从 `@vueuse/core` 引入 `useStorage`，它会自动处理非浏览器环境。

### 2. 接受 Ref 以保持响应性

```typescript
// ✅ 好 — 同时接受原始值和 ref
export function useSearch(query: MaybeRef<string>) {
  const results = ref([])

  watch(
    () => toValue(query),
    async (q) => {
      results.value = await searchAPI(q)
    }
  )

  return { results }
}

// 用法
const query = ref('')
const { results } = useSearch(query) // 响应式！
const { results } = useSearch('static') // 也可以工作
```

### 3. 返回响应式引用

```typescript
// ✅ 好 — 返回 ref 用于模板绑定
export function useTimer() {
  const seconds = ref(0)
  const isRunning = ref(false)
  return { seconds, isRunning, start, stop }
}

// ❌ 差 — 返回普通值，丢失响应性
export function useTimer() {
  let seconds = 0
  return { seconds } // 不是响应式的！
}
```

### 4. 自动清理

始终在 `onBeforeUnmount` 中清理副作用：

```typescript
// ✅ 好 — 卸载时清理
export const useNetwork = () => {
  const online = ref(true)
  const update = () => { online.value = navigator.onLine }

  window.addEventListener('online', update)
  window.addEventListener('offline', update)

  onBeforeUnmount(() => {
    window.removeEventListener('online', update)
    window.removeEventListener('offline', update)
  })

  return { online }
}
```

## 参考

- [Vue.js Composables](https://vuejs.org/guide/reusability/composables.html)
- [VueUse - Collection of Vue Composition Utilities](https://vueuse.org/)
- [Vue.js Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html)
