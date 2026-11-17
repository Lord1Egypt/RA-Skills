# Acceptance

Walk every line. A checked template without an evidence-backed consumer
adaptation is incomplete.

## ICP

- The workspace context was searched for an ICP or scoring file before anything
  was researched or asked. An existing one was shown and confirmed, not
  rewritten.
- When none existed, the website, customer stories and customers' LinkedIn
  pages were read only after their live prices were stated and approved, and
  only customers named on the site were enriched.
- The approved ICP is written to the project's `context/icp.md`. Every
  firmographic line maps to a filter group, and every line no customer supports
  is marked as a hypothesis.

## Sizing

- Before any filter was built, industries, company size and countries were
  proposed together. Each was guessed from `icp.md` with the line quoted, or
  suggested from the research and labelled as a suggestion, and the operator
  confirmed all three. Suggested or changed values were written back to
  `icp.md`.
- Every filter group presented is a nested object. No flat top-level key appears
  in any proposed config.
- Every enum-backed value (industry, seniority, department, funding type,
  language) was resolved through the integration's autocompletes, and the
  resolution is recorded. None was written from memory.
- Each disqualifier AI Ark has a field for is a `_not` filter.
- `countCompanies` was run for every candidate filter, including the one finally
  deployed, and the counts are presented as a table the operator can read a
  decision off.
- `limit` is presented against the counted pool, with the live per-record price,
  its lookup time, the CLI version, and the resulting estimate.

## Guided handoff

- Every substantive agent message names the current phase and ends with a
  `Next step` containing one concrete decision, what it unlocks, and what stays
  blocked.
- Phase one ends by asking the operator to approve the ICP and the three
  minimum criteria (industries, company size, countries).
- Phase two ends by asking the operator to approve the filter, the `limit`, and
  the maximum spend together. Nothing is deployed or synced before that
  approval.
- The report ends on the openings (CRM coverage analysis, enrichment,
  deduplication, scoring) with one recommended, and no other offer. Without a
  CRM, the recommended opening is `account-scoring`.
- In-progress messages that need no decision say `No action needed` and name the
  next checkpoint.

## CDK template

- The agent installed and read `cargo-cdk` before sizing or adapting.
- Every resource is declared in the CDK. No imperative script sources or writes
  anything.
- Exactly one company source exists. The example is `aiArk.fetchCompanies` on
  `tam_companies`; a swapped source replaces it rather than sitting beside it.
- The sourced model carries the `industry`, `employeeSize` and
  `companyLocation` groups (or the swapped source's equivalents), an explicit
  `limit`, and **no schedule** unless the source is free per record
  (FullEnrich). A schedule on a paid source exists only under an approved
  `refresh-cadence` variation whose re-billing cost was stated, with the
  contract check edited and the reason recorded under `## Decisions`.
- The skill deploys one company source connector (AI Ark, or a source from
  `references/sources.md` with the reason recorded), one model and one folder: no CRM
  connector, no unified model, no LLM connector, and no play, agent, tool or
  segment.
- This skill declares **no** `defineContext`.
- `node --import tsx evals/contract.mjs` passes against the adapted resources.
- `cargo-ai cdk types`, `cargo-ai cdk check`, and `cargo-ai cdk plan` pass in the
  consumer project.
- The plan was shown and deployment happened only after the sizing approval.

## Results

- Exactly one sourcing run happened. Rows landed at or under `limit`, and the
  shortfall against the counted pool is explained rather than ignored.
- The report splits the landed rows by industry, size band and country, and a
  share outside the approved criteria was read and explained.
- Actual credits are reported against the estimate, with the pricing lookup
  time.
- No CRM record was created or updated.

## Repository isolation

- This is one root skill. Supporting Markdown lives under `references/`, and no
  nested `SKILL.md` exists.
- No relative import leaves the skill folder.
- The template contains no credential, deployment command, customer data, or
  hard-coded price.
