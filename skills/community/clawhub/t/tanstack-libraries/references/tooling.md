# Tooling

> Devtools / Config / CLI / Intent

---

## Devtools (Alpha)

Unified DevTools panel (Solid.js), supports plugin system.

```bash
npm i -D @tanstack/react-devtools @tanstack/devtools-vite
```

```tsx
import { TanStackDevtools } from '@tanstack/react-devtools'
<TanStackDevtools plugins={[
  { name: 'Query', render: <ReactQueryDevtoolsPanel /> },
  { name: 'Router', render: <TanStackRouterDevtoolsPanel /> },
]} />
```

Packages: `@tanstack/devtools` (core Shell/plugin system) | framework adapters (react/vue/solid/preact-devtools) | `devtools-vite` (source inspection/production stripping) | `devtools-event-client/bus` (WebSocket/SSE)

Features: Plugin system and marketplace, source jumping, console piping, Picture-in-Picture (PiP)

---

## Config

JS/TS package publishing toolchain (pnpm only).

```bash
npm i -D @tanstack/config
pnpm exec tsc-build  # Typed build system, replaces tsc -b
```

Built-in: Build (Eslint/Prettier/esbuild/TypeScript), Testing (Vitest), Publishing (git tag + changelog + GitHub release)

---

## CLI (Alpha)

```bash
npm i -g @tanstack/cli
npx @tanstack/cli create   # Scaffold Start projects
```

Features: Add-ons extension system, MCP Server integration

---

## Intent (Alpha)

```bash
npm i -D @tanstack/intent
```

Publish Agent Skills via npm packages, with auto-discovery and staleness detection. `.intent/` directory manifest → `npx @tanstack/intent doctor` for diagnostics.