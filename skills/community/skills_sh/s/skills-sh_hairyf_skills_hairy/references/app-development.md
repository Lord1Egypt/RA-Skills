---
name: app-development
description: Hairy's preferences for building web applications with Vue, Vite/Nuxt, and UnoCSS
---

# App Development Preferences

Preferences for building web applications.

## Stack Overview

| Aspect | Choice |
|--------|--------|
| Framework | React (Hooks) |
| Build Tool | Vite (SPA) or Next.js (SSR/SSG) |
| Backend | Nest.js |
| Styling | TailwindCSS |
| Utilities | React-use |
| Animation | React-motion or Animejs |

---

## Framework Selection

| Use Case | Choice |
|----------|--------|
| SPA, client-only, library playgrounds | Vite + React |
| SSR, SSG, SEO-critical, file-based routing, API routes | Next.js |
| Backend | Nest.js |

---

## React Conventions

| Convention | Preference |
|------------|------------|
| Props | Always `export interface ComponentProps { ... }` |
| Component internal | Prefer `function onClick() { ... }` over `const onClick = () => { ... }` |
| Objects | Use `@tanstack/react-query`, avoid `const [loading, setLoading] = useState(false)` |

### Props and Emits

Use TypeScript interfaces:

```tsx
export interface ComponentProps {
  title: string
  count?: number
  onUpdate: (value: number) => void
  onClose: () => void
}

export function Component(props: ComponentProps) {
  const { title, count = 0, onUpdate, onClose } = props
  
  function onHandleUpdate() {
    onUpdate(count + 1)
  }

  return (
    <div>
      <h1>{title}</h1>
      <p>{count}</p>
      <button onClick={onHandleUpdate}>Update</button>
      <button onClick={onClose}>Close</button>
    </div>
  )
  )

```

### Conditional Rendering

```tsx
import { If, Else, Then } from '@hairy/utils'

export function Component() {
  return (
    <>
     {/* simple case */}
     <If cond={bool}>
        aaa
     </If>
     {/* ternary case */}
     <If cond={bool}>
        <Then cond={bool2}>
          aaa
        </Then>
        <Else>
          <p>False</p>
        </Else>
     </If>
    </>
  )
}
```