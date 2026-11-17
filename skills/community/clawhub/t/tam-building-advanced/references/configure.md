# Configure

Everything between reading the context and asking the operator to approve the
sources. The paid calls here are the Sales Navigator counts and, when no ICP is
written down, the research; each runs after a yes.

## Reconcile before you edit

Reuse what the project already declares: the source connectors, LinkedIn, and
folders with the same slugs. Two resources with one slug collide at deploy.

**Unify Accounts.** The workspace must have it (`cargo-ai storage model list`,
extractor `unifyAccounts`): it exists once a system of record is connected,
and a deploy cannot create it. If another pipeline in the project already
declares `accounts` (`readiness-scoring`, `account-scoring`'s
`unified-account`), import that declaration and delete this skill's
`infra/models/accounts.ts`. Never add columns or a schedule to it from this
skill: the declaration would become the whole list.

**The CRM.** Find the CRM's companies model (`cargo-ai storage model list`)
and check that it unifies into Unify Accounts: read one account's `ids` and
look for its key (`hubspot___companies`, `salesforce___account`). HubSpot and
Salesforce companies unify by default. A CRM that does not unify makes every
company look net new: fix its unification before you report.

This skill declares no `defineContext`: that resource is a per-workspace
singleton owned by the project.

## 1. The ICP and the three criteria

Read the workspace context for an ICP first (`context/icp.md`, a scoring
rubric, anything `account-scoring` reads). Show it, and move on once the
operator confirms it still holds. When nothing is written, follow
`tam-building`'s research step: the website, the customer stories, and the
customers' LinkedIn pages, after their live prices are stated and approved.

Settle **industries, company size and countries** before any filter is built,
each quoted from `icp.md` or labelled as a suggestion. They are written into
all four sources and into `infra/settings.ts`, so the sources and the gates
say the same thing.

## 2. Your categories

Every company is classified from its own description into a list you own, not
into a provider's industry label. Derive the list before you ask for it:

1. **The CRM's industry field.** If a CRM is connected, read the picklist of
   its company industry property and propose those values. The TAM, the CRM
   and the reports then use the same words.
2. **`icp.md`.** Otherwise, the categories section of the ICP.
3. **Ask** only when neither exists.

Write them into `inScopeCategories` in `infra/settings.ts` and the categories
section of `icp.md`. Keep `outOfScopeCategories` and `unknownCategory`: they
are what a company can be instead, and "Not enough information" is a
coverage gap, flagged for review rather than dropped.

## 3. Translate the brief into each source

| Criterion    | Sales Navigator (URL filters) | AI Ark (`config`)                            | Apollo (`config.filters`)             | Exa (query text)          |
| ------------ | ----------------------------- | -------------------------------------------- | ------------------------------------- | ------------------------- |
| Industries   | `INDUSTRY` ids                | `industry.industry_or`, from `listIndustries` | `q_organization_keyword_tags`         | the category, in words    |
| Company size | `COMPANY_HEADCOUNT` bands     | `employeeSize.min_employee_count` / `max_…`  | `organization_num_employees_ranges` ("51,200") | "50 to 1,000 employees" |
| Countries    | `REGION` ids                  | `companyLocation.location_or`                | `organization_locations`              | "headquartered in France" |

- **Sales Navigator:** build the search in Sales Navigator or from the
  filters, count it, and if it is over 1,000 accounts run the
  `extract-sales-navigator-search` skill to split it. Paste every URL it
  returns into `urls`. Every URL must carry `INDUSTRY`, `COMPANY_HEADCOUNT`
  and `REGION`; the contract checks.
- **AI Ark:** nested groups, never a flat map. Add up to five customer domains
  to `lookalikeDomains`: the customers the context names, or the CRM's
  closed-won companies. Count it with `countCompanies`, which is free:

  ```sh
  cargo-ai orchestration action execute --wait-until-finished \
    --action '{"kind":"connector","integrationSlug":"aiArk","actionSlug":"countCompanies","config":{}}' \
    --data '{"industry":{"industry_or":["software development"]},"employeeSize":{"min_employee_count":51,"max_employee_count":1000},"companyLocation":{"location_or":["France"]},"lookalikeDomains":["customer-one.example"]}'
  ```

- **Apollo:** the same brief in its filters. There is no free count: deploy
  with a small `limit`, read what comes back, then widen.
- **Exa:** write one query per category and country into `exaQueries` in
  `infra/settings.ts`. Seven categories in eight countries is 56 queries;
  start with the categories you expect providers to file elsewhere.

## 4. The budget

Each paid source has its own `limit`. Present, for each source: the counted
or sampled pool, its `limit`, the live per-record price, and the estimate.
Then the profile: every distinct company costs one LinkedIn enrich and one
classification, once, however many sources found it. Estimate it on the
expected number of distinct companies, not on the sum of the sources. Fetch every
price immediately before presenting it:

```sh
cargo-ai connection integration get salesNavigator
cargo-ai connection integration get aiArk
cargo-ai connection integration get apolloio
cargo-ai connection integration get exa
cargo-ai connection integration get linkedin
```

Do not write a price into any file in this skill. Stop for one approval that
covers the filters, the four limits and the maximum spend.

## Complete when

- the ICP came from the context, or was researched with approved spend, and
  the three criteria are confirmed and written into all four sources and
  `settings.ts`
- the categories came from the CRM's industry field or `icp.md`, and are in
  `settings.ts`
- every Sales Navigator URL is under 1,000 accounts and carries the three
  filters
- AI Ark was counted with its lookalike seeds; Apollo has a small first limit
- the operator approved the filters, the limits and the maximum spend together
