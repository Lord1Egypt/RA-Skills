# Readiness scoring: a score that rises with fresh signals and falls as they age

Score every account on how ready it is right now, from its recent signals, with older signals
counting for less. This pipeline deploys the whole loop: signals in, a score rebuilt every hour,
and a Slack message when an account crosses the line.

```sh
cargo-ai project add cookbook/readiness-scoring
```

1. **Signals in.** Two Cargo Signals feeds watch the accounts in `gtm_accounts` for rounds raised
   and jobs posted. Every event lands in Unify Account Events, next to whatever else already unifies
   there: demo requests, signups, CRM meetings, web sessions.
2. **Scored, on the account.** A computed column on Account Events, `readiness_contribution`, gives
   each event its weight times one half per half-life of age, both set per signal type in
   `infra/settings.ts`. A metric column on Unify Accounts, `readiness_score`, sums it, and
   `readiness_stage` turns the sum into `ready_now`, `warming` or `cold`. Both models rebuild hourly,
   so the age is always today's.
3. **Routed.** Two segments on Unify Accounts read the stage, and a play posts each account that
   enters `ready_now` to Slack, once.

```ts
// infra/settings.ts
export const signals = {
  fundraising: { weight: 10, halfLifeDays: 120 },
  job_offers: { weight: 4, halfLifeDays: 21 },
  demo_requests: { weight: 20, halfLifeDays: 30 }, // a first-party model, by slug
};
export const readyThreshold = 8;
export const warmingThreshold = 4;
```

## Why the decay lives in columns

A score written onto a row by a play is right only on the day it is written. The obvious fix, a play
that rewrites every score every hour, runs a workflow per account per hour to do arithmetic. Here
the events are never touched. A computed column is recomputed every time its model rebuilds, and it
can read the clock, so with Account Events on an hourly schedule each event's contribution is
always today's. The sum is an ordinary metric column, so the score sits on the account row every
other pipeline and every rep already reads, on any warehouse, with no SQL to maintain.

## Why everything goes through Account Events

The score reads one model. Any source that unifies as an account event (a Cargo Signals feed, a
webhook model of demo requests, a CRM's meetings) reaches it with no change to the query. The key
for a weight is the event's Cargo Signals `signal_type`, or the source model's slug when it has
none. A key with no weight counts for nothing, so a new source never moves scores until someone
has decided what it is worth.

## How it works

```mermaid
flowchart TD
    feeds["Cargo Signals feeds<br/>fundraising · job offers<br/>on gtm_accounts"]
    first["first-party models<br/>demo requests · signups · meetings"]
    events["Unify Account Events · :00<br/>readiness_contribution = weight × 0.5^(age / half-life)"]
    score["Unify Accounts · :10<br/>readiness_score = SUM(contribution)<br/>readiness_stage"]
    segments["ready_now / warming segments"]
    play["route_ready_accounts play<br/>stage = ready_now · added only · :20"]
    slack["one Slack message per climb"]

    feeds --> events
    first --> events
    events --> score --> segments
    score --> play --> slack
```

| File                                  | Resource           | Role                                                                        |
| ------------------------------------- | ------------------ | --------------------------------------------------------------------------- |
| `infra/settings.ts`                   | (not a resource)   | weights and half-lives per signal type, the two thresholds, the horizon     |
| `infra/models/account-events.ts`      | `defineModel`      | Unify Account Events, adopted: hourly schedule, `readiness_contribution`    |
| `infra/models/accounts.ts`            | `defineModel`      | Unify Accounts, adopted: `readiness_score`, `readiness_stage`, at :10       |
| `infra/models/signal-feeds.ts`        | `defineModel` ×2   | Cargo Signals fundraising and job offers, on a watchlist, as account events |
| `infra/models/gtm-accounts.ts`        | `defineModel`      | the watched accounts, the shared native accounts model                      |
| `infra/segments/readiness.ts`         | `defineSegment` ×2 | `ready_now_accounts`, `warming_accounts`                                    |
| `infra/plays/route-ready-accounts.ts` | `definePlay`       | the Slack post on entering `ready_now`, ships disabled                      |
| `infra/connectors/*.ts`               | `defineConnector`  | Cargo Signals and Slack, bound                                              |
| `infra/folders/index.ts`              | `defineFolder` ×2  | models and plays, named after the skill                                     |

## Placeholders (edit before deploy)

0. **The live columns of Unify Accounts and Account Events**, copied into the two declarations:
   their `additionalColumns` replace the live list, and a column left out is removed.
1. **`signals`** in `infra/settings.ts`, from the inventory query in
   [`references/run.md`](references/run.md) and [`references/weights.md`](references/weights.md).
2. **The thresholds**, after the pilot.
3. **The job title filter** on the job offers feed.
4. **The Slack channel id** in `infra/plays/route-ready-accounts.ts`.

## Cost

The score bills nothing: three columns recomputed in the workspace's own warehouse, with no LLM. Cargo Signals
bills per event delivered on the watched accounts, capped per day by each feed's
`dailyLeadLimit`. The Slack post is one action per account that crosses the line.

## Verification

```sh
node --import tsx evals/contract.mjs   # the graph boundaries, from the compiled registry
cargo-ai project types && cargo-ai project check && cargo-ai project plan
```

`evals/acceptance.md` is the line-by-line acceptance test.

## Composes into

`account-scoring` for the fit gate, `contact-sourcing` and `agentic-engagement` on
`ready_now_accounts`. Works best after `tam-building` or a CRM sync has put the accounts in Unify
Accounts.
