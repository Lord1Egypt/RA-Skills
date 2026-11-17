# Baseline snapshot: the x402 market, measured 2026-10-13

A dated snapshot exists so that a later measurement can be read as drift or as an error. Every figure
below is a measurement, with its source named. Nothing here is a forecast.

## Sample and sources

- Whole-catalogue sweep of `api.cdp.coinbase.com/platform/v2/x402/discovery/resources`:
  327 pages, **32,672 resources**, **2,261 origins**, zero failed pages.
- Live unpaid probes of **80 endpoints** (busiest, random tail, v1-style sellers).
- Scorecards read directly from one directory's service pages.
- Routing and ranking rules read from one public router's own seller pages.
- Catalogue economics read from a marketplace that merchandises bundles of third-party services.

## Demand shape

- Registry-reported calls across the sample: **942,359** over 30 days.
- Median listing: **2 calls per 30 days**. p90 = 6, p99 = 85.
- Top 3 resources held ~50 percent of all calls; the top 15 held ~67 percent.
- The busiest single resource was an AI token-verdict call: ~394,000 calls, ~4,300 unique payers,
  $0.02 per call. Second was an inference gateway at ~74,000 calls, 246 payers, $0.002.
- Inventory is enormous and cheap: tens of thousands of tools, and a large share priced at a
  fraction of a cent.

## Metadata

- `bazaar.info.input` present on 100 percent of the sample; `output.example` on ~89 percent;
  JSON schema on ~99 percent.
- Median description length ~265 characters overall; the 200 busiest listings were leaner
  (~120 characters, ~2.3 tags) than the rest (~266 characters, ~3.2 tags).
- Descriptions over 400 characters averaged materially fewer calls than descriptions under 120.
- Roughly half of sampled resources advertised more than one network; about 39 percent accepted
  Solana alongside Base.

## Delivery of payment terms

- Of 27 decoded live payloads: **26 delivered `accepts[]` in the `PAYMENT-REQUIRED` header**,
  1 in the body.
- The v1-style minority carried `maxAmountRequired`, `outputSchema`, `description` and `mimeType`
  inside `accepts[0]`, with `x402Version: 1` and no header.
- `outputSchema` inside `accepts[0]` was present in 2 of 27 endpoints (~7 percent).

## Directories and routers (as observed)

- One directory scored a tested catalogue **80/100, compliance A, 14/14 checks**, with the check
  list including "x402 v2 envelope delivered in the payment-required header" - passed by a seller
  whose 402 body is literally `{}`. Its badge for automatic conformance was present and dated with an
  expiry (it decays); its paid-delivery badge was absent.
- That scorecard also reported on-chain traction of $8.19 over 30 days from 6 buyers with the top
  buyer at 89 percent of the volume - the signature of self-testing rather than organic demand.
- A public seller-side check tool capped its own probe spend at $0.02 per call and reported a $0.05
  route as "readable but not payable: quote above the cap". Its own seller pages state that a seller
  with no settlement history is routed last, capped at $0.01 per call.
- One router's public leaderboard tracked ~1,040 sellers over 7 days; the great majority sat at
  $0.00 settled. Total across the tracked set: about $25,800 and 1.26 million calls.

## Bundles

- A marketplace operated by a large exchange merchandised four bundles whose names describe an
  outcome ("Morning Briefing", "Market Research", "Talent Market Scanner", "IPO Analysis"), each
  composed of named third-party services with per-call prices, and each priced roughly as the sum of
  its components ($0.03-0.04 for 6-7 calls; $1.65-2.50 for a 10-12 call analyst memo).
- The bundle page carries an agent prompt and a service table. The bundle is therefore an
  orchestration of listed component services, not a single sellable endpoint - which is why the
  winning position for a small seller is being a good component, not publishing a bundle.

## Demand signals beyond the registry

- A paid demand feed listed **4,372 unmet wishes in 1,317 clusters**, with only **2 clusters**
  qualifying as build-worthy under that operator's threshold (at least 5 requests and 3 distinct
  callers over a day): a long tail of one-off requests, topped by a genuinely repeated wish
  ("search the web for x402 adoption", 154 requests from 105 callers, 100 percent find-miss).
- A paid bestseller feed over the same period reported 9,741 sales, $195.98 of revenue across 576
  distinct tools, topped by utility tools averaging $0.001 per call.

Reading it together: the market is wide, shallow, cheap and impatient. The scarce resource is a
buyer's decision to route a call to you, and that decision is driven by whether you are reachable,
priced under their cap, and healthy - not by how much prose your listing carries.
