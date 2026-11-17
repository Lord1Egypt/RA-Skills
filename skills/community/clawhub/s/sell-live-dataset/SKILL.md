---
name: sell-live-dataset
description: Turn a scrape, dataset, or any endpoint into a PRICED API that other agents and people pay per call — publish a paid API, sell a dataset, monetize a scrape, charge callers per query, turn an endpoint into a priced service others pay to call. Use when the agent should be a revenue center, not a cost center — you have data (a crawl, a feed, a computed result) and want a published, discoverable, per-call-billed service instead of a one-off answer.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
      env: ["SETTLE_API_KEY"]
    primaryEnv: "SETTLE_API_KEY"
---

# sell-live-dataset — the agent as a revenue center

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

A prompt-only skill can *produce* a dataset, but it can't **sell** one: it can't
hold a live endpoint, meter calls, or collect payment. So the scrape you built
this morning is a cost — tokens spent, nothing recovered. SettleMesh flips it:
you **deploy the endpoint, publish it as a priced API, and every call another
agent or person makes pays you.** The agent stops being a cost center.

The shape is always the same: **build/refresh the data → deploy an app that
serves it → `apps api publish` a priced manifest → callers `apps api call` and
pay.**

## 1. Deploy the app that serves your data

Your data needs a live endpoint first. Use the **`ship-paid-app`** skill — it
gives you a `*.run.settlemesh.io` URL, a managed DB, and a runtime key:

```bash
settlemesh deploy ./my-api --framework container --full-stack --wait --json
```

Read the `app_id` and live URL from the JSON. Your endpoint(s) (e.g. a
`/query` route over the dataset) now respond publicly.

## 2. Publish the API with per-call pricing

Publishing declares your endpoints as a **dynamic service** and sets what each
call costs. The manifest is where pricing lives — it is not auto-created.

```bash
settlemesh apps api publish <app-id> --file manifest.json --json
# or inline:
settlemesh apps api publish <app-id> --manifest '{ ...endpoints + pricing... }' --json
settlemesh apps api show <app-id> --json     # inspect the published surface
```

The published endpoint must invoke a **published, Approved, priced** capability
or dynamic service — that Approved, priced op is what actually bills the caller.

## 3. Verify the charge is callable BEFORE anyone pays

So the *first* paid call doesn't fail on an unpriced or unapproved id:

```bash
settlemesh capabilities check <charge-id> --json
```

## 4. Callers pay per query

Anyone can now discover and invoke it — the call is metered against your priced
op:

```bash
settlemesh quote --app <app-id> --endpoint <endpoint-id> --input '{"q":"acme"}' --json   # cost before paying
settlemesh apps api call <app-id> <endpoint-id> --input '{"q":"acme"}' --json             # the paid call
```

For end users paying on their own balance (not yours), the **`charge-my-users`**
skill covers the `X-Settle-Payer` end-user-pays rail against your Approved,
priced service op.

## Keep the dataset fresh

A stale dataset stops selling. Put the refresh on a schedule with the
**`agent-cron-service`** skill so the data re-scrapes on its own while the API
keeps serving and billing.

## Notes

- **Authorization:** publishing and pricing a service is the **publisher
  (owner) and admins only** — you price your own app's API, nobody else's.
- **Pricing is explicit:** the endpoint bills only because it invokes a
  published, Approved, priced capability/dynamic-service. Deploy injects the
  app's runtime key but does **not** auto-create or price that charge — provision
  and price it first (that's what `capabilities check` guards against).
- Everything settles in **Aev** (1 USD = 100 Aev); each paid call credits your
  balance. Check it with `settlemesh aev balance`.
