# Run

Deploy, then source and profile one source at a time, then report. **Deploying
a source model starts its first sync**: that is the sourcing spend, and it is
what the budget approval covers. Deploy the sources one at a time for that
reason (comment out the ones not yet due). The profile play is a build step:
no schedule, never enabled, run as a batch after each source sync, so nothing
is enriched or classified until you run it.

## Phase handoffs

Every message names the current phase and ends with `Next step`. A phase
boundary carries the evidence, one concrete approval request, what it unlocks
and what stays blocked. An in-progress update says `No action needed` and names
the next checkpoint.

## Deploy

1. `node --import tsx evals/contract.mjs` from this skill's folder, against the
   adapted resources.
2. `cargo-ai project types`, then `cargo-ai project check`, then
   `cargo-ai project plan`. Confirm the plan shows the connectors, the source
   models with **no schedule** and their unification, `tam_accounts`, Unify
   Accounts **adopted with no column or schedule change**, and the one play
   **disabled, with no schedule**.
3. Deploy only under the budget approval, Sales Navigator's model first.

**Deployed before 0.3.0?** The profile model was `tam_companies`, keyed on
`linkedin_company_id`. The plan now creates `tam_accounts` and leaves the old
model in place: a deploy never deletes. Delete `tam_companies` by hand once
the profile batch has filled `tam_accounts`, or its rows keep unifying into
Accounts next to the new ones.

Resolve `workspaceUuid` from `cargo-ai whoami` and each UUID from
`cargo.state.json`. A model link is
`https://app.getcargo.io/workspaces/<workspaceUuid>/models/<modelUuid>`.

## Source and profile, one source at a time

**Sales Navigator, then AI Ark, then Exa, then Apollo.** Profile each source's
accounts before the next one syncs: the next source's rows then merge onto
accounts that already carry a profile, and the play only pays for the
companies that source adds.

For each source:

1. **The rows landed.** `cargo-ai storage run list --model-uuid <sourceUuid>`
   shows the sync finished. Do not start a second one: it bills every record
   again.
2. **Accounts merged them.** Refresh Unify Accounts
   (`cargo-ai storage run create --model-uuid <accountsUuid>`, then poll
   `storage run list`). Refreshing rebuilds the merge; it never re-runs a
   source's search, so it bills nothing. Then count the source's accounts:

   ```sql
   SELECT COUNT(*) FROM object.accounts
   WHERE JSON_QUERY(ids, '$.sales_navigator___tam_source_sales_navigator') IS NOT NULL
   ```

   The key is `<dataset slug>___<model slug>` (`sales_navigator___…`,
   `ai_ark___…`, `exa___…`, `apolloio___…`, `object___…` for native models). The dataset
   slug is not always the connector slug: read one account's `ids` and use
   the keys you see in every query below. A brand-new company can take up to half an
   hour to appear. Wait until the count matches the source's row count, give
   or take the duplicates inside the source.
3. **Pilot five.** Read the play's deployed filter: `cargo-ai orchestration
   play list` gives the play's `workflowUuid` and `segmentUuid`, and
   `cargo-ai segmentation segment get <segmentUuid>` gives the filter with
   every model reference resolved. Run the workflow on five accounts:

   ```sh
   cargo-ai orchestration batch create --workflow-uuid <playWorkflowUuid> \
     --data '{"kind":"filter","modelUuid":"<accountsUuid>","filter":<the play filter>,"limit":5}' \
     --wait-until-finished
   ```

   Read the five `tam_accounts` rows: category, `computed__status`,
   `computed__exclusion_reason`, domain. A wrong category here is a wrong
   category on every row.
4. **The rest.** The same batch without `limit`. The play stays disabled: it
   is run, not left running. `runCreationRule: "once"` keeps an account from
   being profiled twice, so the same batch after a later source or a refresh
   pays only for the companies that are new.
5. **Done when** no account a source found is left without a profile: the
   play's filter returns nothing, or only accounts whose LinkedIn page could
   not be read (the play returns `unresolved` for them; read a few).

## Refresh

Every three to four months is enough. By hand: re-count Sales Navigator,
re-sync the sources in the same order, run the profile batch after each. On
its own: the `refresh` variation in SKILL.md (a quarterly cron on each paid
source, and on the play the day after). Either way, a company the TAM already
holds is merged and costs only its source record; the profile is paid only for
the companies that are new.

## Report

Confirm the SQL dialect first: `cargo-ai storage model get-ddl <accountsUuid>`.
Every query reads one view of the TAM: the accounts a TAM source found, with
which sources found them, whether the CRM holds them, and their profile.
Replace the CRM key with yours (`hubspot___companies`, `salesforce___account`).

```sql
WITH tam AS (
  SELECT
    a._id AS account_id,
    JSON_QUERY(a.ids, '$.sales_navigator___tam_source_sales_navigator') IS NOT NULL AS sales_navigator,
    JSON_QUERY(a.ids, '$.ai_ark___tam_source_ai_ark') IS NOT NULL AS ai_ark,
    JSON_QUERY(a.ids, '$.exa___tam_source_exa') IS NOT NULL AS exa,
    JSON_QUERY(a.ids, '$.apolloio___tam_source_apollo') IS NOT NULL AS apollo,
    JSON_QUERY(a.ids, '$.hubspot___companies') IS NOT NULL AS in_crm,
    JSON_VALUE(a.ids, '$.object___tam_accounts[0]') AS profile_id
  FROM object.accounts a
),
universe AS (
  SELECT tam.*, c.linkedin_id, c.name, c.domain, c.category,
         c.computed__status AS status, c.computed__exclusion_reason AS exclusion_reason
  FROM tam
  LEFT JOIN object.tam_accounts c ON c._id = tam.profile_id
  WHERE sales_navigator OR ai_ark OR exa OR apollo
)
SELECT status, COUNT(*) AS companies FROM universe GROUP BY status ORDER BY companies DESC
```

Keep the two CTEs and swap the last `SELECT`:

**Net new against the CRM.** The number the operator acts on:

```sql
SELECT
  COUNTIF(status = 'in_scope') AS tam,
  COUNTIF(status = 'in_scope' AND in_crm) AS already_in_crm,
  COUNTIF(status = 'in_scope' AND NOT in_crm) AS net_new
FROM universe
```

**What each source added.** Found, and found by no other source. Read them
together: "found by no other source" does not depend on the order, and it is
what you would lose by dropping the source. "Added in this order" is the same
count taken in the order the sources ran.

```sql
SELECT
  COUNTIF(sales_navigator) AS sales_navigator_found,
  COUNTIF(sales_navigator AND NOT ai_ark AND NOT exa AND NOT apollo) AS sales_navigator_only,
  COUNTIF(ai_ark) AS ai_ark_found,
  COUNTIF(ai_ark AND NOT sales_navigator AND NOT exa AND NOT apollo) AS ai_ark_only,
  COUNTIF(exa) AS exa_found,
  COUNTIF(exa AND NOT sales_navigator AND NOT ai_ark AND NOT apollo) AS exa_only,
  COUNTIF(apollo) AS apollo_found,
  COUNTIF(apollo AND NOT sales_navigator AND NOT ai_ark AND NOT exa) AS apollo_only,
  COUNTIF(ai_ark AND NOT sales_navigator) AS ai_ark_added,
  COUNTIF(exa AND NOT sales_navigator AND NOT ai_ark) AS exa_added,
  COUNTIF(apollo AND NOT sales_navigator AND NOT ai_ark AND NOT exa) AS apollo_added
FROM universe
WHERE status = 'in_scope'
```

**What each source returned that was not your market.** Read it as each
source's noise, not as a ranking:

```sql
SELECT
  CASE WHEN sales_navigator THEN 'sales_navigator' WHEN ai_ark THEN 'ai_ark'
       WHEN exa THEN 'exa' ELSE 'apollo' END AS first_source,
  exclusion_reason, COUNT(*) AS companies
FROM universe
WHERE status != 'in_scope'
GROUP BY first_source, exclusion_reason
ORDER BY first_source, companies DESC
```

**Merges to read.** An account holding two profiles is two LinkedIn pages
Cargo joined through a shared key: usually a source that gave a page the
parent's domain (live: AI Ark's "Orisha Retail Shops" page with `orisha.com`
landed on the Orisha group's account, flagged as a subsidiary). Read each one;
fix the key on the row that carries it when the merge is wrong.

```sql
SELECT _id, ids
FROM object.accounts
WHERE JSON_QUERY(ids, '$.object___tam_accounts[1]') IS NOT NULL
```

**The coverage estimate.** You cannot count the companies no source found, but
two lists built independently estimate them: if Sales Navigator found 73% of
the companies Apollo found, it probably found about 73% of the market. The
formula is `market ≈ found by A × found by B ÷ found by both`
(capture-recapture, the method ecologists use to count fish).

```sql
SELECT
  COUNTIF(sales_navigator) AS a,
  COUNTIF(apollo) AS b,
  COUNTIF(sales_navigator AND apollo) AS both_lists,
  SAFE_DIVIDE(COUNTIF(sales_navigator) * COUNTIF(apollo),
              COUNTIF(sales_navigator AND apollo)) AS estimated_market
FROM universe
WHERE status = 'in_scope'
```

Sales Navigator and Apollo are the pair because both are census searches of
the same brief in different databases. AI Ark (seeded by your customers) and
Exa (written queries) are not trying to enumerate the market, so they would
skew it. Report it as a floor: both lists favour companies that are easy to
see, and the hidden ones are hidden from both. Then coverage is
`tam ÷ estimated_market`. Below a few hundred companies in the overlap, say
the estimate is too thin to quote. Without Apollo, there is no estimate unless
a `reference-list` replaces it.

**How many sources found each company.** Companies several sources agree on
are, in our own build, more often the accounts you want. Keep the split for
`account-scoring`:

```sql
SELECT
  CAST(sales_navigator AS INT64) + CAST(ai_ark AS INT64)
  + CAST(exa AS INT64) + CAST(apollo AS INT64) AS sources,
  COUNT(*) AS companies
FROM universe
WHERE status = 'in_scope'
GROUP BY sources
ORDER BY sources
```

The report gives, in this order:

- the headline: "N companies in your TAM, X net new, Y already in your CRM"
- the funnel by status, and the exclusion reasons by source
- per source: found, found by no other source, added in order
- the coverage estimate with its floor caveat, or why it is too thin
- the split by number of sources
- the merges read, and what was fixed
- actual credits against the estimate (`cargo-ai billing usage get-metrics`),
  with the pricing lookup time
- the links to Unify Accounts, `tam_accounts` and the four sources

## Openings

End by offering what can be built on the TAM, and recommend one:

| Opening                 | What the operator gets                                                                 |
| ----------------------- | -------------------------------------------------------------------------------------- |
| **Score it**            | `account-scoring` tiers the in-scope rows; compare the tiers by number of sources      |
| **Push the net new**    | The net-new accounts created in the CRM: a write the operator approves on its own, with a reviewed sample first. Never a side effect of this skill |
| **Enrich**              | `crm-enrichment` once the accounts are in the CRM                                      |
| **Review the gaps**     | The `needs_review` rows (thin pages, missing size or country), read by a person         |

## Complete when

- the plan showed the sources unscheduled, Unify Accounts unchanged and the
  play disabled before anything was sourced
- each source was synced once, merged and profiled before the next one started
- every account a TAM source found has a profile, or was read as unresolved
- the report gives the headline with net new and already in the CRM, the
  per-source table, the coverage estimate or why it is too thin, the merges
  read, and actual credits against the estimate
- the report ended on the openings, with one recommended
- nothing was written to the CRM
