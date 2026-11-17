---
id: openapi
kind: asset
unlocks: [make, rapidapi, postman, apis-guru]
source: https://fastapi.tiangolo.com/how-to/extending-openapi/, https://hono.dev/examples/zod-openapi, https://raw.githubusercontent.com/honojs/middleware/main/packages/zod-openapi/README.md, https://raw.githubusercontent.com/rswag/rswag/master/README.md, https://redocly.com/docs/cli/commands/lint (loaded 2026-11-08)
---
## Smallest version
One `openapi.yaml`/`openapi.json` (3.1 where the framework supports it) generated from the routes the product already serves, covering the public endpoints customers call with their API key, plus the security scheme. No new endpoints; no internal/admin routes.

## Scaffold
- FastAPI: built in. Served at `/openapi.json` (`openapi_url`); default `openapi_version` is `3.1.0`. Customize title/version/summary via `fastapi.openapi.utils.get_openapi(title=, version=, summary=, description=, routes=app.routes)` assigned to `app.openapi`.
- Hono: `npm i hono@4.13.18 zod@4.6.7 @hono/zod-openapi@1.6.3`; define routes with `createRoute` + `OpenAPIHono`; serve 3.1 with `app.doc31('/docs', { openapi: '3.1.0', info: { title, version } })` or get the object with `getOpenAPI31Document(config)`. (`app.doc` emits the 3.0 config shown on hono.dev.)
- Rails: rswag (`gem 'rswag'` or `rswag-api` + `rswag-ui` + `rswag-specs` in `:development, :test`), `rails g rswag:install`, write request specs, `rake rswag:specs:swaggerize` (alias `rake rswag`); output under `config.openapi_root` (e.g. `openapi/v1/openapi.json`). README documents OpenAPI 3.0 only; 3.1 output is unconfirmed.
- Express / Next.js: no official generator on the pages loaded (unconfirmed). Smallest path: hand-write the spec from the route files, or use Hono's underlying zod-to-openapi library if the routes already use zod (unconfirmed).

## Fields the listings check
`openapi` (version), `info.title`, `info.version`, `info.description`, `servers[].url` (public base URL), `paths` with `operationId`, `summary`, request/response schemas, `components.securitySchemes` + top-level `security`. Which fields each marketplace (Make, RapidAPI, Postman, APIs.guru) requires was not checked on their pages (unconfirmed).

## Steps
claude: list the public routes from the router and the API docs; exclude internal ones
claude: generate with the framework generator above (or hand-write), add `servers`, `securitySchemes` (apiKey header or bearer), an `operationId` and `summary` per operation
claude: export to `openapi.yaml` at the repo root (or `docs/`) so it is a committed file, not only a live route
claude: lint and fix until clean
approve: commit and publish it at a stable public URL (e.g. `https://<docs-domain>/openapi.yaml`)

## Delegate
Contract tests that the spec matches real responses -> mattpocock-skills:tdd.

## Verify locally
`npx @redocly/cli@2.78.0 lint openapi.yaml` (docs show `redocly lint <apis>...`; default ruleset `recommended`, stricter: `--extends=recommended-strict`; the `npx @redocly/cli@2.78.0` package invocation itself is unconfirmed on that page). FastAPI: `curl localhost:8000/openapi.json`.
