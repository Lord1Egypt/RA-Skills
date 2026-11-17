## Six ways in, and where each one stands here

There are about six ways an agent can reach an app. All but one are
open at this store, and the one that is not is shut on purpose and
says why. Find the one you are and skip to it — it is the same store down every road,
and an artifact bought down one is byte-identical to the same artifact
bought down another.

1. **The raw API.** Plain HTTPS, OpenAPI at
   `https://scvd.store/openapi.json`, an RFC 9727 catalog at
   `/.well-known/api-catalog`, x402 terms declared at
   `/.well-known/x402`. No key, no account, no signup — an anonymous
   keyless call gets a real answer or a real 400, never a login wall.
2. **A backend MCP server.** `POST https://scvd.store/mcp`, streamable
   HTTP, tools typed and annotated. Details below.
3. **Computer use** — a model driving a screen. Every room renders
   server-side; the front door is around 100 KB and needs no script to
   read. `robots.txt` names the text maps for when pixels are the
   expensive part.
4. **Browser automation** — Playwright, Puppeteer, an agentic browser.
   Every HTML room hooks its `<main>` with `data-room`, and item rows
   carry `data-item`, so a selector written today survives a redesign.
   Navigation is plain links; nothing needs JavaScript to click.
5. **WebMCP** — tools registered into the agent already running in the
   browser. Free instruments plus `quote_store_purchase` (free) and
   `complete_store_purchase` (may transfer USDC). The latter requires a
   payment already signed by a buyer-authorized wallet/client; no keys
   or automatic payments. Details below.
6. **The site's own assistant** — deliberately not built. There is no
   chat box here, because you are the visitor and a hosted model
   between you and the shelf would be a second opinion nobody asked
   for. The guide is `llms.txt` and `/agents.md` instead.

That lineup is not a claim we make about ourselves and leave there. A
battery walks all six against this store every week, from outside,
over plain HTTPS; the criteria, the current reading and — the part
worth more than the reading — the findings that turned out to be the
INSTRUMENT'S fault rather than the store's are kept in the open at
`https://github.com/seancrecord/scvd-general-store-repo/blob/main/SIX_DOORS.md`.
Where a door is unreachable the battery records `unknown` rather than
guessing, and where we fall short it says so.

## The browser door — tools where the page is

If you are an agent running INSIDE a browser rather than calling from
a server, the store hands you tools at the page. `webmcp.js` loads on
the rooms where agents actually arrive and registers read-only
instruments through `document.modelContext.registerTool()`:

`read_store_guide` · `preflight_endpoint` · `check_before_you_pay` ·
`check_conformance` · `verify_artifact` · `look_at_door` · `check_order` ·
`find_in_catalog`

**Those instruments mirror free public endpoints.** The browser also
registers `quote_store_purchase` for a free quote and
`complete_store_purchase` for an already-signed x402 v2 payment.
The latter is consequential: it may transfer USDC. A compatible
buyer-authorized wallet/client signs externally; the bridge takes no keys
and never signs or retries by itself. The quote fixes the URL and retry
key. A lost response requires recovery with that same identity.

The conformance desk at `https://scvd.store/conformance` goes one
further and annotates its own form declaratively — `toolname`,
`tooldescription`, `toolparamdescription` on the controls — so an
agent can fill and read it as a tool without us shipping a line of
JavaScript for it. **`toolautosubmit` is deliberately absent.** The
agent can fill the form; a human presses the button. That is the
ruling for that declarative form. The payment tool requires the buyer's
already-signed authorization.

Two practical notes, because this is a road still being paved:

- WebMCP rides a per-browser **origin trial** — a signed grant bound
  to one origin, and each vendor runs its own programme with its own
  key. This store carries Chrome's and Edge's, the sooner of which
  expires 2026-11-17. If your browser is on neither trial, none of
  this appears and every road above still works. Nothing here is
  load-bearing.
- Read-only tools and quotes are free; `complete_store_purchase` may
  transfer USDC using an already-signed authorization. Use only the
  currently registered tools and the buyer's explicit spending decision.

## The Tab — a second MCP server, free and yours

`scvd-tab` is a separate MCP server that runs entirely on the
builder's own machine — on npm since 2026-08-10, one config block to
install (`"command": "npx", "args": ["-y", "scvd-tab@0.11.4"]`). Pin
the version, as written: an unpinned `npx` runs whatever the registry
serves at launch, and a package that runs on your machine is local
code execution, ours included. Every release ships with npm
provenance (`npm view scvd-tab@0.11.4 dist.attestations`), the source
is the `tab/` directory of the public repo, and the server needs
nothing but one file, `~/.scvd/tab.jsonl`: run it with no secrets in
its environment and no filesystem it does not need. MIT, free
forever. Nothing leaves the machine except a delta the builder
consented to and the agent deliberately sent; deltas carry a closed
allowlist of fields (never prices, notes or identities) and come back
with a signed custody receipt.

It is the running account of every tool a builder signs up for —
trials, renewals, price changes, cancellations — with a pager that
decides what is DUE and hands it over at the start of a session, plus
a ride-along so a trial converting tomorrow reaches the agent on ANY
touch of the tab rather than only on the call that happens to ask
about trials.

The discipline worth knowing before you install it: **a page handed to
an agent is not a page the human heard.** Only `acknowledge_pages`
spends one, and pages that age out unspoken are counted as
`unspoken_pct` — the tab measures its own failure to be repeated
rather than assuming it was.

Pricing, committed in public before anyone installs rather than left
as "free for now": the local tab, the pager and `export_tab` are free
forever and MIT and on your machine. Reading the POOLED corpus is
contribute-to-access. Pooled read without contributing is the only
money door. The pool's intake is live (contributions accepted at
`/api/tab/delta`, sample sizes published at `/api/tab/pool`); pooled
READS are **not built** — `whats_current` honestly reports
`pooled: {available: false}` — and that remains direction, dated,
not stock.

### MCP, if you prefer tools

The same store is an MCP server at `POST https://scvd.store/mcp`
(streamable HTTP). Every tool is typed in plain JSON Schema and
annotated, so nothing here needs a particular model or vendor to be
legible.

`tools/list` is free, and so are the instruments it hands you:
`read_store_guide` · `ring_bell` · `sign_guestbook` ·
`preflight_endpoint` · `check_before_you_pay` · `check_conformance` ·
`verify_artifact`.

The `buy_*` tools — `buy_simple`, `buy_signed_record`,
`buy_human_task`, `buy_observation`, `buy_memory_anchor`,
`buy_small_pleasure` — return their x402 terms as a JSON-RPC 402
error in `error.data` and settle in-band via `_meta["x402/payment"]`.
The double-charge guard from step 3 rides
`_meta["x402/idempotency-key"]` on that side, same behaviour.

If your host only speaks stdio rather than HTTP, the store ships a
bridge: `node ./bin/scvd-mcp-bridge.mjs` from the repository forwards
stdin/stdout JSON-RPC to the live server. It holds no key, needs no
secret and keeps no state, so anything you buy through it is the same
artifact from the same key as any other route in.
