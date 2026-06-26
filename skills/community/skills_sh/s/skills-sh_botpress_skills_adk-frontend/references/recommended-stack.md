# Recommended Tech Stack for ADK Frontends

## Overview — Why This Stack?

This tech stack is production-proven and represents the modern React ecosystem. It prioritizes:

- **Performance**: Vite for lightning-fast builds, React 19 with compiler optimizations
- **Type Safety**: TypeScript strict mode + TanStack Router's type-safe routing
- **Developer Experience**: Hot module replacement, autocomplete everywhere, minimal boilerplate
- **Maintainability**: Small, focused libraries with clear separation of concerns
- **ADK Integration**: First-class support for @botpress/client and generated types

This is the **recommended starting point** for building frontends that interact with ADK agents.

---

## Core Dependencies

### Build Tool: Vite

**Why Vite?**

- **Instant server start**: No bundling in development, uses native ES modules
- **Lightning-fast HMR**: Updates reflect in <50ms without losing state
- **Optimized builds**: Rollup-based production builds with automatic code splitting
- **React 19 support**: First-class support for React Compiler

**Why NOT Next.js or Create React App?**

- Next.js is overkill if you don't need SSR/SSG (ADK frontends are typically SPAs talking to bot APIs)
- CRA is deprecated and slower than Vite
- Vite gives you modern tooling without framework lock-in

---

### Framework: React 19

**Why React 19?**

- **React Compiler**: Automatic memoization — no more `useMemo`/`useCallback` everywhere
- **Actions**: Built-in form handling with pending states
- **Improved performance**: Faster reconciliation, smaller bundle sizes
- **Forward compatibility**: Long-term support, ecosystem stability

**Critical for ADK Integration**:

- Real-time updates (via TanStack Query) benefit from automatic batching
- Streaming responses from bots can leverage Suspense and concurrent rendering

---

### TypeScript (Strict Mode)

**Why TypeScript?**

- **Botpress API types**: `@botpress/client` provides full TypeScript definitions
- **Generated types**: ADK generates action/table types via `.adk/` (see [Type Generation](./type-generation.md))
- **TanStack Router**: Type-safe routing with autocomplete for routes/params
- **Catch bugs early**: Schema mismatches caught at compile time

---

## Routing: TanStack Router

**Why TanStack Router?**

- **Type-safe routing**: Routes, params, search params all have TypeScript types
- **File-based**: Define routes in `/routes` folder, auto-generated route tree
- **Built-in loaders**: Fetch data before rendering
- **Search param state**: Use URL as state store (shareable links, back button works)

**Why NOT React Router?**

- React Router lacks type safety (you cast `useParams()` manually)
- TanStack Router's loaders prevent waterfall requests
- Better DX with autocomplete for route names

**Critical Plugin Setup**:

```typescript
// vite.config.ts — plugin order matters!
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'
import react from '@vitejs/plugin-react'

export default {
  plugins: [
    TanStackRouterVite(), // MUST be before React plugin
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler', {}]],
      },
    }),
  ],
}
```

**Example Route**:

```typescript
// routes/chat.$ticketId.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/chat/$ticketId')({
  loader: async ({ params }) => {
    return fetchTicket(params.ticketId) // params.ticketId is typed!
  },
  component: ChatPage,
})
```

---

## Data Fetching: TanStack Query

**Why TanStack Query?**

- **Server state management**: Cache, invalidate, refetch, background updates
- **Automatic retries**: Network failures handled gracefully
- **Optimistic updates**: Update UI immediately, rollback on error
- **Devtools**: Inspect queries, cache, and network activity

**Why NOT SWR or Apollo?**

- SWR is simpler but less powerful (no mutation helpers, manual cache invalidation)
- Apollo is GraphQL-specific
- TanStack Query works with any async function — perfect for `@botpress/client` calls

**Example: Fetching Bot Data**:

```typescript
import { useQuery } from '@tanstack/react-query'

function useTickets(botId: string) {
  return useQuery({
    queryKey: ['tickets', botId],
    queryFn: () => listTickets({ state: 'open' }),
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}
```

---

## State Management: Zustand

**Why Zustand?**

- **Simple**: No boilerplate, no providers, no reducers
- **Lightweight**: ~1KB gzipped
- **React integration**: Hooks-based, automatic re-renders
- **Middleware**: Persist, devtools, immer built-in

**When to Use Zustand (ADK-specific)**:

- **Client management**: Caching Botpress client instances (see [Botpress Client](./botpress-client.md))
- **UI state**: Sidebar open/closed, selected theme, active tab
- **Client-side only state**: File uploads, multi-step wizards

**When NOT to Use Zustand**:

- **Server state**: Use TanStack Query instead (bot tables, actions)
- **URL state**: Use TanStack Router search params (filters, pagination)

---

## ADK-Specific Libraries

### @botpress/client

**Required for all ADK frontends.** Provides TypeScript client for Botpress Cloud APIs.

```typescript
import { Client } from '@botpress/client'

const client = new Client({
  token: import.meta.env.VITE_BOTPRESS_TOKEN,
  botId: import.meta.env.VITE_BOT_ID,
  workspaceId: import.meta.env.VITE_WORKSPACE_ID,
  apiUrl: 'https://api.botpress.cloud',
})

// Call bot actions
const result = await client.callAction({
  type: 'lookupOrder',
  input: { orderId: 'ORD-12345' },
})

// Query bot tables
const { rows } = await client.findTableRows({
  table: 'OrdersTable',
  filter: { status: 'pending' },
})
```

> **Tip:** The ADK generates `.adk/client.ts` with a `createAdkClient` function that wraps `@botpress/client` with fully typed action methods.

### Generated Types

ADK generates TypeScript definitions in `.adk/` during `adk dev`. Your frontend imports these via triple-slash references:

```typescript
/// <reference path="../../../bot/.adk/action-types.d.ts" />
import type { BotActionDefinitions } from '@botpress/runtime/_types/actions'
import type { TableDefinitions } from '@botpress/runtime/_types/tables'
```

See [Type Generation](./type-generation.md) for the complete setup.

---

## UI Components: Radix UI + Tailwind CSS

### Radix UI

**Why Radix UI?**

- **Unstyled primitives**: You control CSS (via Tailwind), Radix handles behavior
- **Accessible by default**: ARIA attributes, keyboard navigation, screen reader support
- **Composable**: Build complex components from primitives
- **No runtime CSS**: Unlike Material-UI, no CSS-in-JS overhead

### Tailwind CSS

**Why Tailwind?**

- **Utility-first**: No context switching between HTML and CSS files
- **Zero runtime cost**: Build-time only
- **Design system**: Consistent spacing, colors, typography via theme
- **Tiny production bundles**: Unused styles purged automatically

**Setup with Vite**:

```typescript
// vite.config.ts
import tailwindcss from '@tailwindcss/vite'

export default {
  plugins: [tailwindcss()],
}
```

---

## Utility Libraries

| Library                    | Purpose                                       |
| -------------------------- | --------------------------------------------- |
| `lucide-react`             | Modern icon set (1000+ icons, tree-shakeable) |
| `clsx`                     | Conditionally join class names                |
| `tailwind-merge`           | Resolve conflicting Tailwind classes          |
| `class-variance-authority` | Type-safe component variants                  |
| `date-fns`                 | Date formatting/manipulation (tree-shakeable) |
| `sanitize-html`            | XSS protection for user-generated HTML        |
| `zod`                      | Schema validation in frontend context         |
| `use-stick-to-bottom`      | Auto-scroll in chat interfaces                |
| `@formkit/auto-animate`    | Automatic list/element animations             |

---

## Quick Start Template

```bash
# Create Vite project
pnpm create vite@latest my-bot-frontend --template react-ts
cd my-bot-frontend

# Install core dependencies
pnpm add @botpress/client \
  @tanstack/react-query @tanstack/react-router \
  zustand zod \
  tailwindcss @tailwindcss/vite \
  @radix-ui/react-dialog @radix-ui/react-dropdown-menu \
  lucide-react clsx tailwind-merge class-variance-authority \
  date-fns sanitize-html

# Install dev dependencies
pnpm add -D @tanstack/router-plugin babel-plugin-react-compiler \
  @types/node @types/react @types/react-dom @types/sanitize-html \
  typescript @vitejs/plugin-react

# Setup TanStack Router
mkdir src/routes
touch src/routes/__root.tsx src/routes/index.tsx

# Setup Tailwind
echo "@import 'tailwindcss';" > src/index.css
```

**Configure Vite** (`vite.config.ts`):

```typescript
import { defineConfig } from 'vite'
import path from 'path'
import react from '@vitejs/plugin-react'
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    TanStackRouterVite(),
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler', {}]],
      },
    }),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

**Configure environment** (`.env`):

```bash
VITE_BOT_ID=your_bot_id
VITE_WORKSPACE_ID=your_workspace_id
```

**Start developing:**

```bash
pnpm dev
```

---

## Alternative Approaches

### Using Next.js App Router

**When to use**: SEO-critical pages, server-side rendering, API routes.

**Trade-offs**:

- More complexity (server vs client components, async RSC)
- Larger framework, more abstraction
- Overkill for most ADK dashboards (SPAs)

### Using Vue 3 or Svelte

**When to use**: Team preference, smaller bundle size.

**Trade-offs**:

- Botpress libraries are built for React
- TanStack Query has Vue/Svelte adapters
- Smaller ecosystem for ADK-specific patterns

---

## Summary

This stack is **production-proven**, **type-safe**, and **optimized for ADK integration**:

| Layer     | Choice                             | Why                                    |
| --------- | ---------------------------------- | -------------------------------------- |
| Build     | Vite                               | Instant dev, fast builds               |
| Framework | React 19                           | Compiler, ecosystem, ADK support       |
| Types     | TypeScript strict                  | Generated types, compile-time safety   |
| Routing   | TanStack Router                    | Type-safe routes, loaders              |
| Data      | TanStack Query                     | Cache, polling, mutations              |
| State     | Zustand                            | Client management, UI state            |
| UI        | Radix UI + Tailwind                | Accessible, unstyled, zero-runtime CSS |
| ADK       | @botpress/client + generated types | Full type-safe bot integration         |

**Start here**, customize as needed. Follow the other guides in this series for specific implementation patterns.

---

## See Also

- **[Project Setup](./project-setup.md)** — Scaffolding with this stack
- **[Botpress Client](./botpress-client.md)** — Client initialization and management
- **[Type Generation](./type-generation.md)** — Setting up generated types
- **[Data Fetching](./data-fetching.md)** — TanStack Query patterns
- **[Service Layer](./service-layer.md)** — Building the service abstraction
- **[Overview](./overview.md)** — Architecture and when to use this pattern
