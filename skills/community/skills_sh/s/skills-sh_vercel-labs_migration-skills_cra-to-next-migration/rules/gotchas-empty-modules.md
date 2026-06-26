---
title: Fix Empty Module Exports
impact: LOW
impactDescription: TypeScript isolatedModules requirement
tags: gotchas, typescript, modules
---

## Fix Empty Module Exports

TypeScript's `isolatedModules` option (enabled by default in Next.js) requires every file to have at least one import or export statement.

**Error message:**

```
'file.ts' cannot be compiled under '--isolatedModules' because it is
considered a global script file. Add an import, export, or an empty
'export {}' statement to make it a module.
```

**Common files affected:**

- `pwa.ts` - Progressive Web App registration
- `sw.ts` - Service worker files
- `register-sw.ts` - Service worker registration
- `reportWebVitals.ts` - Web vitals reporting (if empty/commented)
- Type declaration files without exports

**CRA (works without exports):**

```ts
// src/pwa.ts
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
}

// No export needed in CRA
```

**Next.js (requires export):**

```ts
// pwa.ts
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
}

export {} // Add empty export to make it a module
```

**Alternative: Export the logic as a function**

```ts
// pwa.ts
export function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
  }
}

// Call from your app
import { registerServiceWorker } from './pwa'
registerServiceWorker()
```

**Files to check during migration:**

```bash
# Find TypeScript files without exports
grep -L "export" src/**/*.ts
```

**Quick fix pattern:**

Add `export {}` at the end of any standalone TypeScript file that doesn't have imports or exports but contains executable code.
