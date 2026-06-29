# Architecture

## Purpose

This document describes the runtime environment, directory structure, service topology, and key constraints. Use this as the authoritative reference when making decisions about where code lives and how services communicate. Platform-specific overrides are in `knowledge/platform/`.

---

## Environment Overview

| Property | Value |
|----------|-------|
| OS | Linux container with limited package availability |
| Runtime | Bun (not Node.js) — use `bun` commands, not `npm` or `npx` |
| Framework | Next.js 16 with App Router (when building web apps) |
| Language | TypeScript 5 (strict mode) |
| Network | Single port exposed externally (Caddy gateway on port 80/443) |
| Database | SQLite via Prisma ORM |

---

## Directory Layout

```
/home/z/my-project/
  src/
    app/                    Next.js App Router pages
      page.tsx              Main page (only user-visible route)
    components/
      ui/                   shadcn/ui components (pre-installed)
    lib/                    Utility functions and configurations
    hooks/                  Custom React hooks
  prisma/
    schema.prisma           Prisma schema (SQLite)
  mini-services/            Standalone services (websocket, etc.)
  public/                   Static assets
  package.json              Dependencies
  dev.log                   Development server log
```

---

## Service Communication

All external traffic enters through the Caddy reverse proxy. Internal services run on separate ports but are not directly accessible from outside the sandbox.

```
User Browser
      |
      v
Caddy Gateway (port 80/443)
      |
      +-- / ----------------------> Next.js (port 3000)
      |
      +-- /?XTransformPort=3003 --> Mini Service (port 3003)
```

| Rule | Detail |
|------|--------|
| User sees only the `/` route | All UI must render through `src/app/page.tsx` |
| No production build | Only the dev server runs on port 3000 |
| Relative API paths only | Cross-service requests use `?XTransformPort=<port>` |
| SDK backend only | `z-ai-web-dev-sdk` must not be imported in client-side code |
| No localhost in output | Use the Preview Panel or the preview link for the user to see results |

---

## Key Principles

These principles summarize the constraints defined in `constraints/code-standards.md` and `constraints/type-safety.md`. They are repeated here for architectural context only — the authoritative definitions live in the constraints files.

1. **Type safety first** — no `any`, explicit returns, null-safe access
2. **Small, focused functions** — single responsibility, under 50 lines
3. **Named exports** — default exports reserved for page components
4. **Predictable imports** — strict ordering from framework to local types
5. **No silent failures** — every fallible function handles errors explicitly
