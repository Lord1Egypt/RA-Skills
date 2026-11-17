# Working File Templates — SaaS

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/saas/config.yaml` | Key by key, read-modify-write |
| Product context, metric definitions, plans, revenue history, accounts, commitments, churn reasons, due dates, box index | `~/Clawic/data/saas/memory.md` | Rewritten in place; stays small |
| How this business defines each metric | `## Definitions` in `memory.md`; `~/Clawic/data/saas/definitions.md` once it outgrows the section | One line per metric, changed in place |
| Plans, tiers, limits, add-ons and what each includes | `## Plans` in `memory.md`; `~/Clawic/data/saas/plans.md` once it outgrows the section | One row per plan or add-on |
| Monthly MRR movement, metrics and the alerts set on them | `## Revenue` in `memory.md`; `~/Clawic/data/saas/mrr-log.md` once it outgrows the section | One row per month, forever |
| Customer accounts worth remembering — plan, ARR, seats, renewal date, health | `## Accounts` in `memory.md`; `~/Clawic/data/saas/accounts.md` once it outgrows the section | One row per account |
| Non-standard terms granted: SLA, custom DPA clause, MFN, perpetual discount, residency promise | `## Commitments` in `memory.md`; `~/Clawic/data/saas/commitments.md` once it outgrows the section | One row per grant, deleted on expiry |
| Why customers left or shrank | `## Churn Reasons` in `memory.md`; `~/Clawic/data/saas/churn-log.md` once it outgrows the section | One row per event, forever |
| The people behind accounts — champion, buyer, admin, procurement | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill in one address book |
| A multi-month programme with a start and an end — SOC 2, plan migration, billing replatform | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per programme |
| Reusable answers to security questionnaires, DPAs and vendor reviews | `~/Clawic/data/saas/security-answers.md` | Born as its own file; read whole when a questionnaire arrives |
| Outages, their customer impact and the SLA credits they cost | `~/Clawic/data/saas/incidents/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — a runbook, a cancel flow that worked, a packaging or tenancy decision, a pricing-page structure, a renewal sequence | `~/Clawic/data/saas/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/saas/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind, and customer personal data | Nowhere under `~/Clawic/data/` | Pointer or count only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a programme, a supplier, a domain? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a procedure, a decision with its reasoning, a template, a report? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A month closed, or any MRR/ARR number was computed | Its row in `## Revenue`, with the movement buckets and the as-of date |
| A metric had to be defined, or an existing definition changed | `## Definitions`, with the date it changed — a restatement invalidates prior charts |
| A plan, tier, limit, add-on, trial rule or free-tier boundary changed | `## Plans` |
| A customer account was named, upgraded, downgraded, renewed or churned | Its row in `## Accounts`; the human in `contacts.md` (shared) |
| A customer left, shrank, or was saved | `## Churn Reasons`, with the reason code and whether it was voluntary, involuntary or contraction |
| A non-standard term was granted — SLA, DPA clause, MFN, perpetual discount, residency, custom feature | `## Commitments`, in the same turn it is agreed (SKILL.md Rule 7) |
| An outage hit customers, or a credit was issued | `incidents/<year>.md` |
| A security questionnaire, DPA or vendor review was answered | `security-answers.md` — the answer, not the customer who asked |
| A dunning sequence, cancel flow, renewal sequence or onboarding checklist finally worked | `artifacts/` |
| A packaging, tenancy, motion or metering decision was made | `artifacts/`, with the alternatives rejected and the numbers behind it |
| A multi-month programme started, hit a milestone, or ended | `~/Clawic/data/projects/<project>.md` (shared) |
| A failure or surprise cost real effort to diagnose | `## Pain Points`; a second occurrence earns a runbook in `artifacts/` |
| Recurring work was scheduled or run — close, board pack, renewal notices, dunning review, audit, pen test, pricing review | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, incident logs, the answer bank and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/saas/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. A `###` inside `memory.md` becomes a `##` in the extracted file and keeps its exact wording.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

`## Revenue` is the section that always crosses the threshold first: twelve months is twelve rows plus its metrics and alerts, so plan on `mrr-log.md` existing by the end of the first year.

Artifacts, `security-answers.md` and `incidents/<year>.md` are the exception: each is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted billing-provider config, webhook handler, SAML metadata blob, `.env` or support export is the densest source of secrets in this domain: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`env:STRIPE_SECRET_KEY` · `env:PADDLE_API_KEY` · `keychain:billing-live` · `1password:Company/Billing/webhook-signing` · `bitwarden:Ops/SCIM` · `vault:secret/saas/idp` · `ssm:/prod/saas/scim-token` · `file:~/.config/saas/idp-signing.pem`

In a text, the pointer goes where the value was: `webhook_secret: <1password:Company/Billing/webhook-signing>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: plan and tier names, list prices and discounts, MRR/ARR figures, seat counts and usage limits, company account names, renewal and contract dates, churn reason codes, tenant ids and region names, subprocessor names, SOC 2 report dates and audit windows, invoice numbers, entitlement flag names, environment *variable names*, the last four digits of a card.

**Secrets, strip them**: billing-provider live and test API keys, webhook signing secrets, SAML/OIDC private keys and client secrets, SCIM bearer tokens, admin and customer-impersonation tokens, database connection strings, session cookies from a support session, unredeemed coupon and licence codes, and anything in a `.env`.

**Personal data is not a secret but is still not stored**: no user exports, no email lists, no support-ticket bodies. A named contact — champion, buyer, admin — is one row in the shared `contacts.md`; everything else about customers is stored as counts, not as people.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts box](#shared-contacts-box) · [shared projects box](#shared-projects-box) · [security-answers.md](#security-answersmd) · [incidents/](#incidents) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/saas/` if it does not exist.

```yaml
motion: sales-assist
stage: growth
reporting_currency: EUR
billing_platform: stripe
value_metric: hybrid
trial_length_days: 14
annual_discount_pct: 17
discount_ceiling_pct: 20
gross_margin_floor_pct: 70
dunning_window_days: 21
compliance_regime: soc2

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  seat_definition: active-in-last-30-days
  cohort_basis: signup-anniversary
commercial_policy:
  refunds: pro-rata-within-14-days
  auto_renewal_notice_days: 30
  grandfathering: 12-months-then-migrate
cadence:
  close_day: 5
  board_update: monthly
  renewal_notice_days: 60
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# SaaS Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Revenue history (19 months) → `mrr-log.md`; read before any MRR, ARR or trend statement
- Security questionnaire answers → `security-answers.md`; read the moment a questionnaire, DPA or vendor review arrives
- Cancel-flow that lifted saves → `artifacts/cancel-flow.md`; read before touching cancellation or save offers
- Tenancy decision: pooled with per-tenant schema → `artifacts/tenancy-decision.md`; read before any isolation, residency or single-tenant request
- Outages and credits (2026) → `incidents/2026.md`; read before signing or revising an SLA

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Revenue close and movement bridge | month, day 5 | 2026-07-05 | 2026-08-05 |
| Board / investor update | month | 2026-07-08 | 2026-08-08 |
| Renewal notices (60-day window) | month | 2026-07-02 | 2026-08-02 |
| Dunning recovery review | month | 2026-06-30 | 2026-07-31 |
| Packaging and price review | year | 2026-02-14 | 2027-02-14 |
| SOC 2 evidence collection | quarter | 2026-06-30 | 2026-09-30 |
| Penetration test | year | 2025-11-10 | 2026-11-10 |

## Product Context
B2B workflow tool, 340 paying accounts, sold in EUR, EU-hosted. Two founders, one CSM.

## Definitions
| Metric | This business defines it as | Changed |
|---|---|---|
| ARR | MRR × 12, committed subscriptions only; excludes onboarding fees and uncommitted overage | 2026-03-01 |
| Active seat | Logged in within 30 days; billed seats may exceed active seats | 2026-03-01 |
| Churn month | Calendar month of the subscription end date, not of the cancellation request | 2026-05-12 |

## Plans
| Plan | Price | Value metric unit | Included | Hard limits | Notes |
|---|---|---|---|---|---|
| Starter | 29 EUR/seat/mo | seat | 3 projects, 10k events | 5 seats | No SSO |
| Business | 79 EUR/seat/mo | seat | unlimited projects, 100k events | — | SSO, audit log |
| Enterprise | quoted | seat + commit | custom | — | SCIM, DPA, SLA 99.9% |

## Revenue
### Monthly Movement
| Month | Start | New | Expansion | Reactivation | Contraction | Churn | End | As of | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-06 | 78,400 EUR | 6,100 | 2,900 | 300 | 1,200 | 3,300 | 83,200 EUR | 2026-06-30 | closed |
| 2026-07 | 83,200 EUR | 2,400 | 900 | 0 | 400 | 1,100 | 85,000 EUR | 2026-07-18 | month-to-date |

### Metrics
| Month | NRR | GRR | CAC payback | Gross margin | Rule of 40 | Quick ratio |
|---|---|---|---|---|---|---|
| 2026-06 | 104% | 94% | 11 mo | 71% | 46 | 3.1 |

### Alerts Configured
- Involuntary churn above 30% of gross churn: monthly check in the dunning review
- Gross margin below 70% (`gross_margin_floor_pct`): flagged at close

## Accounts
| Account | Plan | ARR | Seats | Renewal | Health | Contact key |
|---|---|---|---|---|---|---|
| Northwind | Enterprise | 42,000 EUR | 120 | 2027-01-31 | green | ana@northwind.example |
| Contoso | Business | 9,480 EUR | 10 | 2026-11-04 | at risk — champion left | — |

## Commitments
| Customer | Commitment | Value | Granted | Expires |
|---|---|---|---|---|
| Northwind | Uptime SLA with credits | 99.9%, credits capped at 25% of monthly fee | 2026-01-31 | 2027-01-31 |
| Contoso | Perpetual discount | 15% off list | 2025-09-01 | none — revisit at renewal |

## Churn Reasons
| Date | Account | Type | Reason | MRR lost | Saved? |
|---|---|---|---|---|---|
| 2026-06-14 | Fabrikam | voluntary | consolidated onto incumbent suite | 790 EUR | no |
| 2026-06-22 | Adventure | involuntary | card expired, no response in 21 days | 158 EUR | recovered 2026-07-02 |

## Pain Points
March 2026: annual prepay booked as revenue, board deck did not tie to the model. Sensitive to deferred revenue since.

## How They Work
Wants the number and the formula, not the framework. Decides packaging in one sitting or not at all.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here.
- **`## Definitions`** is read before any number is computed or reported. A changed definition keeps its old line struck through in the same row's `Changed` date, so nobody compares two periods measured differently.
- **`## Revenue`**: `As of` is the day the number was read. A row whose `As of` is not the last day of the month is month-to-date and must never be compared against a closed month. Re-reading the current month **overwrites** its row; never a second row for the same month. Every amount carries its currency (`83,200 EUR`), because the reporting currency can change and a bare number then means nothing. **All six movement buckets are written as positive magnitudes** — `Contraction` and `Churn` hold the size of the loss (`1,200`), never a negative number (`-1,200`) — because the identity supplies the signs: `Start + New + Expansion + Reactivation − Contraction − Churn = End`, which for 2026-06 reads `78,400 + 6,100 + 2,900 + 300 − 1,200 − 3,300 = 83,200`. Strip the signs off a billing export before writing the row. If the identity does not hold, write the row anyway with a `bridge does not close` note rather than a tidy fiction.
- **`## Accounts`** holds accounts worth remembering — enterprise, at-risk, reference customers, the largest by ARR — not every customer. `Contact key` is the lowercase email that identifies the person in the shared `contacts.md`, never their details repeated here.
- **`## Commitments`**: a row is deleted only when the obligation genuinely ends, and the expiry date is what makes that checkable. `none` in `Expires` is a permanent obligation and should be read as one.
- **`## Churn Reasons`**: `Type` is `voluntary`, `involuntary` or `contraction` — the split that SKILL.md Rule 5 depends on. Reason strings should repeat: reuse the exact wording of an existing reason rather than inventing a synonym, or the distribution becomes uncountable.
- The `###` headings under `## Revenue` are exactly the `##` headings `mrr-log.md` gets when it splits, so the split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their model, plans and numbers |
| `complete` | Know the business, its definitions and its motion well |

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Ana Ruiz | ana@northwind.example | Champion, Northwind | email | Renewal owner; runs the weekly ops review | 2026-07-18 | — |
```

- **Identity is `Key`**: lowercase email, or a handle if there is no email, or `<kebab-name>` plus a stable disambiguator. It is a column of the row, never implicit and never delegated to a per-person file. `Preferred channel` is the type of channel, not the address.
- **Read the file before adding.** If the key is already there, update the row in place — never append a second row for the same person. Rows written by other skills are not yours: add to `Context` if you must, never rewrite them.
- **Leaving is part of the record.** When a champion leaves the account, update `Context` with the date rather than deleting the row; the account row in `## Accounts` loses its `Contact key` in the same turn.
- **Scale cut**: one row per person while there are ≤15, or until one person no longer fits in a row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Never a password, a token, or the contents of a conversation.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per programme, shared with every other skill that tracks work with a start and an end. Use it for a SOC 2 or ISO programme, a billing replatform, a plan migration, a tenancy change — not for routine monthly work, which belongs in `## Due`.

```markdown
# SOC 2 Type II
status: in progress
owner: founder
started: 2026-04-01
target: 2026-12-15

## Objective
Type II report covering security, 6-month observation window, to unblock the 100k+ pipeline.

## Milestones
- 2026-04-20 Auditor selected, scope agreed
- 2026-06-30 Evidence collection quarter 1 complete
- 2026-10-01 Observation window closes

## Decisions
- Observation window 6 months, not 12 — first report only; the second covers 12.
```

- **Identity is the file name** (the project slug). Read the folder before creating: an existing file for the same programme is updated, never duplicated.
- **Closing is a status, not a deletion**: `status: done | cancelled — <date>`. The file is the record of what was delivered. Past ~20 closed programmes, move them to `projects/archive/<project>.md` without renaming.
- **Foreign structure wins.** If the folder's existing files use different headings, follow theirs.
- Amounts inside carry their currency; people are referenced by their `contacts.md` key, never described here.

## security-answers.md

`~/Clawic/data/saas/security-answers.md` — the reusable answer bank, born as its own file with the first answer worth keeping, because a questionnaire is read whole and a fifth of the questions repeat across every buyer.

```markdown
# Security Questionnaire Answers
*Read when a security questionnaire, DPA, vendor review or RFP security section arrives. Reviewed 2026-07-26.*

| Question | Answer | Evidence | Last verified |
|---|---|---|---|
| Encryption in transit / at rest | TLS 1.2+ in transit; AES-256 at rest | Architecture page | 2026-07-01 |
| Data residency options | EU (Frankfurt); US on Enterprise | Plans | 2026-07-01 |
| Subprocessor list | Published, 30-day change notice | Trust page | 2026-06-15 |
| Breach notification window | 72 hours to the controller | DPA §7 | 2026-06-15 |
| Backup and RPO/RTO | Daily snapshot, RPO 24h, RTO 4h, restore tested quarterly | Runbook | 2026-05-02 |
```

- An answer is only reusable if it is true today: `Last verified` is what stops a stale claim being sent to a buyer. Anything older than a year is re-verified before it is reused.
- Never records which customer asked, and never quotes their questionnaire — only the answer.
- Contains no credentials, no architecture diagrams with internal hostnames, and no findings from an unremediated penetration test.

## incidents/

```markdown
# Incidents — 2026

| Date | Duration | Customers affected | Cause | Credit issued | SLA breached |
|------|----------|--------------------|-------|---------------|--------------|
| 2026-05-11 | 38 min | all EU | database failover | 0 EUR | no — 43m allowance at 99.9% |
| 2026-06-02 | 71 min | 12 enterprise | bad migration | 620 EUR | yes — Northwind, capped at 25% |
```

Read before signing or revising any SLA: the measured record is the only honest input to what uptime can be promised (SKILL.md Rule 8). Credits carry their currency. Customer-facing postmortems are artifacts; this table is the ledger.

## artifacts/

One file per thing, at `~/Clawic/data/saas/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a decision with its reasoning** (packaging, tenancy, motion, metering, merchant of record), **a flow or sequence that worked** (cancel flow, dunning sequence, renewal sequence, onboarding checklist), **a runbook** (revenue close, a recurring outage), **a report** (a board pack narrative, a pricing-page structure). Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Packaging decision — three tiers fenced on active seats
*Read before any change to plans, limits or the value metric. 2026-07-26.*

Decision: fence on active seats; usage stays unlimited with a fair-use ceiling.
Rejected: per-event pricing — median account would see a 40% invoice swing month to month.
Rejected: feature-count tiers — 70% of accounts would sit on Starter forever.
Numbers: median 9 active seats, p90 41. Business tier breaks even at 6 seats.
Migration cohorts and notice: see `plan-changes` work in `~/Clawic/data/projects/`.
```

```markdown
# Dunning sequence — 21-day window
*Read when payments fail, or before changing retry timing. Written 2026-07-26.*

Day 0 in-app banner · day 1, 3, 7 retries · day 7 email with update-card link ·
day 14 second email + admin CC · day 21 suspend, data retained 30 days.
Recovered 61% of failed payments over the last two quarters (n=88).
```

If the work behind an artifact runs for months, the programme itself belongs in the shared `~/Clawic/data/projects/<project>.md` and the artifact stays here, referenced by name. Never duplicate the decision into both.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`, promoted one level.

`mrr-log.md` — `## Monthly Movement`, `## Metrics`, `## Alerts Configured`. The reason this file exists is comparison: without a preserved as-of date and a closed/month-to-date flag on every row, a year of numbers cannot be trusted enough to put in front of an investor.

`definitions.md` — the definitions table, unchanged. Read before any number is computed, exactly as when it lived in `memory.md`.

`plans.md` — `## Plans`, plus a `## Retired Plans` heading once the first plan is sunset, with the date and who was grandfathered.

`accounts.md` — the accounts table, unchanged, with the `Contact key` column still pointing at the shared `contacts.md`.

`commitments.md` — the commitments table, unchanged. Read before granting any new term, so the same clause is not conceded twice on different values.

`churn-log.md` — the churn table, unchanged. Read before any retention work: the reason distribution, not the rate, decides where the effort goes.
