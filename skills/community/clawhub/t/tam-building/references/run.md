# Run

Adapt the resources after copying this folder into the consumer project. The
deploy creates one model; the first sync is the only spend. Nothing in this
repository deploys.

## Phase handoffs

Every message names the current phase and ends with `Next step`. A
phase-boundary handoff carries the evidence the operator needs, one concrete
approval request, what approval unlocks, and what stays blocked. An in-progress
update says `No action needed` and names the next checkpoint.

## Deploy

1. `node --import tsx evals/contract.mjs` from this skill's folder, against the adapted
   resources.
2. `cargo-ai cdk types`, then `cargo-ai cdk check`, then `cargo-ai cdk plan`.
   Inspect every resource and action payload.
3. Confirm the plan shows one source connector (AI Ark unless swapped), one
   folder, and `tam_companies` with **no schedule** and the industries,
   company size and countries filters in its config.
4. Deploy only under the sizing approval (filter, `limit`, spend).

Resolve `workspaceUuid` from `cargo-ai whoami` (`workspace.uuid`) and the model
UUID from `cargo.state.json` or `cargo-ai storage model list`. The model link is
`https://app.getcargo.io/workspaces/<workspaceUuid>/models/<modelUuid>`.

## Source, once

Check before you sync: `cargo-ai storage run list --model-uuid <tamCompaniesUuid>`.
If the deploy already started a run, wait for it. A second run bills every
record again.

```sh
cargo-ai storage run create --model-uuid <tamCompaniesUuid>
cargo-ai storage run list --model-uuid <tamCompaniesUuid>
```

**A sync replaces the model's rows.** Verified on 2026-10-03: a model holding
7,294 rows from an earlier filter held exactly the 500 the new sync returned.
Values another skill wrote into custom columns survived only on the companies
that came back. Narrowing the filter or lowering `limit` drops every company
the new run does not return, so say so before a re-sync on a model other skills
already write to.

**A capped run is the top of AI Ark's order, not a sample.** With `limit`
below the counted pool, the verified run returned the largest companies first:
every one of the 500 sat between 387 and 500 employees, against an ICP that
starts at 50. Read the size split with that in mind, and narrow the filter
rather than lowering `limit` when you want a representative slice.

Watch the row count against `limit`. Rows landing well under `limit` means the
pool was smaller than counted, or a filter value matched nothing: check the
enum-backed values and the country names before widening anything.

## Report

Tables are `<datasetSlug>.<modelSlug>`: `cargo-ai storage dataset list` gives
the AI Ark connector's dataset, and `cargo-ai storage model get-ddl
<tamCompaniesUuid>` gives the SQL dialect. Confirm the column names with
`cargo-ai storage column list --model-uuid <tamCompaniesUuid>` rather than
assuming them.

The split the operator reads the market off, one query per dimension:

```sql
SELECT industry, COUNT(*) AS companies
FROM <aiArkDataset>.tam_companies
GROUP BY industry
ORDER BY companies DESC
```

```sql
SELECT
  CASE
    WHEN employee_count < 20 THEN 'under 20 (outside the ICP)'
    WHEN employee_count < 50 THEN '20-49'
    WHEN employee_count < 200 THEN '50-199'
    WHEN employee_count <= 500 THEN '200-500'
    ELSE 'over 500 (outside the ICP)'
  END AS size_band,
  COUNT(*) AS companies
FROM <aiArkDataset>.tam_companies
GROUP BY size_band
ORDER BY size_band
```

```sql
SELECT country, COUNT(*) AS companies
FROM <aiArkDataset>.tam_companies
GROUP BY country
ORDER BY companies DESC
```

Match the size bands to the ones in `icp.md`: the first and last band are the
ICP's own floor and ceiling, so anything that lands in them is a row the filter
should have excluded. A share outside the approved
industries, size or countries means AI Ark's classification differs from the
filter's intent: read a few of those rows before trusting the rest.

Report:

- rows landed in `tam_companies`, against `limit` and against the counted pool
- the split by industry, size band and country
- rows with no domain and no LinkedIn URL (they will be hard to match or enrich
  in any next step)
- estimated credits, actual credits (`cargo-ai billing usage get-metrics`), and
  the variance, with the pricing lookup time
- the direct Cargo link to the model

## Openings

End the report by offering what can be built on the TAM. None of these is part
of this cookbook, and each brings its own dependencies. Recommend one, based on
what the workspace already has, and let the operator pick.

| Opening                   | What the operator gets                                                                             | What it adds                                                                                                                                                                                                                                                                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CRM coverage analysis** | How much of the TAM the CRM already holds, and the net-new list: "your CRM has 60% of your market" | A CRM companies extract (`crm-enrichment` ships one as `crm_accounts`) unified with `tam_companies` into the workspace's unified `accounts` model, which matches on domain and LinkedIn by default. Each unified account's `ids` column then shows whether a CRM record sits behind it. Read the unified model's merge settings; do not change them |
| **Enrichment**            | The fields AI Ark did not return, filled                                                           | `crm-enrichment` once the accounts are in the CRM; `enrich-company-data` for a one-off pass before that                                                                                                                                                                                                                                             |
| **Deduplication**         | No duplicate accounts once the net new are pushed into the CRM                                     | `crm-deduplication`, run after the push                                                                                                                                                                                                                                                                                                             |
| **Scoring**               | The TAM tiered against the same `icp.md`, so the team knows where to start                         | `account-scoring`: an agent tiers each row of `tam_companies` A / B / C / disqualified against a rubric in the context, and writes the reason on the row                                                                                                                                                                                            |

How to pick the one to recommend:

- **The workspace has a CRM:** recommend the CRM coverage analysis first. It
  says how much of the market is already known before anything is pushed or
  enriched, and it produces the net-new list every other opening works from.
- **No CRM yet:** recommend `account-scoring`. It tiers `tam_companies` in
  place, so the team knows which accounts to work first without a CRM.

Pushing net-new accounts into the CRM is a write the operator approves on its
own, with a reviewed sample first. It is never a side effect of any opening.

## Complete when

- the plan showed one connector, one folder and `tam_companies` unscheduled
  before anything was sourced
- exactly one sourcing run happened for the approved `limit`
- the report gives rows landed, the split by industry, size band and country,
  and actual credits against the estimate
- the report ended on the openings, with one recommended
- no credential, customer data, or deploy command was written into the copied
  template
