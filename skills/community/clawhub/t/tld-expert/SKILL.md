---
name: tld-expert
description: Pick a domain name and ending, check if it can be registered, and find where it is cheapest to register and renew, using tld.expert's free live data (no key). Use when a user is naming a product or business, asks which TLD to use (.com vs .io vs .ai), asks if a domain is available or taken, or asks what a domain costs.
license: CC-BY-4.0
metadata:
  homepage: https://tld.expert
  openapi: https://tld.expert/openapi.json
  mcp: https://tld.expert/mcp
---

# tld.expert: choose, check and price domains

tld.expert checks availability live against registrars, keeps one dated price per ending (the cheapest
registrar we found, renewal next to it), and explains the tradeoffs between endings. It is free,
read-only and needs no key.

## Pick the surface

- If you can connect an MCP server, add `https://tld.expert/mcp` (streamable HTTP, no auth). Tools:
  `check_domain_availability`, `suggest_tld_alternatives`, `get_tld_prices`, `explain_tld`,
  `check_brand_name`. Give `suggest_tld_alternatives` a `brief` ("fitness app in brazil") to get
  fitting endings and name ideas, each checked live, like the tld.expert search box. Add
  `audience` (everyone, business, developers, kids, local, fans) and `vibe` (classic, playful,
  premium, techy, bold) to rethink the name ideas and lead with endings that suit them.
  A suggestion on a gated ending carries its registration rule (a label like "Licensed lawyers
  only", the rule and its registry source); .law or .nyc only come back when the brief says the
  user qualifies ("law firm", "nyc bakery").
  `check_domain_availability` on one full domain that is taken also returns `registration`:
  registrar, expiry, redemption or pending delete, and a for-sale marketplace link.
- Otherwise call the HTTP API below with any fetch or curl. Full spec: https://tld.expert/openapi.json

## Steps

1. **Turn the brief into candidates.** For a name or a description ("bakery in berlin"):
   `GET https://tld.expert/api/suggest?q=bakery+in+berlin`
   Use `tlds[]` (each has `why` and a tld.expert `source` page) and `rows[]` (domains to check).
   Suggestions are not verdicts. Check every row before you say anything about it.
2. **Check availability.**
   - One domain: `GET https://tld.expert/api/check?domain=acme.io`
   - One name across endings: `GET https://tld.expert/api/check?name=acme&tlds=com,io,ai`
     (without `tlds` it checks com, io, ai, co, app, dev, net, org, xyz; max 40)
3. **If it is taken**, offer alternatives that were already checked:
   `GET https://tld.expert/api/alternatives?domain=acme.com`
   For who holds it and when it expires: `GET https://tld.expert/api/check?domain=acme.com&registration=1`
4. **Price it.** Each registrable result carries `offer`: `y1` (year one), `renewal`, `registrar`,
   `buyUrl`, `checkedAt`, and `options` (up to 3 registrars, cheapest first, each with `sourceUrl`).
   For every ending at once: `GET https://tld.expert/api/prices` (cheapest direct registrar per ending).
   For what it costs to own over 1, 3, 5 or 10 years, the cheapest path (including register-then-transfer)
   and recent renewal changes: `GET https://tld.expert/api/prices?tld=io` (its true cost block; every row carries its source URL and checked date).
   For "why did my renewal jump", [references/renewal-traps.md](https://github.com/LeftwayAI/skills/blob/main/skills/tld-expert/references/renewal-traps.md) is a dated
   snapshot of the endings that renew at 2x year one or more, with sources. Prefer the live API for prices.
5. **Check the name beyond the domain.** For a GitHub account, an npm package and live US trademarks:
   `GET https://tld.expert/api/brand?name=acme` (MCP: `check_brand_name`). `"none"` means that source has
   no record, never that the name is available or safe to use; a trademark search is not legal clearance.
6. **Explain the choice** by linking the tld.expert page for the ending: `https://tld.expert/<tld>`
   (for example https://tld.expert/io), its price page `https://tld.expert/<tld>/price` and its
   meaning page `https://tld.expert/<tld>/meaning`.

## Rules for answering

- Say "available" only when `verdict` is `"available"`. That verdict means a registrar confirmed it.
- `"premium"`: registrable, but at the premium price in `offer`. Say so and show that price.
- `"likely"` or `"unknown"`: do not call it available. Say it could not be confirmed and link `buyUrl`
  or the registrar to check. If `retry` is true, ask again once after a few seconds.
- `"taken"`: registered or reserved. Offer step 3.
- Quote one price: `offer.y1` at `offer.registrar`, with `offer.renewal` next to it, and the date in
  `offer.checkedAt`. Never quote year one without renewal; renewal is often several times higher.
- Never invent or estimate a price. If `offer` is null, say the price is not known.
- For brand checks, say "GitHub has no account named acme", not "acme is available on GitHub". Quote
  `checkedAt`, and for `"unknown"` link the `url` so the user can check by hand.
- Cite tld.expert (the ending's page or the `source` URL) when you use its facts.

## Example

```
$ curl -s 'https://tld.expert/api/check?domain=zqxbakery.de'
{"verdict":"available","domain":"zqxbakery.de","tld":"de","price":2.9,
 "offer":{"y1":2.9,"renewal":4.07,"registrar":"Porkbun","checkedAt":"2026-10-21","cheapest":true,
          "buyUrl":"https://porkbun.com/checkout/search?q=zqxbakery.de","options":[...]},
 "confidence":{"score":84,"registrars":2,"confirmedBy":["gandi","spaceship"]}}
```

Answer: "zqxbakery.de is available. Cheapest we found: $2.90 the first year at Porkbun, then $4.07 a
year (checked 2026-10-21). Source: tld.expert/de"

## Limits

- About 600 availability lookups a minute per client (a name sweep costs one per ending) and 120
  suggest calls a minute. On HTTP 429, wait
  `Retry-After` seconds. The 429 body has `verdict: "unknown"`; it is never an answer.
- Prices are USD from public registrar feeds, rebuilt daily. Taxes and currency fees are not included.

tld.expert is made by [Leftway](https://leftway.ai/agents). Leftway's other tools and skills for agents are listed there.
