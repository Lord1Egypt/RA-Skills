# Advanced Auth and Permissions — Whop

Use this file only when the user is doing embedded apps, API automation, or permission-sensitive backend work. Most Whop business work does not need this layer first.

## Choose the Right Auth Mode

| Surface | Credential | Where it belongs | Notes |
|--------|------------|------------------|-------|
| Server-to-server REST | `Authorization: Bearer ...` | Backend requests to `https://api.whop.com/api/v1` | Official API accepts a company API key, company scoped JWT, app API key, or user OAuth token as bearer auth |
| Embedded Whop app iframe | `x-whop-user-token` | Requests from the Whop iframe to the app origin | Verify before trusting it; it is not a general API credential |
| Embedded web or mobile components | Short-lived access token from `POST /access_tokens` | Browser or mobile component initialization | Use for official embedded components instead of long-lived secrets |

## REST API Basics

- Base URL: `https://api.whop.com/api/v1`
- Security scheme: bearer auth
- Common scoping ID: `company_id`
- Common list pagination: `after`, `before`, `first`, `last`

```bash
curl -s https://api.whop.com/api/v1/companies \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

## Embedded App User Auth

Whop's iframe sends a JWT in the `x-whop-user-token` header on requests to the app's `window.location.origin`.

Use this mode when the request originates from an embedded app and the action depends on the current Whop user. Keep these rules tight:

- Reject missing or invalid `x-whop-user-token` headers
- Verify the token before reading claims
- Treat the header as user identity for the iframe request only
- Use normal bearer auth for background jobs, scheduled tasks, and generic REST automation

## Access Checks

Use `GET /users/{id}/access/{resource_id}` to confirm whether a user can access a company, product, or experience and to retrieve their access level.

```bash
curl -s "https://api.whop.com/api/v1/users/$WHOP_USER_ID/access/$WHOP_RESOURCE_ID" \
  -H "Authorization: Bearer $WHOP_API_KEY"
```

The response includes:
- `has_access`
- `access_level`

Treat access levels as increasing privilege:
- `view`
- `read`
- `write`
- `mod`
- `admin`

## Permissions Are Endpoint-Specific

The official API reference lists required permissions on each endpoint. Useful anchors from the published OpenAPI:

- `GET /products` requires `access_pass:basic:read`
- `GET /payments` requires `payment:basic:read` plus related plan, member, and promo scopes depending on the fields you need
- `GET /webhooks` requires `developer:manage_webhook`
- `GET /stats/describe`, `GET /stats/raw`, and `GET /stats/sql` require `stats:read`

Practical rule: never guess a scope name when the endpoint already documents it.

## Permission Lifecycle

When an embedded app needs new permissions:

1. Add the requested permissions in the app's settings
2. Install or re-approve the app for the target company
3. Expect old installs to keep failing until re-approval happens
4. Record which company has approved which permission set

Whop's permissions guide notes:
- Apps can request up to 100 permissions
- New permissions trigger a re-approval flow
- Creators can re-approve inside Authorized apps settings

For testing installs, the docs use this pattern:

```text
https://whop.com/apps/app_xxxxxxxxx/install
```

## OAuth and Access Tokens

Use OAuth when the integration needs delegated user access outside the embedded iframe path.

Use `POST /access_tokens` when official embedded components need a short-lived token. The OpenAPI describes this token as the credential for Whop web and mobile embedded components.

## Safe Defaults

- Keep bearer credentials and webhook secrets in env vars
- Separate sandbox permissions and installs from production
- If auth is ambiguous, choose the narrowest valid credential rather than the most powerful one
