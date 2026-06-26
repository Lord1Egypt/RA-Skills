# App SSO Integration Reference

Add Eve SSO login to Eve-deployed apps. Two shared packages -- `@eve-horizon/auth` (backend) and `@eve-horizon/auth-react` (frontend) -- handle token verification, org membership, and session management. The platform auto-injects the required environment variables.

**Related**: [SKILL.md](../SKILL.md) for quick start, Eve platform docs for SSO broker internals.

## Contents

- [Auto-Injected Environment Variables](#auto-injected-environment-variables)
- [Backend API (@eve-horizon/auth)](#backend-api-eveauth)
- [Frontend API (@eve-horizon/auth-react)](#frontend-api-eveauth-react)
- [Types](#types)
- [Verification Strategies](#verification-strategies)
- [Token Flow](#token-flow)
- [Session Bootstrap](#session-bootstrap)
- [Token Lifecycle](#token-lifecycle)
- [NestJS Integration](#nestjs-integration)
- [Custom Role Mapping](#custom-role-mapping)
- [Migration from Custom Auth](#migration-from-custom-auth)
- [Advanced Patterns](#advanced-patterns)

## Auto-Injected Environment Variables

Eve's deployer injects these into every deployed service:

| Variable | Description |
|----------|-------------|
| `EVE_API_URL` | Internal API URL for server-to-server calls |
| `EVE_PUBLIC_API_URL` | Public-facing API URL (optional) |
| `EVE_SSO_URL` | SSO broker URL |
| `EVE_ORG_ID` | Organization ID |
| `EVE_PROJECT_ID` | Project ID |
| `EVE_ENV_NAME` | Environment name |

For local development, set `EVE_SSO_URL`, `EVE_ORG_ID`, and `EVE_API_URL` manually. Use manifest interpolation for custom env vars:

```yaml
services:
  web:
    environment:
      MY_SSO_URL: "${SSO_URL}"
```

## Backend API (@eve-horizon/auth)

Install: `npm install @eve-horizon/auth`

### eveUserAuth(options?)

Express middleware. Verifies Eve RS256 tokens and checks org membership.

- **Non-blocking**: unauthenticated requests pass through. Use `eveAuthGuard()` to enforce.
- Attaches `req.eveUser: { id, email, orgId, role }` on success.
- Extracts tokens from `Authorization: Bearer` header or `?token=` query param.
- Options:
  - `orgId?: string` -- override `EVE_ORG_ID`
  - `eveApiUrl?: string` -- override `EVE_API_URL`
  - `strategy?: 'local' | 'remote'` -- JWKS verification (default) or HTTP verification

### eveAuthGuard()

Express middleware. Returns 401 if `req.eveUser` is not set. Place after `eveUserAuth()`.

### eveAuthConfig()

Express handler. Returns `{ sso_url, eve_api_url, eve_public_api_url, eve_org_id }` from environment variables. The frontend provider fetches this to discover SSO configuration.

### eveAuthMe(options?)

Express handler for `/auth/me`. Reads JWT claims directly (not `req.eveUser`) and returns the full response the React SDK expects — snake_case fields with org memberships and optional project role.

**Important**: Use this instead of returning `req.eveUser` directly. The `req.eveUser` object is camelCase and lacks memberships, which breaks the React SDK.

- Options:
  - `orgId?: string` -- override `EVE_ORG_ID`
  - `eveApiUrl?: string` -- override `EVE_API_URL`
  - `strategy?: 'local' | 'remote'` -- verification strategy
  - `projectHeader?: string` -- request header containing project ID (e.g. `'x-eve-project-id'`). When set, proxies to Eve API to resolve `project_role`.

```typescript
app.get('/auth/me', eveAuthMe({ projectHeader: 'x-eve-project-id' }));
```

### eveAuthMiddleware(options?)

Lower-level middleware for agent/job token verification. Attaches `req.agent` with full `EveTokenClaims`. Returns 401 on failure (blocking, unlike `eveUserAuth`).

- Options:
  - `eveApiUrl?: string` -- override `EVE_API_URL`
  - `strategy?: 'remote' | 'local'` -- HTTP (default) or JWKS verification

### verifyEveToken(token, eveApiUrl?)

Verify a token locally using JWKS (fetched and cached from Eve API). Faster for high-throughput scenarios. Returns `EveTokenClaims`.

### verifyEveTokenRemote(token, eveApiUrl?)

Verify a token by calling Eve API `/auth/token/verify` endpoint. Simplest approach -- no key management. Returns `EveTokenClaims`.

## Frontend API (@eve-horizon/auth-react)

Install: `npm install @eve-horizon/auth-react`

### EveAuthProvider

Context provider. Handles session bootstrap, token caching, SSO probing. Fetches `/auth/config` from the backend to discover SSO URL.

Props:
- `apiUrl?: string` -- backend base URL (default: `'/api'`)
- `projectId?: string` -- sends `X-Eve-Project-Id` header with `/auth/me` to resolve project role

```tsx
<EveAuthProvider apiUrl="/api" projectId={currentProjectId}>
  {children}
</EveAuthProvider>
```

### useEveAuth()

Hook returning `{ user, loading, error, config, orgs, activeOrg, switchOrg, loginWithSso, loginWithToken, logout }`.

- `user: { id, email, orgId, role, projectRole?, organizations? } | null`
- `orgs: EveAuthOrg[]` -- all org memberships
- `activeOrg: EveAuthOrg | null` -- currently selected org
- `switchOrg(orgId: string)` -- switch active org (persists in localStorage)
- `loginWithSso()` -- redirect to SSO broker login page
- `loginWithToken(token: string)` -- validate and store a pasted token
- `logout()` -- clear stored token and reset state

### EveLoginGate

Renders children when authenticated, login form otherwise.

Props:
- `fallback?: ReactNode` -- custom login component (defaults to `EveLoginForm`)
- `loadingFallback?: ReactNode` -- custom loading component (defaults to null)

### EveLoginForm

Built-in login UI with SSO and token paste modes. SSO button is disabled when `sso_url` is not configured.

### createEveClient(baseUrl?)

Fetch wrapper with automatic Bearer token injection. Returns `{ fetch, getToken }`.

```typescript
const client = createEveClient('/api');
const res = await client.fetch('/users');
```

### Token Storage

- `getStoredToken()` -- read cached token from `sessionStorage`
- `storeToken(token)` -- cache a token
- `clearToken()` -- clear cached token and reset state

## Types

```typescript
interface EveTokenClaims {
  valid: true;
  type: 'user' | 'job' | 'service_principal';
  user_id: string;
  email?: string;
  org_id?: string | null;     // Job tokens: single org
  orgs?: Array<{              // User tokens: all memberships
    id: string;
    role: string;
  }>;
  project_id?: string;
  job_id?: string;
  permissions?: string[];
  is_admin?: boolean;
  role?: string;
}

interface EveUser {
  id: string;
  email: string;
  orgId: string;
  role: 'owner' | 'admin' | 'member';
  projectRole?: 'owner' | 'admin' | 'member' | null;  // When project context available
}
```

`eveUserAuth()` attaches `EveUser` to `req.eveUser`. `eveAuthMiddleware()` attaches full `EveTokenClaims` to `req.agent`.

## Verification Strategies

| Strategy | Default for | Latency | Freshness |
|----------|-------------|---------|-----------|
| `'local'` | `eveUserAuth` | Fast (JWKS cached 15 min) | Stale up to 15 min |
| `'remote'` | `eveAuthMiddleware` | ~50ms per request | Always current |

The `'local'` strategy fetches `/.well-known/jwks.json` once and caches keys for 15 minutes. The `'remote'` strategy calls `/auth/token/verify` on every request. Override with the `strategy` option on either middleware.

## Token Flow

1. User visits app -- `EveAuthProvider` checks `sessionStorage` for cached token.
2. No cached token -- probes SSO broker `/session` endpoint (uses root-domain cookie).
3. SSO session exists -- gets fresh Eve RS256 token, caches in `sessionStorage`.
4. No SSO session -- shows login form (SSO redirect or token paste).
5. All API requests include `Authorization: Bearer <token>` header.

## Session Bootstrap

`EveAuthProvider` runs this sequence on mount:

1. Check `sessionStorage` for cached token
   - Verify expiry locally (skip network if expired)
   - Validate via `GET {apiUrl}/auth/me`
   - If valid: set user, done
2. Fetch `GET {apiUrl}/auth/config` to get `sso_url`
3. Probe `GET {sso_url}/session` with `credentials: 'include'`
   - If SSO cookie exists: get fresh token, cache, validate
4. Unauthenticated: `user = null`, `loading = false`

## Token Lifecycle

| Token | Storage | TTL | Refresh Path |
|-------|---------|-----|--------------|
| Eve RS256 access token | `sessionStorage` | 1 day (default) | Re-probe SSO `/session` |
| SSO refresh cookie | httpOnly cookie (root domain) | 30 days | GoTrue refresh |
| GoTrue refresh token | httpOnly cookie (SSO broker) | 30 days | Re-login |

When the cached access token expires, the bootstrap re-probes the SSO session. If the SSO refresh cookie is also expired, the user sees the login form. No manual token refresh logic needed in apps.

## NestJS Integration

The shared packages export Express middleware. For NestJS apps, apply `eveUserAuth()` globally in `main.ts` and use a thin guard wrapper:

```typescript
// main.ts
import { eveUserAuth } from '@eve-horizon/auth';
app.use(eveUserAuth());

// auth.guard.ts
@Injectable()
export class EveGuard implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest();
    if (!req.eveUser) throw new UnauthorizedException('Authentication required');
    return true;
  }
}

// auth-config.controller.ts
@Controller()
export class AuthConfigController {
  private handler = eveAuthConfig();

  @Get('auth/config')
  getConfig(@Req() req: Request, @Res() res: Response) {
    this.handler(req, res);
  }
}
```

## Custom Role Mapping

If your app uses roles beyond Eve's `owner/admin/member`, bridge them after `eveUserAuth()`:

```typescript
app.use((req, _res, next) => {
  if (req.eveUser) {
    req.user = {
      ...req.eveUser,
      appRole: req.eveUser.role === 'member' ? 'viewer' : 'admin',
    };
  }
  next();
});
```

## Migration from Custom Auth

Typical migration replaces ~700-800 lines of hand-rolled auth (JWKS setup, org check, role mapping, token caching, login form) with ~50 lines using the SDK.

**What to delete**: Custom JWKS/token verification, Bearer extraction middleware, auth config endpoint (SSO URL discovery), session probe logic, token storage helpers, login form component.

**What to keep**: App-specific role mapping beyond `owner/admin/member`, local password auth (not covered by the SDK), custom NestJS guard wrappers.

**Steps**:
1. Install `@eve-horizon/auth` (backend) and `@eve-horizon/auth-react` (frontend)
2. Replace backend auth stack with `eveUserAuth()` + `eveAuthGuard()` + `eveAuthConfig()`
3. Replace frontend auth with `EveAuthProvider` + `useEveAuth()` or `EveLoginGate`
4. Remove hardcoded SSO URL discovery hacks -- `eveAuthConfig()` reads auto-injected `EVE_SSO_URL`
5. Verify: `curl /auth/config` returns SSO config, `curl /auth/me -H "Authorization: Bearer $TOKEN"` returns user

## Project Role Resolution

The Eve API `/auth/me` endpoint accepts an optional `X-Eve-Project-Id` header. When present, it queries the `project_memberships` table and returns `project_role` (`'owner' | 'admin' | 'member' | null`).

**Backend**: Use `eveAuthMe()` with `projectHeader` to forward the header:

```typescript
app.get('/auth/me', eveAuthMe({ projectHeader: 'x-eve-project-id' }));
```

**Frontend**: Pass `projectId` to the provider:

```tsx
<EveAuthProvider apiUrl="/api" projectId={currentProjectId}>
```

**Access the role**: `user.projectRole` in `useEveAuth()`.

**Custom app roles**: Map platform roles to app-specific roles (e.g. `editor/viewer`) in middleware after `eveUserAuth()`. See the Custom Role Mapping section.

## Advanced Patterns

### SSE Authentication

The middleware supports `?token=` query parameter for Server-Sent Events:

```
GET /api/events?token=eyJ...
```

### Token Paste Mode

For development or headless environments, get a token from the CLI and paste it into the login form:

```bash
eve auth token  # prints Bearer token
```

### Token Staleness

The `orgs` claim in JWT tokens reflects membership at token mint time. With default 1-day TTL, membership changes take up to 24h to reflect. For immediate membership checks, use `strategy: 'remote'` in `eveUserAuth()`.
