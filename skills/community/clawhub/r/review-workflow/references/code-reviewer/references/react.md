# React Code Review Guide

React 审查重点：Hooks 规则、性能优化的适度性、组件设计、以及现代 React 19/RSC 模式。

## 目录

- [基础 Hooks 规则](#基础-hooks-规则)
- [useEffect 模式](#useeffect-模式)
- [useMemo / useCallback](#usememo--usecallback)
- [组件设计](#组件设计)
- [Error Boundaries & Suspense](#error-boundaries--suspense)
- [Server Components (RSC)](#server-components-rsc)
- [React 19 Actions & Forms](#react-19-actions--forms)
- [Suspense & Streaming SSR](#suspense--streaming-ssr)
- [TanStack Query v5](#tanstack-query-v5)
- [Review Checklists](#review-checklists)

---

## 基础 Hooks 规则

```tsx
// ❌ 条件调用 Hooks — 违反 Hooks 规则
function BadComponent({ isLoggedIn }) {
  if (isLoggedIn) {
    const [user, setUser] = useState(null);  // Error!
  }
  return <div>...</div>;
}

// ✅ Hooks 必须在组件顶层调用
function GoodComponent({ isLoggedIn }) {
  const [user, setUser] = useState(null);
  if (!isLoggedIn) return <LoginPrompt />;
  return <div>{user?.name}</div>;
}
```

---

## useEffect 模式

```tsx
// ❌ 依赖数组缺失或不完整
function BadEffect({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []);  // 缺少 userId 依赖！
}

// ✅ 完整的依赖数组 + 清理函数
function GoodEffect({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    let cancelled = false;
    fetchUser(userId).then(data => {
      if (!cancelled) setUser(data);
    });
    return () => { cancelled = true; };
  }, [userId]);
}

// ❌ useEffect 用于派生状态（反模式）
function BadDerived({ items }) {
  const [filteredItems, setFilteredItems] = useState([]);
  useEffect(() => {
    setFilteredItems(items.filter(i => i.active));
  }, [items]);  // 不必要的 effect + 额外渲染
  return <List items={filteredItems} />;
}

// ✅ 直接在渲染时计算，或用 useMemo
function GoodDerived({ items }) {
  const filteredItems = useMemo(
    () => items.filter(i => i.active),
    [items]
  );
  return <List items={filteredItems} />;
}
```

---

## useMemo / useCallback

```tsx
// ❌ 过度优化 — 常量不需要 useMemo
function OverOptimized() {
  const config = useMemo(() => ({ timeout: 5000 }), []);  // 无意义
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);  // 如果不传给 memo 组件，无意义
}

// ✅ 只在需要时优化（配合 React.memo）
const MemoizedChild = React.memo(function Child({ onClick, items }) {
  return <div onClick={onClick}>{items.length}</div>;
});

function Parent({ rawItems }) {
  const items = useMemo(() => processItems(rawItems), [rawItems]);
  const handleClick = useCallback(() => {
    console.log(items.length);
  }, [items]);
  return <MemoizedChild onClick={handleClick} items={items} />;
}
```

---

## 组件设计

```tsx
// ❌ 在组件内定义组件 — 每次渲染都创建新组件
function BadParent() {
  function ChildComponent() {  // 每次渲染都是新函数！
    return <div>child</div>;
  }
  return <ChildComponent />;
}

// ✅ 组件定义在外部
function ChildComponent() {
  return <div>child</div>;
}
function GoodParent() {
  return <ChildComponent />;
}
```

---

## Error Boundaries & Suspense

```tsx
// ❌ 没有错误边界
function BadApp() {
  return (
    <Suspense fallback={<Loading />}>
      <DataComponent />
    </Suspense>
  );
}

// ✅ Error Boundary 包裹 Suspense
function GoodApp() {
  return (
    <ErrorBoundary fallback={<ErrorUI />}>
      <Suspense fallback={<Loading />}>
        <DataComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

---

## Server Components (RSC)

```tsx
// ❌ 在 Server Component 中使用客户端特性
// app/page.tsx (Server Component by default)
function BadServerComponent() {
  const [count, setCount] = useState(0);  // Error! No hooks in RSC
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// ✅ 交互逻辑提取到 Client Component
// app/counter.tsx
'use client';
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// app/page.tsx (Server Component)
async function GoodServerComponent() {
  const data = await fetchData();  // 可以直接 await
  return (
    <div>
      <h1>{data.title}</h1>
      <Counter />  {/* 客户端组件 */}
    </div>
  );
}
```

---

## React 19 Actions & Forms

### useActionState

```tsx
// ❌ 传统方式：多个状态变量
function OldForm() {
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const handleSubmit = async (formData) => {
    setIsPending(true);
    try {
      const result = await submitForm(formData);
      setData(result);
    } catch (e) {
      setError(e.message);
    } finally {
      setIsPending(false);
    }
  };
}

// ✅ React 19: useActionState 统一管理
import { useActionState } from 'react';

function NewForm() {
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData) => {
      try {
        const result = await submitForm(formData);
        return { success: true, data: result };
      } catch (e) {
        return { success: false, error: e.message };
      }
    },
    { success: false, data: null, error: null }
  );

  return (
    <form action={formAction}>
      <input name="email" />
      <button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </button>
      {state.error && <p className="error">{state.error}</p>}
    </form>
  );
}
```

### useOptimistic

```tsx
// ✅ useOptimistic 即时反馈，失败自动回滚
import { useOptimistic } from 'react';

function FastLike({ postId, likes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (currentLikes, increment) => currentLikes + increment
  );

  const handleLike = async () => {
    addOptimisticLike(1);  // 立即更新 UI
    try {
      await likePost(postId);
    } catch {
      // React 自动回滚到 likes 原值
    }
  };

  return <button onClick={handleLike}>{optimisticLikes} likes</button>;
}
```

---

## TanStack Query v5

### 生产环境推荐配置

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,  // 5 分钟内数据视为新鲜
      gcTime: 1000 * 60 * 30,    // 30 分钟后垃圾回收
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});
```

### queryOptions (v5 新增)

```tsx
// ✅ queryOptions 统一定义，类型安全
import { queryOptions } from '@tanstack/react-query';

const userQueryOptions = (userId: string) =>
  queryOptions({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
  });

function Component1({ userId }) {
  const { data } = useQuery(userQueryOptions(userId));
}

function prefetchUser(queryClient, userId) {
  queryClient.prefetchQuery(userQueryOptions(userId));
}
```

### useSuspenseQuery 限制

| 特性 | useQuery | useSuspenseQuery |
|------|----------|------------------|
| `enabled` 选项 | ✅ 支持 | ❌ 不支持 |
| `placeholderData` | ✅ 支持 | ❌ 不支持 |
| `data` 类型 | `T \| undefined` | `T`（保证有值）|
| 错误处理 | `error` 属性 | 抛出到 Error Boundary |

### v5 状态字段变化

```tsx
// v5: isPending 表示没有数据，isLoading = isPending && isFetching
const { data, isPending, isFetching, isLoading } = useQuery({...});

// isPending: 缓存中没有数据（首次加载）
// isFetching: 正在请求中（包括后台刷新）
// isLoading: isPending && isFetching（首次加载中）
```

---

## Review Checklists

### Hooks 规则
- [ ] Hooks 在组件/自定义 Hook 顶层调用
- [ ] 没有条件/循环中调用 Hooks
- [ ] useEffect 依赖数组完整
- [ ] useEffect 有清理函数（订阅/定时器/请求）
- [ ] 没有用 useEffect 计算派生状态

### 性能优化（适度原则）
- [ ] useMemo/useCallback 只用于真正需要的场景
- [ ] React.memo 配合稳定的 props 引用
- [ ] 没有在组件内定义子组件
- [ ] 没有在 JSX 中创建新对象/函数（除非传给非 memo 组件）

### 组件设计
- [ ] 组件职责单一，不超过 200 行
- [ ] 逻辑与展示分离（Custom Hooks）
- [ ] Props 接口清晰，使用 TypeScript
- [ ] 避免 Props Drilling

### 错误处理
- [ ] 关键区域有 Error Boundary
- [ ] Suspense 配合 Error Boundary 使用
- [ ] 异步操作有错误处理

### Server Components (RSC)
- [ ] 'use client' 只用于需要交互的组件
- [ ] Server Component 不使用 Hooks/事件处理
- [ ] 客户端组件尽量放在叶子节点

### React 19 Forms
- [ ] 使用 useActionState 替代多个 useState
- [ ] useFormStatus 在 form 子组件中调用
- [ ] useOptimistic 不用于关键业务（支付等）

### TanStack Query
- [ ] queryKey 包含所有影响数据的参数
- [ ] 设置合理的 staleTime（不是默认 0）
- [ ] useSuspenseQuery 不使用 enabled
- [ ] Mutation 成功后 invalidate 相关查询
- [ ] 理解 isPending vs isLoading 区别