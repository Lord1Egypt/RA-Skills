---
title: Update ESLint for Next.js
impact: MEDIUM
impactDescription: Enables Next.js-specific linting
tags: setup, eslint, linting
---

## Update ESLint for Next.js

CRA includes ESLint via react-scripts. Next.js provides its own ESLint configuration with Next.js-specific rules.

**CRA ESLint (before):**

```json
// .eslintrc.json or in package.json
{
  "extends": ["react-app", "react-app/jest"]
}
```

**Next.js ESLint (after):**

```json
// .eslintrc.json
{
  "extends": ["next/core-web-vitals"]
}
```

**Or with additional configurations:**

```json
{
  "extends": [
    "next/core-web-vitals",
    "next/typescript"
  ],
  "rules": {
    // Custom rules
  }
}
```

**Run ESLint setup:**

```bash
npm run lint
# or
npx next lint
```

Next.js will prompt to set up ESLint on first run if no config exists.

**Key rules included in `next/core-web-vitals`:**
- Warns about missing `alt` on images
- Enforces `next/link` usage
- Prevents common React mistakes
- Web Vitals optimization hints
