---
title: Use :global Only in CSS Modules
impact: HIGH
impactDescription: :global syntax in regular SCSS files causes build errors
tags: styling, scss, css-modules, global
---

## Use :global Only in CSS Modules

The `:global` syntax is a CSS Modules feature. It only works in `.module.scss` files, not regular `.scss` files. Next.js enforces this more strictly than CRA.

**Problem: :global in regular SCSS**

```scss
// styles/globals.scss - NOT a module
:global {
  .some-class {
    color: red;
  }
}
// Error: :global is not valid in this context
```

**Solution 1: Remove :global from regular SCSS**

Regular SCSS files are already global - they don't need `:global`:

```scss
// styles/globals.scss - Regular SCSS file
.some-class {
  color: red;  // Already global, no wrapper needed
}

body {
  margin: 0;
}

.ant-btn {  // Override third-party styles directly
  border-radius: 4px;
}
```

**Solution 2: Use CSS Modules with :global**

If you need scoped styles with some global overrides, use a module file:

```scss
// components/Button.module.scss
.button {
  padding: 8px 16px;  // Scoped to this module

  :global(.icon) {
    margin-right: 4px;  // Targets global .icon class
  }
}

:global {
  .external-lib-override {
    color: blue;  // Global override
  }
}
```

**When to use which file type:**

| File Type | Use Case | :global Syntax |
|-----------|----------|----------------|
| `globals.scss` | App-wide base styles, resets, third-party overrides | Not needed (already global) |
| `Component.module.scss` | Component-scoped styles | Supported for escaping scope |
| `variables.scss` | SCSS variables, mixins | N/A |

**Importing patterns:**

```tsx
// Global styles - import in layout
// app/layout.tsx
import '@/styles/globals.scss';

// Module styles - import and use classes
// components/Button.tsx
import styles from './Button.module.scss';

function Button() {
  return <button className={styles.button}>Click</button>;
}
```

**Migrating CRA :global usage:**

```scss
// CRA pattern that needs migration
// styles/overrides.scss
:global {
  .ant-modal {
    border-radius: 8px;
  }
  .ant-btn {
    font-weight: 500;
  }
}

// Next.js - remove :global wrapper
// styles/overrides.scss
.ant-modal {
  border-radius: 8px;
}
.ant-btn {
  font-weight: 500;
}
```

**Common error messages:**

- `Selector ":global" is not pure` - Using :global in non-module file
- `Pseudo-class ":global" is not a standard CSS feature` - Same issue

**Pre-migration scan:**

```bash
# Find :global usage in non-module files
grep -r ":global" --include="*.scss" --exclude="*.module.scss" src/
```
