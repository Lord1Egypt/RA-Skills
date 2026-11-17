### The corpus, and the standing rooms derived from it

The store walks a population of x402 endpoints on a weekly cadence and
freezes each round into a signed, hash-chained, OpenTimestamps-anchored
snapshot. It is public and free to read, and so is every view derived
from it. None of these rooms is behind a payment and none ever will
be: what money buys here is our labour on the record, never the record.

Each historical `verdict` retains its x402 meaning. Where a row carries
`protocols_spoken` and `mpp`, preserve both protocol readings and their named
batteries, observation dates and gaps. An MPP-only row can be `not_ready` for
x402 without establishing that the endpoint was globally broken. Older or
unanswered rows without MPP measurements remain unmeasured. Preserve the
signed original unchanged; a fresh inspection cannot fill its missing fields.

- `https://scvd.store/corpus.json` — the chain of snapshots.
- `https://scvd.store/corpus/host/{host}.json` — **everything this
  store has ever observed about one host, over time.** Derived at read
  from the signed chain, so the view cannot drift from what was
  signed; every row cites the digest and URL of the entry it came
  from.
- `https://scvd.store/doors` — every endpoint the ward round has ever
  observed, in one alphabetical list, each with its most recent dated
  observation and a link to its signed history. Good for finding doors
  to test a client against, checking whether your own is in the
  census, or feeding a crawler a starting set. CC-BY, and no use case
  is reserved.
- `https://scvd.store/fresh-set` — the narrower, more useful list: the
  doors that answered a spec-conformant x402 challenge in THIS week's
  census, with what each one's own 402 offered. Dated observations an
  agent can route on today.
- `https://scvd.store/defects` — stable names for the ways an x402
  endpoint can be broken, each with what it asserts, what would
  falsify a finding of it, and whether an unpaid probe can see it at
  all. Published so two independent instruments observing the same
  door can tell whether they actually agree.
- `https://scvd.store/criteria` — what "verified" means here: what
  gets checked, against which published criteria version, what a
  verdict says and what it never says. No mark ships from this store
  before its criteria are public.
- `https://scvd.store/inflows` — what arrived at the payment addresses
  public x402 doors advertise in their own challenges, read from Base
  and Polygon. Counts only: no address, host or sender appears.
- `https://scvd.store/registry` — the same census as a public weekly
  tally: how many listed doors actually work, registry rot, the share
  serving verifiable signed offers, and price quartiles. Aggregates
  only, no names, citable. JSON at the same URL.

Two things about all of that are unusual and both are deliberate.

**It returns the GAPS.** Not just what was seen, but why each blank is
blank — `before_first_sighting`, `not_listed`, `listed_not_walked`,
`possibly_beyond_cap`, `instrument_degraded`. Five different facts
were being written as one silence.

**It publishes no figure without its working.** Each transition is a
dated observation and is published as one. Since 2026-09-02 the house
sentence is: never a ranking, and never a verdict without its
derivation and denominator beside it. A reading derived from a host's
rows — a tier, a fraction — appears only with the rule it came from,
the denominator and the rows, so you can redo the arithmetic or apply
your own rule to the same rows. Nothing orders one host against
another. The rule and the dated note are at `https://scvd.store/criteria`.

Coverage is published beside every verdict rather than left for you to
wonder about: `population_known` (the union of every public directory
we read) against `population_walked` (the subset we actually probed).
If that ratio is small, the artifact says it is small.

### The passport tier (3.12.0, 2026-09-02)

Every endpoint passport carries a tier — `observed`, `established`,
`standing`, `broken` or `indeterminate` — derived at read from that
host's signed rounds by the rule typed once at
`https://scvd.store/criteria`, and never printed without the fraction
it came from (`summary.tier_line`, e.g. "established — 4 of 4,
W33–W36") and the rows behind it (`payload.tier.rows`). The chip and
the hosted profile carry the same line; every host's sits at
`https://scvd.store/corpus/tiers.json`, alphabetical by host, because
ordered by tier would be a ranking. A paid refresh that finds the door
broken moves the tier to broken the same hour.

### The doctrine sentence (3.11.0, 2026-09-02)

The store's refusal changed on the keeper's ruling. It read "never a
score, a rating or a ranking"; it now reads: never a ranking, and never a verdict without its derivation and denominator beside it.
Rankings stay forbidden. What is now in scope is a derived verdict
with a published rule, printed with the fraction it came from and the
rows behind it. Nothing already signed is resigned. The dated note is
at `https://scvd.store/criteria`.
