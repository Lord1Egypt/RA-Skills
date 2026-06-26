---
name: tanstack-libraries
description: Use when users ask about TanStack libraries, TanStack Start/Router/Query/Table/Form/Virtual/Store/DB/Pacer/Config/DevTools/CLI/Intent/Hotkeys/AI usage, package names, framework adapters, maturity status, documentation URLs, installation methods, core APIs, code examples.
---

# TanStack Libraries

Headless, type-safe, framework-agnostic collection of web tooling libraries.

> **Need code examples or detailed features?** Read by category:
> - [Data & State](references/data-state.md) — Start / Router / Query / DB / Store / AI
> - [UI & UX](references/ui-ux.md) — Table / Form / Hotkeys
> - [Performance](references/performance.md) — Virtual / Pacer
> - [Tooling](references/tooling.md) — Devtools / Config / CLI / Intent

## Library Overview

### Stable

| Library | Core Package | Framework Adapters | Purpose |
|---|---|---|---|
| **Query** | `@tanstack/query-core` | react / vue / solid / svelte / angular / lit | Async state management, data fetching/caching/synchronization |
| **Router** | `@tanstack/router-core` | react / solid | Type-safe routing, Search Params, Loader+SWR caching |
| **Table** | `@tanstack/table-core` | react / vue / solid / svelte / angular / qwik / lit | Headless tables: sorting/filtering/pagination/grouping/aggregation |
| **Virtual** | `@tanstack/virtual-core` | react / vue / solid / svelte / angular / lit | Virtual scrolling (vertical/horizontal/grid) |
| **Config** | `@tanstack/config` | — | JS/TS package publishing toolchain (pnpm only) |

### RC

| Library | Core Package | Framework Adapters | Purpose |
|---|---|---|---|
| **Start** | `@tanstack/react-start` `@tanstack/solid-start` | react / solid | Full-stack framework: SSR/Streaming/Server Functions/RSC, built on Router+Vite |

### New

| Library | Core Package | Framework Adapters | Purpose |
|---|---|---|---|
| **Form** | `@tanstack/form-core` | react / vue / angular / solid / lit / preact | Headless form state management, nested fields, async validation |

### Beta

| Library | Package | Framework Adapters | Purpose |
|---|---|---|---|
| **DB** | `@tanstack/db` | react (runtime framework-agnostic) | Reactive client-side storage: Collections + Live Queries + Optimistic mutations |
| **Pacer** | `@tanstack/pacer` `@tanstack/pacer-lite` | react / solid | Debounce/throttle/rate-limit/queue/batching |
| **Store** | `@tanstack/store` | react / vue / angular / solid / svelte | Immutable reactive data store (internal TanStack core dependency) |

### Alpha

| Library | Package | Framework Adapters | Purpose |
|---|---|---|---|
| **AI** | `@tanstack/ai` `@tanstack/ai-client` `@tanstack/ai-react` `@tanstack/ai-solid` | react / solid + server | AI SDK: multi-Provider, tool calling, streaming, speech |
| **Hotkeys** | `@tanstack/hotkeys` | react / preact / solid / angular / vue / lit | Type-safe keyboard shortcuts, sequences, recording |
| **Devtools** | `@tanstack/devtools` and 7 other packages | react / vue / solid / preact | Unified DevTools panel, plugin system, source jumping |
| **CLI** | `@tanstack/cli` | — | Scaffold Start projects, Add-ons, MCP Server |
| **Intent** | `@tanstack/intent` | — | Publish Agent Skills via npm, auto-discovery, staleness detection |

## Core Design Principles

1. **Framework-agnostic** — Core libraries (`*-core`) → Framework adapters
2. **Headless** — Logic completely decoupled from UI, 100% control over markup and styling
3. **Type-safe** — First-class TypeScript support
4. **Lightweight** — Typically 10-15KB, tree-shakeable, zero dependencies
5. **No vendor lock-in** — Fully open source, self-funded