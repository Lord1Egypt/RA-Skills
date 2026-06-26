---
title: Handle CSS-in-JS Libraries
impact: HIGH
impactDescription: Requires SSR configuration
tags: styling, css-in-js, ssr
---

## Handle CSS-in-JS Libraries

CSS-in-JS libraries need special configuration for Server-Side Rendering in Next.js.

**CRA Pattern (before):**

```tsx
// Works out of the box - client-only rendering
import styled from 'styled-components'

const Button = styled.button`
  background: blue;
  color: white;
`
```

**Next.js - Needs configuration (after):**

Most CSS-in-JS libraries require:
1. SSR style extraction
2. Client hydration
3. `'use client'` directive

**Recommended approaches by library:**

| Library | App Router Support | Configuration |
|---------|-------------------|---------------|
| Tailwind CSS | Full | No extra config |
| CSS Modules | Full | No extra config |
| styled-components | Requires setup | See docs |
| Emotion | Requires setup | See docs |
| Vanilla Extract | Full (build-time) | Plugin needed |
| Panda CSS | Full (build-time) | Recommended |

**Zero-config alternatives:**

```tsx
// CSS Modules - works everywhere
import styles from './Button.module.css'

export function Button() {
  return <button className={styles.button}>Click</button>
}
```

```tsx
// Tailwind - works everywhere
export function Button() {
  return <button className="bg-blue-500 text-white px-4 py-2">Click</button>
}
```

**If you must use runtime CSS-in-JS:**

1. Mark components with `'use client'`
2. Follow library-specific setup guides
3. Be aware of hydration issues
4. Consider migrating to build-time CSS solutions
