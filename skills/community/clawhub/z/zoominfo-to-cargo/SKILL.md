---
name: zoominfo-to-cargo
description: "Rebuild a ZoomInfo list on Cargo and measure the coverage you actually lose or gain before the renewal, powered by Cargo. Triggers: \"ZoomInfo alternative\", \"migrate off ZoomInfo\", \"replace ZoomInfo\", \"our ZoomInfo renewal is coming up\", \"ZoomInfo is too expensive\", \"I have a ZoomInfo export\", \"cheaper than ZoomInfo\", \"Lusha alternative\", \"Cognism alternative\". Providers: waterfall. Skip when: you are porting a Clay table rather than a contact list — use clay-to-cargo; or you have no list yet and simply want contacts sourced — use find-b2b-leads."
version: "1.0.4"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/gtm-skills
metadata:
  author: getcargo
  source: one-off
  personas:
    - revops
    - sales-leadership
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

# ZoomInfo to Cargo

A seat-priced database renewal is decided months before it lands, usually on a guess about how
much coverage you would lose. This turns that guess into a number, on your own rows, for about
the price of a coffee.

The same procedure applies to Lusha and Cognism: they are the same shape of purchase and the
comparison does not change.

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
run the comparison end to end without a purchase gate. Say the free balance out loud before the
first paid call on a new account.

Already signed in? `cargo-ai whoami` confirms it.

## Do the job

### 1. Sample the export, and keep what it already claims

Export 10 to 20 rows. Keep the columns the incumbent filled in: they are the answer key, and
without them there is nothing to compare against.

### 2. Re-derive the same rows from the identifiers only

Feed in name and domain, nothing the incumbent found, and see what comes back:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"waterfall","actionSlug":"enrichContact"}' \
  --records '[{"full_name":"Jane Doe","domain":"acme.com"},{"linkedin":"https://linkedin.com/in/someone"}]' \
  --wait-until-finished
```

Company rows the same way, since seat-priced tools are often kept for firmographics rather than
for contacts:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"waterfall","actionSlug":"enrichCompany"}' \
  --records '[{"domain":"acme.com"}]' \
  --wait-until-finished
```

### 3. Verify both sides, including theirs

This is the step people skip and it is the one that decides the answer. An incumbent's address is
not correct because it was expensive:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"waterfall","actionSlug":"verifyEmail"}' \
  --records '[{"email":"jane@acme.com"}]' \
  --wait-until-finished
```

### 4. Report three numbers

**Verified coverage from the incumbent**, **verified coverage from the waterfall**, and **the
credits the second one cost**. Those three decide a renewal. Anything else is a preference.

Operations are asynchronous. `--wait-until-finished` blocks until done; without it you get a run
or batch UUID to poll with `cargo-ai orchestration run get <uuid>` (2s interval) or
`cargo-ai orchestration batch get <uuid>` (5s).

## Example

> Our ZoomInfo renewal is next month — measure what we'd lose on 20 rows from `zi-export.csv`.

Illustrative output, fictional records:

| Measure | ZoomInfo export | Cargo waterfall |
|---|---|---|
| Emails present | 20 / 20 | 17 / 20 |
| Verified deliverable | 13 / 20 | 15 / 20 |
| Credits for the sample | seat licence | 43.7 |

Verified coverage 13 of 20 from the incumbent against 15 of 20 from the waterfall, for 43.7 credits (20 × 2 to re-derive + 37 × 0.1 to verify both sides).

## What it costs

| Action | Credits |
|---|---|
| `waterfall.verifyEmail` | 0.1 |
| `waterfall.enrichCompany` | 1 |
| `waterfall.enrichContact` | 2 |

Twenty contact rows re-derived and both sides verified is roughly 20 × (2 + 0.2), around 44
credits, inside the free balance a new account starts with.

**Never run this across a full list on the first attempt.** Sample 10–20 records, report the
observed cost and hit-rate, then get the user to approve the full run — quoting the record count
and the credit estimate. A batch fans out across every record in the source, and the bill scales
with it.

## Worth knowing

- **Sample the segment you actually sell into.** Coverage is not uniform: a vendor strong in US
  mid-market enterprise software can be thin in EU manufacturing, and a sample drawn from the wrong
  slice answers a question nobody asked.
- **Do not compare against the export's row count.** Compare against its *verified* rows. Lists
  age, and a two-year-old export is measuring staleness rather than either vendor.
- **The honest answer is sometimes "keep it".** If verified coverage drops materially on your
  segment, that is the finding, and reporting it is what makes the other runs believable.

## Going further

This skill does one job. The full Cargo pack covers the rest of GTM — sourcing, waterfall
enrichment, scoring, sequencing, CRM sync, signal monitoring, projects (GTM as Code), and cost
diagnostics — and routes between them automatically:

```bash
npx skills add getcargohq/cargo-skills
```

The complete, validated flow behind this skill lives in
[`cargo-gtm/provider-playbooks/waterfall.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/waterfall.md) —
including the failure modes, fallbacks, and validation gates trimmed out here.

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
