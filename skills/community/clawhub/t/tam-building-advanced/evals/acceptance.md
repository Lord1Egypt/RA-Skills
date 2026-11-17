# Acceptance

Walk every line. A checked template without an evidence-backed consumer
adaptation is incomplete.

## ICP and categories

- The workspace context was read for an ICP before anything was researched or
  asked. An existing one was shown and confirmed, not rewritten.
- Industries, company size and countries were proposed from `icp.md` (or
  suggested and labelled), confirmed, and written into all four sources and
  `infra/settings.ts`.
- The categories came from the CRM's company industry field when a CRM is
  connected, otherwise from `icp.md`, and are in `settings.ts`.
  "Not enough information" is still an allowed answer.

## Sources

- Every Sales Navigator URL is under 1,000 accounts and carries `INDUSTRY`,
  `COMPANY_HEADCOUNT` and `REGION`. A larger market was split with
  `extract-sales-navigator-search`. No `identityIds`.
- AI Ark's filter is nested groups, enum values come from the autocompletes,
  and `countCompanies` was run on the deployed filter, lookalike seeds
  included.
- Apollo was deployed with a small first `limit` and read before widening.
- The Exa queries are written one per category and country, in the words a
  buyer would use, in `exaQueries` (`settings.ts`).
- Every paid source has an explicit `limit` and no schedule.
- The operator approved the filters, the four limits and the maximum spend in
  one approval, with live prices and their lookup time.

## Guided handoff

- Every substantive message names the phase and ends with `Next step`: one
  concrete decision, what it unlocks, what stays blocked.
- In-progress messages that need no decision say `No action needed` and name
  the next checkpoint.

## Project

- `cargo-project` was installed and read before adapting.
- Every resource is declared in the project; no imperative script sources or
  writes anything.
- The connectors are the four sources and LinkedIn. The CRM is read through
  Unify Accounts, never written.
- Every source model and `tam_accounts` declare a custom account unification;
  Sales Navigator's is there (its default is off).
- Unify Accounts is adopted with nothing else declared on it, and the plan
  showed no column or schedule change on it.
- There is one play, on Unify Accounts, and no tool.
- This skill declares no `defineContext`.
- `node --import tsx evals/contract.mjs` passes against the adapted resources,
  and `cargo-ai project types`, `check` and `plan` pass.

## Results

- The sources were synced, merged into Accounts and profiled one at a time, in
  order, each finished before the next started.
- Five accounts of the first source were profiled and read before the rest.
- Every account a TAM source found has a profile in `tam_accounts` with a
  LinkedIn company id, a category and a status, or was read as unresolved.
- No LinkedIn company id sits on two accounts, and every account holding two
  profiles was read.
- The report gives the headline (TAM, net new, already in the CRM), the
  per-source table (found, only this source, added in order), the exclusion
  reasons by source, the coverage estimate or why it is too thin, and actual
  credits against the estimate.
- No CRM record was created or updated.

## Repository isolation

- One root skill; supporting Markdown under `references/`; no nested
  `SKILL.md`.
- No relative import leaves the skill folder.
- No credential, deployment command, customer data or hard-coded price in the
  template.
