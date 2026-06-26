---
title: Configure PostCSS
impact: LOW
impactDescription: Same configuration as CRA
tags: styling, postcss, configuration
---

## Configure PostCSS

PostCSS configuration in Next.js works the same as in CRA with a `postcss.config.js` file.

**CRA Pattern (before):**

```js
// postcss.config.js
module.exports = {
  plugins: {
    autoprefixer: {},
    'postcss-preset-env': {
      stage: 3,
      features: {
        'nesting-rules': true,
      },
    },
  },
}
```

**Next.js Pattern (after):**

```js
// postcss.config.js
module.exports = {
  plugins: {
    autoprefixer: {},
    'postcss-preset-env': {
      stage: 3,
      features: {
        'nesting-rules': true,
      },
    },
  },
}
```

**With Tailwind CSS:**

```js
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**Next.js default (no config needed):**

Next.js includes these by default:
- `autoprefixer`
- `flexbox-fixes`
- Modern CSS features (handled by SWC)

**Custom plugins:**

```bash
npm install postcss-import postcss-nesting
```

```js
// postcss.config.js
module.exports = {
  plugins: {
    'postcss-import': {},
    'postcss-nesting': {},
    autoprefixer: {},
  },
}
```

**Note:** If you create a `postcss.config.js`, you need to explicitly add all plugins including `autoprefixer` as the defaults are overridden.
