---
name: thumbtack
description: "Query thumbtack.com from a shell — search local service pros by trade and zip, and read pro profiles with ratings, reviews, credentials, business hours and pricing. Uses plain curl against Thumbtack's SSR pages and its anonymous GraphQL endpoint; no API key, no login, no browser extension. Use when you want Thumbtack data without an MCP server, in a script, or one-shot."
---

# Thumbtack access (curl)

Thumbtack's consumer surface is **reachable server-side with plain `curl`** —
no bot wall, no key, no session. Everything in this skill is anonymous.

Three surfaces, all verified:

1. **Search pages** — `www.thumbtack.com/k/<slug>/near-me?zip_code=<zip>`.
   Results are embedded as JSON in `__NEXT_DATA__`.
2. **Pro profile pages** — carry `window.__APOLLO_STATE__` (a bare JS
   assignment, needs brace-matching) plus a clean `ld+json` business node.
3. **GraphQL** — `app.thumbtack.com/graphql` accepts ad-hoc anonymous queries.
   Introspection is off, so field names come from an Apollo dump.

## Setup

None. `curl`, `jq` and `node` (for the bundled extractor) are all you need.

```sh
TT=~/.claude/skills/thumbtack/tt-extract.mjs   # adjust to wherever this skill lives
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
```

Send the browser `User-Agent`. Requests work without it, but match the browser.

## Core calls

**Search pros** — `-L` is mandatory (see the resolve rule below):

```sh
curl -sSL -A "$UA" "https://www.thumbtack.com/k/house-cleaning/near-me?zip_code=28203" \
  | node "$TT" next \
  | jq '.props.pageProps.frontDoorPage.proListSection.proListResults'
```

**Read a pro profile** — the `ld+json` path is simplest:

```sh
curl -sSL -A "$UA" "<profile-url>" | node "$TT" ldjson | jq '.["@graph"][0]'
```

For credentials, business hours, payment methods and specialties use
`node "$TT" apollo` instead — those live only in the Apollo store.

The extractor takes one mode: `next` | `apollo` | `ldjson`. It reads HTML on
stdin, writes JSON on stdout, and exits `3` if that store isn't on the page.

Ready-to-run projections and `jq` recipes: **`references/discovery.md`**.
Read it before composing a call — the per-store field paths are all there.

## Rules

- **Resolve the slug first.** Loose service names redirect to a canonical
  slug (`/k/plumbing/…` → `/k/plumbers/…`). Always pass `-L`, and take the
  canonical slug from the **final** URL (`-w '%{url_effective}'`) rather than
  assuming your guess was right.
- **Pick the store by page type.** Search pages have `__NEXT_DATA__` and *no*
  Apollo state; profile pages have Apollo state and `ld+json` and *no*
  `__NEXT_DATA__`. Using the wrong mode exits `3`.
- **`jq` alone cannot read a profile page.** `__APOLLO_STATE__` is a bare
  `window.x = {…}` assignment, not a script tag — that is what the bundled
  extractor's brace-matcher is for. Don't try to regex it.
- **Address the Apollo payload by key prefix**, never by literal key: it is
  `servicePage({...the entire input json...})` and changes per page.
  `.ROOT_QUERY | to_entries | map(select(.key|startswith("servicePage")))[0].value`
- **Never filter JSON-LD on `@type == "LocalBusiness"`.** Thumbtack uses the
  trade-specific schema.org subtype — a plumber's node is `"@type":"Plumber"`,
  an electrician's is `"Electrician"`. Take `@graph[0]`, or match by shape
  (a `name` plus an `aggregateRating`/`address`).
- **GraphQL answers HTTP 200 with an `errors[]` body.** Check `.errors`, not
  the status code.
- **`servicePage` needs its *full* input object.** A partial input returns
  `badRequest` even when the query validates. Lift the whole input from the
  page's own Apollo key.
- **Search returns 10 results and no cursor.** Deeper paging needs GraphQL.
- **Shapes vary by category.** `priceInfo` is a union — a pro may return
  `ServicePagePriceSubsectionNoPrice` ("Contact for price") instead of a
  number. Handle the absent case; don't assume a price exists.
- Read-only. Nothing here writes, books, or contacts a pro.

## In context groups

On a host with context groups (mcp-host), the MCP's tools sit in the
**home** group. None of them is a canonical read: Thumbtack is an anonymous
directory of local pros, so nothing in it is new, due or on for you, and it
has no listable subjects. Every read is a `lookup` (search, resolve a
service, a pro's profile and reviews); the GraphQL escape hatch is `other`.
A compound home ask ("is the pool heater on, and find me a pool repair pro
near 28203") reaches Thumbtack for the lookup half only. It needs no
browser and no sign-in, so the group never reports it as "needs your
browser open".

## What this skill does NOT cover

- **Your own Thumbtack account** (projects, messages, quotes). The login is
  reCAPTCHA-gated, so there is no server-side password login — that surface
  needs the browser bridge and is not part of this skill.
- **The Partner Platform API** (`developers.thumbtack.com`). Real, documented,
  and gated behind partner credentials via "Request Access" — a seller
  surface, not a consumer one.
