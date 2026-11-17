# The CRM audit

The audit has two halves, and neither is a script. The platform extracts the CRM into three models;
the agent reads them with the fixed SQL in `infra/agents/win-loss-analyst.prompt.ts`. This file is
what each model holds, how the queries read it, and how to move to another CRM.

## The models

| Model          | Extractor                     | What it holds                                                                                                                        |
| -------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `crm_deals`    | `fetchRecords` on `deals`     | Every deal, open and closed, all columns. The queries narrow to closed deals (won or lost) and never select an amount                |
| `crm_accounts` | `fetchRecords` on `companies` | Every company, all columns. Declared as crm-enrichment and crm-deduplication declare it                                              |
| `crm_contacts` | `fetchRecords` on `contacts`  | Every contact, all columns. Declared as crm-enrichment and crm-deduplication declare it. The audit reads titles and company ids only |

Columns are named after the HubSpot properties. In SQL a model is `<dataset>.<model>`, and a
connector-backed model's dataset is its connector's slug, so the queries read `crm.crm_deals`,
`crm.crm_accounts` and `crm.crm_contacts`. Extraction bills no credits, and all three sync
hourly, as the other CRM cookbooks sync theirs. No model filters in its config: pull everything,
narrow in the query.

## The queries

Each has a name, and every `[R: <name>, n of N]` tag in the context files cites one. The run record
under `outputs/` holds each result.

| Query                    | What it answers                                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------------------------- |
| `pipelines`              | Won and lost per pipeline in the window. More than one pipeline is the one question the operator gets |
| `lost_reasons`           | Each lost reason and its count. The empty reason's count is the hygiene finding's complement          |
| `contacts_on_deals`      | Won, lost, and deals with at least one contact: the association rate                                  |
| `by_industry`            | Won and lost per account industry                                                                     |
| `by_size`                | Won and lost per employee band                                                                        |
| `by_country`             | Won and lost per account country                                                                      |
| `titles_at_won_accounts` | Each job title and the number of won accounts it appears at                                           |
| `deals_since`            | Every deal closed since the last run, with its account: ids for receipts, accounts for `client/`      |

`<window start>` is the window's first day; `<since>` is the date of the last merged run record, or
the window start on the first pass. The agent substitutes those two and nothing else.

## Reading the numbers

- Fewer than `VERIFY_MIN_WON` wins in the window means hypothesis mode: every finding carries its
  denominator and `confidence: hypothesis`.
- A lost-reason fill rate of 0 with lost deals in the window is almost always a custom property, not
  a team that never records reasons. Find it and set `LOST_REASON_COLUMN`.
- An association rate well under the closed count means titles are a sample, and the persona
  reconciliation says so with the denominator.
- Titles are read at the won accounts, through `crm_contacts.associatedcompanyid`: everyone at the
  account, not only the people on the deal. The `deal_contacts` variation narrows it.
- Zero won with deals you know closed means the flags are typed differently on this portal (a
  boolean rather than the string `'true'`). Change the comparison in the prompt once.

## Another CRM

The connector, the three models' config and the queries change together; the prompt's rules do
not.

- **Salesforce:** `Opportunity` with `IsClosed`, `IsWon`, `CloseDate`, `StageName`, `AccountId`
  for `crm_deals`; `Account` and `Contact` for the other two. Lost reasons are usually a custom
  field (`Loss_Reason__c` or similar). Titles at won accounts join `Contact.AccountId`; titles on the
  opportunity itself come from `OpportunityContactRole`.
- **Attio:** the `deals` object with its stage or status attribute, `companies`, and `people`. The
  lost reason is whatever attribute the workspace keeps it in.

Read each object's live fields before writing a query, and check the first pass by eye: field names
vary per org far more than on HubSpot.
