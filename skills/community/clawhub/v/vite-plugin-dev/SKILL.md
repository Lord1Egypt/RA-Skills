---
name: vite-plugin-dev
description: >
  Use when developing Vite plugins: scaffolding plugin structure, implementing
  hooks (transform, resolveId, load, buildStart, etc.), handling virtual modules,
  HMR integration, SSR compatibility, and publishing to npm. Covers Vite 5/6 plugin API.
---

# Vite Plugin Development

## When to Use
- Building a custom Vite plugin from scratch
- Implementing transform/resolve hooks for special file types
- Creating virtual modules or runtime injections
- Adding HMR (Hot Module Replacement) support
- Making plugins SSR-compatible
- Publishing a plugin package to npm

## Core Workflow

### 1. Plugin Scaffold
Every Vite plugin is a factory function returning a plugin object:
```ts
import type { Plugin } from 'vite'

export interface MyPluginOptions {
  include?: string | RegExp | (string | RegExp)[]
  exclude?: string | RegExp | (string | RegExp)[]
}

export default function myPlugin(options: MyPluginOptions = {}): Plugin {
  return {
    name: 'vite-plugin-my',          // required, unique name
    enforce: 'pre',                   // 'pre' | 'post' | undefined
    apply: 'build',                   // 'build' | 'serve' | ((config, env) => bool)

    // lifecycle hooks below...
  }
}
```

### 2. Key Hooks

| Hook | Phase | Purpose |
|------|-------|---------|
| `config` | Both | Modify resolved config |
| `configResolved` | Both | Read final config |
| `buildStart` | Both | Initialize plugin state |
| `resolveId` | Both | Custom module resolution |
| `load` | Both | Custom module content |
| `transform` | Both | Code transformation |
| `generateBundle` | Build | Post-process output |
| `configureServer` | Serve | Extend dev server |
| `handleHotUpdate` | Serve | Custom HMR logic |

### 3. Transform Hook Pattern
```ts
transform(code, id) {
  if (!id.endsWith('.myext')) return null  // return null = skip
  const transformed = doTransform(code)
  return {
    code: transformed,
    map: null,  // provide sourcemap when possible
  }
},
```

### 4. Virtual Modules
```ts
const VIRTUAL_ID = 'virtual:my-module'
const RESOLVED_ID = '\0' + VIRTUAL_ID   // prefix \0 to avoid collisions

resolveId(id) {
  if (id === VIRTUAL_ID) return RESOLVED_ID
},
load(id) {
  if (id === RESOLVED_ID) {
    return `export const data = ${JSON.stringify(myData)}`
  }
},
```

### 5. HMR Support
```ts
handleHotUpdate({ file, server }) {
  if (file.endsWith('.myext')) {
    server.ws.send({ type: 'full-reload' })
    return []  // prevent default HMR
  }
},
```

### 6. SSR Compatibility Checklist
- Check `options.ssr` in `transform` / `load` hooks
- Avoid browser-only APIs at transform time
- Mark side-effect-free modules: set `moduleSideEffects: false`
- Test with `vite build --ssr`

### 7. Testing Strategy
```ts
// Use vite's createServer for integration tests
import { createServer } from 'vite'
const server = await createServer({ plugins: [myPlugin()] })
const mod = await server.ssrLoadModule('/src/test.myext')
```

## Publishing Checklist
- [ ] `package.json` `main` + `module` + `types` fields set
- [ ] `peerDependencies`: `"vite": "^5.0.0 || ^6.0.0"`
- [ ] README with usage example + options table
- [ ] Export TypeScript types
- [ ] Test against Vite 5 and 6
- [ ] `vite-plugin-` prefix in package name (ecosystem convention)
