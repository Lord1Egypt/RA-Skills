---
name: state-architecture
description: Designs scalable state management architecture for complex frontend apps. Covers store slicing, server vs client state separation, optimistic updates, cross-tab sync, and state machine patterns. Use when 状态管理, store 设计, Zustand, Redux, 状态架构, 乐观更新, 状态机, or state design.
model: opus
---

# 状态管理架构（State Architecture）

为复杂前端应用设计可扩展的状态管理方案——不只是"用哪个库"，而是如何切分、如何同步、如何避免状态腐化。

## 触发场景

- 「状态管理怎么设计」「store 越来越乱」「组件间状态共享」
- 「乐观更新怎么做」「状态和服务端不同步」「跨 tab 同步」
- 「要不要用状态机」「这个流程状态太复杂了」
- 新项目技术选型，或现有状态管理出现明显问题

## 核心原则

**状态分类是第一步，选库是第二步。**

| 状态类型 | 定义 | 推荐管理方式 |
|---------|------|------------|
| 服务端状态 | 来自 API，有缓存/失效/同步问题 | React Query / SWR |
| 全局 UI 状态 | 跨组件共享，与服务端无关（主题、侧边栏、弹层） | Zustand / Jotai |
| 本地 UI 状态 | 单组件内部（输入值、hover、展开收起） | useState / useReducer |
| URL 状态 | 可分享、可回退（筛选、分页、tab） | URL 参数（nuqs / useSearchParams） |
| 表单状态 | 输入、校验、提交 | React Hook Form |

**最常见的错误**：把服务端状态放进全局 store，然后手动维护缓存和同步——这是 React Query 要解决的问题，不要重复造轮子。

---

## 执行流程

### 1. 先诊断，再设计

用户说「状态管理有问题」时，先问清楚症状：

| 症状 | 根因 | 方向 |
|-----|------|------|
| 「store 里全是接口数据」 | 服务端状态混入全局 store | 迁移到 React Query，store 只留 UI 状态 |
| 「A 组件改了，B 组件不更新」 | 状态没有提升到公共祖先，或订阅粒度太粗 | 检查状态归属，或细化 selector |
| 「store 越来越大，不知道谁在用」 | 缺乏 slice 边界，状态所有权不清 | 按功能域切分 slice，明确所有权 |
| 「乐观更新回滚逻辑很乱」 | 没有统一的乐观更新模式 | 用 React Query 的 `onMutate/onError` 模式 |
| 「这个流程有 10 种状态，if/else 写不下去了」 | 需要状态机 | 用 XState 或手写状态机 |

### 2. 状态归属决策树

拿到一个状态，按这个顺序判断放哪里：

```
这个状态是从 API 来的吗？
├── 是 → 用 React Query/SWR，不要放 store
└── 否 → 只有一个组件用吗？
    ├── 是 → useState，不要提升
    └── 否 → 需要在 URL 里体现吗（可分享/可回退）？
        ├── 是 → URL 参数
        └── 否 → 全局 store（Zustand/Jotai）
```

**原则：状态尽量下沉，能放组件内就不放 store，能放 URL 就不放 store。**

### 3. Zustand store 设计规范

**按功能域切 slice，不要一个大 store：**

```ts
// ❌ 错：一个 store 装所有东西
const useStore = create((set) => ({
  user: null,
  theme: 'light',
  sidebarOpen: false,
  notifications: [],
  cartItems: [],
  // ...越来越多
}))

// ✅ 对：按功能域切分
const useUIStore = create((set) => ({
  theme: 'light',
  sidebarOpen: false,
  setTheme: (theme) => set({ theme }),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}))

const useNotificationStore = create((set) => ({
  items: [],
  add: (item) => set((s) => ({ items: [...s.items, item] })),
  dismiss: (id) => set((s) => ({ items: s.items.filter(i => i.id !== id) })),
}))
```

**selector 细化，避免无效重渲染：**

```ts
// ❌ 错：订阅整个 store，任何字段变化都重渲染
const { theme, sidebarOpen } = useUIStore()

// ✅ 对：只订阅需要的字段
const theme = useUIStore((s) => s.theme)
const sidebarOpen = useUIStore((s) => s.sidebarOpen)
```

### 4. 乐观更新的标准模式

用 React Query 的 `useMutation` + `onMutate/onError/onSettled`：

```ts
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    // 1. 取消正在进行的请求，避免覆盖乐观更新
    await queryClient.cancelQueries({ queryKey: ['todos'] })
    // 2. 保存快照用于回滚
    const snapshot = queryClient.getQueryData(['todos'])
    // 3. 乐观更新缓存
    queryClient.setQueryData(['todos'], (old) =>
      old.map(t => t.id === newTodo.id ? { ...t, ...newTodo } : t)
    )
    return { snapshot }
  },
  onError: (err, newTodo, context) => {
    // 4. 失败时回滚
    queryClient.setQueryData(['todos'], context.snapshot)
  },
  onSettled: () => {
    // 5. 无论成功失败，重新拉取确保数据一致
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})
```

**不要自己在 store 里手写乐观更新逻辑**——React Query 的这套模式处理了所有边界情况。

### 5. 状态机：什么时候用，怎么用

**需要状态机的信号：**
- 一个流程有 5+ 种状态，且状态之间有明确的转换规则
- 出现了「在状态 A 下不能做 B」这类约束
- 状态转换有副作用（发请求、记日志）
- 团队经常讨论「现在到底是什么状态」

**轻量状态机（不引入 XState）：**

```ts
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: Data }
  | { status: 'error'; error: Error }

type Event =
  | { type: 'FETCH' }
  | { type: 'SUCCESS'; data: Data }
  | { type: 'ERROR'; error: Error }
  | { type: 'RESET' }

function reducer(state: State, event: Event): State {
  switch (state.status) {
    case 'idle':
      if (event.type === 'FETCH') return { status: 'loading' }
      return state
    case 'loading':
      if (event.type === 'SUCCESS') return { status: 'success', data: event.data }
      if (event.type === 'ERROR') return { status: 'error', error: event.error }
      return state
    case 'success':
    case 'error':
      if (event.type === 'RESET') return { status: 'idle' }
      return state
  }
}
```

**用 XState 的时机：** 流程有并行状态、历史状态、延迟转换，或需要可视化状态图给产品/测试看。

### 6. 跨 Tab 状态同步

需要多 tab 共享状态时（如登录态、购物车）：

```ts
// 用 BroadcastChannel（现代浏览器原生支持）
const channel = new BroadcastChannel('app-state')

// 发送
channel.postMessage({ type: 'CART_UPDATED', payload: cartItems })

// 接收
channel.onmessage = (event) => {
  if (event.data.type === 'CART_UPDATED') {
    useCartStore.setState({ items: event.data.payload })
  }
}

// 或用 Zustand 的 persist + storage event 监听 localStorage 变化
```

---

## 常见反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| 把 API 响应直接存 store | 手动维护缓存，容易不同步 | 用 React Query |
| store 里存派生数据 | 数据源不唯一，容易不一致 | 用 selector 计算派生数据 |
| 组件里直接 `store.getState()` | 绕过响应式，不会触发重渲染 | 用 hook 订阅 |
| 一个 action 改多个 slice | 耦合，难以追踪 | 每个 slice 只管自己的状态，用事件驱动跨 slice 通信 |
| 状态里存 UI 临时状态（hover、focus） | 不必要的全局状态 | 用组件本地 state |

## 输出模板

```markdown
## 状态管理方案

### 状态分类
| 状态 | 类型 | 管理方式 | 理由 |
|------|------|---------|------|
| 用户信息 | 服务端状态 | React Query | 需要缓存和同步 |
| 主题 | 全局 UI | Zustand | 跨组件，与服务端无关 |
| 表单输入 | 本地 UI | useState | 单组件内部 |
| 筛选条件 | URL 状态 | useSearchParams | 可分享、可回退 |

### Store 结构
- useUIStore：主题、侧边栏、弹层
- use[Domain]Store：[具体业务域]

### 关键决策
- 乐观更新：用 React Query onMutate 模式
- 跨 Tab 同步：BroadcastChannel / localStorage event
- 复杂流程：状态机（轻量 reducer / XState）
```
