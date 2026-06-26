---
name: pocketbase-best-practices
description: PocketBase development best practices covering collection design, API rules, authentication, SDK usage, query optimization, realtime subscriptions, file handling, and deployment. Use when building PocketBase backends, designing schemas, implementing access control, setting up auth flows, or optimizing performance.
license: MIT
compatibility: Works with any agent. Requires PocketBase v0.36+.
metadata:
  author: community
  version: "1.2.0"
  repository: https://github.com/greendesertsnow/pocketbase-skills
  documentation: https://pocketbase.io/docs/
---

# PocketBase Best Practices

63 rules across 9 categories for PocketBase v0.36+, prioritized by impact.

## Categories by Priority

| Priority | Category | Impact | Rules |
|----------|----------|--------|-------|
| 1 | Collection Design | CRITICAL | coll-field-types, coll-auth-vs-base, coll-relations, coll-indexes, coll-view-collections, coll-geopoint |
| 2 | API Rules & Security | CRITICAL | rules-basics, rules-filter-syntax, rules-request-context, rules-cross-collection, rules-locked-vs-open, rules-strftime |
| 3 | Authentication | CRITICAL | auth-password, auth-oauth2, auth-otp, auth-token-management, auth-mfa, auth-impersonation |
| 4 | SDK Usage | HIGH | sdk-initialization, sdk-auth-store, sdk-error-handling, sdk-auto-cancellation, sdk-filter-binding, sdk-field-modifiers, sdk-send-hooks |
| 5 | Query Performance | HIGH | query-pagination, query-expand, query-field-selection, query-batch-operations, query-n-plus-one, query-first-item, query-back-relations |
| 6 | Realtime | MEDIUM | realtime-subscribe, realtime-events, realtime-auth, realtime-reconnection |
| 7 | File Handling | MEDIUM | file-upload, file-serving, file-validation |
| 8 | Production & Deployment | MEDIUM | deploy-backup, deploy-configuration, deploy-reverse-proxy, deploy-sqlite-considerations, deploy-rate-limiting, deploy-scaling |
| 9 | Server-Side Extending | HIGH | ext-go-setup, ext-js-setup, ext-hooks-chain, ext-hooks-record-vs-request, ext-routing-custom, ext-transactions, ext-filter-binding-server, ext-filesystem, ext-cron-jobs, ext-go-migrations, ext-js-migrations, ext-mailer, ext-settings, ext-testing, ext-compose-request-flow, ext-go-custom-sqlite, ext-jsvm-scope, ext-jsvm-modules |

## Quick Reference

### Collection Design (CRITICAL)
- **coll-field-types**: Use appropriate field types (json for objects, select for enums)
- **coll-auth-vs-base**: Extend auth collection for users, base for non-auth data
- **coll-relations**: Use relation fields, not manual ID strings
- **coll-indexes**: Create indexes on frequently filtered/sorted fields
- **coll-view-collections**: Use views for complex aggregations
- **coll-geopoint**: Store coordinates as json field with lat/lng

### API Rules (CRITICAL)
- **rules-basics**: Always set API rules; empty = public access
- **rules-filter-syntax**: Use @request.auth, @collection, @now in rules
- **rules-request-context**: Access request data via @request.body, @request.query; `@request.context` values: `default`/`oauth2`/`otp`/`password`/`realtime`/`protectedFile`
- **rules-cross-collection**: Use @collection.name.field for cross-collection checks
- **rules-locked-vs-open**: Start locked, open selectively
- **rules-strftime**: Use `strftime('%Y-%m-%d', created)` for date arithmetic (v0.36+)

### Authentication (CRITICAL)
- **auth-password**: Use authWithPassword for email/password login
- **auth-oauth2**: Configure OAuth2 providers via Admin UI
- **auth-otp**: Two-step `requestOTP` → `authWithOTP`; rate-limit requestOTP and never leak email existence
- **auth-token-management**: Store tokens securely, refresh before expiry
- **auth-mfa**: Enable MFA for sensitive applications
- **auth-impersonation**: Use impersonation for admin actions on behalf of users

### SDK Usage (HIGH)
- **sdk-initialization**: Initialize client once, reuse instance
- **sdk-auth-store**: Use AsyncAuthStore for React Native/SSR
- **sdk-error-handling**: Catch ClientResponseError, check status codes
- **sdk-auto-cancellation**: Disable auto-cancel for concurrent requests
- **sdk-filter-binding**: Use filter binding to prevent injection

### Query Performance (HIGH)
- **query-expand**: Expand relations to avoid N+1 queries
- **query-field-selection**: Select only needed fields
- **query-pagination**: Use cursor pagination for large datasets
- **query-batch-operations**: Batch creates/updates when possible

### Realtime (MEDIUM)
- **realtime-subscribe**: Subscribe to specific records or collections
- **realtime-events**: Handle create, update, delete events separately
- **realtime-auth**: Realtime respects API rules automatically
- **realtime-reconnection**: Implement reconnection logic

### File Handling (MEDIUM)
- **file-upload**: Use FormData for uploads, set proper content types
- **file-serving**: Use pb.files.getURL() for file URLs
- **file-validation**: Validate file types and sizes server-side

### Deployment (MEDIUM)
- **deploy-backup**: Schedule regular backups of pb_data
- **deploy-configuration**: Use environment variables for config
- **deploy-reverse-proxy**: Put behind nginx/caddy in production
- **deploy-sqlite-considerations**: Optimize SQLite for production workloads
- **deploy-rate-limiting**: Enable the built-in rate limiter (fixed-window as of v0.36.7); front with Nginx/Caddy for defense in depth
- **deploy-scaling**: Raise `ulimit -n` for realtime, set `GOMEMLIMIT`, enable settings encryption

### Server-Side Extending (HIGH)
- **ext-go-setup**: Use `app.OnServe()` to register routes; use `e.App` inside hooks, not the parent-scope app
- **ext-js-setup**: Drop `*.pb.js` in `pb_hooks/`; add `/// <reference path="../pb_data/types.d.ts" />`
- **ext-hooks-chain**: Always call `e.Next()`/`e.next()`; use `Bind` with an Id for later `Unbind`
- **ext-hooks-record-vs-request**: Use `OnRecordEnrich` to shape responses (incl. realtime); `OnRecordRequest` for HTTP-only
- **ext-routing-custom**: Namespace routes under `/api/{yourapp}/`; attach `RequireAuth()` middleware
- **ext-transactions**: Use the scoped `txApp` inside `RunInTransaction`; never capture the outer `app`
- **ext-filter-binding-server**: Bind user input with `{:name}` + `dbx.Params` in `FindFirstRecordByFilter` / `FindRecordsByFilter`
- **ext-filesystem**: `defer fs.Close()` on every `NewFilesystem()` / `NewBackupsFilesystem()` handle
- **ext-cron-jobs**: Register with `app.Cron().MustAdd(id, expr, fn)` / `cronAdd()`; stable ids, no `__pb*__` prefix
- **ext-go-migrations**: Versioned `.go` files under `migrations/`; `Automigrate: osutils.IsProbablyGoRun()`
- **ext-js-migrations**: `pb_migrations/<unix>_*.js` with `migrate(upFn, downFn)`; auto-discovered by filename
- **ext-mailer**: Resolve sender from `app.Settings().Meta` at send-time; never ship `no-reply@example.com`; create the mail client per send
- **ext-settings**: Read via `app.Settings()` at call time; set `PB_ENCRYPTION` (32 chars) to encrypt `_params` at rest
- **ext-testing**: `tests.NewTestApp(testDataDir)` + `tests.ApiScenario`; `defer app.Cleanup()`, assert `ExpectedEvents`
- **ext-compose-request-flow**: Composite walkthrough showing which app instance is active at each layer (route → tx → hook → enrich)
- **ext-go-custom-sqlite**: Only use `DBConnect` when you need FTS5/ICU; `DBConnect` is called twice (data.db + auxiliary.db)
- **ext-jsvm-scope**: Variables outside handlers are undefined at runtime — load shared config via `require()` inside the handler
- **ext-jsvm-modules**: Only CJS (`require()`) works in goja; bundle ESM first; avoid mutable module state

## Example Prompts

Try these with your AI agent to see the skill in action:

**Building a new feature:**
- "Design a PocketBase schema for an e-commerce app with products, orders, and reviews"
- "Implement OAuth2 login with Google and GitHub for my app"
- "Build a real-time notification system with PocketBase subscriptions"
- "Create a file upload form with image validation and thumbnail previews"

**Fixing issues:**
- "My list query is slow on 100k records -- optimize it"
- "I'm getting 403 errors on my batch operations"
- "Fix the N+1 query problem in my posts list that loads author data in a loop"
- "My realtime subscriptions stop working after a few minutes"

**Security review:**
- "Review my API rules -- users should only access their own data"
- "Set up proper access control: admins manage all content, users edit only their own"
- "Are my authentication cookies configured securely for SSR?"
- "Audit my collection rules for IDOR vulnerabilities"

**Going to production:**
- "Configure Nginx with HTTPS, rate limiting, and security headers for PocketBase"
- "Set up automated backups for my PocketBase database"
- "Optimize SQLite settings for a production workload with ~500 concurrent users"
- "Deploy PocketBase with Docker Compose and Caddy"

**Extending PocketBase:**
- "Add a custom Go route that sends a Slack notification after a record is created"
- "Write a pb_hooks script that validates an email domain before user signup"
- "Set up FTS5 full-text search with a custom SQLite driver in my Go app"
- "Share a config object across multiple pb_hooks files without race conditions"

## Detailed Rules

Load the relevant category for complete rule documentation with code examples:

- [Collection Design](references/collection-design.md) - Schema patterns, field types, relations, indexes
- [API Rules & Security](references/api-rules-security.md) - Access control, filter expressions, security patterns
- [Authentication](references/authentication.md) - Password auth, OAuth2, MFA, token management
- [SDK Usage](references/sdk-usage.md) - Client initialization, auth stores, error handling, hooks
- [Query Performance](references/query-performance.md) - Pagination, expansion, batch operations, N+1 prevention
- [Realtime](references/realtime.md) - SSE subscriptions, event handling, reconnection
- [File Handling](references/file-handling.md) - Uploads, serving, validation
- [Production & Deployment](references/production-deployment.md) - Backup, configuration, reverse proxy, SQLite optimization
- [Server-Side Extending](references/server-side-extending.md) - Go/JSVM setup, event hooks, custom routes, modules, custom SQLite
