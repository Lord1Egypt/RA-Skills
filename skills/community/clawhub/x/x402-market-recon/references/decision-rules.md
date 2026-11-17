# Decision rules and thresholds

Every anchor below was measured on 2026-10-13 against the live ecosystem. Re-measure before quoting
them; treat them as a shape, not as constants.

## Rank thresholds (a whole-catalogue sample, registry-reported calls over 30 days)

| target | calls / 30 days | calls / day |
|---|---|---|
| rank 10 | ~9,800 | ~327 |
| rank 50 | ~1,140 | ~38 |
| rank 100 | ~455 | ~15 |
| rank 500 | ~60 | ~2 |
| rank 1000 | ~29 | ~1 |

Concentration is brutal: the top 3 resources held about half of all calls in the sample, and the top
15 held about two thirds. A median listing shows roughly 2 calls per 30 days. Translation: most of
the catalogue is inert, so a small number of real payers moves you further than any copy edit.

## Price bands vs demand (same sample, median calls per 30 days per listing)

The head of the market is cheap. In a 200-row sample of the busiest listings, the great majority sat
at or below $0.005 and only about a tenth were above $0.03. Meanwhile buyers have hard caps that are
not negotiable:

- the official client SDK refuses to sign more than $1 per payment unless the caller raises the cap;
- at least one public router caps what it will spend on a seller with **no settlement history** at
  $0.01 per call, and routes such sellers last;
- at least one paid seller-check tool caps its own probe spend at $0.02 per call, so it cannot buy a
  $0.03 route at all - it will report your endpoint as readable but not payable.

So: if you want a route to be buyable by default clients and by routers during bootstrap, keep at
least one route per product at or below the tightest cap you intend to serve. Adding a cheap sibling
route is a product decision; silently discounting an established route is a positioning decision.
Do not do the second one to chase a rank.

## Metadata: what is table stakes and what is not

In the sample, `bazaar.info.input` was present on essentially every resource, `output.example` on
about 89 percent, and a JSON schema on about 99 percent. Median description length was around 265
characters overall, while the 200 busiest listings were LEANER than the rest (median ~120 characters,
~2.3 tags versus ~3.2). Description length above 400 characters correlated with lower mean demand.

Rules of thumb:

- lead with the verb and the artifact: "Send a token address, get a 0-100 safety score with the
  components listed"; the operator must be able to decide in one line;
- add one clause only if it prevents real misuse ("entertainment, not trading advice");
- do not inflate tags: pick the two or three a buyer would actually type;
- completeness does not sell, but its absence is still disqualifying - keep the example and schema.

## `accepts[]`: header versus body

Measured on 27 decoded live payloads: 26 delivered the terms in the `PAYMENT-REQUIRED` header, 1 in
the body. Body-carried terms belong to v1-style sellers, who also tend to carry `outputSchema`,
`description` and `mimeType` inside `accepts[0]` and put the price in `maxAmountRequired`.

Consequences:

- a directory that says it checks "the x402 v2 envelope delivered in the payment-required header" is
  satisfied by header-only delivery: mirroring into the body buys nothing there;
- the fields worth adding to `accepts[0]` because they are cheap and occasionally read:
  `description`, `mimeType`. `outputSchema` was present in only about 7 percent of endpoints, so it
  is an option, not a norm;
- never widen a published asset or network guard to accommodate a seller using a lookalike token.

## Badge semantics (read the check list, not the summary)

Two badges that sound alike mean different things and cost different things:

- **payment-ready / conformance**: earned by an automatic, free, unpaid probe that the endpoint
  answers a real 402 with well-formed terms. It decays if probes start failing, and it can be
  re-earned automatically. It is a discovery signal, not an endorsement.
- **verified / paid delivery**: earned only when the directory pays a real call that settles on chain
  and the service actually delivers. It cannot be self-declared, and paying the fee does not buy it -
  a call that does not deliver costs the fee and earns nothing.

Ownership verification is separate again, and it is a signature problem: a proof is an EIP-191
`personal_sign` over the origin URL made by the `payTo` key, and the proof must live in the right
place in your discovery document. If `payTo` is a **smart-contract account** (an email-login smart
wallet holds no private key), no ECDSA recovery can ever return it and the badge is unreachable by
design. Then publish your own evidence (receiving address plus settlement receipts) rather than
leaving a silent zero, and say plainly that this is a design choice, not an oversight.

## Router ranking order (one published example, quote it with its source)

A public router that sells other sellers' tools states its shortlist order as: task match, then crawl
health, then distinct payers over the last 30 days, then price, then a curated flag, then shorter
slug first, with a model allowed to pick from that shortlist. It also states that a seller with no
settlement history is tried only after every proven candidate, capped at a low per-call amount.

The spreadsheet lesson: distinct payers and crawl health are both measured, and both come from real
traffic. Copy, tags and manifest text only decide whether you enter the shortlist at all.

## Reading the census fields without fooling yourself

- `l30DaysTotalCalls` is the registry's own number. Its exact definition is not published; call it
  "registry-reported calls", never "settlements" unless you verified the transfers yourself.
- Use medians. The registry contains at least one nonsense amount, so a mean is a lie generator.
- Registry membership itself is not neutral: presence in a discovery feed generally follows a first
  settled paid call, so a catalogue of inert listings tells you nothing about the market's appetite.
- A seller with real volume may publish no manifest at all, and a seller with a beautiful manifest
  may have no volume. Never infer one from the other, in either direction.
