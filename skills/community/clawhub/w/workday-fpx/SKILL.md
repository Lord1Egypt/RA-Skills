---
name: workday-fpx
description: >-
  Read Workday HR data (org chart, worker profiles, tasks, pay, benefits,
  compensation, your app menu) from a shell with the fpx CLI (@fetchproxy/cli)
  instead of running the workday-mcp server — fetch any *.htmld data endpoint through your own
  signed-in *.myworkday.com tab (SSO/Ping/Okta/Entra already cleared). Use
  when you want Workday data without the MCP, in a script, or on a machine
  where the MCP isn't installed.
---

# Workday via fpx (no MCP)

Workday employees have no personal API — the official REST/SOAP surface
needs a tenant-admin-registered OAuth client. The only usable surface is the
employee's own signed-in web session behind corporate SSO (Ping/Okta/Entra +
MFA). `fpx` routes the request through the user's already-authenticated
`*.myworkday.com` browser tab (the ContextMint Bridge extension), so a `*.htmld`
data endpoint that would otherwise bounce to the IdP returns clean JSON.

This is the same access the `workday_*` MCP tools use (a widget-tree JSON
response, parsed here with `jq` instead of `workday-mcp`'s TypeScript
parser), reached with one CLI call instead of a running server.

## One-time setup

```sh
npm install -g @fetchproxy/cli                # provides `fpx`
fpx profile add workday --domain myworkday.com # apex domain (per-tenant subdomain e.g. wd5)
fpx pair -p workday                            # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** extension installed (from
https://github.com/nullnet-app/contextmint-bridge/releases — Chrome: load the
chrome zip unpacked, after checking it against the `.sha256` beside it; Safari is
not available yet (it will ship inside the ContextMint app, which has no public
download link), so use Chrome for now — it is the fetchproxy browser extension
renamed, source public at https://github.com/nullnet-app/contextmint-bridge), an
open tab at `https://<host>/<tenant>` (e.g. `https://wd5.myworkday.com/acme`) with SSO
already completed, and the extension's Chrome **Site access** allowing
`myworkday.com`. Pairing persists — after the first approval every later
`fpx` call reuses it.

## Core call

Every read is a `GET` of a tenant-scoped `*.htmld` data endpoint. Send it raw
so stdout is the JSON body, ready for `jq`:

```sh
fpx get 'https://wd5.myworkday.com/acme/quickaccess/fetch.htmld?shouldFetchUpcApps=true' -p workday \
  | jq '[.. | objects | select(.widget=="configuredAppsItem") | {label, taskId: .taskIid}] | unique_by(.label)'
```

Ready-to-run endpoint paths (apps list, task/data-card read, worker profile +
its ~40-task drill-in catalog, org chart, grid tables, healthcheck probe) with
`jq` projection recipes are in `references/endpoints.md`. The
full widget-tree schema and gotchas are captured in the repo at
`docs/WORKDAY-API.md` — the operations here are the same live-verified
shapes `src/client.ts` / `src/tools/*.ts` use.

## Path rules (mirror `WorkdayClient.resolvePath`)

- **SPA routes are HTML, not data.** `/{tenant}/d/...` returns the app
  shell — never fetch it. If you copied a `/{tenant}/d/inst/....htmld` URL
  from your browser, drop the `/d/` segment to get the data endpoint:
  `/{tenant}/inst/....htmld`.
- **A bare task id resolves directly**: an id shaped like `2998$43525`
  (digits `$` alnum/`-`/`_`) is the constructable endpoint
  `/{tenant}/task/2998$43525.htmld` — no page-context token needed. Container
  / launcher task ids often return a near-empty shell; rich data needs the
  `cacheable-task` → `card/all` crawl below.
- **Data-card paths carry an opaque, page-context-bound token** (the
  `<pageCtx>` segment in `/{tenant}/card/all/<cardId>/<pageCtx>.htmld`) —
  it is NOT constructable. Get it from the parent `cacheable-task` response's
  own references, or by pasting the URL of the page you have open.
- A trailing `#fragment` on a copied URL is inert — strip it before fetching.

## Resolve-first rule

Call the apps list first (`quickaccess/fetch.htmld`, above) to discover a
`taskId`, or open the target page in your browser and copy its URL — then
fetch that specific task/card path. There's no search/id-lookup step here;
Workday's own navigation supplies the ids.

## Never dump the raw envelope — project fields only

Every `*.htmld` response's `root` envelope carries a **`sessionSecureToken`**
(and other envelope-internal fields) alongside the real data in `body`. The
`workday-mcp` parser (`src/parse.ts`) never emits it — it reads an explicit
allowlist only. Do the same here: **never pipe a response through bare
`jq '.'`** — always use one of the field-selecting filters in
`references/endpoints.md` (they select `text`/`moniker`/`configuredAppsItem`
widget nodes, never the envelope wholesale), so nothing secret rides into
your terminal or a script's output.

## Session-expiry tell

A stale SSO session bounces the fetch to the IdP instead of returning JSON.
Signs (`fpx` still exits `0` — Workday returns this as a 200):
- The response isn't JSON — it's an HTML login/SAML page (grep for
  `SAMLRequest`, `pingfederate`, or `Sign On to`).
- `fpx`'s reported final URL host differs from the tenant host (cross-origin
  redirect to the IdP).

Fix: open `https://<host>/<tenant>` in your browser, complete SSO, and
retry — there's no separate login step for `fpx`.

## Exit codes (fetch verbs)

- `0` — success (still check the body isn't an SSO/login page — see above).
- `2` — bridge unavailable: extension not connected or pairing pending →
  `fpx pair -p workday`, confirm a `myworkday.com` tab is open.
- `3` — bot wall (not expected on an internal SSO tenant, but the generic
  fpx contract).
- `4` — upstream non-2xx from Workday.

## Notes

- Read-only, and touches only your own data — this is the same surface the
  `workday_*` MCP tools read, not the official admin-only REST/SOAP API.
- `fpx health -p workday` shows bridge connection state when a call fails.
- Inbox/"My Tasks" and global search have no GET-able endpoint — they are served
  by the GraphQL surface (`/wday/pex/graphql/graphql?operation=...`, POST). See
  `references/endpoints.md` for what else was verified NOT GET-able, so you
  don't re-probe it.
- This project is developed and maintained by AI (Claude).
