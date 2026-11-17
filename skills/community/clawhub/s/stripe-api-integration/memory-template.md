# Working File Templates — Stripe API Integration

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/stripe-api-integration/config.yaml` | Key by key, read-modify-write |
| Account context, integration shape, catalog, endpoints, volume, due dates, box index | `~/Clawic/data/stripe-api-integration/memory.md` | Rewritten in place; stays small |
| Products, prices, coupons and promotion codes in use | `## Catalog` in `memory.md`; `~/Clawic/data/stripe-api-integration/catalog.md` once it outgrows it | One row per price |
| Webhook endpoints, their events and their API version | `## Webhook Endpoints` in `memory.md`; `webhook-endpoints.md` once it outgrows it | One row per endpoint, per environment |
| Payment incidents — duplicate charges, mass declines, an outage, a bad migration | `~/Clawic/data/stripe-api-integration/incidents/<year>.md` | Append-only, cut by year |
| Disputes and what won or lost them | `~/Clawic/data/stripe-api-integration/disputes/<year>.md` | Append-only, cut by year; the monthly rate is computed from it |
| Things you produced that get re-read — runbooks, evidence packets, integration decisions, Radar rule sets, migration plans, reconciliation procedures | `~/Clawic/data/stripe-api-integration/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A person: marketplace seller, invoiced client, whoever owns the Stripe login | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person; referenced here by name only |
| The Stripe account as a money account, and paid Stripe add-ons | `~/Clawic/data/finances/accounts.md` and `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row each; amounts carry their currency |
| Physical Terminal readers | `~/Clawic/data/devices/devices.md` (**shared**) | One row per reader |
| **Anything durable this table does not name** | `~/Clawic/data/stripe-api-integration/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Secret keys, signing secrets, `client_secret`, card data | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Three questions decide anything the table missed, in order: **would another skill want to read it?** → the shared box. **Is it a text read whole when its subject comes up?** → `artifacts/`. **Is it one more row of something accumulating?** → a section of `memory.md` until the threshold, then its own box.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A product, price, coupon or promotion code was created or retired | Its row in `## Catalog` |
| A webhook endpoint was created, re-pointed, disabled or its event list changed | Its row in `## Webhook Endpoints` |
| The integration shape was decided or changed — charge type, who holds the customer, which events are handled, Checkout vs Elements | `## Integration Shape`, and the reasoning to `artifacts/` if it took work to reach |
| A duplicate charge, a mass decline, a payout that did not arrive, a bad backfill | `incidents/<year>.md` |
| A dispute was filed, and again when it closed | `disputes/<year>.md` |
| A month was reconciled: volume, fees, net, refunds, disputes | `## Volume & Fees` |
| A runbook, an evidence packet that won, a Radar rule set, a migration plan came out of the session | `artifacts/` |
| A seller, client or account owner was named | `~/Clawic/data/contacts/contacts.md`, name only referenced here |
| The payout bank, entity or a paid Stripe add-on was established | `~/Clawic/data/finances/` |
| A Terminal reader was registered or moved | `~/Clawic/data/devices/devices.md` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except artifacts, the two logs and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. **Who**: the agent that is about to add the entry, in the turn it adds it.
2. **When**: count the entries in the section **before** appending. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — split first, then append.
3. **What happens to the original**: in the same turn, create the new file in `~/Clawic/data/stripe-api-integration/`, move the whole section into it, **delete the section from `memory.md`**, and add its line to `## Boxes`. `memory.md` keeps the index line and nothing else.
4. **Precedence**: never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

**Isomorphism**: the headings are identical on both sides of the move. `## Catalog` splits into `catalog.md` carrying `## Products & Prices`, `## Coupons & Promotion Codes`, `## Retired`; `## Webhook Endpoints` splits into `webhook-endpoints.md` carrying `## Endpoints` and `## Events Handled`. Keep them the same and the split is a copy-paste instead of a rewrite that drops rows.

Artifacts and the two logs are the exception: a runbook, an evidence packet, an incident or a dispute is born in its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:STRIPE_SECRET_KEY` · `env:STRIPE_WEBHOOK_SECRET` · `keychain:stripe-live` · `1password:Work/Stripe/live` · `bitwarden:Stripe/restricted-refunds` · `ssm:/prod/stripe/webhook-secret` · `secretsmanager:prod/stripe/api-key` · `file:~/.config/stripe/config.toml`

When the user pastes something to save — a `.env`, a webhook handler, a support thread, a log of API calls — replace each secret value before writing and leave the pointer visible: `STRIPE_SECRET_KEY=<keychain:stripe-live>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: publishable keys (`pk_live_…`, public by design), account ids (`acct_`), customer, payment intent, charge, subscription, price, product, invoice, event, dispute and endpoint ids, webhook URLs, card brand and last four, expiry month of a saved card, statement descriptors, payout ids, invoice numbers, country and currency codes. **Secrets, strip them**: secret and restricted API keys (`sk_…`, `rk_…`), webhook signing secrets (`whsec_…`), any `client_secret` (`pi_…_secret_…`, `seti_…_secret_…`), Connect OAuth access and refresh tokens, Terminal connection tokens, full card numbers, CVC, full bank account, routing and IBAN numbers, Dashboard passwords and 2FA recovery codes, government id numbers collected through Identity.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts](#shared-contacts) · [shared finances](#shared-finances) · [shared devices](#shared-devices) · [artifacts/](#artifacts) · [incidents/](#incidents) · [disputes/](#disputes) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/stripe-api-integration/` if it does not exist.

```yaml
stack: node
api_version: "2025-04-30"
default_currency: eur
billing_model: subscription
live_mode_policy: confirm-each
metadata_keys: [order_id, tenant_id]
tax_handling: stripe_tax
reconciliation_day: 5

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  idempotency_key: "<entity>-<id>-<action>"
  statement_descriptor: "ACME"
platform:
  account_country: IE
  presentment_currencies: [eur, usd, gbp]
safety_posture:
  refunds: confirm-each
  emit_delete_calls: false
restrictions:
  pci_scope: elements-only        # never accept a raw PAN
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Stripe Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Catalog (22 prices) → `catalog.md`; read before creating any price or quoting a plan
- Webhook endpoints (4) → `webhook-endpoints.md`; read before touching any handler or event list
- Disputes 2026 (9) → `disputes/2026.md`; read before a dispute answer and at the monthly rate review
- Incidents 2026 (3) → `incidents/2026.md`; read when the same symptom reappears
- Checkout duplicate-charge runbook → `artifacts/runbook-duplicate-charge.md`; read the moment a customer reports being billed twice
- Chargeback evidence packet that won → `artifacts/evidence-packet-saas.md`; read before answering any dispute
- Charge-type decision for the marketplace → `artifacts/decision-destination-charges.md`; read before any change to how money splits

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Payout and fee reconciliation | month, day 5 | 2026-07-05 | 2026-08-05 |
| Dispute-rate review | month | 2026-07-05 | 2026-08-05 |
| Webhook endpoint audit (failures, unused events) | quarter | 2026-05-12 | 2026-08-12 |
| API version upgrade review | quarter | 2026-04-20 | 2026-07-20 |
| API key rotation | year, or immediately on any leak or departure | 2026-02-01 | 2027-02-01 |

## Account Context
acct_1AbC…, Irish entity, live since 2024, EUR payout, sells B2B SaaS in EU + US.
Dashboard owner: Marta (see contacts). Keys: `keychain:stripe-live`, `env:STRIPE_WEBHOOK_SECRET`.

## Integration Shape
Node + Stripe SDK, API version pinned 2025-04-30. Checkout Session (subscription mode) for signup,
Billing Portal for plan changes and cancellation, Elements nowhere. Customer is created before Checkout
so metadata survives. Fulfillment hangs off `checkout.session.completed` + `invoice.paid`; handlers
deduplicate by `event.id` in Postgres.

## Catalog
### Products & Prices
| Price id | Product | Model | Amount | Interval | Live subs | Notes |
|---|---|---|---|---|---|---|
| price_1Team | Team | per-seat | 29 EUR | month | 140 | replaces price_1TeamOld |
| price_1Usage | API calls | metered, graduated | tiers in `catalog.md` | month | 38 | meter `api_calls` |

### Coupons & Promotion Codes
| Code | Effect | Duration | Redemptions | Active |
|---|---|---|---|---|
| LAUNCH20 | 20% off | 3 months | 61 | no, ended 2026-03 |

## Webhook Endpoints
| Environment | URL | Events | API version | Secret | Status |
|---|---|---|---|---|---|
| live | https://api.example.com/stripe/billing | 7 billing events | 2025-04-30 | env:STRIPE_WEBHOOK_SECRET | healthy |
| live | https://api.example.com/stripe/disputes | 3 dispute events | 2025-04-30 | ssm:/prod/stripe/whsec-disputes | healthy |

## Volume & Fees
| Month | Gross | Refunds | Disputes | Fees | Net | Effective rate | As of |
|---|---|---|---|---|---|---|---|
| 2026-06 | 48,200 EUR | 1,100 EUR | 2 (240 EUR + fees) | 1,610 EUR | 45,250 EUR | 3.34% | 2026-07-05 |

## Pain Points
March 2026: a retry loop without idempotency keys double-charged 31 customers. Refunds plus goodwill
cost more than the month's fees. Every write has carried a business-scoped key since.

## How They Work
Wants the exact call and the event that closes the loop. No framework scaffolding. Never emits live
writes without asking first.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. `reconciliation_day` from `config.yaml` sets the day of the reconciliation row.
- **`## Catalog`**: price ids are the one thing nobody can reconstruct from memory, and a price is effectively immutable once live — record what replaced what, and keep retired prices with the date instead of deleting them, because live subscriptions still point at them.
- **`## Webhook Endpoints`**: the `Secret` column holds a pointer, never a value. Record the API version per endpoint: an endpoint pinned to an old version delivers a payload shape your current code may not parse.
- **`## Volume & Fees`**: `As of` is the day the number was read; amounts always carry their currency. Effective rate = `fees ÷ gross`, and it is the number that says whether the fee stack is drifting. Re-checking a month **overwrites** its row; never a second row for the same month.
- These headings are exactly the ones the split-out files inherit, so a split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their account and integration |
| `complete` | Know the integration, the catalog and the failure history well |

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md`, shared with every other skill that knows people — the user may have none of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Role | Preferred channel | Context |
|------|------|-------------------|---------|
| Marta Ruiz | Stripe account owner, Acme | marta@acme.example | Approves refunds above 500 EUR |
```

- **Identity is the email or handle.** Read the file before adding. If that person is already there, update the row in place; only absence justifies a new row. Rows written by other skills are not yours — never rewrite them.
- **Scale cut**: one table while there are ≤15 people. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index (`Name | Role | → file`). If the folder already looks like that when you arrive, follow it — never start a parallel `contacts.md`.
- **Foreign columns win.** If the file exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Retirement**: when a relationship ends, delete the row and note the date in `memory.md`.
- Here in the Stripe box, a seller or client is **a name only**. Duplicating the person is how two skills end up contradicting each other.

## Shared finances

Lives at `~/Clawic/data/finances/`, shared with every money skill.

```markdown
# Accounts

| Account | Kind | Institution | Currency | Reference | Notes |
|---------|------|-------------|----------|-----------|-------|
| Stripe (Acme Ltd) | payment processor | Stripe | EUR | acct_1AbC… · payout to bank ••4471 | revenue in, payout T+2 standard |
```

```markdown
# Subscriptions

| Service | What for | Amount | Cycle | Renews | Notes |
|---------|----------|--------|-------|--------|-------|
| Stripe Billing | recurring invoicing | % of recurring volume | monthly | with settlement | verify rate on the pricing page |
| Stripe Tax | VAT/OSS calculation | % per transaction | monthly | with settlement | — |
```

- **Identity is the account name (or the service name for a subscription).** Read before adding; if it exists, update in place. Only your own rows.
- **Every amount carries its currency inside the value** (`45,250 EUR`, not `€45,250`) — another skill will sum this column across providers. Estimates carry the date they were estimated.
- **Bank details are a reference, never a value**: last four digits or a pointer, never a full account, routing or IBAN number.
- **Scale cut**: `accounts.md` and `subscriptions.md` stay flat tables; past ~15 rows each, one file per account at `~/Clawic/data/finances/<account>.md` with the same fields and the table becomes the index.
- **Foreign columns win**, same rule as contacts. **Retirement**: closing the account or cancelling the add-on deletes the row, with the date noted here.

## Shared devices

Only when the user runs Stripe Terminal. Lives at `~/Clawic/data/devices/devices.md`.

```markdown
# Devices

| Name | Kind | Model | Location | Network | Reference |
|------|------|-------|----------|---------|-----------|
| till-1 | card reader | WisePOS E | Store, Calle Mayor 4 | shop-wifi · a4:cf:12:… | tmr_… · location tml_… |
```

- **Identity is the network name or the MAC address** — `Name` holds the name the device answers to on the network (`till-1`), and the MAC goes in `Network` whenever the reader has no stable hostname. That is the key the shared box uses, so a home-automation skill and this one land on the same row instead of writing the same Terminal reader twice. The reader serial and its `tmr_` id go in `Reference`, never in the key.
- Read the file before adding and look the device up by that key. If it is already there, **update the row in place**; only absence justifies a new row. Rows written by other skills are not yours — never rewrite them.
- **Scale cut**: one flat table while there are ≤15 devices. Past that, one file per device at `~/Clawic/data/devices/<name>.md` with the same fields, and `devices.md` becomes the index (`Name | Kind | Location | → file`). If the folder already looks like that when you arrive, follow it — never start a parallel `devices.md`.
- **Foreign columns win** — a home-automation skill may own this file already; match its columns rather than reshaping it, and add anything missing as a trailing note. Never rewrite its header.
- **Retirement**: when the reader is decommissioned, delete the row and note the date in `memory.md`.
- Connection tokens are single-use credentials and are never written here.

## artifacts/

One file per thing, at `~/Clawic/data/stripe-api-integration/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **runbook**, **dispute evidence packet**, **integration decision**, **Radar rule set that worked**, **migration plan**, **reconciliation procedure**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Runbook — customer billed twice
*Read when: a customer reports a duplicate charge. Written 2026-07-26.*

1. Find both charges by `metadata[order_id]`, not by amount and date.
...steps, with every secret replaced by its pointer...
```

```markdown
# Evidence packet — SaaS subscription, "unrecognized" dispute
*Read before answering any dispute of this type. Won 6 of 8 since 2026-01.*

Fields submitted, in order, with what each one proves...
```

```markdown
# Integration decision — destination charges, not separate transfers
*Read before any change to how money splits. 2026-07-26.*

Decision: ...one sentence...
Rejected: separate charges and transfers — reporting per seller was worse and payout timing drifted.
Liability: platform holds dispute liability; budget the per-dispute fee accordingly.
Fees: application fee X% on top of processing; recorded in `## Volume & Fees`.
```

## incidents/

```markdown
# Incidents — 2026

| Date | Symptom | Root cause | Money impact | Fix | Runbook |
|------|---------|-----------|--------------|-----|---------|
| 2026-03-14 | 31 customers charged twice | Retry loop, fresh idempotency key per attempt | 1,240 EUR refunded | Business-scoped keys | `artifacts/runbook-duplicate-charge.md` |
```

Write the row when the incident closes, not while firefighting. If the fix produced a procedure, the procedure goes to `artifacts/` and is referenced here by filename.

## disputes/

```markdown
# Disputes — 2026

| Opened | Amount | Reason | Evidence sent | Due by | Outcome | Closed |
|--------|--------|--------|---------------|--------|---------|--------|
| 2026-06-02 | 290 EUR | product_not_received | tracking + delivery confirmation | 2026-06-16 | won | 2026-07-01 |
| 2026-06-19 | 29 EUR | subscription_canceled | cancellation policy + usage log | 2026-07-03 | lost | 2026-07-20 |
```

Two writes per dispute: one when it is filed (with `Due by`, the only date that counts), one when it closes. The monthly dispute rate is computed from this file against `## Volume & Fees` — it is the number that decides whether network monitoring is a risk, so a dispute nobody recorded is a rate nobody can defend.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`catalog.md` — `## Products & Prices`, `## Coupons & Promotion Codes`, `## Retired`. The retired section is the reason this file exists: a price that no longer sells still bills the subscriptions attached to it, and deleting its row is how a plan becomes unexplainable.

`webhook-endpoints.md` — `## Endpoints`, `## Events Handled`. The second section maps event → what the handler does → what breaks if it does not run; it is the only place that answer is written down.
