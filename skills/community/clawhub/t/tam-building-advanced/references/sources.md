# Sources

Four sources, because none of them is your market on its own. Each one gets
the same brief and searches it its own way, and that difference is the point:
a company filed under the wrong industry, ranked too low, or missing from one
database is found by another.

| Source          | Its job                              | Model                                               | How it reaches Accounts            |
| --------------- | ------------------------------------ | --------------------------------------------------- | ---------------------------------- |
| Sales Navigator | The census: every company LinkedIn files under your filters | `tam_source_sales_navigator` (`fetchAccountSearch`) | the LinkedIn company id |
| AI Ark          | Lookalikes of the customers you name | `tam_source_ai_ark` (`fetchCompanies`)              | the domain and the LinkedIn page   |
| Exa             | Search by meaning: what the website says the company does | `tam_source_exa` (`fetchSearch`) | the domain |
| Apollo          | The second census, a different database; optional | `tam_source_apollo` (`fetchOrganizations`) | the domain and the LinkedIn page   |

Every source declares its unification (`source: "custom"`, type `account`), and
Cargo merges the rows into Unify Accounts. Cargo normalises the keys itself:
`http://www.linkedin.com/company/acme` and `https://linkedin.com/company/acme/`
are one page, `https://www.acme.example/about` is `acme.example`.

**What joins Sales Navigator to the rest.** Sales Navigator returns the numeric
LinkedIn id. Apollo returns it too, as `linkedin_uid`, so a company both found
merges directly. AI Ark returns the LinkedIn page name (`/company/acme`), never
the id, and Exa returns a website: neither has anything in common with Sales
Navigator, and they reach it through Apollo only for companies Apollo also
found. The profile play's LinkedIn enrich returns the id, the page and the
domain together, and its row in `tam_accounts` unifies into the same account,
which is what makes the rest one.
That is why each source is profiled before the next one syncs.

Every source runs on Cargo credits through a managed connection, so none needs
a key in `.env`. Prices change, so this file names no number. Read the live
per-record price with `cargo-ai connection integration get <slug>` before any
sync.

## Why this order

Sales Navigator, then AI Ark, then Exa, then Apollo. The largest source goes
first and is profiled; every later source mostly merges onto accounts that
already have a profile, which costs nothing, so the play only pays for the
companies it adds. The order also gives the report its "added in this order"
column.

## Sales Navigator

- **For:** LinkedIn's own taxonomy, which is what reps see. Every row carries
  the LinkedIn company id, the strongest key an account can have.
- **Against:** one search serves at most 1,000 accounts. A market bigger than
  that is split into several searches, each under the cap: run the
  `extract-sales-navigator-search` skill, which counts, splits, merges back to
  the fewest searches and re-counts, then paste its URLs into the model. Counts
  drift week to week, so re-count right before you sync. A count costs a fixed
  fee per search.
- **Its unification is off by default.** The declaration in the model is what
  brings it into Accounts. Remove it and the census silently disappears from
  the TAM.
- **No seat:** leave `identityIds` off. Searches run on Cargo's side without a
  LinkedIn account.

## AI Ark

- **For:** `countCompanies` is free and takes the same filter groups,
  `lookalikeDomains` included, so the pool is sized before anything bills.
  `lookalikeDomains` (up to five customer domains) finds companies that look
  like your best customers, which a filter search ranks low or files elsewhere.
- **Against:** industries are enum members resolved through `listIndustries`,
  or they match nothing. A sync caps at 10,000 records.

## Exa

- **For:** it finds companies by what their website says, which is how it
  reaches the ones LinkedIn files under an industry nobody would filter on.
- **Against:** it only finds what the queries describe, and it returns the
  domain alone: no LinkedIn page, so it reaches Sales Navigator's accounts
  only through the profile play. The queries live in `exaQueries`
  (`settings.ts`, at most 50); a sync runs each one once, with `category:
  "company"` so every result is a company and its own domain. Billed per
  request plus per result past the tenth: queries × `exaResultsPerQuery` is the
  cap.
- **Queries that worked:** one per category and country, written the way a
  buyer would describe the company: "AI agent platform headquartered in
  France, 50 to 1,000 employees, selling to businesses".

## Apollo

- **For:** a different database searched with the same brief, which is what
  makes the Sales Navigator × Apollo overlap usable for the coverage estimate.
  Hiring filters (`q_organization_job_titles`, `organization_num_jobs_range`)
  and funding filters are there if your market is defined by them.
- **Against:** no industry taxonomy: industries are keyword tags, which over-
  and under-match. That is acceptable here because no source label is trusted:
  every company is classified from its own description. No free count, so
  size the pool with a small `limit` first.
- **Optional.** Run it when you want the coverage estimate, or when the
  per-source table shows the first three missed accounts you expected (the
  `apollo-as-fallback` variation in SKILL.md).

## Other sources

| Source                     | When to add it                                       | How                                                                                                                         |
| -------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| FullEnrich                 | Free per record, so a scheduled refresh costs nothing | One more source model with a declared account unification, one line in the play's filter. Edit the connector list in `evals/contract.mjs` in the same change |
| A reference list (Crunchbase export, an old TAM, a CRM list built another way) | A better coverage estimate | The `reference-list` variation in SKILL.md                                                         |
