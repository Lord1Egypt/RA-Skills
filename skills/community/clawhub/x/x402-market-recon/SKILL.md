---
name: x402-market-recon
description: Use when deciding whether an x402 endpoint can actually be discovered and bought. Read-only measurement of the live market (registry demand, 402 delivery shape, directory checks, router caps) before anything is changed.
category: research
tags: [x402, market-research, discovery, pricing, evidence, agents]
allowed-tools: [read-only-network, file-write-out-dir]
permissions:
  network:
    scheme: https-only
    documented_hosts:
      - https://api.cdp.coinbase.com
      - https://www.x402scan.com
      - https://x402-list.com
      - https://agent402.tools
    other_hosts: "unpaid reads only, and only with --allow-any-host, which prints every host first"
    payment: none
  file_write: "the --out directory only (default ./recon)"
  file_read: none
  environment: none
  secrets: none
  shell: none
---

# x402 market recon: measure before you change anything

Trigger, when the question is about an x402 endpoint's discoverability or its price:

- "why is nobody buying my x402 endpoint", "should I rewrite my endpoint descriptions"
- "where do I list this", "is my price wrong", "does anyone actually see this endpoint"
- a plan to change a payment path, a discovery document or a listing that currently rests on a hunch

Do not invoke this skill for: debugging an unrelated payment failure, rewriting copy on a marketplace
whose rules you already know, or building a new paid endpoint from scratch - that last one is an
implementation task, not a measurement one. This skill measures; it does not build or spend.

The whole skill is one habit: **turn the question into a number you can re-measure, before editing
anything you would have to test with real money.** In practice this reorders the usual plan. Retrofit
projects get cancelled, and the real blocker usually turns out to be one of three things: your
discovery document does not publish route/price/description, your price sits above the buyer's hard
cap, or the directory you care about never sees a settlement from you.

## Declared permissions, and how each one is enforced

| capability | scope | enforcement inside the artifact |
|---|---|---|
| network read | https only; the four documented hosts above need no flag | one guarded helper handles every request: it refuses non-https, refuses any other host unless `--allow-any-host` was given, and prints the off-domain hosts before contacting them |
| network read, off-domain | the seller URLs a run is aimed at, e.g. probe and manifest targets | refused by default. `--allow-any-host` makes it the operator's decision rather than something a listing can trigger |
| internal addressing | never | every host is resolved first and loopback, private, link-local, multicast and reserved addresses are refused, again on each redirect hop - so a hostile listing cannot aim this at an internal service or a cloud metadata endpoint |
| network write | none | reads carry an empty body and no credentials. No payment header, signature or token is ever produced, because there is no payment code in this artifact |
| file write | the `--out` directory only | every output path is built under `--out` |
| file read | none | no key file, no config file, no environment variable, no wallet |
| shell / exec | none | pure Python standard library: no subprocess, no `exec`, no `eval` |
| secrets | none | this artifact never asks for a private key and never touches one. Paying is out of scope on purpose |

## What this skill will NOT do

- It will not spend, sign or settle anything. There is no wallet code here: a tool that can move
  money deserves its own description, its own declared permissions and its own review, so it belongs
  in a separate artifact rather than inside a measurement tool.
- It will not read a private key, a seed phrase, a token file or a password.
- It will not send your data anywhere. The only bytes that leave the machine are the URLs and the
  empty bodies of the reads listed above: no telemetry, no analytics, no callback.
- It will not write outside `--out`, and it will not touch a service you own.

## The five measurements, in this order

Do them in this order; each one either kills the plan or sharpens it.

**1. Census the registry and find where demand actually is** (`census`)
`GET https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources?limit=100&offset=N`
is offset-paginated with no server-side filter, and each item carries
`quality: {l30DaysTotalCalls, l30DaysUniquePayers, lastCalledAt}`. That field is the difference
between guessing what sells and counting it. Answers: median demand per listing, how concentrated the
demand is, which price bands and tags get picked, and what it takes to reach a visible rank.

**2. Probe live 402s and see how terms are actually delivered** (`probe`)
Ask each endpoint unpaid, read the answer, and record whether the payment terms arrived in the
`PAYMENT-REQUIRED` header or in the body, and what fields `accepts[0]` carries. This is what ends
arguments about "maybe the directory reads the body" - with a count, not an opinion.

**3. Read the directory's own check list** (see `references/decision-rules.md`)
Directories publish exactly which checks they run and what each badge requires. Read the checks, not
a prose summary of them, and never quote a browsing agent's paraphrase of a method page as fact.

**4. Read the router's published ranking rule and its caps**
A router that sends buyers your way ranks candidates by a published sequence and often caps what it
will spend on a seller with no settlement history. Find that sentence before promising anyone that a
listing equals sales: those caps are the usual reason a healthy endpoint is never bought.

**5. Compare your discovery document against live truth** (`manifest`)
Crawlers read `/.well-known/x402` for route, price and description. If it publishes bare URLs, the
crawler has nothing to match a task against, even though every paid endpoint is perfect. Build the
missing part from measured live challenge values, keep every other key byte-identical, back up
outside the docroot, and re-fetch the public URL to compare hashes.

## Decision rules

The full table with the measured anchors is in `references/decision-rules.md`. The short version:

- **Metadata completeness is table stakes, not a differentiator.** Most of the catalogue already has
  examples and schemas; if nearly everyone has it, it cannot be what separates you.
- **Description length is not quality.** Long descriptions correlate with LOWER demand. Lead with
  what the call does and what it returns; add one honest "not for" clause if it prevents misuse.
- **Price decides who can buy you.** Buyers and routers have hard caps (a default client cap, a
  router's bootstrap cap). A route priced above the cap is invisible in practice, however good.
- **Settlements, not requests, build every published rank.** Two callers rank a listing: distinct
  payers over a window, and settled volume. A free endpoint creates neither.
- **A manifest is not evidence of demand, and demand is not evidence of a good manifest.** Measure
  both; never infer one from the other.

## Pitfalls that cost real time

1. **Reading only `accepts[0].amount` invents free resources.** v1-style sellers put the price in
   `maxAmountRequired`. Read both keys, or you will "discover" a market of free endpoints that is
   actually paid.
2. **HTTP headers are case-insensitive.** `PAYMENT-REQUIRED` and `payment-required` are the same
   header. A probe that looks for one exact spelling reports "no terms" about a healthy endpoint.
3. **A single probe can report a 404/405 that only means the wrong verb.** Try the verb the route
   declares, and try twice: a trial or consumed preview can answer 200 once and 402 on the retry.
4. **Registry numbers have an unpublished definition and are not clean.** One sampled amount was
   larger than the entire ecosystem's volume; use medians, and label the count as registry-reported.
5. **A browsing agent's "quote" is data, not evidence.** Cross-check anything that would change a
   decision against a machine-readable source: a check list, a raw fetch, an API.
6. **Never edit an audited payment path for a cosmetic metadata claim.** Mirroring `accepts[]` into
   the body buys v1-reader compatibility only, and the graders already pass header-only endpoints.
7. **Anything left under the docroot is published.** Backup files, `.bak`, `~` copies: move backups
   outside and re-check that the old URLs answer 404.
8. **A payment from your own wallet is a test, not revenue.** Label it, keep the tx hash, and read the
   payer from the USDC `Transfer` log (`from`), never from `tx.from` - a facilitator relays the
   transfer and pays the gas.
9. **The cheapest listed price is not the cheapest path to a rank.** Manufacturing transactions is
   penny-scale and detectable; if you build loop traffic, disclose it next to the number.

## Hand back a report, not an opinion

Deliver: the measured baseline (with the date, the sample size and each figure's source), the one or
two blockers the numbers exposed, and a short list of next actions with their exact cost, cheapest
first. Mark anything you did not verify as unverified rather than leaving it out.

## Files

- `scripts/recon_x402_market.py` - census, probe and manifest comparison. Read-only, Python standard
  library only. Off-domain reads need `--allow-any-host`, and internal addresses stay refused.
- `references/decision-rules.md` - thresholds, badge semantics, router order, what each finding means.
- `references/findings-baseline.md` - a dated snapshot of the ecosystem, so drift is distinguishable
  from a measurement error.
