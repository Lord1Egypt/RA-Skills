---
name: win-loss-review
description: 'Run a monthly win-loss review of your CRM''s closed deals, landed in context/ as one pull request: the ICP verified against won versus lost with a disqualifier, dated insights with counts and denominators, objections from recorded lost reasons, and a client file per closed-won account; a five-line Slack digest says what changed. Never edits a persona, nor the ICP after the first pass. Triggers: "verify our ICP against won and lost deals", "what do closed-lost deals say about who we should not sell to", "keep the context repo current from the CRM every month", "our lost reasons should become objections", "run a monthly win-loss review". Cargo project, harness claudeCode, HubSpot, Salesforce, Attio, Slack. Skip when: there is no CRM yet and the context should come from the website, which is web-capture; or you want one account researched before a call, which is research-account.'
version: "0.2.0"
compatibility: "Requires @cargo-ai/cli 1.0.154 or later with @cargo-ai/cdk 1.0.150 or later (harness agents bound to the project's connected state), a Cargo workspace, an authenticated Anthropic connector (the harness runs against Cargo's proxy), an authorized GitHub connector, an authorized Slack connector, an authorized CRM connection (HubSpot in the checked example; Salesforce and Attio adapt the connector, the models and the queries), and a GTM repository with `context/` and `outputs/` at its root (the shape `cargo-ai project init` scaffolds). Nothing here needs a credential in .env, and nothing here reads calls, postings or the website."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/win-loss-review
metadata:
  author: getcargo
  source: cookbook
  personas:
    - revops
    - sales-leadership
    - gtm-engineering
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

# Win-loss review

**State: to-be-approved.** Deploy-verified against a live workspace: not yet. Treat `Done when`
below as the acceptance test and review `cargo-ai project plan` before deploying. Make no outcome claim
for this skill until it is approved.

## The outcome

What the CRM knows about who buys and who does not stops living in a report nobody reopens. Once a
month one agent runs, and two things land in your repository:

1. **The context files.** On the first pass the agent verifies `icp/` against what separates won
   from lost and names a disqualifier; it writes dated `insight/` files in three buckets (who we
   talk to, where we win, where we lose), every count with its denominator; `objection/` files from
   lost reasons where the CRM records them; and a `client/` file per closed-won account. Every month
   after, it appends what the new deals say and edits nothing that exists.
2. **The run record.** `outputs/<date>-win-loss-review/README.md` holds every query's result,
   counts and ids only, so every `[R: <query>]` tag in the context files points somewhere a reader
   can check. Its date is where next month starts.

Then it opens one pull request and posts a five-line digest to Slack. A human merges, and the next
`cargo-ai project deploy` syncs `context/` into the workspace context repository, which is where every
other Cargo agent reads before it acts.

The CRM is its only source, and it reaches it through models. Three `defineModel`s extract it into
Cargo storage, whole: every deal, company and contact, every column, with no filter in their
config. The queries do the narrowing (closed deals, the window, the columns each one needs), and
none of them selects an amount. `crm_deals` is new; `crm_accounts` and `crm_contacts` are declared
exactly as crm-enrichment and crm-deduplication declare them, so a project running those keeps one copy of its CRM. Extraction
bills no credits. The audit is a fixed set of SQL queries in the agent's prompt, run with
`cargo-ai storage query execute`: counts by pipeline, the lost reasons, contacts on deals, won
versus lost by industry, size and country, titles at won accounts, and the deals since the last
run. There is no collector script.

The confidence follows the data. With twenty or more closed-won deals in the window the run is in
**verify mode** and states what won versus lost shows with conviction. Below that it is in
**hypothesis mode**: the same files, every finding carrying its denominator and
`confidence: hypothesis`, and the pull request says how many wins would make it an analysis. Two
hygiene findings open every pull request, stated plainly and never worked around: the lost-reason
fill rate, which decides whether objections can come from the CRM at all, and the deal-to-contact
association rate, which says how many closed deals are blind for stakeholder mapping.

Three properties make it safe enough to run unattended:

- **The audit is deterministic.** The platform extracts, the queries are fixed, and the agent is
  told to run no other. The same questions every month are what make a month comparable to the
  last.
- **The pull request is the gate.** The agent has repository write access and `postMessage` to one
  locked channel. It cannot write the workspace context directly, cannot touch the CRM, cannot
  email anyone, and cannot merge itself.
- **Personas are never edited, and the ICP only on the first pass.** They are what the scorer and
  every outbound agent key on. A change the deals suggest is a proposal in the pull request body,
  with the deal ids, and a human decides.

## Example

> Every month, read what our HubSpot won and lost deals say, verify the ICP, and post the digest to #gtm-context.

Illustrative output, fictional records:

```text
:bar_chart: *Win-loss review Oct 2026*: 23 deals closed
Won 9, lost 14 · lost reason on 11 of 14 · contacts on 19 of 23
Learned: a RevOps title at 6 of 9 won accounts · 8 of 14 losses were under 50 employees · "no budget this quarter" on 5 of 11 reasons
Proposed: add "under 50 employees" as an ICP disqualifier (8 of 14 losses, 0 of 9 wins), in the PR body
PR: https://github.com/northwind/gtm/pull/331
```

The pull request adds four dated `insight/` files, two `objection/` files and nine `client/` files,
and modifies nothing under `icp/` or `persona/`; the disqualifier waits for a human.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it: the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/win-loss-review` writes the resources to `infra/win-loss-review/` and
   this procedure to `.agents/skills/win-loss-review/`. No project yet?
   `cargo-ai project init <dir> --cookbook win-loss-review && cd <dir> && npm install` does both; this
   folder never ships a shell. **If you are reading this from the project's `.claude/skills/`, the
   install already happened: start at step 2.** On a CLI too old to have `add`, copy this folder in
   as a sibling of what is there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** If the project already has a `crm`, GitHub,
   Slack or Anthropic connector, or `crm_accounts` / `crm_contacts` models (crm-enrichment and
   crm-deduplication declare both, identically), rewire the imports to the existing ones and drop
   the copies; two resources with one slug is a collision at deploy. The knowledge layer needs no
   work: the scaffold already declares the repo's root `context/` in `infra/context.ts`, and
   `defineContext` is a per-workspace singleton, which is why this folder ships none. **Append
   nothing to `.env.example`:** nothing here holds a credential.
3. **Fit the deals model to the CRM.** Read the live deal schema
   (`cargo-ai connection connector autocomplete` on the CRM connector, or the CRM's settings). If the
   lost reason is a custom property, set it as `LOST_REASON_COLUMN` in
   `infra/agents/win-loss-analyst.prompt.ts`; the model already extracts every property. A CRM other than HubSpot
   changes the connector, the models' config and the queries together, following
   [`references/crm-audit.md`](references/crm-audit.md).
4. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted; _What you will be asked_ is the floor, and you derive before you ask. Set the
   Slack channel id and the model. Record what you changed and why under a `## Decisions` section in
   your copy of this file.
5. **Plan, then stop.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root (`check` validates the resource tree
   offline; the blank template ships it). Show the diff: one agent, three models (fewer when the
   project already declares the shared two), the bound connectors and two folders. Deploy only on an
   explicit yes: `cargo-ai project deploy`. Never `cargo-ai project init --force` into a non-empty directory.
6. **Check the models, then run the first pass by hand.** Once the models have synced, run the
   `pipelines` query from the prompt with `cargo-ai storage query execute` and confirm won and lost
   are both non-zero: zero won with deals you know closed means the closed flags are typed
   differently on this portal, and the comparison in the prompt changes once. Then start the first
   pass from the workspace UI or with
   `cargo-ai ai message create --agent-uuid <uuid> --parts '[{"type":"text","text":"Run the win-loss review first pass. Follow your system prompt exactly and open one pull request."}]'`.
   The cron takes it from there.
7. **Verify.** Walk _Done when_ line by line and report each with evidence. Deployed cleanly and
   produced nothing is the normal failure, and the second normal failure is a pull request of fifty
   files nobody reads: check the hygiene findings and the tag counts in its body before you call
   this done.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked. Only the rows marked
_asked_ genuinely live in the operator's head; the agent runs on a cron, so it asks in the pull
request body, never in a chat.

| Input                                                     | Kind      | How it is answered                                                                                                                                                                                                                                                                          | Why it matters                                                                                                                                                                                         |
| --------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CRM connection (`infra/connectors/crm.ts`)                | value     | **derived**: `cargo-ai connection connector list` shows the authorized CRM. **asked** only when the workspace holds two                                                                                                                                                                     | The models read one CRM; the wrong one is a clean audit of the wrong deals                                                                                                                             |
| pipelines                                                 | value     | **derived** by the `pipelines` query: every pipeline is read and listed with its counts. **asked** in the first pull request only when there is more than one: which are the sales pipelines                                                                                                | Partner, renewal and support pipelines close deals too, and they are not the same evidence                                                                                                             |
| CRM hygiene findings                                      | value     | **derived** by the `lost_reasons` and `contacts_on_deals` queries and **stated**, never asked and never worked around                                                                                                                                                                       | The first decides whether objections can come from the CRM at all. The second says how many closed deals are blind for stakeholder mapping, so every title count is read against the right denominator |
| lost-reason property (`LOST_REASON_COLUMN`)               | value     | **derived**: HubSpot's standard `closed_lost_reason` ships. A fill rate of 0 of N with lost deals in the window is the cue to find the custom property and set it                                                                                                                           | Most portals record the reason on a custom property. Left wrong, the audit reports a team that never records reasons, and writes no objections, forever                                                |
| mode                                                      | value     | **derived**: `verify` at `VERIFY_MIN_WON` (20) or more won deals in the window, else `hypothesis`. Never asked                                                                                                                                                                              | The line is a number so nobody argues it per run                                                                                                                                                       |
| `icp/`, `insight/`, `objection/`, `client/`               | generated | **derived** from the queries, as the prompt describes; a seeded ICP gets one dated "Verified against the CRM" section on the first pass and is never edited after                                                                                                                           | The disqualifier is the half of an ICP that protects the team's time, and won versus lost is the only place it comes from with evidence                                                                |
| Slack channel (`infra/agents/win-loss-analyst.ts`)        | value     | **asked**: the channel the digest lands in, locked on the `postMessage` use. An id (`C…`), not a name                                                                                                                                                                                       | Locked so the agent cannot pick a customer shared channel; a digest about lost deals is internal                                                                                                       |
| project binding (`infra/agents/win-loss-analyst.ts`)      | value     | **derived**: leave `state` unset and deploy binds the project's connected state (`cargo.state.json`): its repository, directory and production branch. `cargo-ai project check` prints the binding; a project whose state is not connected deploys the agent unbound, with an empty sandbox | This is the working tree the harness clones and the only place its output can land                                                                                                                     |
| LLM connector and model (`infra/connectors/anthropic.ts`) | value     | **derived**: `cargo-ai connection connector list` shows whether an Anthropic connector is authorized; the agent's `languageModel` is a placeholder to set                                                                                                                                   | A harness does not bring its own model; this is what the monthly run is billed and metered against                                                                                                     |

Checked before moving on, not after the deploy:

- the `pipelines` query returns non-zero won and lost counts once the models have synced
- `cargo-ai project check` prints the agent bound to the repository root, not `infra/`
- exactly one `crm` connector and one each of `crm_accounts` and `crm_contacts` in the project
- the Slack channel id is an id, not a name, and not a customer shared channel

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something; that is what makes it a variation and not the
default.

| Variation               | When it is right                                                                         | How                                                                                                                                                              | What it costs                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `another_crm`           | The deals live in Salesforce or Attio                                                    | Change the connector, the three models' config and the queries together, following `references/crm-audit.md`                                                     | Field names vary per org, so the queries are rewritten against the live schema and the first pass is checked by eye            |
| `deal_contacts`         | Titles at won accounts are too broad, and the team wants the titles on the deals only    | Add `associationObjectTypes: ["contacts"]` to `crm-deals.ts`, read the column it creates after the sync, and replace `titles_at_won_accounts` with a query on it | One more column to keep in sync with the extractor's naming, and a query to re-check if the extractor changes it               |
| `raise_the_verify_line` | Twenty wins is too few to separate won from lost in your market (long cycles, few deals) | Raise `VERIFY_MIN_WON` in `infra/agents/win-loss-analyst.prompt.ts`                                                                                              | More months land in hypothesis mode, and the files assert less                                                                 |
| `wider_window`          | Your sales cycle is longer than a year, or last year was not representative              | Raise `WINDOW_DAYS` in the same file                                                                                                                             | Older deals describe an older market, and a two-year window on a company that repositioned last spring verifies the old ICP    |
| `quarterly`             | Fewer than ten deals close a month and the digest is mostly "nothing new"                | Change the cron in `infra/agents/win-loss-analyst.ts` to the first of every third month                                                                          | A lost reason that recurs in month one is written in month three. The append-only rule means nothing is lost, only late        |
| `no_digest`             | The team reads pull requests and does not want a Slack post                              | Delete `infra/connectors/slack.ts`, the `uses` block on the agent and step 8 of the prompt                                                                       | The pull request is the only surface, and a monthly pull request nobody is pinged about is a monthly pull request nobody opens |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The CRM is the only source.** (`win-loss-analyst.prompt.ts`) No calls, no postings, no website,
  no inbox. Each is another cookbook's evidence; wire one in here and a verification gets mixed
  with a hypothesis nobody can tell apart afterwards.
- **The audit is the queries in the prompt, and nothing else.** (`win-loss-analyst.prompt.ts`) An
  agent that writes its own SQL each month asks a slightly different question each month, and the
  months stop being comparable.
- **The models pull all the data; the queries filter.** (`infra/models/`) No filter and no column
  picking in a model's config: a filter there is a second place the question is asked, invisible to
  anyone reading the queries, and changing it means a redeploy and a re-extraction instead of an
  edited query. Every query on deals narrows to closed deals itself, because the model holds open
  deals whose close date is a forecast. The contract checks both.
- **No query selects an amount.** (`win-loss-analyst.prompt.ts`) The deals carry amounts in storage;
  nothing reads them, so none reaches `context/`, which is read by every agent, including the ones
  that talk to prospects. The contract fails if a query mentions one.
- **The shared models stay identical to the other CRM cookbooks'.** (`infra/models/crm-accounts.ts`,
  `crm-contacts.ts`) That is what lets one copy serve all three; a different config is a slug
  collision at deploy.
- **The one-PR write path.** (`infra/agents/win-loss-analyst.ts`) The agent never writes the
  workspace context directly and has no `context` capability: the repository is the source and
  `cargo-ai project deploy` syncs it.
- **Personas are never edited, and the ICP only on the first pass, append-only.**
  (`win-loss-analyst.prompt.ts`) A monthly agent quietly rewriting them is how a knowledge base
  drifts without anyone deciding it should.
- **The hygiene findings are stated, never worked around.** (`win-loss-analyst.prompt.ts`) A fill
  rate under half means no objections from the CRM this month, said out loud.
- **Every count carries its denominator.** (`win-loss-analyst.prompt.ts`) "6 of 9 wins", never
  "67%".
- **The channel is locked on the `postMessage` use.** (`infra/agents/win-loss-analyst.ts`) A digest
  about lost deals in a customer shared channel is the one failure nobody can undo.

## Done when

- the models synced, and the `pipelines` query returned non-zero won and lost counts
- `cargo-ai project check` prints the agent bound to the repository root, and `cargo-ai project plan`
  reports one agent, the models, the bound connectors and two folders
- the first pass opened one pull request whose body opens with the two hygiene findings with
  denominators, then the mode and the won count that set it
- `outputs/<date>-win-loss-review/README.md` holds every query's result, with no amount and no
  email
- `icp/` carries a disqualifier derived from won versus lost, as a new file or as one dated section
  appended to the seeded one
- `insight/` holds dated files in the three buckets with counts and denominators, and every title at
  a won account is mapped to a persona or listed as undetected
- with the fill rate under half, no `objection/` file exists and the body says why; at or above it,
  every objection cites two or more deals by id
- every `client/` file carries `reference_permission: unknown` and no amount
- nothing under `persona/` changed, and any proposed change is in the pull request body with deal
  ids
- the Slack digest is five lines, its numbers match the run record, and the last line is the pull
  request link
- a monthly run with new deals opened a pull request that adds files and modifies none under `icp/`
  or `persona/`; with none it opened no pull request and the digest said so
- after merging and `cargo-ai project deploy`, the verified ICP section is readable from the workspace
  context repository and an agent with the `context` capability quotes it back with its tag

## What it costs

CRM extraction bills no credits, and neither do the SQL queries. The recurring cost is one harness
run a month, scaling with how many deals closed since the previous one, plus the first pass over the
whole window. Confirm the extraction price for the workspace's CRM with
`cargo-ai connection integration get hubspot` before the first deploy.

## Composes into

`account-scoring` (reads the verified `icp/`, disqualifier included), `website-building` (the
client files and proof from closed-won deals are what the pages may cite), and any agent with the
`context` capability.
