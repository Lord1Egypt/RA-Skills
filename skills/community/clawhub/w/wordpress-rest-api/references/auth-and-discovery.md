# Auth And Discovery

Primary docs:

- Application Passwords integration guide: <https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/#basic-authentication-with-application-passwords>
- Authentication overview: <https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/>

## Route Discovery

Default route discovery flow:

1. request `GET /wp-json/`
2. inspect `namespaces`
3. inspect the `routes` object
4. send `OPTIONS` to a target route when you need methods, args, or schema hints

Use:

```bash
scripts/inspect-rest-api.sh --site https://example.com
scripts/inspect-rest-api.sh --site https://example.com --route /wp/v2/posts --method OPTIONS
```

## Authentication Models

### Application Passwords

Use this for remote automation that is not running inside an already-authenticated wp-admin browser session.

Properties:

- core-supported
- works over HTTPS
- usually sent with Basic Auth using the WordPress username plus application password
- best default for external automations, bridges, and API testing

Do not embed long-lived credentials into skill folders or publish packs.

### Cookie Plus Nonce

Use this for same-site or browser-admin flows where the caller is already logged in.

Common pattern:

- logged-in cookie
- `X-WP-Nonce` header

This is appropriate for admin UI integrations, not generic external service-to-service calls.

### Plugin Auth

JWT, OAuth, and custom headers are usually plugin-defined, not part of core REST auth.

Treat those as site-specific:

- inspect the plugin docs
- inspect the live routes
- inspect `permission_callback` server-side if you own the code

## Pagination And Response Shaping

For large collections:

- send `page` and `per_page`
- inspect `X-WP-Total`
- inspect `X-WP-TotalPages`
- trim payloads with `_fields`

Use `_embed` only when you actually need related objects in one response.

## Safe Discovery Rules

- start with `GET /wp-json/`
- do not assume `/wp/v2` is the only namespace
- use `OPTIONS` before write automations against unfamiliar routes
- assume plugin routes may enforce custom auth or custom required params
