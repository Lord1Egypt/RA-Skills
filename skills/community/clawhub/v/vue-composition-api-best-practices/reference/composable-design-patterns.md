# 组合式函数设计模式

基于 Vue 3 Composition API 的组合式函数（composable）设计模式总结。

---

## 1. 目录结构规范

```
src/hooks/
├── web/                    # 业务相关 hooks
│   ├── useDesign.ts        # 命名空间/样式前缀
│   ├── useEmitt.ts         # 事件总线
│   ├── useEngine.ts        # 搜索引擎
│   ├── useI18n.ts          # 国际化
│   ├── useLocalForage.ts   # IndexedDB 存储
│   ├── useLocale.ts        # 语言切换
│   ├── useNetwork.ts       # 网络状态
│   ├── usePageIcon.ts      # 页面图标
│   ├── useSideCategory.ts  # 侧边栏分类
│   ├── useSuggestion.ts    # 搜索建议
│   └── useTimeAgo.ts       # 时间格式化
└── event/                  # DOM 事件相关 hooks
    └── useScrollTo.ts      # 滚动定位
```

**规则**：
- 按功能域划分子目录（`web/`、`event/`）
- 每个文件一个 composable，文件名即函数名
- 函数名以 `use` 开头

---

## 2. 五种设计模式

### 模式 1：有状态服务

封装独立的响应式状态和操作逻辑。

```typescript
// hooks/web/useNetwork.ts
import { ref } from 'vue'

export function useNetwork() {
  const isOnline = ref(navigator.onLine)

  const updateOnline = () => (isOnline.value = navigator.onLine)

  window.addEventListener('online', updateOnline)
  window.addEventListener('offline', updateOnline)

  // 注意：此处未自动清理，因为网络状态是全局性的
  // 如果需要组件级清理，参考 Pattern 3

  return { isOnline }
}
```

**特征**：维护全局状态，通常不需要组件级清理。

### 模式 2：Store 桥接

用 composable 封装 store 访问，隐藏 store 内部实现细节。

```typescript
// hooks/web/usePageIcon.ts
import { computed } from 'vue'
import { useBusinessStoreWithOut } from '@/store/modules/business'

export function usePageIcon() {
  const businessStore = useBusinessStoreWithOut()

  const pageIcon = computed(() => businessStore.getPageIcon)

  function addPageIcon(icon: IconItem) {
    businessStore.addPageIcon(icon)
  }

  function removePageIcon(id: string) {
    businessStore.removePageIcon(id)
  }

  return { pageIcon, addPageIcon, removePageIcon }
}
```

**特征**：
- 使用 `useXxxStoreWithOut` 访问 store（因为 hook 可能在组件外使用）
- 对外暴露语义化接口，隐藏 store action 细节
- 不维护自身状态，仅转发 store 数据

**何时使用**：当多个组件需要以相同方式访问同一 store 数据时。

### 模式 3：生命周期感知

自动在组件卸载时清理副作用。

```typescript
// hooks/web/useEmitt.ts
import { onUnmounted } from 'vue'
import { mittBus } from '@/utils/mitt'

export function useEmitt() {
  const listeners: Array<{ event: string; handler: (...args: any[]) => void }> = []

  function on(event: string, handler: (...args: any[]) => void) {
    mittBus.on(event, handler)
    listeners.push({ event, handler })
  }

  function emit(event: string, ...args: any[]) {
    mittBus.emit(event, ...args)
  }

  // 组件卸载时自动解绑所有通过此 hook 注册的事件
  onUnmounted(() => {
    listeners.forEach(({ event, handler }) => {
      mittBus.off(event, handler)
    })
    listeners.length = 0
  })

  return { on, emit }
}
```

**特征**：
- 使用 `onUnmounted` 自动清理
- 内部维护清理队列
- 防止内存泄漏

**何时使用**：涉及事件监听、定时器、DOM 事件等需要清理的副作用。

> 另见：[跨功能依赖 - 模式 4：事件总线模式](cross-feature-dependencies.md#模式-4事件总线模式适用于复杂的多对多场景) 了解此模式在跨组件通信中的实际应用。

### 模式 4：异步资源

封装异步资源加载，提供加载状态。

```typescript
// hooks/web/useLocalForage.ts
import { ref } from 'vue'
import localforage from 'localforage'

export function useLocalForage(storeName: string) {
  const store = localforage.createInstance({ name: storeName })
  const loading = ref(false)

  async function getItem<T>(key: string): Promise<T | null> {
    loading.value = true
    try {
      return await store.getItem<T>(key)
    } finally {
      loading.value = false
    }
  }

  async function setItem<T>(key: string, value: T): Promise<void> {
    loading.value = true
    try {
      await store.setItem(key, value)
    } finally {
      loading.value = false
    }
  }

  return { loading, getItem, setItem }
}
```

**特征**：
- 提供 `loading` 状态
- `try/finally` 保证状态重置
- 支持泛型返回值

**何时使用**：封装 IndexedDB、fetch、文件读取等异步操作。

### 模式 5：参数化工具

接收参数，返回计算结果或操作函数，不维护持久状态。

```typescript
// hooks/web/useDesign.ts
import { useAppStoreWithOut } from '@/store/modules/app'

export function useDesign(scope: string) {
  const appStore = useAppStoreWithOut()

  const prefixCls = computed(() => `${appStore.getPrefixCls}-${scope}`)
  const variables = computed(() => ({
    '--prefix-cls': prefixCls.value,
  }))

  return { prefixCls, variables }
}
```

```typescript
// hooks/event/useScrollTo.ts
export function useScrollTo() {
  function scrollTo(target: HTMLElement, options?: ScrollToOptions) {
    target.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
      ...options,
    })
  }

  return { scrollTo }
}
```

**特征**：
- 纯函数式，无副作用
- 参数决定返回值
- 不需要清理

**何时使用**：工具类逻辑，如样式计算、DOM 操作、格式化函数。

---

## 3. 参数设计原则

### 单一职责参数

```typescript
// ✅ GOOD: 每个参数职责明确
export function useLocalForage(storeName: string) { ... }

// ✅ GOOD: 可选参数用 Options 模式
export function useSuggestion(engine: string, options?: SuggestionOptions) { ... }
```

### Options 模式

当参数超过 2 个时，使用 Options 对象：

```typescript
interface SuggestionOptions {
  timeout?: number
  maxResults?: number
  callbackName?: string
}

export function useSuggestion(engine: string, options?: SuggestionOptions) {
  const { timeout = 5000, maxResults = 10, callbackName } = options ?? {}
  // ...
}
```

---

## 4. 返回值设计原则

### 最小暴露原则

只返回外部真正需要的：

```typescript
// ✅ GOOD: 只暴露必要的接口
export function usePageIcon() {
  const businessStore = useBusinessStoreWithOut()
  const pageIcon = computed(() => businessStore.getPageIcon)

  function addPageIcon(icon: IconItem) { businessStore.addPageIcon(icon) }
  function removePageIcon(id: string) { businessStore.removePageIcon(id) }

  return { pageIcon, addPageIcon, removePageIcon }
}

// ❌ BAD: 暴露了整个 store
export function usePageIcon() {
  const businessStore = useBusinessStoreWithOut()
  return { businessStore } // 调用方可随意修改 store
}
```

### Ref vs Computed

| 返回类型 | 使用场景 | 特征 |
|---------|---------|------|
| `computed` | 派生状态，依赖其他响应式源 | 只读，自动更新，有缓存 |
| `ref` | 独立状态 | 可读写 |
| `readonly(ref)` | 只读状态，内部可修改 | 防止外部篡改 |

```typescript
export function useSideCategory() {
  // 派生自 store → computed
  const categories = computed(() => businessStore.getSideCategory)

  // 独立状态 → ref
  const activeId = ref<string>('')

  // 只读暴露 → readonly
  const isEditing = ref(false)
  const editingState = readonly(isEditing)

  return { categories, activeId, editingState }
}
```

---

## 5. 类型设计原则

### 泛型约束

```typescript
// ✅ GOOD: 泛型支持不同数据类型
export function useLocalForage(storeName: string) {
  async function getItem<T>(key: string): Promise<T | null> { ... }
  async function setItem<T>(key: string, value: T): Promise<void> { ... }
  return { getItem, setItem }
}
```

### 输入类型严格

```typescript
// ✅ GOOD: 参数类型精确
export function useEngine(engineType: SearchEngineType) { ... }

// ❌ BAD: 参数类型过于宽泛
export function useEngine(engineType: string) { ... }
```

### 返回类型推断

让 TypeScript 自动推断返回类型，除非需要导出：

```typescript
// 一般不需要显式声明返回类型
export function usePageIcon() {
  // TypeScript 自动推断返回 { pageIcon: ComputedRef<...>, addPageIcon: (...) => void, ... }
  return { pageIcon, addPageIcon, removePageIcon }
}

// 如果其他模块需要使用返回值类型，用 Extract 类型工具
export type PageIconReturn = ReturnType<typeof usePageIcon>
```

---

## 6. 错误处理原则

### 静默失败 vs 抛出异常

| 场景 | 策略 | 原因 |
|------|------|------|
| 数据获取 | 静默失败 + 降级 | 不应阻塞 UI |
| 关键操作 | 抛出异常 | 必须让调用方感知 |
| 生命周期清理 | 静默失败 | 卸载时不应抛错 |

```typescript
// 数据获取：静默失败 + 降级
export function useSuggestion(engine: string) {
  const suggestions = ref<string[]>([])

  async function fetchSuggestion(keyword: string) {
    try {
      suggestions.value = await doFetch(keyword)
    } catch {
      suggestions.value = [] // 降级为空列表
    }
  }

  return { suggestions, fetchSuggestion }
}

// 关键操作：抛出异常
export function useBackup() {
  async function exportData(): Promise<Blob> {
    const data = await collectData()
    if (!data) throw new Error('No data to export')
    return packZip(data)
  }

  return { exportData }
}
```

---

## 7. Composable 与组件的边界

### 放在 Composable 中

- 可复用的状态逻辑
- 与特定 UI 无关的数据转换
- Store 访问桥接
- 浏览器 API 封装

### 放在组件中

- 模板渲染相关计算
- 仅当前组件使用的 UI 状态（如弹窗开关）
- DOM 直接操作（通过 ref）

```typescript
// ✅ 放 composable：可复用的搜索引擎逻辑
// hooks/web/useEngine.ts
export function useEngine() {
  const businessStore = useBusinessStoreWithOut()
  const currentEngine = computed(() => businessStore.getSearchEngine)
  function switchEngine() { ... }
  return { currentEngine, switchEngine }
}

// ✅ 放组件：仅当前组件使用的弹窗状态
<script setup lang="ts">
const dialogVisible = ref(false)
const openDialog = () => (dialogVisible.value = true)
</script>
```

---

## 8. 完整示例：生产级 Composable

```typescript
// hooks/web/useSuggestion.ts
import { ref, onUnmounted } from 'vue'
import { useEngine } from './useEngine'
import { SUGGESTION_TIMEOUT } from '@/constants'

interface SuggestionOptions {
  timeout?: number
  maxResults?: number
}

export function useSuggestion(options?: SuggestionOptions) {
  const { currentEngine } = useEngine()
  const { timeout = SUGGESTION_TIMEOUT, maxResults = 10 } = options ?? {}

  // 状态
  const suggestions = ref<string[]>([])
  const loading = ref(false)

  // 清理：JSONP 脚本和超时定时器
  let scriptEl: HTMLScriptElement | null = null
  let timer: ReturnType<typeof setTimeout> | null = null

  function cleanup() {
    if (scriptEl) {
      scriptEl.remove()
      scriptEl = null
    }
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
  }

  async function fetch(keyword: string) {
    if (!keyword.trim()) {
      suggestions.value = []
      return
    }

    cleanup()
    loading.value = true

    return new Promise<void>((resolve) => {
      const callbackName = `suggestion_${Date.now()}`

      // JSONP 回调
      ;(window as any)[callbackName] = (data: string[]) => {
        suggestions.value = data.slice(0, maxResults)
        loading.value = false
        cleanup()
        delete (window as any)[callbackName]
        resolve()
      }

      // 超时处理
      timer = setTimeout(() => {
        suggestions.value = []
        loading.value = false
        cleanup()
        delete (window as any)[callbackName]
        resolve()
      }, timeout)

      // 注入脚本
      const url = currentEngine.value.suggestionUrl(keyword, callbackName)
      scriptEl = document.createElement('script')
      scriptEl.src = url
      document.head.appendChild(scriptEl)
    })
  }

  // 自动清理
  onUnmounted(cleanup)

  return { suggestions, loading, fetch }
}
```

这个示例综合了多种模式：
- **Options 模式**：可配置超时和最大结果数
- **异步资源**：loading 状态管理
- **生命周期感知**：onUnmounted 自动清理
- **最小暴露**：只返回 suggestions、loading、fetch
- **错误处理**：超时降级为空列表

---

## 9. 测试 Composable

Composable 是纯函数（返回响应式状态 + 方法），非常适合单元测试。推荐使用 **Vitest + @vue/test-utils**。

### 测试纯计算型 Composable

```typescript
// hooks/__tests__/useDesign.test.ts
import { describe, it, expect } from 'vitest'
import { useDesign } from '../web/useDesign'

describe('useDesign', () => {
  it('should generate correct prefix class', () => {
    const { getPrefixCls } = useDesign()
    expect(getPrefixCls('layout')).toBe('mi-layout')
  })

  it('should expose namespace variables', () => {
    const { variables, simplePrefixCls } = useDesign()
    expect(variables.namespace).toBeDefined()
    expect(simplePrefixCls).toBeDefined()
  })
})
```

### 测试有状态 Composable

```typescript
// hooks/__tests__/useEngine.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useEngine } from '../web/useEngine'

describe('useEngine', () => {
  beforeEach(() => {
    setActivePinia(createPinia()) // 每次测试前创建新的 pinia 实例
  })

  it('should return current search engine', () => {
    const { selectEngine, engineInfo } = useEngine()
    expect(selectEngine.value).toBe('baidu')
    expect(engineInfo.value.label).toBe('百度')
  })

  it('should switch to next engine', () => {
    const { selectEngine, nextEngine } = useEngine()
    nextEngine()
    expect(selectEngine.value).toBe('google')
  })

  it('should cycle back to first engine', () => {
    const { selectEngine, updateSelectEngine, nextEngine } = useEngine()
    // 切换到最后一个
    updateSelectEngine('sogou')
    nextEngine()
    expect(selectEngine.value).toBe('baidu')
  })
})
```

### 测试含生命周期的 Composable

```typescript
// hooks/__tests__/useNetwork.test.ts
import { describe, it, expect, vi, afterEach } from 'vitest'
import { useNetwork } from '../web/useNetwork'

describe('useNetwork', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('should reflect online status', async () => {
    vi.spyOn(navigator, 'onLine', 'get').mockReturnValue(true)
    const { isOnline } = useNetwork()
    expect(isOnline.value).toBe(true)
  })

  it('should update when going offline', async () => {
    vi.spyOn(navigator, 'onLine', 'get').mockReturnValue(false)
    const { isOnline } = useNetwork()
    expect(isOnline.value).toBe(false)
  })
})
```

### 测试异步 Composable

```typescript
// hooks/__tests__/useLocalForage.test.ts
import { describe, it, expect } from 'vitest'
import { useLocalForage } from '../web/useLocalForage'

describe('useLocalForage', () => {
  it('should get and set items', async () => {
    const { setItem, getItem, loading } = useLocalForage('test')

    await setItem('key1', { name: 'test' })
    expect(loading.value).toBe(false)

    const result = await getItem<{ name: string }>('key1')
    expect(result?.name).toBe('test')
  })

  it('should handle missing items', async () => {
    const { getItem } = useLocalForage('test')
    const result = await getItem('nonexistent')
    expect(result).toBeNull()
  })
})
```

### 测试 Store Bridge Composable

Store Bridge 模式的 composable 测试关键是初始化 pinia：

```typescript
// hooks/__tests__/usePageIcon.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { usePageIcon } from '../web/usePageIcon'

describe('usePageIcon', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should add page icon', () => {
    const { addPageIcon, curPageIcons } = usePageIcon()

    addPageIcon({
      label: '测试',
      url: 'https://example.com',
      icon: 'test-icon',
      iconType: 'online',
      type: 'icon'
    })

    expect(curPageIcons.value.length).toBe(1)
    expect(curPageIcons.value[0].label).toBe('测试')
  })
})
```

### 测试原则

| 原则 | 说明 |
|------|------|
| 每个 test 独立 | 用 `beforeEach` + `setActivePinia(createPinia())` 重置状态 |
| 只测试公开接口 | 只测 `return` 的值和方法，不测内部实现 |
| Mock 副作用 | 网络请求、浏览器 API 用 `vi.spyOn` / `vi.mock` 隔离 |
| 覆盖边界情况 | 空输入、异常路径、极限值 |
| 测试异步行为 | 用 `async/await` + 断言 `loading` 状态变化 |

**目录结构建议：**

```
src/hooks/
├── web/
│   ├── __tests__/           # 测试文件目录
│   │   ├── useDesign.test.ts
│   │   ├── useEngine.test.ts
│   │   ├── useNetwork.test.ts
│   │   ├── usePageIcon.test.ts
│   │   └── useLocalForage.test.ts
│   ├── useDesign.ts
│   ├── useEngine.ts
│   └── ...
```
