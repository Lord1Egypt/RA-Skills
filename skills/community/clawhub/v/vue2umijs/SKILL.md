---
name: vue-to-umijs
description: >-
  Migrate Vue 2/3 projects to React on UmiJS (@umijs/max): conventions, constraints,
  stack mapping, and syntax examples (single SKILL.md). Use for .vue → Umi pages and data flow.
license: MIT
---

# Vue → UmiJS + React migration

**Goal**: move a **Vue codebase** to **UmiJS (`@umijs/max`) + React 18 + antd**, with behavior parity and Umi’s routing, data flow, and folder conventions.

**Document layout**: rules and constraints first; **Stack and Umi mapping** next; **Syntax examples** last.

## Scope

- **Source**: Vue 2 / 3 (Options API, Composition API, SFC).
- **Target**: **Umi 4 + @umijs/max + React 18**; function components and hooks; TypeScript for public APIs.
- **Default stack**: **antd**; **`src/models` + `useModel`**; **React Router v6** (via Umi); **Less** + **`*.module.less`**; pages as **`PageName/index.tsx` + `PageName/index.module.less`**.

## Principles

1. **Parity first**: routing, URL, guards, loading/errors, and UX before micro-optimizations.
2. **Single source of truth**: no duplicate domain state across store and local state unless there is an explicit draft/edit buffer.
3. **Side-effect boundaries**: `useEffect` (or Umi equivalents) for subscriptions and async with cleanup; cancel in-flight work with `AbortController` where needed.
4. **No Vue runtime**: replace plugins, mixins, filters, and global buses with hooks, Umi models, and explicit modules.
5. **Closures and deps**: dependency arrays reflect real deps; derive with render/`useMemo`, not effects for pure derivation.

## API mapping (summary)

| Area                                      | Direction                                                                                              |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Page `.vue`                               | **`PageName/index.tsx` + `index.module.less`**                                                         |
| Child `.vue`                              | **`Foo.tsx` + `Foo.module.less`** (same folder, matching basename)                                     |
| Component API                             | `defineComponent` → `function Name(props: NameProps)`; `emit` → `onXxx`                                |
| `ref` / `reactive` / `computed` / `watch` | `useState` / `useRef`, `useReducer`, `useMemo`, `useEffect` (deps + cleanup)                           |
| Vue Router                                | Umi **`config` / `routes`**; **`useNavigate`**, **`useParams`**, etc. — see **Routing and data** below |
| Pinia / Vuex                              | **`src/models` + `useModel`** by domain; prefer **`useRequest`** for local fetch/cache                 |
| Element UI / Element Plus                 | Map to **antd** with matching interaction and validation semantics                                     |

## Constraints

1. **One router tree**: use Umi nested routes/layouts; **do not** add a standalone **`BrowserRouter`** beside Umi; avoid full-page navigations that break SPA where the old app used in-app routing.
2. **Typing**: avoid **`any`** on exported components, route params, and model shapes.
3. **Security and a11y**: no untrusted `dangerouslySetInnerHTML`; preserve focus, labels, and keyboard behavior; env vars and URL semantics stay aligned or are explicitly documented.
4. **Styles**: **`index.module.less`** next to **`index.tsx`** for pages; child components: **`.tsx` + `.module.less`** with the same basename.
5. **Vue-specific features**: custom directives, plugins, `defineExpose` + parent refs must map to explicit React/Umi patterns (controlled props, **`forwardRef`/`useImperativeHandle`**, permission guards)—**never silently drop behavior**.
6. **Async and lists**: clean up listeners and requests on unmount or dep changes; use **stable ids** for list `key`s, not indexes when order changes.
7. **Do not**: run side effects **during render**; use **`useEffect` for pure derivation**; recreate **EventBus / mixin / filter pipelines**; **mirror props to state** without need; introduce a **second global state stack** for the same domain without a plan (prefer **Umi models**).

### Additional constraints (often missed—verify explicitly)

1. **i18n**: migrate `vue-i18n` keys/namespaces and locale switching to the chosen solution (including Umi locale plugins); avoid leftover hard-coded copy or mixed languages.
2. **HTTP and errors**: use the shared **`request`** wrapper (and `@umijs/max` request APIs) so interceptors, error codes, auth headers, and global toasts **match** the old Vue layer; avoid ad-hoc **`fetch`** that bypasses global handling.
3. **Environment**: map `VITE_*` / `import.meta.env` to Umi **env / `define`**; **never** ship secrets or internal-only URLs in the client bundle.
4. **Forms and tables**: align Element validation rules, async validation, and blur/submit timing with **antd `Form`**; keep **`Table` `rowKey`**, pagination, sort, and filter params aligned with backend contracts; validate dynamic forms (`Form.List`, etc.) behavior-by-behavior.
5. **API scalars**: keep **explicit conversion** between backend **`0/1`**, stringly numbers, enums, and UI booleans—prefer normalization at submit/response boundaries to avoid silent drift.
6. **Build and deploy**: **`publicPath` / `base`**, static asset URLs, and CDN prefixes match the old site or are **documented**; avoid production 404s for assets.
7. **Dev / integration**: move **mocks** and dev **proxy** from the Vue setup into Umi conventions (`mock/`, **`proxy`**) so local and joint-debug environments stay consistent.
8. **SSR vs CSR**: with **Umi SSR**, do not use **`window` / `document` / `localStorage`** on the server render path; with CSR-only, document any first-screen / SEO differences vs the legacy app.

## Pre-release checklist

- [ ] Routing, query, and auth behavior matches the legacy app (or differences are documented).
- [ ] `useEffect` deps are complete; async work is cancelled or ignored when stale.
- [ ] Pages include **`index.tsx` + `index.module.less`**; child style files match basename.
- [ ] Custom directives/plugins/exposed methods have a mapped implementation or migration note.
- [ ] Request layer, env vars, and deploy paths checked against **Additional constraints**.
- [ ] Sample pass on critical forms/tables and i18n paths vs legacy behavior.

## Style and structure

- Prefer function components and hooks; **`emit`** → **`onXxx`**.
- Keep feature boundaries similar to the Vue repo; page folder naming: see **Vue SFC styles → Umi components** below.

## Stack and Umi mapping

Umi/antd APIs follow the [official docs](https://umijs.org/).

## Target stack

| Layer         | Choice                                                          |
| ------------- | --------------------------------------------------------------- |
| App framework | **[@umijs/max](https://umijs.org/)** (Umi 4)                    |
| UI            | **[Ant Design](https://ant.design/)** (`antd`)                  |
| Global state  | **Umi data flow**: `src/models` + **`useModel`**                |
| Runtime       | **React 18**                                                    |
| Routing       | **React Router v6** (via Umi; configure in `config` + `routes`) |

Styling: **Less** + **CSS Modules** (`*.module.less`). Pages: **`PageName/index.tsx`** + **`PageName/index.module.less`**.

## Routing and data (Umi)

| Typical Vue pattern                   | Umi + React                                                                                                     |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Fetch in `onMounted` after navigation | **`useRequest`**, **`useModel`**, or `useEffect` + project **`request`** in page/layout                         |
| `beforeEach` auth                     | **`access`**, route **`wrappers`**, or layout-level guards (see Umi docs)                                       |
| Navigation / URL params               | **`useNavigate`**, **`useParams`**, **`useSearchParams`**, **`useLocation`** from **`@umijs/max`** or **`umi`** |

Do not add a second standalone **`BrowserRouter`** root outside Umi.

## Pinia / Vuex → Umi data flow

| Vue               | Umi                                                               |
| ----------------- | ----------------------------------------------------------------- |
| Modular store     | **`src/models`** split by domain + **`useModel`**                 |
| Getters / derived | Logic in models or **`useMemo`** in components                    |
| Async actions     | Model **effects**, or **`useRequest`** in pages then update model |

Prefer **`useRequest`** for local request/cache when global state is not needed.

## Vue SFC styles → Umi components

| Vue                   | React (Umi)                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------- |
| Page `<style scoped>` | **`PageDir/index.tsx`** + **`index.module.less`**, `import styles from './index.module.less'` |
| Child scoped          | **`Foo.tsx`** + **`Foo.module.less`** in the same folder                                      |
| `<style lang="less">` | Same content in the matching **`*.module.less`**                                              |

For **HTTP, i18n, env, deploy, and mock** constraints, see **Additional constraints** above.

## Syntax examples

Vue vs React syntax; use **`@umijs/max`**, **antd**, and the rules above in real pages.

### 1. Counter

**Vue 3 (`<script setup>`)**

```vue
<script setup lang="ts">
import { ref } from 'vue'
const count = ref(0)
function inc() {
  count.value++
}
</script>
<template>
  <button type="button" @click="inc">{{ count }}</button>
</template>
```

**React**

```tsx
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return (
    <button type="button" onClick={() => setCount((c) => c + 1)}>
      {count}
    </button>
  )
}
```

### 2. Conditional list

**Vue**

```vue
<template>
  <ul v-if="items.length">
    <li v-for="item in items" :key="item.id">{{ item.name }}</li>
  </ul>
  <p v-else>No data</p>
</template>
```

**React**

```tsx
return items.length ? (
  <ul>
    {items.map((item) => (
      <li key={item.id}>{item.name}</li>
    ))}
  </ul>
) : (
  <p>No data</p>
)
```

### 3. Controlled input

**Vue**

```vue
<input v-model="text" />
```

**React**

```tsx
const [text, setText] = useState('')
<input value={text} onChange={(e) => setText(e.target.value)} />
```

### 4. Child events (`emit`)

**Vue**

```vue
<script setup lang="ts">
const emit = defineEmits<{ (e: 'update', v: number): void }>()
function notify() {
  emit('update', 1)
}
</script>
```

**React**

```tsx
type Props = { onUpdate: (v: number) => void }
export function Child({ onUpdate }: Props) {
  function notify() {
    onUpdate(1)
  }
}
```

### 5. `computed` and `watch`

**Vue**

```ts
const doubled = computed(() => count.value * 2)
watch(count, (v) => console.log(v))
```

**React**

```tsx
const doubled = useMemo(() => count * 2, [count])
useEffect(() => {
  console.log(count)
}, [count])
```

### 6. Provide / inject

**Vue**

```ts
provide('theme', 'dark')
const theme = inject('theme')
```

**React**

```tsx
import { createContext, useContext, useMemo, useState } from 'react'

type Theme = 'light' | 'dark'
type ThemeContextValue = {
  theme: Theme
  setTheme: (v: Theme) => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')
  const value = useMemo(() => ({ theme, setTheme }), [theme])
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider')
  return ctx
}

// usage:
// const { theme, setTheme } = useTheme()
```

### 7. Cleanup

**Vue**

```ts
onUnmounted(() => window.removeEventListener('resize', onResize))
```

**React**

```tsx
useEffect(() => {
  window.addEventListener('resize', onResize)
  return () => window.removeEventListener('resize', onResize)
}, [])
```

### 8. Scoped slot → render prop

**Vue**

```vue
<Child v-slot="{ row }">
  <span>{{ row.name }}</span>
</Child>
```

**React**

```tsx
<Child renderRow={(row) => <span>{row.name}</span>} />
```

### 9. Route params

**Vue**

```ts
const route = useRoute()
const id = route.params.id as string
```

**Umi (same as React Router v6)**

```tsx
import { useParams } from '@umijs/max'
// or import { useParams } from 'umi'

const { id } = useParams<{ id: string }>()
```

### 10. React mental model: closure and deps

**Common but not recommended**

```tsx
// stale closure: interval always sees initial count
useEffect(() => {
  const timer = setInterval(() => {
    setCount(count + 1)
  }, 1000)
  return () => clearInterval(timer)
}, []) // count is missing
```

**Recommended**

```tsx
// use functional update to avoid stale closure
useEffect(() => {
  const timer = setInterval(() => {
    setCount((c) => c + 1)
  }, 1000)
  return () => clearInterval(timer)
}, [])
```

**Common but not recommended**

```tsx
// derives data via effect + extra state
const [fullName, setFullName] = useState('')
useEffect(() => {
  setFullName(`${user.firstName} ${user.lastName}`)
}, [user.firstName, user.lastName])
```

**Recommended**

```tsx
// derive directly in render / useMemo
const fullName = useMemo(
  () => `${user.firstName} ${user.lastName}`,
  [user.firstName, user.lastName]
)
```
