---
title: SFC Code Organization Order
impact: HIGH
impactDescription: 代码组织混乱会导致维护困难、难以理解组件结构，以及团队成员之间代码风格不一致
type: best-practice
tags: [vue3, composition-api, script-setup, code-organization, maintainability]
---

# SFC 代码组织顺序

**影响等级：高** - 良好组织的 SFC（单文件组件）对可维护性和团队协作至关重要。遵循一致的顺序使代码可预测且易于导航。

## 任务清单

- [ ] 遵循标准的 SFC 代码组织顺序
- [ ] 使用 useXxx 函数按功能分组相关代码
- [ ] 将 Vue 公共项（options、props、emits 等）放在顶部
- [ ] 将功能实现放在底部，IDE 中默认折叠
- [ ] 使用清晰的区块注释进行分隔

## 问题所在

`<script setup>` 带来了自由和灵活性，但如果没有约定，每个 SFC 文件可能看起来完全不同，使得维护和重构变得困难。

**BAD - 组织混乱的代码：**

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted, provide, inject } from 'vue'

// 分散的状态
const count = ref(0)
const user = ref(null)
const loading = ref(false)

// 函数随意穿插在中间
function fetchUser() {
  loading.value = true
  // ...
}

// 计算属性混在其中
const doubleCount = computed(() => count.value * 2)

// 又一个状态
const theme = ref('dark')

// props 定义在很后面
const props = defineProps<{
  id: string
}>()

// watch 散落在某处
watch(() => props.id, fetchUser)

// 生命周期钩子
onMounted(() => {
  fetchUser()
})

// 更多函数...
function increment() {
  count.value++
}

// emits 放在底部
const emit = defineEmits(['update'])

// provide 分散在各处
provide('theme', theme)
</script>
```

**GOOD - 组织良好的代码：**

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted, provide, inject } from 'vue'

// 组件名
defineOptions({
  name: 'UserComponent'
})

// props
const props = defineProps<{
  id: string
}>()

// model
const model = defineModel<string>()

// inject
const globalConfig = inject('config')

// emits
const emit = defineEmits<{
  update: [value: string]
}>()

// store
const appStore = useAppStore()

// 外部 hooks
const { user, loading, fetchUser } = useUser()
const { theme, toggleTheme } = useTheme()

// 功能声明
const { count, doubleCount, increment } = useCounter()

// provide
provide('theme', theme)

// expose
defineExpose({
  increment,
  fetchUser
})

// ============ 功能实现 ============

// 用户管理功能
function useUser() {
  const user = ref<User | null>(null)
  const loading = ref(false)

  const fetchUser = async () => {
    loading.value = true
    try {
      user.value = await fetchUserData(props.id)
    } finally {
      loading.value = false
    }
  }

  watch(() => props.id, fetchUser, { immediate: true })
  onMounted(fetchUser)

  return {
    user,
    loading,
    fetchUser
  }
}

// 主题功能
function useTheme() {
  const theme = ref<'light' | 'dark'>('dark')

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }

  return {
    theme,
    toggleTheme
  }
}

// 计数器功能
function useCounter() {
  const count = ref(0)

  const doubleCount = computed(() => count.value * 2)

  const increment = () => {
    count.value++
    emit('update', count.value.toString())
  }

  return {
    count,
    doubleCount,
    increment
  }
}
</script>
```

## 标准组织顺序

| 顺序 | 区块 | 是否必须 | 描述 |
|-------|---------|----------|-------------|
| 1 | `defineOptions` | ✅ 推荐 | 组件名称（DevTools、keep-alive、递归组件） |
| 2 | `defineProps` | 可选 | 带类型声明的组件 props |
| 3 | `defineModel` | 可选 | 双向绑定 model（Vue 3.4+） |
| 4 | `inject` | 可选 | 注入的依赖 |
| 5 | `defineEmits` | 可选 | 带类型声明的组件事件 |
| 6 | Store 声明 | 可选 | Pinia store 实例（`useXxxStore()`） |
| 7 | 外部 hooks | 可选 | 导入的组合式函数 |
| 8 | 功能声明 | 可选 | `const { ... } = useFeature()` |
| 9 | `provide` | 可选 | 提供的依赖 |
| 10 | `defineExpose` | 可选 | 暴露的公共 API |
| 11 | 功能实现 | 按需 | `function useFeature() {}` |

## 区块注释风格

使用清晰、简洁的区块注释。两种常见风格：

### 风格一：简洁中文注释（推荐中文团队使用）

```typescript
// 组件名
defineOptions({ name: 'Layout' })

// props
const props = defineProps<{ id: string }>()

// emits
const emit = defineEmits<{ update: [value: string] }>()

// store
const appStore = useAppStore()

// 外部 hooks
const { t } = useI18n()

// 功能声明
const { imageBgUrl, videoBgUrl } = useBackground()

// ============ 功能实现 ============

function useBackground() { /* ... */ }
```

### 风格二：分隔线风格（适用于大型组件）

```typescript
// ============ Vue 公共项 ============

defineOptions({ name: 'UserComponent' })

// ============ Store ============

const appStore = useAppStore()

// ============ 外部 Hooks ============

const { t } = useI18n()

// ============ 功能声明 ============

const { search, results } = useSearch()

// ============ 功能实现 ============

function useSearch() { /* ... */ }
```

## 收益

1. **结构可预测**：团队成员知道在哪里找到特定代码
2. **快速概览**：顶部区域让组件接口一目了然
3. **IDE 导航**：点击声明中的函数名即可跳转到实现
4. **默认折叠**：功能实现保持折叠状态，减少视觉干扰
5. **依赖清晰**：一眼看清每个功能返回和消费了什么
6. **Store 聚合**：所有 store 实例集中声明，便于识别

## 适用场景

- **始终遵循**：对所有 `<script setup>` 组件使用此组织方式
- **小型组件**：即使区块较少，仍应遵循此顺序
- **大型组件**：功能较多时，对保持可读性至关重要
- **团队项目**：通过代码审查和 lint 规则强制保持一致性

## 真实案例

```vue
<script setup lang="ts">
import { useAppStore } from '@/store/modules/app'

// 组件名
defineOptions({
  name: 'MiSearch'
})

// store
const appStore = useAppStore()
const businessStore = useBusinessStore()

// 多语言
const { t } = useI18n()

// 简单前缀
const { getPrefixCls } = useDesign()

// useEngine
const { engineInfo, nextEngine } = useEngine()

// useSearchInput
const {
  searchContent,
  handleChange,
  handleSearch,
  isComposing,
  searchHistoryRef,
  searchSuggestionRef,
  operaHistoryOrSuggestion,
  searchInputRef
} = useSearchInput()

// 输入框
function useSearchInput() {
  const searchContent = ref('')
  const isComposing = ref(false)

  const handleSearch = (val) => {
    if (isComposing.value) return
    const useContent = encodeURIComponent(val)
    if (!useContent) return
    businessStore.updateHistoryList(val)
    window.open(`${engineInfo.value.url}${useContent}`, appStore.openType)
  }

  // ... 更多逻辑

  return {
    searchContent,
    isComposing,
    handleSearch,
    handleChange,
    searchHistoryRef,
    searchSuggestionRef,
    operaHistoryOrSuggestion,
    searchInputRef
  }
}
</script>
```

## 参考

- [Vue.js Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Vue.js script setup](https://vuejs.org/api/sfc-script-setup.html)
- [官方示例：FileExplorer.vue](https://github.com/vuejs-translations/docs-zh-cn/blob/main/assets/FileExplorer.vue)
