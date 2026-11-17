---
id: mcp-remote
kind: asset
unlocks: [smithery, glama, claude-connectors, vercel-connectors, zapier, manus, chatgpt-apps, hermes]
source: https://developers.cloudflare.com/agents/guides/remote-mcp-server/, https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel, https://smithery.ai/future, https://glama.ai/mcp/connectors, https://glama.ai/mcp/connectors/fyi.jotter/jot (loaded 2026-11-08)
---
## Smallest version
The same 2-5 API-wrapper tools as `mcp-server`, served over Streamable HTTP at one public HTTPS path (`/mcp` or `/api/mcp`) on a platform the product already deploys to. Auth: OAuth if any target listing needs it (chatgpt-apps, manus -> see `mcp-oauth`); otherwise a bearer API key in the `Authorization` header. Never take the key in the query string.

## Scaffold
- Cloudflare Workers (no existing host): `npm create cloudflare@2.74.11 -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless`; dev `npm start` (port 8788, endpoint `/mcp`); deploy `npx wrangler@4.161.0 deploy`. OAuth variant: an authorization-server Worker with `OAuthAuthorizationServer` + MCP handler wrapped in `OAuthResourceServer`; signed-in user via `getMcpAuthContext()`.
- Existing Next.js on Vercel (Node 20+): `npm i mcp-handler@2.1.1 @modelcontextprotocol/server@2.4.0 zod@4.6.7`; route `app/api/mcp/route.ts` with `createMcpHandler(server => server.registerTool(...))`, `export { handler as GET, handler as POST }`. Auth: `withMcpAuth(handler, verifyToken, { required: true, requiredScopes, resourceMetadataPath: '/.well-known/oauth-protected-resource' })` (401 without token, 403 on missing scope) and `protectedResourceHandler({ authServerUrls, resourceUrl })` at `app/.well-known/oauth-protected-resource/route.ts`. `mcp-handler` verifies tokens; it does not issue them.

## Fields the listings check
- Transport: Streamable HTTP (both docs); v2 `mcp-handler` dropped legacy HTTP+SSE.
- Unauthenticated request -> 401 (not 403) with `WWW-Authenticate` `resource_metadata` so OAuth discovery works (MCP spec; see mcp-oauth). The Smithery docs' 401-vs-403, `SmitheryBot/1.0` user agent and `/.well-known/mcp/server-card.json` (`serverInfo` required) guidance came only from a search snippet: the docs URLs now return 404 (unconfirmed).
- Smithery: per smithery.ai/future, on 2026-10-31 Smithery shut down its proxy, API, accounts/API keys, CLI and SDKs; smithery.ai continues as a non-proxied directory "powered by Arcade.dev". smithery.ai/new returns 404. How to get listed now is not documented (unconfirmed); contact listed on the page: ani@smithery.ai.
- Glama: connectors show Healthy/Unhealthy from periodic health checks and a tool-definition-quality letter grade (criteria not documented on the page, unconfirmed). "A test profile lets Glama authenticate for health checks and discover tools"; author flow: claim ownership, then Admin -> Test Profile. Claim proof via GitHub identity, an HTTP challenge JSON at `/.well-known/glama.json` on the connector origin, or DNS; this claim detail came from a search summary of listing pages, not a docs page (unconfirmed).

## Steps
claude: reuse the mcp-server tools; scaffold on the existing host (Vercel route) or Cloudflare template
claude: auth: read `Authorization: Bearer <YOUR_API_KEY>` and pass it to the product API, or wire OAuth per mcp-oauth; return 401 when missing
claude: write tool descriptions that say when to use each tool vs its siblings (Glama grades tool definitions)
human: create/choose the hosting account and set env secrets
approve: deploy (`npx wrangler@4.161.0 deploy` or git push to Vercel)
claude: add a `remotes[]` entry (`type` streamable-http (unconfirmed value), `url`) to server.json and republish to the MCP Registry (see mcp-server)
human: Glama: claim the connector, add a test profile with a test API key or OAuth sign-in

## Delegate
Tools -> mcp-server-dev:build-mcp-server or anthropic-skills:mcp-builder. Auth middleware tests -> mattpocock-skills:tdd.

## Verify locally
`npx @modelcontextprotocol/inspector@2.15.0` -> Streamable HTTP -> `http://localhost:3000/api/mcp` (or `:8788/mcp`) -> Connect -> List Tools -> call one. Then `curl -i -X POST https://<host>/mcp` without a token returns 401.
