# z.ai Sandbox Constraints

## Purpose

This document describes behaviors and limitations specific to the z.ai sandbox platform. These are not theoretical concerns — they cause real failures if ignored. Review this document before debugging, as many errors that appear to be code bugs are actually platform constraint violations.

**Note**: This file is platform-specific. For universal coding knowledge (architecture, conventions, error patterns), see `knowledge/universal/`.

---

## Sandbox Environment

| Situation | Expected Behavior | Actual Behavior | Why |
|-----------|------------------|-----------------|-----|
| User visits `localhost:3000` | User can access the dev server | User cannot access it — only the Preview Panel works | The sandbox exposes no raw ports to the user's browser |
| `bun run build` | Produces a production build | Not supported — only the dev server runs | The sandbox is a development environment with no production mode |
| Multiple ports exposed | Each service is individually accessible | Only one port exposed, routed via Caddy gateway | Caddy reverse-proxies all traffic through a single external port |
| Absolute API URL (`fetch('http://localhost:3001/api')`) | Request reaches the target service | Request fails — external access to internal ports is blocked | The gateway is the only entry point; absolute URLs bypass it |
| WebSocket direct connect (`io('ws://localhost:3003')`) | Socket connects to the service | Connection refused — direct port access is blocked | Same gateway constraint; WebSocket must route through Caddy |

---

## Gateway Routing

Caddy is the sole external entry point for all traffic. Internal services are never directly reachable from outside the sandbox.

### API Requests

```typescript
// [REQUIRED] correct — routes through Caddy
fetch('/api/users?XTransformPort=3001')

// [CRITICAL-ban] — will fail in sandbox
fetch('http://localhost:3001/api/users')
```

### WebSocket Connections

```typescript
// [REQUIRED] correct — routes through Caddy
const socket = io('/?XTransformPort=3003');

// [CRITICAL-ban] — will fail in sandbox
const socket = io('http://localhost:3003');
```

Why: Caddy proxies requests to internal services based on the `XTransformPort` query parameter. Absolute URLs bypass the proxy entirely.

---

## Next.js Specifics

| Constraint | Detail | Severity |
|------------|--------|----------|
| Single user-visible route | Users only see `/` — all UI must live in `src/app/page.tsx` | [REQUIRED] |
| No additional route files | Do not create `src/app/about/page.tsx` or similar — users cannot navigate to them | [REQUIRED] |
| Automatic dev server | `bun run dev` runs automatically — do not start it manually | [REQUIRED] |
| Dev log location | Check `/home/z/my-project/dev.log` for server errors and startup issues | [REQUIRED] |
| SDK placement | `z-ai-web-dev-sdk` must only be imported in server-side or API route code | [CRITICAL] |

---

## Filesystem

| Path | Behavior | Why |
|------|----------|-----|
| `/home/z/my-project/` | Project root — always use absolute paths | Relative paths can resolve incorrectly depending on the working directory |
| `/home/z/.stellar-trails-repo/` | Skill framework repo — has its own `.git/` | Git operations for stellar-trails MUST use `git -C $HOME/.stellar-trails-repo/` — never run bare `git` from parent |
| `skills/` | May be wiped on session reset | ZAI service auto-extracts from `/home/user_skills/stellar-trails.zip` (PolarFS persistent); `skills/` is re-populated each session |
| `download/` | May persist, but not guaranteed | Use `skills/` when persistence is required |
| `/tmp/` | Session-scoped — cleaned up between sessions | Temporary files are not safe for cross-session storage |

### Git Repository Isolation

`/home/z/my-project/` and `$HOME/.stellar-trails-repo/` are **separate git repositories**. They must never share git operations:

```
# [REQUIRED] stellar-trails git operations
git -C $HOME/.stellar-trails-repo/ <command>

# [BAN] never do this — operates on the parent repo, not the skill repo
git <command>   # from /home/z/my-project/ without -C
```

Consequences of violating this rule: the parent repo may have the same remote URL as the skill repo. A `git pull` or `git push` without `-C` will contaminate the parent's history with skill commits (or vice versa), causing rebase conflicts and commit loss. The parent repo has no remote configured as a safeguard.

---

## Prisma

| Constraint | Detail | Severity |
|------------|--------|----------|
| SQLite only | No MySQL or PostgreSQL — only the SQLite client is available | [CRITICAL] |
| Schema push | Use `bun run db:push` (not `bun run db:migrate`) | [REQUIRED] |
| Database client import | `import { db } from '@/lib/db'` | [REQUIRED] |
| Scalar types cannot be lists | Prisma scalar fields with `[]` are not supported in SQLite | [CRITICAL] |

---

## Common Pitfalls

The following are advisory items ordered by frequency of occurrence.

1. **Omitting `?XTransformPort=` on cross-service requests** [CRITICAL]
   Produces a "network error" or timeout that appears to be a code bug. Always include the query parameter when targeting a mini-service.

2. **Using `npm` instead of `bun`** [REQUIRED]
   Packages may install, but scripts and module resolution can behave differently. Always use `bun` for install and run commands.

3. **Creating new route files under `src/app/`** [REQUIRED]
   Users cannot navigate to additional routes. All UI must be rendered within the existing `/` route.

4. **Importing `z-ai-web-dev-sdk` in client components** [CRITICAL]
   The SDK contains server-side dependencies that fail at runtime or build time in client bundles. Restrict SDK usage to server actions and API routes.

5. **Assuming the filesystem persists between sessions** [REQUIRED]
   Only the `skills/` directory is guaranteed to survive session resets. Store important files there.
