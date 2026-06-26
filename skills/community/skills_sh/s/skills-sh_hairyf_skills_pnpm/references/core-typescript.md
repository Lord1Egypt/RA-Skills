---
name: pnpm-typescript
description: TypeScript integration—preserveSymlinks, @types workspace issues
---

# pnpm + TypeScript

## Do Not Preserve Symlinks

Don't use TypeScript's `preserveSymlinks: true`. It breaks type resolution in pnpm's linked `node_modules`. If you must preserve symlinks, set `nodeLinker=hoisted` in pnpm.

## @types/ Workspace Conflicts

Different versions of `@types/` in a workspace can cause errors when a package (e.g. `antd`) relies on types without declaring them in dependencies.

**Fix via packageExtensions:**

```yaml
# pnpm-workspace.yaml
packageExtensions:
  antd:
    peerDependencies:
      '@types/react': '*'
```

**Or use config dependency:**

```bash
pnpm add @pnpm/plugin-types-fixer --config
```

<!--
Source references:
- https://pnpm.io/typescript
-->
