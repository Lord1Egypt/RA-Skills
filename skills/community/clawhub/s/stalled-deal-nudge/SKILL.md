---
name: stalled-deal-nudge
description: 'Flag stalled deals and nudge each rep with a drafted follow-up: every Monday each rep gets one Slack digest of their open deals that went quiet, with how long since the last logged activity, the line that activity left off on, why the deal is worth a touch now, and a follow-up drafted for them to send. Triggers: "flag deals that went quiet", "weekly stalled deal report in slack", "nudge reps on deals with no activity", "which open deals have gone cold", "remind reps to follow up on stuck opportunities", "draft follow-ups for stalled deals weekly". Cargo project, defineAgent, native deal, account and activity models, SQL, Slack postMessage, workspace context, ledger model; adapts to HubSpot, Salesforce or Attio. Skip when: you want the week''s GTM work ranked against initiatives, which is weekly-planning; or you want one account researched now, which is research-account.'
version: "0.1.2"
compatibility: "Requires @cargo-ai/cli with @cargo-ai/cdk 1.0.92 or later, a Cargo workspace, and authorized Slack and Anthropic connectors. No CRM connector: the example runs on Cargo native models. Reads the workspace context when the project declares one."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/stalled-deal-nudge
metadata:
  author: getcargo
  source: cookbook
  personas:
    - account-executive
    - sales-leadership
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

# Stalled-deal nudge

## The outcome

An open deal stops dying in silence. Every Monday morning one agent finds the open deals with no
logged activity in the last fourteen days and posts one digest per owner to a locked Slack channel.
For each deal:

- **How quiet**: days since the last logged activity, and how many Mondays running it has been
  flagged.
- **Last**: the line the last note, meeting or call left off on, quoted with its date.
- **Why now**: one sentence grounded in that deal, such as a close date about to slip, a next step
  nobody took, or an objection left unanswered.
- **Draft**: a follow-up of at most four sentences that picks up from the quoted line, for the owner
  to send. The agent never sends it.

The worked example runs on Cargo native models, with no CRM connector: `gtm_opportunities` (the standard deal
schema), `gtm_accounts`, and `gtm_activities`, one row per logged email, meeting, call or note. Last
activity is computed in SQL as the latest `occurred_at` per deal, not read off a roll-up property,
so "quiet for N days" is a query anyone can read. With deals in HubSpot, Salesforce or Attio, the
models are swapped for connector-backed ones and the agent does not change (`crm-backed` below).
A ledger records each deal nudged per ISO week: a re-run the same Monday posts nothing, and a failed
post is retried the next run. A native write takes a few minutes to become readable, through SQL
and `search_records` alike, so a re-run within those minutes does not see the ledger yet and posts
again; the Monday cadence never comes close. The agent reads the deal models and never writes them.

## Example

> Every Monday, tell each rep which of their open deals went quiet and draft the follow-up.

Illustrative output, fictional records:

```text
:hourglass: *Stalled deals · Dana Ruiz · 2026-W41*
_2 open deals with no logged activity in 14+ days._

*Fabrikam — Platform* — Proposal, $64,000, closes Oct 31 · quiet 19 days, flagged 1 Monday running
Last: Sep 17 "Send the security questionnaire and we'll take it to procurement."
Why now: The close date is three weeks out and the questionnaire that unblocks procurement never went.
Draft: > Hi Lee, attaching the completed security questionnaire you asked for on the 17th.
       > If procurement needs anything else to keep the Oct 31 date, send it my way today.

*Northwind — Expansion* — Discovery, $22,000, closes Nov 20 · quiet 16 days
Last: Sep 20 "Let's regroup once the Q4 budget is set."
Why now: Q4 budgets were due Oct 1, so the regroup they asked for is now.
Draft: > Hi Priya, you mentioned regrouping once Q4 budget was set. Is this week good?
```

Five owners had stalled deals, so five digests landed and eleven rows were added to `deal_nudges`; a
second run that Monday posted nothing.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/stalled-deal-nudge` writes this example to
   `infra/stalled-deal-nudge/` and this procedure to `.claude/skills/stalled-deal-nudge/`. No
   project yet? `cargo-ai project init <dir> --cookbook stalled-deal-nudge && cd <dir> && npm install`
   does both. **If you are reading this from the project's `.claude/skills/`, the install already
   happened — start at step 2.** On a CLI too old to have `add`, copy this folder in as a sibling of
   what is there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** If the project already has a Slack or Anthropic
   connector, or `gtm_opportunities`, `gtm_accounts` or `gtm_activities` models, rewire the imports to the existing one
   and drop the copy; two resources with one slug is a collision at deploy. If the deals live in a
   CRM, apply `crm-backed` now, before the first deploy.
3. **Point Slack at your channel and name the owners.** Authorize the Slack connector if the
   workspace does not have one (`cargo-ai project add connector/slack`). Set `channelId` in
   `infra/agents/nudger.ts` to a channel id (`C…`) from that connector's channel autocomplete, and
   invite the bot. Fill `OWNERS` in `infra/agents/nudger.prompt.ts` from the distinct `owner_id`
   values on open deals. `references/digest.md` (installed beside this file) is the digest shape.
4. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted; _What you will be asked_ is the floor, and you derive before you ask. If you
   are asking more than about four questions you have skipped lookups. Record what you changed and
   why under a `## Decisions` section in your copy of this file.
5. **Check, then plan.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root. Show the diff, and deploy only on an
   explicit yes: `cargo-ai project deploy`. Never `cargo-ai project init --force` into a non-empty directory.
6. **Verify.** With the models filled (or seeded with test rows,
   `cargo-ai storage record create-bulk`), run the prompt's selection by hand (`cargo-ai storage`
   SQL over the models) and compare it with what a rep would call stalled. Then
   send the agent its trigger text once (`cargo-ai ai message create`), walk _Done when_ line by line
   with evidence, and send it again: the second run must post nothing.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked. Only the ones marked
_asked_ genuinely live in the operator's head.

| Input                                                     | Kind    | How it is answered                                                                                                                                                                    | Why it matters                                                                                                                                           |
| --------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| where deals and activities come from                       | asked   | the native models in this folder, filled by whatever the team already runs (a sync, call-capture, a sequencer), or a CRM via `crm-backed`. Check what fills them before anything else.                     | An empty `gtm_activities` model makes every open deal look quiet, and the first digest flags the whole pipeline.                                               |
| deal and activity columns                                  | derived | Read the models' columns once. The native `defineDeal` schema carries `is_closed`, `owner_id`, `stage_name`, `close_date`; `gtm_activities` carries `opportunity_id` and `occurred_at`.                              | The selection rests on these. A CRM-backed swap renames them, and the prompt's SQL has to follow.                                                          |
| `QUIET_DAYS` (`infra/agents/nudger.prompt.ts`)            | asked   | the number of days without logged activity after which the team agrees a deal is stalled. Default fourteen.                                                                         | Too short and the digest is noise reps mute; too long and it reports deals already lost.                                                                 |
| `OWNERS` (`infra/agents/nudger.prompt.ts`)                | derived | `SELECT DISTINCT owner_id` over open deals, then the name the digest prints for each.                                                                                                 | An owner missing from the map lands under "Unassigned or unmapped owner", which nobody reads as theirs.                                                  |
| `channelId` (`infra/agents/nudger.ts`)                    | asked   | the Slack channel id (`C…`) the digests may land in, read from the connector's channel autocomplete. Invite the bot.                                                                 | Digests quote deal amounts and prospect lines. Locked so they never land in a customer shared channel.                                                   |
| LLM connector and model (`infra/connectors/anthropic.ts`) | value   | **derived**: `cargo-ai connection connector list`. `languageModel` is a placeholder to set.                                                                                           | It is what every Monday is billed against.                                                                                                               |

Checked before moving on, not after the deploy:

- `gtm_opportunities` and `gtm_activities` hold rows, and every open deal's activities carry its `opportunity_id`
- the selection SQL run by hand returned deals a rep agrees are stalled, and none that are closed
- `channelId` is a `C…` id the Slack connector can see, and the bot is in that channel
- `node --import tsx evals/contract.mjs` passes

## What you can change

| Variation        | When it is right                                                    | How                                                                                                                               | What it costs                                                                                                                            |
| ---------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `quiet-by-stage` | Late-stage deals should be flagged sooner than early ones           | Replace the single `QUIET_DAYS` condition in §1 of the prompt with a `CASE` on `dealstage`                                         | The rule gets harder to read in one glance. Keep the table of stage to days in the prompt, not in someone's head.                        |
| `per-rep-dm`     | Reps want their own digest, not a shared channel                    | Replace the locked `channelId` with one `postMessage` use per rep                                                                  | One use per rep to maintain. Dropping the lock instead lets the agent pick the destination, which is how a digest reaches the wrong person. |
| `min-amount`     | Small deals flood the digest                                        | Add `amount >= <floor>` to the §1 SQL                                                                                              | Small deals that matter (a land for a big expansion) go unflagged.                                                                       |
| `manager-rollup` | Leadership wants one view of every stalled deal                     | Add a final post to the same channel: one line per owner with their count and total amount                                         | One more post. It turns a nudge into a scoreboard, which changes how reps read the digest above it.                                       |
| `crm-backed`     | The deals already live in HubSpot, Salesforce or Attio                                     | Replace `gtm_opportunities` and `gtm_activities` with connector-backed models of the same slugs that extract every record and every column (`fetchRecords`, `columnSelectionMode: "all"`, no filter): HubSpot `deals` plus `notes`, `meetings`, `calls` and `emails`, or Salesforce `Opportunity` plus `Task` and `Event`. Last activity maps to the latest engagement timestamp (`hs_timestamp`, `ActivityDate`), or to the deal roll-up (`notes_last_updated`, `LastActivityDate`) if you extract only deals. Adapt the column names in §1 of the prompt; drop the no-connector assertion in the contract | One connector to authorize and a sync to schedule. A roll-up property is only as fresh as the CRM keeps it; engagement rows are what actually happened. |
| `no-drafts`      | Reps prefer to write their own follow-ups                           | Drop the Draft line from §3 and §4 of the prompt                                                                                   | The digest says what is stuck but not how to unstick it; the cheapest follow-up is the one already written.                              |

## What should not change

- **"Stalled" is asked in SQL, over every deal.** (`infra/agents/nudger.prompt.ts` §1) Neither the
  models nor a CRM-backed extractor filter. Put the rule in an extractor's config and it becomes
  invisible to anyone reading the query, and changing N means a redeploy and a re-extraction instead
  of an edited line.
- **Last activity is computed from activity rows.** (`infra/agents/nudger.prompt.ts` §1) A roll-up
  property a sync forgets to refresh makes every deal look quiet.
- **The ledger is checked before research and written after the post.**
  (`infra/agents/nudger.prompt.ts` §2 and §5) Check after and every re-run pays for the research
  again. Write before and a failed post is recorded as sent, so the owner hears nothing and the
  deal is skipped all week.
- **The ledger, not Slack history, is the dedupe.** (`infra/agents/nudger.ts`) Reading the channel
  back treats a deleted digest or another bot's post as "already nudged". The contract fails if a
  Slack read sits on `uses`.
- **`channelId` is locked on `postMessage`.** (`infra/agents/nudger.ts`) Digests carry deal amounts
  and quoted prospect lines.
- **The deal models are read, never written.** (`infra/agents/nudger.ts`) A nudge that could move a
  stage or close a deal changes the forecast from a guess. The only writable model is the ledger.
- **The draft is never sent.** (`infra/agents/nudger.prompt.ts`) The owner knows things the CRM does
  not, such as a call last week nobody logged. A sent draft is how a prospect gets a "just checking
  in" the day after they signed.
- **Weekly.** (`infra/agents/nudger.ts`) The ledger keys on the ISO week. A daily cron would post
  Monday's digest and then nothing for six days, which reads as broken; to nudge daily, change the
  ledger key with it.

## Done when

- `node --import tsx evals/contract.mjs` passes
- `cargo-ai project plan` reports the agent, the `gtm_opportunities`, `gtm_accounts`, `gtm_activities` and `deal_nudges`
  models, the two connectors and the two folders
- the hand-run selection returned only open deals whose latest activity is older than `QUIET_DAYS`
- the first run posted exactly one digest per owner with stalled deals, in the `references/digest.md`
  shape, and wrote one `deal_nudges` row per deal with the digest's Slack `ts`
- a second run the same Monday, once the first run's ledger rows read back through SQL, posted
  nothing and added no row
- every `Last:` quote exists in the `gtm_activities` row it came from, with that date
- no draft was sent and no deal, account or activity row changed

## What it costs

There is no enrichment provider, no CRM connector and no per-record fan-out: the selection and the
last-activity reads are SQL over the workspace's own models. The one connector action is the Slack
post. Immediately before the plan, read its live price:

- `cargo-ai orchestration action list postMessage --kind connector --integration-slug slack`

Say the number out loud; the run posts once per owner with stalled deals. The recurring cost is the
agent run, once a week, billed as LLM tokens through the Anthropic connector. It scales with the
number of stalled deals that week, and `maxSteps` caps it per run. A `crm-backed` adaptation adds
the CRM extract: read its price with `cargo-ai connection integration get <crm>`.

## Composes into

`call-capture` (logged calls are the activity that keeps a deal off the list), `meeting-prep` (the
meeting the nudge books gets a card), and `weekly-planning` (the stalled count is a line in the
week's plan).
