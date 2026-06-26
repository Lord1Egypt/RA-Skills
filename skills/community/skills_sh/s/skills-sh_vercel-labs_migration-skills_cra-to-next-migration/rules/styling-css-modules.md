---
title: CSS Modules Work with Minor Changes
impact: LOW
impactDescription: Mostly compatible
tags: styling, css-modules
---

## CSS Modules Work with Minor Changes

CSS Modules work almost identically in Next.js. The main difference is file naming convention.

**CRA Pattern (before):**

```css
/* src/components/Button.module.css */
.button {
  background: blue;
  color: white;
}

.primary {
  background: green;
}
```

```tsx
// src/components/Button.tsx
import styles from './Button.module.css'

export function Button({ variant = 'default' }) {
  return (
    <button className={`${styles.button} ${variant === 'primary' ? styles.primary : ''}`}>
      Click me
    </button>
  )
}
```

**Next.js Pattern (after):**

```css
/* components/Button.module.css */
.button {
  background: blue;
  color: white;
}

.primary {
  background: green;
}
```

```tsx
// components/Button.tsx
import styles from './Button.module.css'

export function Button({ variant = 'default' }) {
  return (
    <button className={`${styles.button} ${variant === 'primary' ? styles.primary : ''}`}>
      Click me
    </button>
  )
}
```

**Key points:**
- Same `.module.css` naming convention
- Same import and usage pattern
- Works in both Server and Client Components
- Scoped class names generated automatically

**With clsx for cleaner class handling:**

```tsx
import styles from './Button.module.css'
import clsx from 'clsx'

export function Button({ variant, disabled }) {
  return (
    <button
      className={clsx(
        styles.button,
        variant === 'primary' && styles.primary,
        disabled && styles.disabled
      )}
    >
      Click me
    </button>
  )
}
```
