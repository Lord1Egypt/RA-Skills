---
id: mcp-oauth
kind: asset
unlocks: [manus, chatgpt-apps]
source: https://modelcontextprotocol.io/specification/latest/basic/authorization (resolves to 2026-07-28), https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery.md (loaded 2026-11-08)
---
## Smallest version
Make the existing remote MCP server an OAuth 2.1 resource server only. Reuse the product's existing identity provider (or a hosted OAuth provider) as the authorization server; the MCP server just advertises it, rejects missing/invalid tokens with 401, and checks each token was issued for it. Do not build an authorization server unless the product has none.

## Scaffold
No official scaffold on the spec pages. Use the auth helpers of the MCP SDK the server already uses (delegate) or the hosting platform's OAuth provider (see mcp-remote).

## Fields the listings check
Spec version 2026-07-28. Authorization is OPTIONAL in MCP; when supported over HTTP:
- Protected Resource Metadata (RFC 9728) is a MUST. Document MUST include `authorization_servers` (at least one). Served at `/.well-known/oauth-protected-resource/<mcp path>` (e.g. `/.well-known/oauth-protected-resource/mcp`) or root `/.well-known/oauth-protected-resource`.
- 401 for missing/invalid/expired tokens, with `WWW-Authenticate: Bearer resource_metadata="https://<host>/.well-known/oauth-protected-resource", scope="<scopes>"` (scope SHOULD).
- 403 + `error="insufficient_scope"` for missing scopes; 400 for malformed requests.
- Token: `Authorization: Bearer <token>` on every request, never in the query string. Server MUST validate audience per RFC 8707 (token issued for this server's canonical URI, e.g. `https://mcp.example.com`, no trailing slash) and MUST NOT pass tokens through to upstream APIs.
- Authorization server MUST expose RFC 8414 `/.well-known/oauth-authorization-server` or OIDC `/.well-known/openid-configuration`; `issuer` must match exactly.
- Client registration: Client ID Metadata Documents SHOULD be supported; Dynamic Client Registration (RFC 7591) MAY, and is deprecated (kept for backwards compatibility); pre-registration is the third option.
- PRM `scopes_supported`: minimal scopes; SHOULD NOT include `offline_access`.

## Steps
claude: list the scopes the MCP tools need (read vs write) mapped to existing API permissions
human: in the identity provider, create the OAuth app/API audience for the MCP canonical URI and enable Client ID Metadata Documents or DCR; note issuer URL
claude: add the PRM route with `resource`, `authorization_servers`, `scopes_supported`
claude: add middleware: no/invalid token -> 401 with the `WWW-Authenticate` header above; verify signature, expiry, `aud`/resource = canonical URI; scope miss -> 403 insufficient_scope
claude: call the product API with the user's identity from the token, not by forwarding the MCP token
approve: deploy to the remote host
human: connect from a real client (Claude, ChatGPT developer mode) and complete the browser sign-in once

## Delegate
SDK auth wiring -> mcp-server-dev:build-mcp-server or anthropic-skills:mcp-builder. Middleware tests (401/403/audience) -> mattpocock-skills:tdd.

## Verify locally
`curl -i https://<host>/mcp` returns 401 with `resource_metadata=`; `curl https://<host>/.well-known/oauth-protected-resource/mcp` returns JSON with `authorization_servers`; `curl <issuer>/.well-known/oauth-authorization-server` returns matching `issuer`. Then MCP Inspector's OAuth flow completes (unconfirmed: Inspector OAuth UI not checked on an official page).
