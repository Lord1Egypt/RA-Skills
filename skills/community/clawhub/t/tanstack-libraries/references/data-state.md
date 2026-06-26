# Data & State

> Start / Router / Query / DB / Store / AI

---

## Query

**Installation:** `npm i @tanstack/react-query` (adapters: react/vue/solid/svelte/angular/lit)

```ts
// Provider
const queryClient = new QueryClient()
// <QueryClientProvider client={queryClient}>

// Queries
const { data, isPending, error } = useQuery({ queryKey: ['todos'], queryFn: () => fetch('/api/todos').then(r => r.json()) })

// Mutations
const mutation = useMutation({
  mutationFn: (todo) => fetch('/api/todos', { method: 'POST', body: JSON.stringify(todo) }),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
})

// Status: status(pending/error/success) + fetchStatus(fetching/paused/idle)
// Invalidation: queryClient.invalidateQueries({ queryKey: ['todos'] })
// Prefetching: queryClient.prefetchQuery({ queryKey, queryFn, staleTime })
// Parallel: useQuery + useQuery / useQueries({ queries: [...] })
// Pagination: placeholderData: keepPreviousData
// Infinite scrolling: useInfiniteQuery({ getNextPageParam })
// Suspense: useSuspenseQuery({ queryKey, queryFn })
// Network mode: online(default) / always / offlineFirst
// staleTime(cache freshness duration) vs gcTime(garbage collection time)
```

**v5 changes:** All hooks unified to single object signature `useQuery({ queryKey, queryFn })`

**Optimistic updates:**
```ts
onMutate: async (vars) => {
  await queryClient.cancelQueries({ queryKey })
  const prev = queryClient.getQueryData(queryKey)
  queryClient.setQueryData(queryKey, old => [...old, vars])
  return { prev }  // → onMutateResult
},
onError: (err, vars, onMutateResult) => queryClient.setQueryData(queryKey, onMutateResult.prev),
onSettled: () => queryClient.invalidateQueries({ queryKey }),
```

**Mutations lifecycle:** `onMutate → mutationFn → onSuccess/onError → onSettled`

**ESLint:** `npm i -D @tanstack/eslint-plugin-query` (detects missing useQuery dependencies, conservative staleTime, etc.)

---

## Router

**Installation:** `npm i @tanstack/react-router` (adapters: react/solid)

```ts
// Type registration
declare module '@tanstack/react-router' { interface Register { router: typeof router } }

// File-based routing (src/routes/)
// posts.$postId.tsx → export const Route = createFileRoute('/posts/$postId')({
//   loader: ({ params }) => fetchPost(params.postId),
//   component: () => { const { postId } = Route.useParams(); return <div>{postId}</div> }
// })

// Code-based routing
const rootRoute = createRootRoute()
const indexRoute = createRoute({ getParentRoute: () => rootRoute, path: '/', component: Index })
const router = createRouter({ routeTree: rootRoute.addChildren([indexRoute]) })
```

**Core features:**
- 100% type inference (path params/Search/navigation)
- Search Params JSON auto-parsing + Schema validation
- Loader + SWR caching (can integrate with Query)
- Code splitting: `autoCodeSplitting: true` / `.lazy.tsx` / Virtual Routes
- Navigation blocking: `useBlocker({ shouldBlockFn })`

**Data loading lifecycle:** Route Matching → `beforeLoad` (serial) → `loader` (parallel)

**Query integration:**
```ts
const opts = queryOptions({ queryKey: ['posts'], queryFn: fetchPosts })
export const Route = createFileRoute('/posts')({
  loader: () => queryClient.ensureQueryData(opts),
  component: () => { const { data } = useSuspenseQuery(opts); return ... }
})
```

---

## Start (RC)

Full-stack framework: SSR/Streaming/Server Functions/RSC, built on Router+Vite.
- `@tanstack/react-start` / `@tanstack/solid-start`

---

## DB (Beta)

Based on TypeScript differential dataflow (d2ts):
```ts
const todos = createCollection(queryCollectionOptions({ queryKey: ['todos'], queryFn: fetchTodos, getKey: (item) => item.id }))
const { data } = useLiveQuery((q) => q.from({ todo: todos }).where(({ todo }) => !todo.completed))
todos.update(id, (draft) => { draft.completed = true })  // Optimistic mutation
```

Sync modes: eager (<10k full) / on-demand (component query) / progressive
Collection types: Query / Electric / TrailBase / RxDB / PowerSync / LocalStorage
Schema: Compatible with Standard Schema (Zod/Valibot/ArkType/Effect)

---

## Store (Alpha)

```ts
import { Store } from '@tanstack/store'
const store = new Store({ count: 0 })
store.setState((s) => ({ count: s.count + 1 }))
```

Internal TanStack core dependency, drives Form/Router/Pacer. Adapters: react/vue/angular/solid/svelte.

---

## AI (Alpha)

Unified interface for multiple Providers (openrouter/openai/anthropic/gemini/ollama/groq/grok/fal).

```bash
npm i @tanstack/ai @tanstack/ai-react @tanstack/ai-openai
```

```ts
import { chat, toolDefinition } from '@tanstack/ai'
import { openaiText } from '@tanstack/ai-openai'

const getProducts = toolDefinition({
  name: 'getProducts',
  inputSchema: z.object({ query: z.string() }),
}).server(async ({ query }) => await db.search(query))

chat({ adapter: openaiText('gpt-5.2'), messages: [...], tools: [getProducts] })
```

Features: Isomorphic tools (.server/.client), streaming + Thinking tokens, middleware, Code Mode (Sandbox TS), real-time speech