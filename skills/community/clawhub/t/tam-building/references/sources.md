# Sources

AI Ark is the example source because it is the only company search in the
catalog that **counts for free with the same filters it bills on**. It is not
the only good one. Pick the source whose filters describe your market, then
keep exactly one: a swapped source replaces `infra/connectors/ai-ark.ts` and
the extractor on `infra/models/tam-companies.ts`. It does not sit beside them.

Every source below runs on Cargo credits through a managed connection, so none
needs a key in `.env`. Prices change, so this file names only the cost class.
Read the live per-record price with `cargo-ai connection integration get <slug>`
(the extractor's entry under `credits.costs`) before any preview.

## Model sources the contract supports

`evals/contract.mjs` knows these four. For each one it checks the extractor and
the config path of the three minimum criteria: industries, company size and
countries.

| Source                             | Extractor            | Industries · size · countries                                                                                          | Per record          | Cap per sync |
| ---------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------ |
| AI Ark (`aiArk`), the default      | `fetchCompanies`     | `industry` · `employeeSize` · `companyLocation`                                                                        | low                 | 10,000       |
| FullEnrich (`FullEnrich`)          | `fetchCompanies`     | `industry` · `headcount` · `headquarters`                                                                              | free                | 10,000       |
| Apollo (`apolloio`)                | `fetchOrganizations` | `filters.q_organization_keyword_tags` · `filters.organization_num_employees_ranges` · `filters.organization_locations` | low                 | 50,000       |
| Sales Navigator (`salesNavigator`) | `fetchAccounts`      | `industryCodes` · `companyHeadcounts` · `headquarterLocationIds`                                                       | highest of the four | 5,000        |

### AI Ark

- **For:** `countCompanies` is free and takes the same filter groups, so every
  candidate filter has a pool size before anything bills. It has the widest
  filter surface here: `employeeRole` (the company already employs the
  persona), `headcountGrowth`, `employeeByDepartment`, `technologies`,
  `funding`, and `lookalikeDomains` (up to five seed customers, accepted by
  both the count and the extractor). Rows carry a domain.
- **Against:** industries, seniorities, departments and funding types are enum
  members you must resolve through the autocompletes, or they match nothing.
  It bills per returned record, so the 10,000 cap means a bigger market is
  split into separately counted syncs.

### FullEnrich

- **For:** it is free per record. That changes the economics of this skill:
  sourcing stops being the spend, and a `refresh-cadence` schedule re-runs
  at no charge. It is the one source the contract allows a schedule on. Filters are plain strings (`industry`, `headcount`
  `{min, max}`, `headquarters`, `technologies`, `specialties`, `keywords`),
  with no autocomplete step.
- **Against:** it has no count action. Size the pool with a small `limit`
  first (free, but slower than a count, and it caps at what you pulled). The
  filter surface is narrower than AI Ark's: no persona, funding, growth or
  lookalike filter. Plain-string industries are matched as text, so read a
  sample before you trust a large pull.

### Apollo

- **For:** it has the largest cap per sync (50,000), and it is the only source
  here with **hiring filters** (`q_organization_job_titles`,
  `organization_num_jobs_range`, `organization_job_posted_at_range`), next to
  funding amount and date, revenue, and technologies. It suits a TAM defined
  by "is staffing X right now".
- **Against:** there is no industry taxonomy. Industries go through keyword
  tags, which are fuzzy and both over- and under-match, so read a sample per
  tag. Employee ranges are strings in Apollo's own `"min,max"` format,
  technologies are Apollo UIDs, and there is no free count in Cargo, so size
  the pool with a small `limit` first. All filters sit under one `filters`
  object rather than in nested groups.

### Sales Navigator

- **For:** it uses LinkedIn's own taxonomy, which is what reps see when they
  open an account. It has filters nothing else has: department headcount and
  its growth, spotlights, and Fortune ranking. Use it when the market is
  easier to describe in LinkedIn's terms than as firmographics.
- **Against:** it is the most expensive per record of the four.
  Filters take LinkedIn's internal codes, not names. It returns **no domain**,
  so every later step that keys on a website pays to resolve one. The cap is
  5,000 per search, and a count (`searchCompanyMetrics`) costs a fixed fee
  rather than nothing. Use `fetchAccounts` with codes: `fetchAccountSearch`
  takes saved-search URLs, and the contract cannot see the three criteria
  inside a URL.
- **No seat:** leave `identityIds` off. Searches run on Cargo's side without a
  LinkedIn account, and running through someone's own account puts it at risk
  of being restricted.

## Other sources, and why they are not the default

| Source                                                                                     | What it is good at                                                                             | Why not the TAM model                                                                                                                                      |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| People Data Labs (`peopleDataLabs.fetchCompanies`)                                         | Deep company records and a query language (`filter`, `query`) that can express almost anything | By far the highest price per record in this list, which is a poor fit for sourcing a whole market. Use it to enrich a slice, not to source                 |
| TheirStack (`theirStack.fetchCompanies`)                                                   | Tech stack and hiring, both read from job posts                                                | Firmographics are secondary. Use it when the TAM really is "companies running X" (see `find-companies-using-tech`), not as the general universe            |
| Ocean.io (`oceanio.searchCompanies`), CompanyEnrich (`companyEnrich.findSimilarCompanies`) | Lookalikes from seed customers                                                                 | Actions only, with no extractor, so they cannot back a model. Use them during research to find seeds, then feed those seeds to AI Ark's `lookalikeDomains` |

## How to choose

- **You need the pool size before you commit:** AI Ark. It is the only free
  count.
- **Budget is the constraint, or you want a scheduled refresh:** FullEnrich.
  Accept the narrower filters.
- **The market is defined by hiring or funding:** Apollo.
- **The market is defined by LinkedIn facets:** Sales Navigator. Budget for the domain resolution that follows.

Whichever you pick, the rest of the skill does not change. The ICP comes from
`context/icp.md`, the three minimum criteria are confirmed first, the pool is
sized before the sync, and there is one approval for filter, `limit` and spend.
Record the choice and the reason under `## Decisions`.
