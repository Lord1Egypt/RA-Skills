---
title: Handle Turbopack Compatibility Issues
impact: HIGH
impactDescription: Next.js 16+ uses Turbopack by default
tags: gotchas, turbopack, scss, webpack
---

## Handle Turbopack Compatibility Issues

Next.js 16+ uses Turbopack as the default bundler for development. Some webpack-specific features are not supported.

**Problem: SCSS `:export` syntax doesn't work with Turbopack**

```scss
// styles/colors.scss - CRA pattern that breaks
$primary: #007bff;
$secondary: #6c757d;

:export {
  primary: $primary;
  secondary: $secondary;
}
```

```tsx
// This import fails with Turbopack
import colors from './colors.scss'
console.log(colors.primary) // undefined or error
```

**Solution 1: Use `--webpack` flag**

For projects with extensive SCSS `:export` usage, use webpack mode:

```json
{
  "scripts": {
    "dev": "next dev --webpack",
    "build": "next build"
  }
}
```

Note: Build always uses webpack, so this only affects development.

**Solution 2: Migrate to CSS Custom Properties (Recommended)**

Replace SCSS `:export` with CSS custom properties for better compatibility:

```scss
// styles/colors.scss
$primary: #007bff;
$secondary: #6c757d;

:root {
  --color-primary: #{$primary};
  --color-secondary: #{$secondary};
}
```

```tsx
// Access via CSS or JavaScript
function Component() {
  const handleClick = () => {
    const primary = getComputedStyle(document.documentElement)
      .getPropertyValue('--color-primary')
  }

  return (
    <div style={{ color: 'var(--color-primary)' }}>
      Styled with CSS custom properties
    </div>
  )
}
```

**Solution 3: Create a TypeScript constants file**

```ts
// constants/colors.ts
export const colors = {
  primary: '#007bff',
  secondary: '#6c757d',
} as const

// Use in both SCSS and TypeScript
```

```scss
// styles/colors.scss
@use 'sass:meta';

$primary: #007bff;
$secondary: #6c757d;

// No :export needed - colors defined in TS
```

**Problem: TurboPack tree-shaking breaks some packages**

TurboPack can incorrectly tree-shake internal package code, causing runtime errors for libraries like antd or @ant-design/icons.

**Symptom:**

```
ReferenceError: _closableObj_closeIcon is not defined
```

**Solution: Add to transpilePackages**

```typescript
// next.config.ts
const nextConfig = {
  transpilePackages: ['antd', '@ant-design/icons'], // Add problematic packages

  experimental: {
    optimizePackageImports: [
      // Remove packages that break with optimization
      // 'antd', // Don't include here if in transpilePackages
    ],
  },
};

export default nextConfig;
```

**Other Turbopack incompatibilities:**

- Custom webpack loaders may not work
- Some webpack plugins are unsupported
- `webpack` property in `next.config.js` is ignored in dev mode

**Check Turbopack compatibility:**

```bash
# Run with verbose output to see warnings
next dev --turbo
```

If you see errors related to webpack features, add `--webpack` to your dev script as a temporary workaround while migrating the incompatible patterns.

**Problem: Empty turbopack config required when using webpack config**

In Next.js 16+, if you have a `webpack` property in your config, you must also include a `turbopack` property (even if empty). Otherwise, you'll see this error:

```
Error: The webpack config is being used without specifying a turbopack config.
Please add a turbopack config to your next.config.js file.
```

**Solution: Add empty turbopack config**

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    // Your webpack customizations
    return config
  },

  // Required placeholder when using webpack config in Next.js 16+
  turbopack: {},
}

module.exports = nextConfig
```

This tells Next.js you're aware that Turbopack exists and your webpack config is intentional. The empty object serves as an acknowledgment that you'll handle Turbopack compatibility separately (or use `--webpack` flag for development).

**Problem: Dynamic require() patterns**

Some libraries use dynamic `require()` patterns that Turbopack cannot statically analyze:

```js
// Libraries like woff2, sharp, or native bindings often do this
const binding = require('./build/' + process.platform + '/binding.node')
```

**Error you might see:**

```
Error: Cannot find module './build/darwin/binding.node'
Module not found: Can't resolve 'woff2'
```

**Solution: Use webpack mode**

For projects with complex native dependencies or dynamic requires:

```json
{
  "scripts": {
    "dev": "next dev --webpack",
    "build": "next build"
  }
}
```

**Libraries that commonly need webpack mode:**

- `woff2` / `woff2-bindings` (font compression)
- `sharp` (image processing, though often works)
- Native Node.js addons with dynamic loading
- Libraries using `require.context()` or dynamic `require()`

**Check if you need webpack mode:**

```bash
# Run dev and watch for module resolution errors
npm run dev

# If you see "Module not found" for native bindings,
# add --webpack to your dev script
```

**Note:** Production builds always use webpack, so this only affects the development experience. Once Turbopack matures, more of these patterns will be supported.
