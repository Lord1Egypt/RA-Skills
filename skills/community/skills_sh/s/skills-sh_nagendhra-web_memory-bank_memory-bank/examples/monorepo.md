# Project Memory (Master Index)
Last updated: 2025-04-06 | Session 15 | Branch: main
Health: 6/10 (frontend stale, API fresh)

## Project Overview
SaaS project management (TaskFlow). Turborepo: Next.js frontend, Express API, shared packages. 4-person team. Post-beta, iterating toward GA.

## Domain Files
| Domain | File | Status | Updated |
|--------|------|--------|---------|
| Frontend | MEMORY-frontend.md | Stale (8d) | S11 |
| API | MEMORY-api.md | Fresh | S15 |
| Shared | MEMORY-shared.md | Current | S14 |

## Where We Left Off
- **Focus:** API team on GraphQL migration (S13-15)
- **Frontend:** Paused at S11, waiting for GraphQL API to stabilize
- **Next:** Complete Task mutations in `apps/api/src/graphql/resolvers/task.ts`, then wire frontend with Apollo Client

## Blockers
- Frontend can't switch to GraphQL until Task + Project + User queries/mutations all migrated. ETA: 2-3 sessions.

## Key Decisions
| Decision | Why |
|----------|-----|
| Turborepo over Nx | Simpler config, Vercel-native |
| REST -> GraphQL migration | Frontend needs flexible queries, REST over-fetching |
| Incremental migration | Can't afford full rewrite, REST + GraphQL coexist |
| Shared Zod schemas | Single source of truth for validation |

## Structure
```
apps/web/        -> Next.js 14 (Vercel)
apps/api/        -> Express + Apollo Server (Railway)
packages/shared/ -> Types, Zod schemas, utils
packages/ui/     -> Shared React components
packages/config/ -> ESLint, TS, Tailwind config
```

## Session Log
| S# | Date | Domain | Summary |
|----|------|--------|---------|
| 13 | 04-01 | API | Apollo Server setup, User resolvers |
| 14 | 04-03 | Shared | GraphQL type exports, Zod alignment |
| 15 | 04-06 | API | Project resolvers, started Task schema |
