---
name: docyrus-api-dev
description: Develop applications using the Docyrus API with @docyrus/api-client and @docyrus/signin libraries. Use when building apps that authenticate with Docyrus OAuth2 (PKCE, iframe, client credentials, device code), make REST API calls to Docyrus data source endpoints, construct query payloads with filters, aggregations, formulas, pivots, and child queries, or integrate with external connectors (discover connectors, send requests through provider auth, run actions). Triggers on tasks involving Docyrus API integration, @docyrus/api-client usage, @docyrus/signin authentication, data source query building, Docyrus REST endpoint consumption, connector discovery, or external provider requests.
---

# Docyrus API Developer

Integrate with the Docyrus API using `@docyrus/api-client` (REST client) and `@docyrus/signin` (React auth provider). Authenticate via OAuth2 PKCE, query data sources with powerful filtering/aggregation, and consume REST endpoints.

## Authentication Quick Start

### React Apps — Use @docyrus/signin

```tsx
import { DocyrusAuthProvider, useDocyrusAuth, useDocyrusClient, SignInButton } from '@docyrus/signin'

// 1. Wrap root
<DocyrusAuthProvider
  apiUrl={import.meta.env.VITE_API_BASE_URL}
  clientId={import.meta.env.VITE_OAUTH2_CLIENT_ID}
  redirectUri={import.meta.env.VITE_OAUTH2_REDIRECT_URI}
  scopes={['offline_access', 'Read.All', 'DS.ReadWrite.All', 'Users.Read']}
  callbackPath="/auth/callback"
>
  <App />
</DocyrusAuthProvider>

// 2. Use hooks
function App() {
  const { status, signOut } = useDocyrusAuth()
  const client = useDocyrusClient()  // RestApiClient | null

  if (status === 'loading') return <Spinner />
  if (status === 'unauthenticated') return <SignInButton />

  // client is ready — make API calls
  const user = await client!.get('/v1/users/me')
}
```

### Non-React / Server — Use OAuth2Client Directly

```typescript
import { RestApiClient, OAuth2Client, OAuth2TokenManagerAdapter, BrowserOAuth2TokenStorage } from '@docyrus/api-client'

const tokenStorage = new BrowserOAuth2TokenStorage(localStorage)
const oauth2 = new OAuth2Client({
  baseURL: 'https://api.docyrus.com',
  clientId: 'your-client-id',
  redirectUri: 'http://localhost:3000/callback',
  usePKCE: true,
  tokenStorage,
})

// Auth Code flow
const { url } = await oauth2.getAuthorizationUrl({ scope: 'openid offline_access Users.Read' })
window.location.href = url
// After redirect:
const tokens = await oauth2.handleCallback(window.location.href)

// Create API client with auto-refresh
const client = new RestApiClient({
  baseURL: 'https://api.docyrus.com',
  tokenManager: new OAuth2TokenManagerAdapter(tokenStorage, async () => {
    return (await oauth2.refreshAccessToken()).accessToken
  }),
})
```

## API Endpoints

### Data Source Items (Dynamic per tenant)
```
GET    /v1/apps/{appSlug}/data-sources/{slug}/items          — List with query payload
GET    /v1/apps/{appSlug}/data-sources/{slug}/items/{id}     — Get one
POST   /v1/apps/{appSlug}/data-sources/{slug}/items          — Create
PATCH  /v1/apps/{appSlug}/data-sources/{slug}/items/{id}     — Update
DELETE /v1/apps/{appSlug}/data-sources/{slug}/items/{id}     — Delete one
DELETE /v1/apps/{appSlug}/data-sources/{slug}/items          — Delete many (body: { recordIds })
```

Endpoints exist only if the data source is defined in the tenant. Check the tenant's OpenAPI spec at `GET /v1/api/openapi.json`.

### System Endpoints (Always Available)
```
GET    /v1/users          — List users
POST   /v1/users          — Create user
GET    /v1/users/me       — Current user profile
PATCH  /v1/users/me       — Update current user
```

### Connector Discovery & External Request Endpoints
```
GET    /v1/connectors?q=&limit=&offset=                                    — List connectors with keyword search
GET    /v1/connectors/{dataProviderSlug}                                    — Get connector detail (dataSources + actions)
GET    /v1/connectors/{dataProviderSlug}/actions/{actionKey}                — Get action detail (input/output schemas, API endpoint)
GET    /v1/connectors/{dataProviderSlug}/connections                        — Get tenant connections + user connection status
PUT    /v1/connectors/{dataProviderSlug}                                    — Send HTTP request through connector provider auth
```

Scopes: `Read.All`, `ReadWrite.All`, or `Connectors.Read.All`. The `PUT` endpoint requires `ReadWrite.All`.

**PUT request body** for sending requests through a connector:
```json
{
  "endpoint": "relative/path/or/absolute-url",
  "requestMethod": "GET",
  "data": { "fields": "id,name", "limit": 20 },
  "contentType": "application/json",
  "headers": { "Authorization": "Bearer <override-token>" },
  "connectionId": "optional-tenant-connection-uuid",
  "connectionAccountId": "optional-connection-account-uuid"
}
```

The connector resolves auth credentials (OAuth tokens, base URL) from the provider configuration and stored connections. Custom `headers.Authorization` overrides the stored token.

### Action Run Endpoints
```
GET    /v1/apps/base/actions                                               — List base actions
GET    /v1/apps/{appSlug}/actions/{actionSlug}                             — Get action metadata
POST   /v1/apps/{appSlug}/actions/{actionSlug}/run                         — Run action directly
```

Action run accepts arbitrary JSON body as input. Optional headers: `x-connection-id`, `x-connection-account-id`.

### ACL / Role Management Endpoints
```
GET    /v1/users/acl?dataSourceId={uuid}&recordId={uuid}   — Read record ACL rows
POST   /v1/users/acl/share                                 — Upsert record shares
DELETE /v1/users/acl/share                                 — Revoke record shares
PUT    /v1/users/acl/owner                                 — Transfer record ownership

GET    /v1/users/acl/roles                                 — List roles
GET    /v1/users/acl/roles/{roleId}                        — Get one role
POST   /v1/users/acl/roles                                 — Create role
PATCH  /v1/users/acl/roles/{roleId}                        — Update role
DELETE /v1/users/acl/roles/{roleId}                        — Delete role

GET    /v1/users/acl/user-roles                            — List user-role assignments
GET    /v1/users/acl/users/{userId}/roles                  — List one user's roles
POST   /v1/users/acl/users/{userId}/roles                  — Add roles to a user
PUT    /v1/users/acl/users/{userId}/roles                  — Replace a user's full role set
DELETE /v1/users/acl/users/{userId}/roles/{roleId}         — Remove one role assignment

GET    /v1/users/acl/role-queries                          — List role queries
GET    /v1/users/acl/role-queries/{roleQueryId}            — Get one role query
POST   /v1/users/acl/role-queries                          — Create role query
PATCH  /v1/users/acl/role-queries/{roleQueryId}            — Update role query
DELETE /v1/users/acl/role-queries/{roleQueryId}            — Delete role query
```

ACL routes require the normal authenticated API session, but they may not appear in generated Swagger/OpenAPI output because the backend currently excludes them from public docs. Integrate them with direct `RestApiClient` calls when you need record sharing, role CRUD, user-role assignment management, or role-query management.

For all ACL role operations, prefer using role `uid` values returned by the API. Nested role objects expose both `id` and `uid`, and both map to the role UID value.

> To **configure** ACL (create roles, assign operation-level permissions, build role queries and an org hierarchy) use the **docyrus-acl-design** skill (`docyrus acl …`). The endpoints above are the runtime REST surface for app/frontend integration.

### Making API Calls

```typescript
// List items with query payload
const items = await client.get('/v1/apps/base/data-sources/project/items', {
  columns: 'name, status, record_owner(firstname,lastname)',
  filters: { rules: [{ field: 'status', operator: '!=', value: 'archived' }] },
  orderBy: 'created_on DESC',
  limit: 50,
})

// Get single item
const item = await client.get('/v1/apps/base/data-sources/project/items/uuid-here', {
  columns: 'name, description, status',
})

// Create
const newItem = await client.post('/v1/apps/base/data-sources/project/items', {
  name: 'New Project',
  status: 'status-enum-id',
})

// Update
await client.patch('/v1/apps/base/data-sources/project/items/uuid-here', {
  name: 'Updated Name',
})

// Delete
await client.delete('/v1/apps/base/data-sources/project/items/uuid-here')
```

## Query Payload Summary

The GET items endpoint accepts a powerful query payload:

| Feature | Purpose |
|---------|---------|
| `columns` | Select fields, expand relations `field(subfields)`, alias `alias:field`, spread `...field()` |
| `filters` | Nested AND/OR groups with 50+ operators (comparison, date shortcuts, user-related) |
| `filterKeyword` | Full-text search across all searchable fields |
| `orderBy` | Sort by fields with direction, including related fields |
| `limit`/`offset` | Pagination (default limit: 100) |
| `fullCount` | Return total matching count alongside results |
| `calculations` | Aggregations: count, sum, avg, min, max with grouping |
| `formulas` | Computed virtual columns (simple functions, block AST, correlated subqueries) |
| `childQueries` | Fetch related child records as nested JSON arrays |
| `pivot` | Cross-tab matrix queries with date range series |
| `expand` | Return full objects for relation/user/enum fields instead of IDs |

**For full query and formula references, read**:
- `references/data-source-query-guide.md`
- `references/formula-design-guide-llm.md`

## Critical Rules

1. **Always send `columns`** in list/get calls. Without it, only `id` is returned.
2. **Data source endpoints are dynamic** — they exist only for data sources defined in the tenant.
3. **Use `id` field** for `count` calculations. Use the actual field slug for `sum`, `avg`, `min`, `max`.
4. **Child query keys must appear in `columns`** — if childQuery key is `orders`, include `orders` in columns.
5. **Formula keys must appear in `columns`** — if formula key is `total`, include `total` in columns.
6. **Filter by related field** using `rel_{{relation_field}}/{{field}}` syntax.
7. **ACL routes may be hidden from generated OpenAPI** — call them directly via `RestApiClient` instead of expecting generated collection support.
8. **Prefer role `uid` values** for ACL role writes, user-role `roleIds`, and role-query `roleIds`.
9. **Treat `PUT /v1/users/acl/users/:userId/roles` as full replacement** and `POST /v1/users/acl/users/:userId/roles` as additive.
10. **Send role-query `query` as raw JSON** and let backend derive `tenantAppId` from `dataSourceId` when applicable.
11. **After deleting a role, refresh dependent ACL state** — role lists, user-role lists, role-query lists, and any UI showing primary-role labels.

## References

Read these files when you need detailed information:

- **`references/api-client.md`** — Full RestApiClient API, OAuth2Client (all flows: PKCE, client credentials, device code), token managers, interceptors, error classes, SSE/streaming, file upload/download, HTML to PDF, retry logic
- **`references/authentication.md`** — @docyrus/signin React provider, useDocyrusAuth/useDocyrusClient hooks, hasRole/hasPermission authorization helpers, SignInButton, standalone vs iframe auth modes, env vars, API client access pattern
- **`references/data-source-query-guide.md`** — Up-to-date query payload guide: columns, filters, orderBy, pagination, calculations, formulas, child queries, pivots, and operator reference
- **`references/formula-design-guide-llm.md`** — Up-to-date formula design guide for building and validating `formulas` payloads
