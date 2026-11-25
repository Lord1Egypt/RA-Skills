---
name: verify-email-list
description: "Verify a list of email addresses so you stop sending to bounces, powered by Cargo. Triggers: \"verify these emails\", \"clean my email list\", \"check if these addresses are valid\", \"our bounce rate is too high\", \"validate emails before sending\", \"check deliverability before the campaign goes out\". Providers: the workspace's preset Verify email tool first, then waterfall by hand. Skip when: you do not have the emails yet — use find-work-email first."
version: "1.1.0"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/gtm-skills
metadata:
  author: getcargo
  source: one-off
  personas:
    - marketing
    - sales-development
    - revops
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

# Verify Email List

Verify a list of email addresses so you stop sending to bounces.

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
run this skill end to end without a purchase gate. Say the free balance out loud before the first
paid call on a new account.

Already signed in? `cargo-ai whoami` confirms it.

## Do the job

Every Cargo workspace has a read-only **Verify email** tool in its Cargo Tools folder (neverBounce
behind it). Use it first, by its template slug `email_validator`: the action resolves to this
workspace's own copy, so there is no UUID to look up (needs `@cargo-ai/cli` 1.0.138 or later).

```bash
# 1. Run a sample, then the approved list
cargo-ai orchestration action execute-batch \
  --action '{"kind":"tool","templateSlug":"email_validator"}' \
  --records '[{"email":"john@acme.com"}]' \
  --limit 20 --wait-until-finished

# 2. Read the rows: cargo_status and cargo_is_safe (true only when status is valid)
cargo-ai orchestration batch download --uuid <batch-uuid>
```

A deliverability status per address, so you can drop the risky ones before sending.

**Half the price by hand:** `waterfall.verifyEmail` is 0.1 against the tool's 0.2, and is the
fallback when the tool is missing from the workspace. It returns `email_status` instead of
`status` and `is_safe`:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"waterfall","actionSlug":"verifyEmail"}' \
  --records '[{"email":"john@acme.com"}]' \
  --wait-until-finished
```

Operations are asynchronous. `--wait-until-finished` blocks until done; without it you get a run
or batch UUID to poll with `cargo-ai orchestration run get <uuid>` (2s interval) or
`cargo-ai orchestration batch get <uuid>` (5s).

## Example

> Check the 200 addresses in `q3-newsletter-optins.csv` before tomorrow's send and tell me which to drop.

Illustrative output, fictional records:

| email | status | is_safe |
|---|---|---|
| priya.raman@northwind.example | valid | true |
| sales@fabrikam.example | catchall | false |
| j.doe@globex.example | invalid | false |
| m.klein@contoso.example | valid | true |

171 safe to send, 29 not (18 catch-all, 11 invalid): drop 29 before sending; 40 credits (200 × 0.2) with the Verify email tool, or 20 by hand with `waterfall.verifyEmail`.

## What it costs

| Action | Credits |
|---|---|
| Verify email tool (`"kind":"tool"`) | 0.2 |
| `waterfall.verifyEmail` | 0.1 |

**Never run this across a full list on the first attempt.** Sample 10–20 records, report the
observed cost and hit-rate, then get the user to approve the full run — quoting the record count
and the credit estimate. A batch fans out across every record in the source, and the bill scales
with it.

## Worth knowing

- `is_safe` is true only for `valid`. Treat everything else (catch-all, unknown, invalid, disposable)
  as unproven, and decide with the user whether catch-alls go out.
- Addresses from `find-work-email`'s Find email tool were already checked before it returned them;
  verifying them again spends credits for nothing.
- `waterfall.verifyEmail` is the cheapest verification tier in the priority stack.

## Going further

This skill does one job. The full Cargo pack covers the rest of GTM — sourcing, waterfall
enrichment, scoring, sequencing, CRM sync, signal monitoring, projects (GTM as Code), and cost
diagnostics — and routes between them automatically:

```bash
npx skills add getcargohq/cargo-skills
```

The complete, validated flow behind this skill lives in
[`cargo-gtm/recipes/outreach-activation.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/outreach-activation.md) —
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
