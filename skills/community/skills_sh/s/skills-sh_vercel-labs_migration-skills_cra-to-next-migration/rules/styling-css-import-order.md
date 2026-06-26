---
title: Control CSS Import Order in Layouts
impact: HIGH
impactDescription: Import order determines style cascade and specificity
tags: styling, css, import, layout, cascade
---

## Control CSS Import Order in Layouts

CSS import order in your layout files determines the cascade. Styles imported later override earlier ones when specificity is equal. This matters more in Next.js because all CSS is bundled together.

**Recommended import order:**

```tsx
// app/layout.tsx

// 1. CSS Resets / Normalizers (first - lowest priority)
import 'normalize.css';
// or
import 'antd/dist/reset.css';

// 2. Third-party component styles
import 'antd/dist/antd.css';
import 'react-datepicker/dist/react-datepicker.css';

// 3. Global application styles
import '@/styles/globals.scss';

// 4. Tailwind (usually last for utility overrides)
import '@/styles/tailwind.css';
```

**Why order matters:**

```tsx
// If imported in wrong order:
import '@/styles/globals.scss';  // Your .btn { color: red }
import 'bootstrap/dist/css/bootstrap.css';  // Bootstrap's .btn overwrites yours!

// Correct order:
import 'bootstrap/dist/css/bootstrap.css';  // Bootstrap base
import '@/styles/globals.scss';  // Your overrides win
```

**Tailwind integration pattern:**

```css
/* styles/tailwind.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom utilities after Tailwind's */
@layer utilities {
  .custom-gradient {
    background: linear-gradient(to right, #000, #fff);
  }
}
```

```tsx
// app/layout.tsx
import 'antd/dist/reset.css';      // 1. Reset
import '@/styles/globals.scss';     // 2. Global styles
import '@/styles/tailwind.css';     // 3. Tailwind last
```

**Debugging style conflicts:**

If styles aren't applying after migration:

1. **Check import order** in layout.tsx
2. **Look for duplicate imports** in nested layouts
3. **Use more specific selectors** if needed
4. **Check DevTools** to see which rule wins

```tsx
// app/layout.tsx
import '@/styles/globals.scss';

// app/(dashboard)/layout.tsx
import '@/styles/globals.scss';  // BAD - duplicate import

// The second import may override the first or cause duplication
```

**Nested layout imports:**

```tsx
// app/layout.tsx - Root layout
import '@/styles/globals.scss';
import '@/styles/tailwind.css';

export default function RootLayout({ children }) {
  return <html><body>{children}</body></html>;
}

// app/(marketing)/layout.tsx - Nested layout
// Only import ADDITIONAL styles needed for this section
import '@/styles/marketing.scss';  // Don't re-import globals

export default function MarketingLayout({ children }) {
  return <div className="marketing">{children}</div>;
}
```

**Common issues:**

| Problem | Cause | Fix |
|---------|-------|-----|
| Third-party styles override yours | Wrong import order | Import third-party first |
| Tailwind utilities don't work | Tailwind imported too early | Import Tailwind last |
| Styles duplicated | Same import in multiple layouts | Only import in root layout |
| Specificity wars | Equal specificity, wrong order | Reorder imports or increase specificity |

**CSS Module styles:**

CSS Modules are scoped and don't compete with global styles:

```tsx
// These are independent of import order
import styles from './Button.module.scss';
import otherStyles from './Card.module.scss';

// They generate unique class names like .Button_btn__x7h3f
```
