---
title: Migrate TypeScript Configuration
impact: HIGH
impactDescription: Required for TypeScript projects
tags: setup, typescript, tsconfig
---

## Migrate TypeScript Configuration

CRA's TypeScript setup differs from Next.js. Next.js will auto-generate a compatible `tsconfig.json` on first run.

**CRA tsconfig.json (before):**

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src"
  },
  "include": ["src"]
}
```

**Next.js tsconfig.json (after):**

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Key changes:**
- `jsx` changes from `react-jsx` to `preserve` (Next.js handles JSX transformation)
- `moduleResolution` uses `bundler` for better compatibility
- Add `next` plugin for enhanced type checking
- Path aliases use `@/*` pointing to root, not `src/`
- Include `next-env.d.ts` for Next.js types

## TypeScript Version Compatibility

The `moduleResolution: "bundler"` option requires TypeScript 5.0 or later.

**Check your TypeScript version:**

```bash
npx tsc --version
```

**For TypeScript 5.0+ (recommended):**

```json
{
  "compilerOptions": {
    "moduleResolution": "bundler"
  }
}
```

**For TypeScript 4.x projects (fallback):**

If you cannot upgrade TypeScript immediately, use `"node"` instead:

```json
{
  "compilerOptions": {
    "moduleResolution": "node"
  }
}
```

Note: `"node"` resolution works but may have subtle differences in how modules are resolved. Plan to upgrade to TypeScript 5.0+ for full compatibility.

**Explicit types array:**

If you encounter type resolution issues, explicitly declare the types to include:

```json
{
  "compilerOptions": {
    "types": ["node", "react", "react-dom", "jest"]
  }
}
```

This ensures TypeScript finds type definitions correctly, especially in monorepos or projects with complex dependency structures.
