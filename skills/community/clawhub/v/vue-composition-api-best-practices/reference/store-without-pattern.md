# Store Without 模式

## 问题

Pinia 的 `useStore()` 默认依赖 Vue 组件上下文（inject/provide）。在组件外（hooks、utils、plugins、路由守卫、axios 拦截器）直接调用会抛出错误：

```
Error: "getActivePinia()" was called but there was no active Pinia.
```

## 解决方案：Store Without 模式

每个 store 模块额外导出一个 `useXxxStoreWithOut` 函数，接收全局 pinia 实例作为参数，使 store 可在任意上下文中安全访问。

### 模式定义

```typescript
// store/modules/app.ts
import { defineStore } from 'pinia'
import { store } from '@/store'

export const useAppStore = defineStore('app', {
  // ... store 定义
})

// 在组件外使用时，传入全局 pinia 实例
export const useAppStoreWithOut = () => {
  return useAppStore(store)
}
```

### 全局 Pinia 实例

```typescript
// store/index.ts
import { createPinia } from 'pinia'

const pinia = createPinia()

export default pinia

// 导出 store 供 Without 函数使用
export const store = pinia
```

## 使用规则

### 何时使用哪个

| 函数 | 使用场景 | 原因 |
|------|---------|------|
| `useAppStore()` | Vue 组件 `<script setup>` 内 | 自动从组件上下文获取 pinia |
| `useAppStoreWithOut()` | hooks、utils、plugins、路由守卫等 | 组件上下文不可用，需显式传入 pinia |

### 在 Vue 组件中（始终使用标准方式）

```typescript
// ✅ GOOD：组件内使用标准方式
<script setup lang="ts">
import { useAppStore } from '@/store/modules/app'

const appStore = useAppStore()
</script>
```

```typescript
// ❌ BAD：组件内使用 WithOut 是多余的
<script setup lang="ts">
import { useAppStoreWithOut } from '@/store/modules/app'

const appStore = useAppStoreWithOut() // 可以工作但不必要
</script>
```

### 在 Hooks / Utils / Plugins 中（必须使用 WithOut）

```typescript
// ✅ GOOD：hooks 中使用 WithOut
// hooks/web/useSideCategory.ts
import { useBusinessStoreWithOut } from '@/store/modules/business'

export function useSideCategory() {
  const businessStore = useBusinessStoreWithOut()
  const categories = computed(() => businessStore.getSideCategory)
  return { categories }
}
```

```typescript
// ✅ GOOD：utils 中使用 WithOut
// utils/migration.ts
import { useBusinessStoreWithOut } from '@/store/modules/business'

export async function migrateOnlineIcons() {
  const businessStore = useBusinessStoreWithOut()
  // ...
}
```

```typescript
// ❌ BAD：组件外直接使用标准方式会报错
// utils/migration.ts
import { useBusinessStore } from '@/store/modules/business'

export async function migrateOnlineIcons() {
  const businessStore = useBusinessStore() // Error: no active Pinia
}
```

## 命名规范

所有模块遵循统一命名规范：

| Store 模块 | 标准函数 | WithOut 函数 |
|-----------|---------|-------------|
| `app.ts` | `useAppStore` | `useAppStoreWithOut` |
| `business.ts` | `useBusinessStore` | `useBusinessStoreWithOut` |
| `dict.ts` | `useDictStore` | `useDictStoreWithOut` |
| `locale.ts` | `useLocaleStore` | `useLocaleStoreWithOut` |

**规则**：`use{ModuleName}StoreWithOut` — 模块名首字母大写 + Store + WithOut（注意大小写）。

## 实现清单

每个 store 模块必须：

- [ ] 导出标准 `useXxxStore` 函数（`defineStore` 的返回值）
- [ ] 导出 `useXxxStoreWithOut` 函数，内部调用 `useXxxStore(store)`
- [ ] 从 `@/store` 导入全局 `store` 实例
- [ ] WithOut 函数放在文件底部，紧跟标准函数之后

## 为什么不直接使用 `useXxxStore(pinia)`？

理论上可以直接调用 `useAppStore(pinia)`，但 `WithOut` 函数提供了：

1. **语义明确** — 函数名直接表达"在组件外使用"的意图
2. **统一入口** — 不需要每个调用方都 import `store`，减少依赖
3. **集中管理** — 如果 pinia 实例获取方式变更，只需改 WithOut 函数
4. **可搜索** — 搜索 `WithOut` 即可找到所有组件外使用 store 的地方

## 替代方案：`storeToRefs` 注意事项

注意 `useXxxStoreWithOut()` 返回的是 store 实例，如需解构响应式属性，仍需使用 `storeToRefs`：

```typescript
import { storeToRefs } from 'pinia'
import { useAppStoreWithOut } from '@/store/modules/app'

export function useAppInfo() {
  const appStore = useAppStoreWithOut()
  const { pure, theme } = storeToRefs(appStore) // 保持响应式
  return { pure, theme }
}
```

## 总结

| 优势 | 说明 |
|------|------|
| 解决组件外访问 | 核心价值，让 store 可在任意上下文使用 |
| 命名约定清晰 | `WithOut` 后缀一目了然 |
| 减少样板代码 | 调用方无需 import store |
| 易于维护 | pinia 实例变更只需改一处 |
| 可追溯 | 搜索 `WithOut` 可定位所有组件外使用 |
