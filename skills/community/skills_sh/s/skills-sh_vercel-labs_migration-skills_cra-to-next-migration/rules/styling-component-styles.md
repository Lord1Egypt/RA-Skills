---
title: Import Component Styles Properly
impact: MEDIUM
impactDescription: Avoid global CSS in components
tags: styling, imports, css-modules
---

## Import Component Styles Properly

In Next.js App Router, component-level CSS must use CSS Modules, not global CSS imports.

**CRA Pattern (before):**

```tsx
// src/components/Card.tsx
import './Card.css' // Global CSS import - works in CRA

export function Card() {
  return <div className="card">Content</div>
}
```

```css
/* src/components/Card.css */
.card {
  border: 1px solid #ccc;
  padding: 16px;
}
```

**Next.js Pattern - WRONG:**

```tsx
// components/Card.tsx
import './Card.css' // ERROR: Global CSS cannot be imported from components

export function Card() {
  return <div className="card">Content</div>
}
```

**Next.js Pattern - CORRECT:**

```tsx
// components/Card.tsx
import styles from './Card.module.css' // Use CSS Modules

export function Card() {
  return <div className={styles.card}>Content</div>
}
```

```css
/* components/Card.module.css */
.card {
  border: 1px solid #ccc;
  padding: 16px;
}
```

**Migration steps:**

1. Rename `Component.css` to `Component.module.css`
2. Import as `import styles from './Component.module.css'`
3. Replace `className="name"` with `className={styles.name}`

**Why this restriction?**
- Prevents CSS ordering issues
- Ensures styles are scoped
- Enables better code splitting
- Avoids conflicts between components
