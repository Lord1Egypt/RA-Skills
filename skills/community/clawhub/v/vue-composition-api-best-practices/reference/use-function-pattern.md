---
title: UseXxx Function Pattern for Feature Encapsulation
impact: HIGH
impactDescription: 如果不使用 useXxx 模式，功能逻辑会变得分散，难以理解每个功能暴露了什么，也难以追踪功能之间的依赖关系
type: best-practice
tags: [vue3, composition-api, script-setup, use-pattern, code-organization]
---

# UseXxx 函数模式：功能封装

**影响等级：高** - useXxx 模式将相关逻辑封装到自包含的函数中，使功能易于理解、测试和复用。

## 任务清单

- [ ] 将功能逻辑封装在 `useFeatureName()` 函数中
- [ ] 仅返回外部需要的值和方法
- [ ] 将功能实现放在 script 底部
- [ ] 在顶部使用解构声明功能使用
- [ ] 功能函数命名清晰，能反映其用途

## 问题所在

没有封装时，相关的变量、计算属性、监听器和方法散落在代码各处，难以理解哪些代码属于哪个功能。

**BAD - 功能逻辑分散：**

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'

// 搜索功能分散
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

// 分页功能混在一起
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(0)

// 随意放置的 computed
const hasResults = computed(() => searchResults.value.length > 0)

// 另一个功能开始
const selectedItem = ref(null)

// 搜索函数
async function handleSearch() {
  isSearching.value = true
  searchResults.value = await fetchResults(searchQuery.value)
  isSearching.value = false
}

// 分页函数
function changePage(page: number) {
  currentPage.value = page
  handleSearch()
}

// watch 分散
watch(searchQuery, handleSearch)

// 选择函数
function selectItem(item: any) {
  selectedItem.value = item
}
</script>
```

**GOOD - 使用 useXxx 模式封装：**

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'

// 功能声明

// 搜索功能 - 一目了然的接口
const {
  searchQuery,
  searchResults,
  isSearching,
  hasResults,
  handleSearch
} = useSearch()

// 分页功能 - 自包含
const {
  currentPage,
  pageSize,
  totalItems,
  changePage
} = usePagination({ onPageChange: handleSearch })

// 选择功能 - 独立
const {
  selectedItem,
  selectItem
} = useSelection()

// ============ 功能实现 ============

function useSearch() {
  const searchQuery = ref('')
  const searchResults = ref<SearchResult[]>([])
  const isSearching = ref(false)

  const hasResults = computed(() => searchResults.value.length > 0)

  const handleSearch = async () => {
    isSearching.value = true
    try {
      searchResults.value = await fetchResults(searchQuery.value)
    } finally {
      isSearching.value = false
    }
  }

  watch(searchQuery, handleSearch)

  return {
    searchQuery,
    searchResults,
    isSearching,
    hasResults,
    handleSearch
  }
}

function usePagination(options: { onPageChange: () => void }) {
  const currentPage = ref(1)
  const pageSize = ref(10)
  const totalItems = ref(0)

  const changePage = (page: number) => {
    currentPage.value = page
    options.onPageChange()
  }

  return {
    currentPage,
    pageSize,
    totalItems,
    changePage
  }
}

function useSelection() {
  const selectedItem = ref<SearchResult | null>(null)

  const selectItem = (item: SearchResult) => {
    selectedItem.value = item
  }

  return {
    selectedItem,
    selectItem
  }
}
</script>
```

## 核心原则

### 1. 清晰的返回接口

return 语句记录了该功能暴露了什么：

```typescript
function useSearch() {
  // 内部状态 - 不返回
  const abortController = ref<AbortController | null>(null)

  // 公共状态
  const searchQuery = ref('')
  const searchResults = ref<SearchResult[]>([])

  // 公共方法
  const handleSearch = async () => { /* ... */ }

  return {
    // 只暴露需要的内容
    searchQuery,
    searchResults,
    handleSearch
  }
}
```

### 2. 自包含的逻辑

每个 useXxx 函数包含所有相关的内容：
- 状态（ref、reactive）
- 计算属性
- 监听器
- 生命周期钩子
- 方法

```typescript
function useSearch() {
  // 状态
  const query = ref('')
  const results = ref([])

  // 计算属性
  const isEmpty = computed(() => results.value.length === 0)

  // 监听器
  watch(query, debounce(search, 300))

  // 生命周期
  onMounted(() => {
    if (query.value) search()
  })

  // 方法
  async function search() { /* ... */ }

  return { query, results, isEmpty, search }
}
```

### 3. 通过参数进行依赖注入

将依赖作为参数传递，实现跨功能通信：

```typescript
function usePagination(options: {
  onPageChange?: () => void
  initialPage?: number
} = {}) {
  const currentPage = ref(options.initialPage ?? 1)

  const goToPage = (page: number) => {
    currentPage.value = page
    options.onPageChange?.()
  }

  return { currentPage, goToPage }
}

// 使用方式
const { handleSearch } = useSearch()
const { currentPage, goToPage } = usePagination({
  onPageChange: handleSearch
})
```

### 4. Store 桥接模式

当组合式函数封装 store 访问时，需提供干净的接口来隐藏 store 实现细节：

```typescript
// 页面图标管理 hooks - 封装 store 访问
export const usePageIcon = () => {
  const appStore = useAppStoreWithOut()

  // 当前 page
  const curPage = computed(() => appStore.selectCategory.key)

  // 当前 page icons
  const curPageIcons = computed(() => appStore.pageIconMap[curPage.value] || [])

  // 新增 page icon
  const addPageIcon = (icon: PageItemWithOptionalKey, page?: string) => {
    if (!appStore.pageIconMap[page || curPage.value]) {
      appStore.addPageIconInfo(page || curPage.value)
    }
    const icons = appStore.pageIconMap[page || curPage.value]
    if (!icon.key) {
      icon.key = `${page || curPage.value}-icon-${icon.type}-${icons.length}`
    }
    appStore.updatePageIconInfo(page || curPage.value, icons.concat(icon as PageItem))
  }

  // 更新 page icon
  const updatePageIcon = (icon: PageItem, page: string) => {
    const icons = appStore.pageIconMap[page]
    const targetIdx = icons.findIndex((i) => i.key === icon.key)
    if (targetIdx !== -1) {
      icons[targetIdx] = icon
      appStore.updatePageIconInfo(page, icons)
    }
  }

  // 删除 page icon
  const removePageIcon = (icon: PageItem, page?: string) => {
    const icons = appStore.pageIconMap[page || curPage.value]
    if (icons) {
      appStore.updatePageIconInfo(
        page || curPage.value,
        icons.filter((item) => item.key !== icon.key)
      )
    }
  }

  return {
    curPage,
    curPageIcons,
    addPageIcon,
    updatePageIcon,
    removePageIcon
  }
}
```

**Store 桥接模式的收益：**
- 组件无需了解 store 内部结构
- 业务逻辑集中在一处
- 便于在无需更新所有组件的情况下更改 store 结构
- 与 `useXxxStoreWithOut` 无缝配合，适用于非组件场景

## 命名约定

| 模式 | 示例 | 使用场景 |
|---------|---------|----------|
| `useXxx` | `useSearch()` | 组件内部的功能封装 |
| `useXxx` | `useUserStore()` | 外部组合式函数导入 |
| `useXxxStoreWithOut` | `useAppStoreWithOut()` | 组件外部的 store 访问 |
| `useXxx`（桥接） | `usePageIcon()` | Store 桥接组合式函数 |

## 何时提取到外部文件

满足以下条件时移至外部文件：
- 跨多个组件使用
- 复杂度足够高，需要单独测试
- 不依赖父组件状态
- 作为 store 数据的桥接层

```typescript
// hooks/web/usePageIcon.ts
export const usePageIcon = () => {
  const appStore = useAppStoreWithOut()
  // ...
  return { curPageIcons, addPageIcon, updatePageIcon, removePageIcon }
}

// 在组件中
import { usePageIcon } from '@/hooks/web/usePageIcon'
const { curPageIcons, addPageIcon } = usePageIcon()
```

## 功能实现检查清单

编写 `useXxx` 函数时：

- [ ] 所有相关状态都在函数内部（不散落在外部）
- [ ] 从状态派生的计算属性都在函数内部
- [ ] 响应状态变化的监听器都在函数内部
- [ ] 生命周期钩子（`onMounted`、`onBeforeUnmount`）都在函数内部
- [ ] 清理逻辑（`removeEventListener`、`off`）在 `onBeforeUnmount` 内
- [ ] 只返回组件需要的内容
- [ ] 内部实现细节被隐藏

## 参考

- [Vue.js Composables](https://vuejs.org/guide/reusability/composables.html)
- [Vue.js Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html)
