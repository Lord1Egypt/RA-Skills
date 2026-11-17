# Configure

Everything between reading the context and asking the operator to approve a
filter. The only paid calls in this file are the research calls in step 2, and
they run only when no ICP is written down, after a yes.

## Reconcile before you edit

Reuse what the project already declares: an AI Ark connector (or the swapped
source from [`sources.md`](sources.md)) and TAM-building folders. Two resources with one slug collide at deploy. Nothing else is needed:
this cookbook carries no CRM, no LLM and no unified model.

Upgrading from the earlier tiering version of this skill: its models folder is
also named "TAM building", so creating `tam_building_models` fails with
`duplicateName`. Bind the existing folder instead of renaming it:
`cargo-ai project import folder:tam_building_models <folderUuid>`, with the
UUID from the error. The old agent, play and segments stay live until a deploy
runs with `--prune`, and that prune also deletes the old folder entry, which
now points at the same folder: retire it from state first.

This skill declares no `defineContext`: that resource is a **per-workspace
singleton** owned by the project (a scaffolded repo points it at the root
`context/`).

## 1. Read the ICP before you research one

Look in the workspace context repository for anything that already defines who
the company sells to: `icp.md`, a scoring rubric, the ICP files
`account-scoring` reads, a positioning doc. If one exists, show it to the
operator as the definition and move to sizing once they confirm it still holds.

Do not rewrite an ICP someone already wrote. If it is thin (no headcount band,
no disqualifiers), say which lines are missing and ask only for those.

## 2. Research the market when nothing is written

Three sources, in this order, each feeding the next:

| Source                        | What to read                                                                                       | Action                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| The company's website         | Homepage, product and pricing pages: who they say the product is for, and which problems they name | `parallel.extract` on the URLs, with that objective                |
| Customer stories              | The customers page and case studies: named customers, and what each bought the product to fix      | `parallel.extract` on the case-study URLs                          |
| The customers' LinkedIn pages | Industry, headcount band, headquarters, specialties, for each named customer                       | `linkedin.enrichCompanyFromDomain`, one record per customer domain |

```sh
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"parallel","actionSlug":"extract","config":{}}' \
  --records '[{"urls":["https://acme.com","https://acme.com/customers"],"objective":"Who the product is for, which problems it names, and which customers it names"}]' \
  --wait-until-finished

cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"linkedin","actionSlug":"enrichCompanyFromDomain","config":{}}' \
  --records '[{"domain":"customer-one.com"},{"domain":"customer-two.com"}]' \
  --wait-until-finished
```

Before running either, fetch the live prices
(`cargo-ai connection integration get parallel`,
`cargo-ai connection integration get linkedin`), state the total for the
number of pages and customers you plan to read, and get a yes. Keep the
customer list to the ones the site names; a customer you guessed is not
evidence.

Then write the draft `context/icp.md` from what the customers share, using
this skill's `context/icp.md` as the shape: who buys, where it came from, the
firmographics (each mapped to a filter group), the disqualifiers. Mark any line
no customer supports as a hypothesis. The operator corrects it, and the
corrected file is what gets approved.

Keep the customer domains. They are the seeds for the `lookalike-sourcing`
variation, and offering it is part of this step.

## 3. The minimum: industries, company size, countries

Before any AI Ark filter is built, settle the three criteria every TAM needs.
Each one is the floor of a dimension; without it the search has no edge there
and bills for every industry, every size, or every country up to `limit`.

| Criterion    | Where to look in `icp.md`                        | Filter group                                                       |
| ------------ | ------------------------------------------------ | ------------------------------------------------------------------ |
| Industries   | the industry line, "who buys", the disqualifiers | `industry.industry_or` (and `industry_not`), from `listIndustries` |
| Company size | the headcount line, the size disqualifiers       | `employeeSize.min_employee_count` / `max_employee_count`           |
| Countries    | the geography or countries line                  | `companyLocation.location_or` (and `location_not`)                 |

For each one:

1. **Guess it from `icp.md`** and quote the line it came from, so the operator
   checks the source rather than your reading of it.
2. **When the file does not state it**, suggest a value from what the research
   found (the customers' LinkedIn pages carry industry, headcount and
   headquarters) and label it a suggestion. With no research to lean on, ask.
   "No restriction" is an answer only when the operator gives it explicitly,
   and it is recorded as such.
3. **Show the three together** as a short proposal the operator can correct in
   one reply:

   | Criterion    | Proposed                                            | From                              |
   | ------------ | --------------------------------------------------- | --------------------------------- |
   | Industries   | software development, computer and network security | `icp.md`: "Industry: …"           |
   | Company size | 20 to 500 employees                                 | `icp.md`: "Headcount: 20 to 500"  |
   | Countries    | United States, United Kingdom, Canada               | suggested: 9 of 12 customers' HQs |

Write the confirmed values back into `icp.md` when they were suggested or
changed, so the file and the filter say the same thing. Countries in
`companyLocation` are free text (country, state or city); use full country
names and let the count in step 5 tell you whether a name matched.

## 4. Filter groups, not a flat map

This section is AI Ark's shape. If the market is better described by another
source (FullEnrich, Apollo, Sales Navigator), choose it now, before the filter
is built: [`sources.md`](sources.md) gives each one's pros, cons, and where the
three criteria live in its config.

`fetchCompanies` and `countCompanies` take the same shape: **nested groups**,
each one config key holding suffixed sub-keys.

| Group                                                                                                                                                                                                      | What it constrains                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `companyInfo`                                                                                                                                                                                              | `domain_or`, `name_or`, `linkedin_url_or`                              |
| `industry`                                                                                                                                                                                                 | `industry_or` / `industry_not`, enum-backed                            |
| `employeeSize`                                                                                                                                                                                             | `min_employee_count`, `max_employee_count`, numbers                    |
| `companyType`                                                                                                                                                                                              | `company_type_or`, for example privately held or public                |
| `employeeRole`                                                                                                                                                                                             | `employee_title_or`, the persona the company already employs           |
| `technologies`                                                                                                                                                                                             | the stack a company runs                                               |
| `funding`                                                                                                                                                                                                  | `funding_type` (enum-backed), `min_total_funding`, `max_total_funding` |
| `companyLocation`, `companyKeywords`, `productAndServices`, `naics`, `annualRevenue`, `foundedYear`, `locationCount`, `headcountGrowth`, `employeeByDepartment`, `operationLanguage`, `companySocialMedia` | the rest of the surface                                                |

Conventions inside a group:

- **`_or` includes, `_not` excludes.** Every one takes a string or an array.
  Each disqualifier in `icp.md` that AI Ark has a field for becomes a `_not`,
  so it is never sourced or paid for.
- **Enum-backed fields come from autocompletes.** `industry`, seniority,
  department, funding type and language must be valid members. Resolve them with
  `listIndustries`, `listSeniorities`, `listDepartmentsAndFunctions`,
  `listCompanyDepartments`, `listFundingTypes`, `listLanguages`. A guessed label
  matches nothing and returns an empty sync that reads like a broken connector.
  `listIndustries` returns one page of 100 and ignores the search value, so a
  valid member can be missing from what you see (`computer and network
security` is one). Count such a value on its own: a non-zero
  `countCompanies` proves it matched.
- **Numeric ranges are numbers**, not stringified numbers.
- **A flat map expresses nothing.** `{"industry": "Software"}` at the top level
  is ignored, silently, and you source the whole database up to `limit`.

`employeeRole` is worth reaching for early. "The company already employs the
persona" is usually the sharpest single ICP signal available at sourcing time,
and applying it in the filter is free.

## 5. The count-first gate

`aiArk.countCompanies` takes exactly the filter groups above, minus `limit`,
returns `{"count": N}`, and is **free**:

```sh
cargo-ai orchestration action execute --wait-until-finished \
  --action '{"kind":"connector","integrationSlug":"aiArk","actionSlug":"countCompanies","config":{}}' \
  --data '{
    "industry": {"industry_or": ["software development"]},
    "employeeSize": {"min_employee_count": 20, "max_employee_count": 500},
    "companyLocation": {"location_or": ["United States", "United Kingdom"]},
    "employeeRole": {"employee_title_or": ["Revenue Operations"]}
  }'
```

Counting is design-time work, so it stays a CLI call rather than a deployed
resource: a resource that only ever wraps one connector action is ceremony, and
the count has to happen while the filter is still being argued about.

Count every candidate, not just the final one. The useful output of this phase
is a small table the operator can read a decision off:

| Filter                  | Count | What it changes                                 |
| ----------------------- | ----- | ----------------------------------------------- |
| Industries only         | …     | the ceiling                                     |
| plus the headcount band | …     | how much of the ceiling the ICP actually claims |
| plus `employeeRole`     | …     | how many already employ the persona             |
| the proposed filter     | …     | what `limit` is a fraction of                   |

## Prices

Immediately before any preview, run `cargo-ai connection integration get aiArk`
and read the current `fetchCompanies` entry under `credits.costs`. Record the
CLI version, the lookup time, the extractor slug, and the unit price alongside
the estimate, so the post-run variance is checkable against something.

Do not write a price into any file in this skill. Prices change; a number
committed to markdown goes stale silently and gets quoted to an operator months
later.

## The approval

Present the counted pool, `limit` against it, the live unit price, and the
estimate. Stop for approval of the filter, the `limit`
and that maximum spend together: narrowing the filter and lowering the budget
are the same lever pulled in different places. That approval covers the deploy
and the first sync.

## What to edit, together

In `infra/models/tam-companies.ts`:

- `config`: the filter groups and `limit`, always including `industry`,
  `employeeSize` and `companyLocation`
- keep no `schedule`

In the project's `context/`:

- `icp.md`, in the operator's own language

## Complete when

- the ICP came from the context repo, or was researched with approved spend and
  written to `context/icp.md`
- industries, company size and countries were proposed from `icp.md` (or
  suggested and labelled), confirmed by the operator, and written back to it
- every filter group is nested and every enum-backed value came from an
  autocomplete
- `countCompanies` was run for each candidate filter and the numbers are recorded
- `limit` is at or below the counted pool and the operator has seen the estimate
