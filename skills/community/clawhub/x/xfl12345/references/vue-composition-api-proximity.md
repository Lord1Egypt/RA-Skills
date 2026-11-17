---
name: vue-composition-api-proximity
description: 在编写或重构 Vue 3 Composition API `<script setup>` 代码时使用——组织函数定义、计算属性、响应式状态和分段注释。在创建新组件、重新整理 script setup 代码块或审查 Vue SFC 代码布局时触发。
---

# Vue Composition API 就近原则

## 核心原则

**组合式 API 的核心价值是减少阅读时的眼球跳跃距离。** 代码组织围绕"读者翻阅跨度最小化"，而非按类型分类。

Options API 按类型分桶（data/methods/computed 各一块），翻阅一个逻辑链要跳三个区域。Composition API 打破了这个限制，应当充分利用。

## 目标

读者从上往下扫一遍，不需要上下翻找就能理解每个值的来源。

## 就近规则

### 区分"脚本消费者"与"纯模板绑定"

变量的放置取决于它**在脚本中被谁使用**，而非模板：

- **脚本中有消费者**（被函数读写、被 computed 引用）→ 紧贴脚本中第一个消费者上方
- **纯模板绑定**（脚本内无任何引用，仅通过模板 `:xxx="var"` 或 `v-model="var"` 传入）→ 归入顶部公共区域，与 composable 初始化并列

```typescript
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Modal from './Modal.vue'

// ✅ 顶部公共区域：纯模板绑定 + composable
const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()
const dialogVisible = ref(false)                       // 仅模板 v-model="dialogVisible" 使用
const containerClass = ref('')                         // 仅模板 :class 引用

// ... 其他代码 ...

// ✅ 一旦变量也被脚本函数改写，就不再是纯模板绑定，应紧贴消费者
const panelOpen = ref(false)
function onOpenPanel() {
  panelOpen.value = true
}
function onClosePanel() {
  panelOpen.value = false
}
```

**判断方法：** 在 `<script setup>` 中搜索该变量名。只出现在模板里 → 顶部。脚本中有读/写 → 紧贴消费者。

### 函数紧贴消费者

只被调用一两次的函数，定义在消费者**正上方**，函数与其直接消费者之间无空行（生命周期钩子如 `onMounted` 同此原则，紧贴它操作的响应式状态）：

```typescript
import { computed, ref } from 'vue'

interface Address {
  city: string
  zip: string
}
const addresses = ref<Address[]>([])

function formatAddress(addr: Address): string {
  return `${addr.zip} ${addr.city}`
}
const summary = computed(() =>
  addresses.value.map(formatAddress).join('，'),
)

function countValid(addr: Address): number {
  return addr.city && addr.zip ? 1 : 0
}
const validCount = computed(() =>
  addresses.value.reduce((sum, addr) => sum + countValid(addr), 0),
)
```

#### 例外

被多处复用的、或需要抽成独立库的函数，提取并集中到单独文件。

### 分段注释只加在真正独立的逻辑域

```typescript
import { onMounted } from 'vue'

// ── 地址相关 ──    ← 合理：独立逻辑域
interface Address { city: string; zip: string }
// ...

// ── 属性 ──        ← 多余：defineProps 函数属于 vue 开发基本常识
const props = withDefaults(defineProps<Props>(), { ... })
```

**判断标准：** 去掉注释读者是否还能识别这段在做什么？能 → 删注释。

### Vue 函数不需要分组注释

`withDefaults(defineProps<Props>(), { ... })` 结构明确，加 `// ── Props ──` 是噪音。

## 典型布局

```typescript
import { computed, onMounted, ref } from 'vue'

// props（无注释）
const props = withDefaults(defineProps<Props>(), { ... })

// ── 独立逻辑域 ──
interface LocalType { ... }

function helperOnlyUsedOnce() { ... }
const consumerOfHelper = computed(() => helperOnlyUsedOnce(...))

const state = ref(...)
const derived = computed(() => ... /* uses state */)

onMounted(() => { ... /* uses state */ })
```

## Anti-Patterns

| 做法 | 问题 |
|------|------|
| 按类型分块（所有 function → 所有 ref → 所有 computed） | Options API 思维，翻阅跨度大 |
| 每个 section 都加注释 | 注释噪音，读者忽略后等于没有 |
| 工具函数集中到文件顶部或底部 | 调用处和定义处跨几十行，来回跳 |
| 纯模板绑定变量混在 handler 之间 | 无脚本消费者却占据逻辑流中间位置，打断阅读 |
| 所有代码无空行分隔 | 丧失视觉节奏，分不清边界 |
