---
name: spm-frontend
version: 1.0.0
description: 前端开发规范 — React/Vue 组件设计原则、状态管理、性能、可访问性、AI 常见反模式。SPM 自动检测项目框架后引用。也可独立使用。
---

# SPM Frontend — 前端开发规范

> 不教 React 语法。教 Agent 写出"不被 reviewer 骂"的前端代码。

## 自动检测

SPM Phase 3 检测到项目含 `react`/`vue`/`next` → 子代理 dispatch 时自动引用本技能。

## 组件原则

### 大小边界

```
✅ 单个组件 ≤ 200 行
❌ 一个组件 500 行做 5 件事

超过 200 行 → 拆。按职责拆，不按"感觉"拆。
```

### 命名

```
✅ UserProfile.tsx, useAuth.ts, formatDate.ts
❌ Component.tsx, utils.ts, helpers.ts, data.ts
```

| 类型 | 命名模式 | 示例 |
|------|---------|------|
| 页面组件 | `XxxPage.tsx` | `DashboardPage.tsx` |
| 功能组件 | `XxxPanel.tsx` / `XxxCard.tsx` | `UserCard.tsx` |
| 自定义 Hook | `useXxx.ts` | `useDebounce.ts` |
| 工具函数 | `verbNoun.ts` | `formatCurrency.ts` |
| 类型定义 | `Xxx.types.ts` | `user.types.ts` |

### Props 设计

```
✅ 每个 prop 有明确类型、有默认值、optional 有 ?
❌ props: any, 10 个以上的 props（该拆了）
❌ 传整个对象下去（传需要的字段）
```

## 状态管理

### 选择决策树

```
数据只在一个组件用？
  → useState ✅

数据在父子间传递？
  → props drilling ≤ 2 层 → props ✅
  → props drilling > 2 层 → Context / composition ✅

数据全局共享（用户信息、主题、多页面）？
  → Zustand / Pinia ✅

服务端数据（API 请求、缓存）？
  → React Query / SWR ✅
  → 不要用 useState + useEffect 手动管理 ❌
```

### 常见反模式

```typescript
// ❌ 用 index 做 key
{items.map((item, index) => <Item key={index} />)}

// ✅ 用唯一 ID
{items.map(item => <Item key={item.id} />)}

// ❌ 在 useEffect 里 fetch
useEffect(() => { fetch('/api/data').then(setData) }, [])

// ✅ 用 React Query
const { data } = useQuery({ queryKey: ['data'], queryFn: fetchData })
```

## AI 前端代码 7 大反模式

**这是本文件最有价值的部分。每次写组件前自查。**

| # | 反模式 | 为什么坏 | 怎么改 |
|---|--------|---------|--------|
| 1 | **index 做 key** | 列表增删时 React 复用错误 DOM，输入框内容串位 | 用 `item.id` |
| 2 | **useEffect 里 fetch** | 竞态条件、重复请求、缓存缺失、加载状态混乱 | 用 React Query / SWR |
| 3 | **一个巨型组件** | 改一行提心吊胆，测试覆盖不到 | 拆成 ≤200 行的子组件 |
| 4 | **全局状态滥用** | 一个 checkbox 值放进 Zustand store | 局部状态用 useState |
| 5 | **inline 函数 + 无 memo** | 每次渲染创建新函数引用，子组件全部重渲染 | `useCallback` / `useMemo`（只在需要时） |
| 6 | **不处理 loading/error/empty** | 接口挂了用户看到白屏或 spinner 永远转 | 每个数据组件必须有三个状态 |
| 7 | **div 套 div 套 div** | 可访问性为 0，屏幕阅读器读不出结构 | 用 `<main> <nav> <article> <section> <button>` |

### 反模式 6 的标准模板

```typescript
// ❌
return <div>{data.map(item => <Card item={item} />)}</div>

// ✅
if (isLoading) return <Skeleton count={3} />
if (error) return <ErrorBanner message={error.message} onRetry={refetch} />
if (!data?.length) return <EmptyState type="no-results" />
return <div>{data.map(item => <Card key={item.id} item={item} />)}</div>
```

## 性能

不追极致优化，但底线必须守住：

```
✅ 列表 > 100 条 → 虚拟滚动 (react-window / vue-virtual-scroller)
✅ 大体积依赖 → 动态 import (React.lazy / defineAsyncComponent)
✅ 图片 → next/image 或 loading="lazy" + 宽高
✅ 事件处理 → debounce/throttle (搜索输入、scroll、resize)
❌ 不要每个组件都用 memo — 只在 props 频繁变化时用
```

## 可访问性

最低标准：

```
✅ 所有 <button> 有 accessible name（文本内容或 aria-label）
✅ 所有 <input> 关联 <label>
✅ 页面有一个 <h1>
✅ 颜色对比度 ≥ 4.5:1（正常文字）
✅ 键盘 Tab 顺序合理（不用 tabindex > 0）
❌ 不要 div onclick 代替 button
```

## 测试前端

| 测什么 | 怎么测 | 优先级 |
|--------|--------|--------|
| 组件渲染 + 交互 | React Testing Library / Vue Test Utils | 🔴 必须 |
| 用户关键流程 | Playwright / Cypress E2E | 🟡 有前端路由就要 |
| 视觉回归 | Chromatic / Percy | 🟢 可选 |
| 纯函数/工具 | 普通单元测试 | 🔴 必须 |

**前端不该测的：**
- ❌ 库的内部实现
- ❌ CSS 样式精确度（用视觉回归替代）
- ❌ 浏览器默认行为

## 与 SPM 集成

本技能被 SPM Phase 3 自动引用时，子代理会收到：

```
冷启动上下文：Task X 是一个 React Dashboard 组件。
前端规范参考：spm-frontend → 特别注意反模式 1/5/6。
```

也可独立使用——直接说"按 spm-frontend 规范写一个登录表单"。
