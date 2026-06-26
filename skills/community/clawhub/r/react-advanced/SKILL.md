---
name: react-advanced
description: Advanced React patterns and Next.js architecture: RSC, Suspense, concurrent features, render optimization, custom hooks design, and App Router best practices. Use when React Server Components, RSC, Suspense, useTransition, Next.js App Router, 渲染优化, 自定义 hook, or advanced React patterns.
model: opus
---

# React 进阶（React Advanced）

掌握 React 并发特性、Server Components、渲染优化和 Next.js App Router 架构，写出真正高性能的 React 应用。

## 触发场景

- 「React Server Components 怎么用」「RSC 和 Client Component 怎么分」
- 「Suspense 怎么用」「useTransition 什么时候用」
- 「组件重渲染太多」「memo 没效果」「渲染优化」
- 「自定义 hook 怎么设计」「hook 复用」
- 「Next.js App Router 架构」「数据获取策略」

---

## 执行流程

### 1. 先判断用户的问题类型

| 用户描述 | 实际问题 | 第一步 |
|---------|---------|-------|
| 「RSC 怎么用」「Server Component」 | RSC 概念和边界 | 解释 RSC/CC 边界，给出决策树 |
| 「重渲染太多」「性能差」 | 渲染优化 | 先用 React DevTools Profiler 定位，再给方案 |
| 「memo 没用」「useMemo 没效果」 | 优化工具误用 | 检查引用稳定性，找真正的重渲染原因 |
| 「Suspense 怎么用」 | 异步渲染 | 区分数据加载 Suspense 和代码分割 Suspense |
| 「hook 怎么设计」 | 抽象和复用 | 问：要解决什么问题？是状态逻辑还��副作用？ |

### 2. RSC vs Client Component 决策树

```
这个组件需要以下任意一项吗？
├── useState / useReducer
├── useEffect / useLayoutEffect
├── 浏览器 API（window、document、localStorage）
├── 事件监听（onClick、onChange）
├── 第三方需要浏览器环境的库
│
├── 是 → Client Component（文件顶部加 'use client'）
└── 否 → Server Component（默认，不需要标注）
    ├── 可以直接 async/await 获取数据
    ├── 可以访问数据库、文件系统、环境变量
    └── 不会打包进客户端 bundle
```

**RSC 的核心价值：**
- ��据获取在服务端，不暴露 API 密钥
- 组件代码不进客户端 bundle（大型依赖如 markdown 解析器）
- 消除客户端的 loading 状态（数据已经在服务端准备好）

**常见误区：**

```tsx
// ❌ 错：在 Server Component 里用 useState
// 这会报错，Server Component 不能有状态
async function ServerComp() {
  const [count, setCount] = useState(0)  // 报错
}

// ✅ 对：状态放在 Client Component，数据获取放在 Server Component
async function ServerComp() {
  const data = await fetchData()  // 服务端获取
  return <ClientComp initialData={data} />  // 传给客户端
}

'use client'
function ClientComp({ initialData }) {
  const [data, setData] = useState(initialData)  // 客户端状态
}
```

**'use client' 是边界，不是标签：**
- 加了 `'use client'` 的文件及其所有子组件都变成 Client Component
- 尽量把 `'use client'` 推到叶子节点，让更多组件保持 Server Component

### 3. Suspense 的正确用法

**两种用途，不要混淆：**

**用途 1：代码分割（懒加载组件）**

```tsx
const HeavyChart = lazy(() => import('./HeavyChart'))

function Dashboard() {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <HeavyChart />
    </Suspense>
  )
}
```

**用途 2：数据加载（配合 React Query 或 RSC）**

```tsx
// React Query + Suspense
function UserProfile({ userId }) {
  // useSuspenseQuery 在数据未就绪时抛出 Promise，触发最近的 Suspense
  const { data } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  })
  return <div>{data.name}</div>
}

// 父组件
function App() {
  return (
    <Suspense fallback={<Skeleton />}>
      <ErrorBoundary fallback={<Error />}>
        <UserProfile userId={1} />
      </ErrorBoundary>
    </Suspense>
  )
}
```

**Suspense 边界的粒度：**
- 太粗（整页一个 Suspense）→ 一个慢请求阻塞整页
- 太细（每个组件一个 Suspense）→ 骨架屏闪烁，体验差
- 推荐：按页面区块划分，独立的数据区域各自一个 Suspense

### 4. useTransition 和 useDeferredValue

**useTransition：** 把状态更新标记为"非紧急"，让 React 优先处理用户输入。

```tsx
function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  function handleSearch(e) {
    setQuery(e.target.value)  // 紧急：立即更新输入框
    startTransition(() => {
      setResults(heavyFilter(e.target.value))  // 非紧急：可以被打断
    })
  }

  return (
    <>
      <input value={query} onChange={handleSearch} />
      {isPending ? <Spinner /> : <ResultList results={results} />}
    </>
  )
}
```

**useDeferredValue：** 延迟某个值的更新，适合不能修改子组件的场景。

```tsx
function SearchPage() {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)  // 延迟跟随 query

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <Suspense fallback={<Spinner />}>
        <SearchResults query={deferredQuery} />  {/* 用延迟值 */}
      </Suspense>
    </>
  )
}
```

**什么时候用哪个：**
- 能修改触发更新的代码 → `useTransition`
- 不能修改（第三方组件、props 传下来的值）→ `useDeferredValue`

### 5. 渲染优化：找到真正的问题

**先用工具定位，不要凭感觉优化：**

1. React DevTools → Profiler → 录制一次操作
2. 找到渲染时间长的组件（红色/橙色）
3. 看"Why did this render?"（需要开启 DevTools 的 "Record why each component rendered"）

**memo 不生效的常见原因：**

```tsx
// ❌ 每次渲染都创建新对象，memo 无效
function Parent() {
  return <Child style={{ color: 'red' }} />  // 每次新对象
}

// ✅ 提到组件外或用 useMemo
const style = { color: 'red' }  // 组件外，引用稳定
function Parent() {
  return <Child style={style} />
}

// ❌ 每次渲染都创建新函数，memo 无效
function Parent() {
  return <Child onClick={() => doSomething()} />
}

// ✅ 用 useCallback
function Parent() {
  const handleClick = useCallback(() => doSomething(), [])
  return <Child onClick={handleClick} />
}
```

**memo 的正确使用时机：**
- 组件渲染开销大（复杂计算、大列表）
- 父组件频繁重渲染但 props 不变
- **不要默认给所有组件加 memo**——大多数组件渲染很快，memo 本身也有开销

**Context 导致的过度渲染：**

```tsx
// ❌ 任何 context 值变化，所有消费者都重渲染
const AppContext = createContext({ user, theme, notifications })

// ✅ 拆分 context，按更新频率分组
const UserContext = createContext(user)      // 很少变
const ThemeContext = createContext(theme)    // 偶尔变
const NotifContext = createContext(notifs)   // 频繁变
```

### 6. 自定义 Hook 设计原则

**好的自定义 hook 的特征：**
- 封装一个完整的"关注点"，不是随机打包几个 useState
- 返回值语义清晰，调用方不需要看实现就知道怎么用
- 内部状态对外不可见，只暴露必要的接口

**设计模式：**

```ts
// ❌ 只是打包了几个 state，没有封装关注点
function useForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  return { name, setName, email, setEmail }
}

// ✅ 封装了表单的完整行为
function useForm(schema, onSubmit) {
  const [values, setValues] = useState({})
  const [errors, setErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const setValue = useCallback((field, value) => {
    setValues(v => ({ ...v, [field]: value }))
    // 清除该字段的错误
    setErrors(e => ({ ...e, [field]: undefined }))
  }, [])

  const submit = useCallback(async () => {
    const result = schema.safeParse(values)
    if (!result.success) {
      setErrors(result.error.flatten().fieldErrors)
      return
    }
    setIsSubmitting(true)
    try { await onSubmit(result.data) }
    finally { setIsSubmitting(false) }
  }, [values, schema, onSubmit])

  return { values, errors, isSubmitting, setValue, submit }
}
```

**hook 的命名规范：**
- `useXxx`：返回状态和操作（`useModal`、`useForm`）
- `useXxxQuery`：封装数据获取（`useUserQuery`）
- `useXxxStore`：封装 store 订阅（`useCartStore`）

### 7. Next.js App Router 数据获取策略

| 场景 | 方案 | 原因 |
|------|------|------|
| 静态内容（博客、文档） | RSC + `fetch` 默认缓存 | 构建时生成，CDN 缓存 |
| 动态内容（用户数据） | RSC + `fetch` + `cache: 'no-store'` | 每次请求都获取最新数据 |
| 需要实时更新 | Client Component + React Query | 客户端轮询或 WebSocket |
| 表单提交 | Server Actions | 无需 API 路由，直接操作数据库 |

**Server Actions（表单提交）：**

```tsx
// app/actions.ts
'use server'
export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  await db.post.create({ data: { title } })
  revalidatePath('/posts')  // 重新验证缓存
}

// app/new-post/page.tsx
import { createPost } from '../actions'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">发布</button>
    </form>
  )
}
```

---

## 常见反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| 所有组件加 `'use client'` | 失去 RSC 的所有优势 | 只在需要交互的叶子节点加 |
| useEffect 做数据获取 | 竞态条件、闪烁、重复请求 | 用 React Query 或 RSC |
| 默认给所有组件加 memo | 过早优化，增加代码复杂度 | 先 profile，再优化 |
| Context 存高频更新的状态 | 全局重渲染 | 高频状态用 Zustand |
| 在 useEffect 里更新 state 触发另一个 useEffect | 依赖链难以追踪 | 合并逻辑或用 useReducer |
