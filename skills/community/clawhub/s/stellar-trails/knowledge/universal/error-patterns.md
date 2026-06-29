# Error Patterns

## Purpose

This document catalogs common errors encountered in the z.ai sandbox, with focus on platform-specific issues that are not obvious from the error message alone. Generic TypeScript and React errors are excluded — those are assumed knowledge.

For the structured error resolution workflow, see `procedure/decision-trees/error-resolution.md`.

---

## Network / Gateway Errors

### `ECONNREFUSED` / `fetch failed` [CRITICAL]

| Context | Cause | Fix |
|---------|-------|-----|
| API call to own service | Using absolute URL (`http://localhost:...`) | Change to relative path: `/api/...?XTransformPort=...` |
| WebSocket connection | Direct port connection | Change to `io('/?XTransformPort=...')` |
| External API call | No internet access or domain blocked | Use `z-ai-web-dev-sdk` on the server side |

### `XTransformPort` related errors [REQUIRED]

| Symptom | Cause | Fix |
|---------|-------|-----|
| Gateway timeout | Port number is incorrect or target service is down | Verify the service is running and the port matches |
| 502 Bad Gateway | Target service not started | Start the mini-service before making requests |
| Request routed to wrong service | Port collision between two services | Assign unique port numbers to each service |

### CORS errors [REQUIRED]

| Context | Cause | Fix |
|---------|-------|-----|
| API call returns a CORS block | Using absolute URL with `localhost` | Use a relative path — Caddy handles CORS internally |
| Cross-origin fetch to mini-service | Direct port reference in URL | Use `?XTransformPort=` to route through the same-origin gateway |

---

## Runtime Errors

### `Port 3000 already in use` [REQUIRED]

| Cause | Fix |
|-------|-----|
| Previous dev server process still running | Kill the process: `lsof -ti:3000 \| xargs kill` |

### `PrismaClient not generated` [REQUIRED]

| Cause | Fix |
|-------|-----|
| Schema changed but not pushed to the database | Run `bun run db:push` |
| First-time project setup | Run `bun run db:push` |

### `Module not found` (after adding a dependency) [REQUIRED]

| Cause | Fix |
|-------|-----|
| Package installed but not resolved in `node_modules` | Run `bun install` |
| Typo in package name | Verify the name in `package.json` |

### `Prisma unique constraint violation` [REQUIRED]

| Context | Cause | Fix |
|---------|-------|-----|
| `Unique constraint failed on the fields` | Attempting to insert a duplicate on a unique field | Use `upsert` or check existence with `findFirst` before inserting |

### `TypeError: Cannot read properties of undefined` [REQUIRED]

| Context | Cause | Fix |
|---------|-------|-----|
| Accessing a nested object property | Parent object is null or undefined | Use optional chaining (`obj?.prop?.nested`) or add an explicit null check |
| After a `fetch` / API call | Response shape differs from what was expected | Validate the response structure before accessing nested fields |

---

## Build / Dev Server Errors

### `Module not found` at build time [REQUIRED]

| Context | Cause | Fix |
|---------|-------|-----|
| Import path has incorrect casing | Linux filesystem is case-sensitive | Verify that the file name casing matches the import exactly |
| Barrel export missing | A newly created file was not added to `index.ts` | Add the export to the barrel file or use a direct import path |

### `SyntaxError: Unexpected token` [REQUIRED]

| Context | Cause | Fix |
|---------|-------|-----|
| Using JSX syntax in a `.js` file | The file extension must support JSX | Rename to `.tsx` |
| Importing CSS in a server component | CSS imports require a client component context | Move the CSS import to a client component or add the `'use client'` directive |

---

## WebSocket Errors

### `socket.io` connection failed [REQUIRED]

| Cause | Fix |
|-------|-----|
| Using a direct URL instead of gateway routing | Change to `io('/?XTransformPort=<port>')` |
| Target service not running | Start the mini-service first |
| Path is not `/` | The path must be `/` for Caddy to forward the request |

### WebSocket disconnects / reconnect loop [REQUIRED]

| Cause | Fix |
|-------|-----|
| Mini-service process crashed | Check the mini-service logs and restart it |
| Port mismatch between client and server | Verify that the same port is used in the `io()` call and the server's `listen()` call |

---

## Source Data Integrity

### Stale Local Data / Local-Remote Divergence [CRITICAL]

| Context | Cause | Fix |
|---------|-------|-----|
| Analyzing code that was modified in a previous session or by another contributor | Local clone not synchronized with remote before analysis began | Run `git fetch && git log origin/<branch> --oneline` to verify local matches remote. If behind, `git pull` or `git checkout <branch>` |
| Making claims about commit history, branch state, or code presence | Checked local refs only without verifying against remote | Always verify against `origin/<branch>` for any claim about what is or is not in the repository |
| Cross-session task where previous session pushed commits | Context compression summary does not carry forward exact git state | Perform Source State Verification as first action in SPECIFY |
| QA Attestation evidence based on file reads from stale checkout | Evidence is technically accurate (files were read) but fundamentally misleading (wrong version) | Evidence must include source state verification for any git-backed analysis task |

---

## Debug Flow

When encountering an error, follow this sequence:

1. Read the error message carefully — do not skim it. The message often contains the root cause.
2. Check the dev log at `/home/z/my-project/dev.log` — read the file directly to inspect recent errors and server output.
3. Determine whether this is a sandbox-specific issue:
   - Does it involve `localhost`, port numbers, `XTransformPort`, Prisma, or the SDK?
   - If yes: match against the patterns in this document and in `knowledge/platform/zai-sandbox.md`.
   - If no: apply standard debugging (type check, syntax review, logic trace).
4. If no pattern matches: isolate the error to the smallest possible reproduction and investigate from there.
