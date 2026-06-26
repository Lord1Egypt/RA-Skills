# List query filters (`buildFilters`)

List endpoints that support filtering use a **fixed allowlist** of query parameter names. Anything not in the allowlist for that route is ignored. Pagination uses `limit` and `offset` on most list handlers.

## Where the code lives

Resolve paths from the **workspace root** (the folder that contains the `simpleerp-api` project), not from this skill folder:

| Artifact | Path |
|----------|------|
| Shared helper | `simpleerp-api/src/utils/queryFilters.js` |
| Per-resource allowlists | `simpleerp-api/src/routes/<resource>.js` (each file defines `FILTERS` or reads `req.query` manually) |

If the API repo is checked out elsewhere, substitute that root: `<your-simpleerp-api>/src/utils/queryFilters.js`.

**Scope:** Inspecting these source files is **optional** and only when a `simpleerp-api` tree is **already** present in the workspace. Do **not** enumerate the filesystem, open unrelated projects, or read secrets or arbitrary files under the guise of “workspace root.”

## What `buildFilters` does

`buildFilters({ query, allowedFilters, initialBinds, bindPrefix })` returns `{ whereSql, binds }` by walking **only** keys present in `allowedFilters` and in `query`. Supported per-filter options include:

- `column`, `op` (default `=`)
- `number`, `boolean`, `toUpper`, `nullable`
- `wrapLike`, `stripLikeWildcard` (for `LIKE` patterns)
- `customClause` (for non-standard SQL fragments, e.g. deliveries `orderId` + `REL_ENTITY`)

See the implementation in `queryFilters.js` for the full behavior.

## Related

- Allowlisted params per HTTP path: [ENDPOINTS.md](ENDPOINTS.md) and the **Dynamic list query filters** section in the parent skill file.
