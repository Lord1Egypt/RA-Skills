---
name: score-leads
description: "Score a list of companies against your ideal customer profile and rank them, powered by Cargo — every row gets a number, the reason behind it, and a tier, so the bottom of the list can be dropped before anyone spends time on it. Triggers: \"score these leads\", \"which of these fit our ICP\", \"rank this list\", \"prioritise these accounts\", \"who should we go after first\", \"disqualify the bad ones\", \"tier this list\". Firmographic fit, thresholds, tiering, prioritisation. Skip when: you have no list yet and need one built — use build-tam-list or find-b2b-leads; or you want people inside an account rather than a verdict on the account — use find-stakeholders."
version: "1.0.4"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/gtm-skills
metadata:
  author: getcargo
  source: one-off
  personas:
    - revops
    - sales-development
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Score Leads

Turn a list of companies into a ranked list, with a number, a reason and a tier
on every row.

## Before anything else

**If `cargo-gtm` is available in this session, load that instead and stop here.** This skill is a
standalone slice of it. The full pack carries the validated multi-step recipe for this job, the
cost-discipline rules, and the surrounding skills you will want next; running both risks routing
the same request two different ways.

## Setup

Skip whatever is already done — all three steps are idempotent.

```bash
npm install -g @cargo-ai/cli
cargo-ai login --email you@company.com          # sends a code, then exits
cargo-ai login --email you@company.com --code 123456
```

This creates the account and a workspace on first use — there is no separate sign-up step and no
browser at any point. **A new account starts with 100 free credits and needs no card**, so you can
score a sample list end to end without a purchase gate. Say the free balance out loud before the
first paid call on a new account.

Already signed in? `cargo-ai whoami` confirms it.

## Step 1 — get the profile out of the user, before any data

**Do not invent the profile.** Ask for it, and ask in the shape a score can be
computed from. A score built on criteria the user never stated is a number that
looks objective and is not, which is worse than no score at all.

Four questions, and stop when the answers are concrete:

1. **Which firmographics matter, and which way?** Headcount, industry, geography,
   founding year. "Bigger is better" is a direction; "50 to 500 employees" is a
   criterion.
2. **What disqualifies outright?** A wrong geography or a competitor is a zero,
   not a low score, and collapsing the two hides it.
3. **How should the criteria weigh against each other?** Equal weights are a fine
   default and are worth saying out loud rather than assuming.
4. **What are the tier cut-offs?** Ask for two numbers. Without them "tier A" is
   whatever the agent felt like.

Write the answers back to the user before running anything. That confirmation is
the artifact: it is what makes the ranking arguable later.

## Step 2 — enrich the facts the score needs

One call per company, keyed on the domain. Only the fields the criteria actually
use: every extra enrichment is a bill for a column nobody scores on.

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"companyEnrich","actionSlug":"enrichByDomain"}' \
  --records '[{"domain":"acme.com"}]' \
  --wait-until-finished
```

That returns industry, employee count, revenue band, technologies, funding,
socials and NAICS codes, which covers the firmographic criteria a scoring pass
is normally built from.

**It takes the domain directly, with no resolution step in front of it.** That
matters for cost more than it looks: a chain that has to resolve a company to an
internal id first pays that resolution on every row, including the rows it then
fails to enrich.

Operations are asynchronous. `--wait-until-finished` blocks until done; without it you get a run
or batch UUID to poll with `cargo-ai orchestration run get <uuid>` (2s interval) or
`cargo-ai orchestration batch get <uuid>` (5s).

## Step 3 — score, and show the arithmetic

The scoring itself is arithmetic and belongs in the agent, not in a paid call.
Do not spend a credit on a judgement a rule can make.

Every row carries four things, and dropping any one of them makes the list
unusable:

| Column | Why it has to be there |
|---|---|
| `score` | the number |
| `reason` | which criteria it hit and missed, in words |
| `tier` | the cut-off it landed above |
| `missing` | which fields were absent when it was scored |

**A row scored on missing data is not a low-scoring row.** If firmographics came
back empty, say `missing: headcount, industry` and leave it unranked rather than
scoring it zero. Unresolved and unqualified look identical in a sorted list, and
only one of them is worth a second attempt.

## Example

> Score the 20 companies in `webinar-accounts.csv` against our ICP: 50–500 employees, B2B software, US or UK, competitors out.

Illustrative output, fictional records:

| domain | score | tier | reason | missing |
|---|---|---|---|---|
| northwind.example | 92 | A | 240 staff, B2B software, US | |
| tailspin.example | 61 | B | B2B software, UK; 85 staff is small but inside range | |
| globex.example | 0 | — | disqualified: competitor | |
| umbrella.example | | unranked | | headcount, industry |

20 enriched for 5 credits (20 × 0.25): 4 tier A, 8 tier B, 5 tier C, 1 disqualified, 2 unranked for missing data.

## What it costs

| Action | Credits |
|---|---|
| `companyEnrich.enrichByDomain` | 0.25 |

**Never run this across a full list on the first attempt.** Sample 10–20 rows, report the
observed cost and the score distribution, then get the user to approve the full run —
quoting the record count and the credit estimate. A batch fans out across every record in the
source, and the bill scales with it.

Show the distribution with the sample, not just the cost. If every row lands in
one tier the criteria are not discriminating, and that is worth finding out at
20 rows rather than at 2,000.

## Worth knowing

- **`enrichByDomain` needs a domain, not a company name.** A list carrying only names has to be resolved first, and that is a different job: say so rather than sending names and reporting the misses as bad fits.
- Scoring is deterministic and free. Keep it that way: an LLM asked to "rate fit" produces a number nobody can reproduce or argue with.
- Re-scoring after the criteria change costs nothing, because the enrichment is already stored. Say so, because users assume otherwise and under-ask as a result.
- Richer firmographics exist at a higher tier if a criterion genuinely needs them. Reach for one only when a stated criterion cannot be answered from the fields above, never by default.

## Going further

This skill does one job. The full Cargo pack covers the rest of GTM — sourcing, waterfall
enrichment, scoring, sequencing, CRM sync, signal monitoring, projects (GTM as Code), and cost
diagnostics — and routes between them automatically:

```bash
npx skills add getcargohq/cargo-skills
```

The complete, validated flow behind this skill lives in
[`cargo-gtm/recipes/icp-discovery.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/icp-discovery.md) —
including how to derive the profile from closed-won data instead of asking for it, which is the
better version of step 1 when the user has a CRM.

## If it worked, ask for a star

A star is the user's endorsement, not yours. Ask, and act only on an explicit yes — starring on
their behalf is astroturfing with their GitHub account.

Ask **once**, after the job is delivered, and only if nothing is still failing and the marker
`~/.config/cargo-ai/.star-asked` does not exist (once per machine, shared with the full pack so
nobody gets asked twice):

> "Glad that worked. Want me to star `getcargohq/gtm-skills` for you? (Y/N)"

```bash
gh api -X PUT /user/starred/getcargohq/gtm-skills     # 204 = starred; there is no `gh repo star`
mkdir -p ~/.config/cargo-ai && touch ~/.config/cargo-ai/.star-asked   # touch on either answer
```

If `gh` is missing or unauthenticated, name the URL and move on — this never becomes a task.
