# Working File Templates — Salesforce API Integration

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/salesforce-api-integration/config.yaml` | Key by key, read-modify-write |
| Org context, schema map, integrations, saved queries, gotchas, observed limits, due dates, box index | `~/Clawic/data/salesforce-api-integration/memory.md` | Rewritten in place; stays small |
| Orgs: alias, type, instance URL, API version, auth flow, credential pointer | `## Org Context` in `memory.md` while there is one; `~/Clawic/data/salesforce-api-integration/orgs.md` from the second | One row per org, sandboxes included |
| One line per object the user works with: API name, key fields, external id, quirks | `## Schema Map` in `memory.md` | One row per object |
| The full field table for an object that needed describing | `~/Clawic/data/salesforce-api-integration/schema/<object-api-name>.md` | Born as its own file, from the first describe |
| SOQL and report ids worth reusing | `## Saved Queries` in `memory.md` | One row per query |
| An error whose cause took work to find, and what fixed it | `## Gotchas` in `memory.md` | One row per cause |
| Observed allocations, usage peaks, storage | `## Limits Observed` in `memory.md` | Rewritten with the newer reading |
| Bulk loads, exports and metadata deploys that ran | `~/Clawic/data/salesforce-api-integration/loads/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — integration designs, field mappings, migration plans, runbooks | `~/Clawic/data/salesforce-api-integration/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A person: client, org admin, the sysadmin who owns the Connected App | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's contacts in one file |
| A migration or integration the user tracks as a piece of work | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| Salesforce edition, license count and what it costs | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row, amount with currency inside the value |
| **Anything durable this table does not name** | `~/Clawic/data/salesforce-api-integration/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Access tokens, client secrets, private keys, passwords, security tokens | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something new goes, in order: **would another skill want to read it?** → shared box. **Is it a text read whole when its subject comes up** (design, mapping, runbook, policy)? → `artifacts/`. **Is it one more row of something that accumulates?** → a section of `memory.md` until the threshold, then its own box.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| An org was connected, refreshed, or its instance URL changed | Its row in `## Org Context` (or `orgs.md`) |
| An object was described, or a custom field or external id turned up | `## Schema Map`, plus `schema/<object>.md` if the full field table was needed |
| A SOQL query or a report id proved worth keeping | `## Saved Queries` |
| A bulk load, export or metadata deploy ran | `loads/<year>.md` |
| An error's real cause was found | `## Gotchas` |
| `/limits` was read, or usage came close to a ceiling | `## Limits Observed` |
| An integration design, field mapping, migration plan or runbook came out of the session | `artifacts/` |
| A certificate, secret rotation, sandbox refresh or version review was scheduled or done | `## Due` |
| A person was named as owner, admin or client | `~/Clawic/data/contacts/contacts.md` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, per-object schema files, load records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. **Who and when**: the agent about to append counts the section's entries **before** adding the one that would cross the line.
2. **Threshold**: past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count, and in tables the entry count rules — then, in the same turn: create the new file in `~/Clawic/data/salesforce-api-integration/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. **Identical headings on both sides** of the move, so the split is a copy-paste and never a rewrite.
4. **Precedence**: never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts and per-object schema files are the exception: they are born as their own file whatever their size, because each is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:SF_ACCESS_TOKEN` · `env:SF_CLIENT_SECRET` · `keychain:sf-prod` · `1password:Work/Salesforce/prod` · `vault:secret/sf/prod` · `file:~/.certs/sf-jwt.key` · `profile:sf-prod`

When the user pastes something to save — a `.env`, a token response, a curl command with credentials in it, an Apex snippet with a hardcoded key — replace each secret value before writing and leave the pointer visible: `client_secret: <keychain:sf-prod>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: org id and instance URL, My Domain name, Connected App name and Consumer Key (public by design), record ids and 3-char prefixes, object and field API names, external id field names, profile and permission set names, integration usernames, job ids, report ids, API version. **Secrets, strip them**: access and refresh tokens, session ids, Consumer Secret, JWT private keys and their passphrases, user passwords, the security token appended to a password, signed request payloads, Named Credential passwords, and any `sfdx-url`/auth URL, which contains a refresh token in plain text.

Also strip **record data**: memory files hold schema and counts, never the rows themselves. Any field named in `pii_fields` is replaced by `<redacted>` even in an example.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [schema/](#schema) · [artifacts/](#artifacts) · [loads/](#loads) · [shared boxes](#shared-boxes) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/salesforce-api-integration/` if it does not exist.

```yaml
api_version: v62.0
default_org: prod
auth_flow: jwt-bearer
code_style: python
bulk_threshold: 5000
all_or_none: true
sandbox_first: true
pii_fields: [Contact.Email, Contact.Phone, Lead.Email]

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  sdk: simple-salesforce
  deploy: sf-cli
conventions:
  external_id_suffix: _Ext_Id__c
  csv_date_format: "YYYY-MM-DDThh:mm:ssZ"
safety_posture:
  hard_delete: forbidden
  bypass_validation_rules: ask-first
sync_posture:
  poll_minutes: 15
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Salesforce Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Orgs (3: prod, uat, dev) → `orgs.md`; read before any call, to pick the instance URL
- Opportunity field table → `schema/Opportunity.md`; read before writing any Opportunity query or load
- NetSuite → Salesforce sync design → `artifacts/sync-netsuite-accounts.md`; read whenever the nightly sync is the subject
- Load history (2026) → `loads/2026.md`; read before repeating a load, to reuse its mapping and row counts

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| API version review | Salesforce release (~4 months) | 2026-06-10 | 2026-10-10 |
| JWT signing cert expiry | year | 2026-03-02 | 2027-03-02 |
| Full sandbox refresh | 29 days minimum | 2026-07-04 | 2026-08-02 |
| Integration user FLS audit | quarter | 2026-04-15 | 2026-07-15 |
| API usage check | week | 2026-07-20 | 2026-07-27 |

## Org Context
prod — Enterprise Edition, ~40 licenses, My Domain acme, heavy Apex on Opportunity.

## Schema Map
| Object | API name | External id | Notes |
|--------|----------|-------------|-------|
| Account | Account | `ERP_Id__c` | Person accounts off; 6 required custom fields |
| Opportunity | Opportunity | none | Trigger recalculates Amount on insert — never trust the value you sent back |
| Shipment | `Shipment__c` | `Tracking_No__c` | Master-detail to Account, so reparenting is blocked |

## Integrations
| Name | Direction | Mechanism | Objects | Owner |
|------|-----------|-----------|---------|-------|
| Nightly ERP sync | in | Bulk 2.0 upsert on `ERP_Id__c` | Account, `Shipment__c` | Dana (see contacts) |
| Warehouse feed | out | CDC → Pub/Sub | Opportunity, Account | us |

## Saved Queries
| Purpose | Kind | Query or id | Notes |
|---------|------|-------------|-------|
| Open pipeline this quarter | SOQL | `SELECT Id, Name, Amount, StageName FROM Opportunity WHERE IsClosed = false AND CloseDate = THIS_QUARTER` | Selective on CloseDate |
| Weekly pipeline report | Report | `00O5g000004abcd` | 2,000-row ceiling reached in Q2 — use the SOQL above instead |

## Gotchas
| Symptom | Real cause | Fix |
|---------|-----------|-----|
| `INVALID_FIELD: Discount__c` on a field visible in the UI | Integration user's permission set lacks FLS read | Added to Integration User PS 2026-05-02 |
| Bulk Contact update fails ~15% with `UNABLE_TO_LOCK_ROW` | Parallel chunks touching the same Account | Sort the CSV by AccountId before upload |

## Limits Observed
| Reading | Value | As of |
|---------|-------|-------|
| Daily API requests, allocation | 55,000 | 2026-07-20 |
| Daily API requests, typical use | ~12,000 (peaks 31,000 on load days) | 2026-07-20 |
| Data storage used | 41% | 2026-07-01 |

## How They Work
Runs everything from Python. Wants the SOQL and the call count, not the theory.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Certificate and secret expiries belong here the day they are created; a JWT integration dies silently at cert expiry, and nothing warns you.
- **`## Org Context` / `orgs.md`**: never a token, only its pointer. Sandbox usernames are the production username plus `.<sandboxname>` — worth recording, because it is the most common cause of a login that "should work".
- **`## Schema Map`** is the index; a full field table lives in `schema/<object>.md`. The map's `Notes` column is for behaviour a describe cannot show: triggers that rewrite values, master-detail relationships, required fields the UI defaults but the API does not.
- **`## Limits Observed`**: `As of` is the day the number was read, and a new reading **overwrites** the row rather than adding one. Allocations change with license count.
- These headings are exactly the ones the split-out files get, so the split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their org |
| `complete` | Know their org, objects and integrations well |

## schema/

One file per object, at `~/Clawic/data/salesforce-api-integration/schema/<object-api-name>.md`, created the first time a full describe was needed. It exists so the next session does not spend a describe call and a re-read on the same 200-field object.

```markdown
# Opportunity — field map
*Read before writing any Opportunity query, load or mapping. Described against v62.0 on 2026-07-26, org: prod.*

| API name | Type | Req | Notes |
|----------|------|-----|-------|
| Name | string(120) | yes | |
| StageName | picklist | yes | Values: Prospecting, Qualification, Proposal, Closed Won, Closed Lost |
| CloseDate | date | yes | Indexed; the selective filter for this object |
| Amount | currency | no | Overwritten by a trigger on insert |
| ERP_Deal__c | string(40) | no | External Id + Unique — upsert target |

Compound fields (none here) · Record types: Direct, Partner · Child relationships: OpportunityLineItems, Notes
```

Re-describe when a field error appears or the org's release changed; overwrite the file and update the date line. Field *values* never go in here — this is schema, not data.

## artifacts/

One file per thing, at `~/Clawic/data/salesforce-api-integration/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **integration design**, **field mapping**, **migration plan**, **runbook for a recurring failure**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Field mapping — HubSpot → Salesforce
*Read before any run of the HubSpot import, and before changing either schema. 2026-07-26.*

| Source field | Target | Transform | Notes |
|--------------|--------|-----------|-------|
| company.domain | `Account.ERP_Id__c` | lowercase | external id, upsert key |
| deal.amount | Opportunity.Amount | cents → units | trigger recalculates; verify after load |
```

```markdown
# Integration design — nightly ERP sync
*Read whenever the nightly sync is the subject, before changing it or debugging a gap. 2026-07-26.*

Direction: ERP → Salesforce, Bulk 2.0 upsert on `ERP_Id__c`, 02:00 UTC.
Volume: ~28,000 Accounts, ~4,000 Shipments. Cost: ~20 API calls.
Order: Account, then `Shipment__c` (master-detail parent must exist).
Failure handling: failedResults downloaded to the job folder; parent-lock failures re-run sorted by AccountId.
First limit met: 200-record trigger chunks against the Account trigger's 100-SOQL ceiling.
Credentials: <file:~/.certs/sf-jwt.key>, Consumer Key in the design doc, secret never here.
```

If the user tracks this work as a project, the summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the detail staying here and referenced by name.

## loads/

Every bulk load, export and metadata deploy, cut by year. This is what makes "we already tried that" answerable.

```markdown
# Loads and deploys — 2026

## Data Loads
| Date | Object | Operation | Rows in | Succeeded | Failed | Job id | Notes |
|------|--------|-----------|---------|-----------|--------|--------|-------|
| 2026-07-14 | Account | upsert on ERP_Id__c | 28,412 | 28,390 | 22 | 750...A1B | 22 failed on a required custom field; mapping fixed |

## Metadata Deploys
| Date | What | Target org | Result | Rollback |
|------|------|-----------|--------|----------|
| 2026-07-02 | 2 fields + 1 permission set | uat → prod | success | destructive changes package kept |
```

## Shared boxes

These files are shared with every other skill and the user may have none of them installed, so the format travels with this skill. In all three: **read the file before adding**, find the identity key, and if it is there, update that row in place — only its absence justifies a new row. Update and retire your own rows; never touch a row another source wrote. **If the file already exists with a different column set, match its columns** and add anything missing as a trailing note — never rewrite its header. Amounts carry their currency inside the value.

**`~/Clawic/data/contacts/contacts.md`** — identity is email or handle.

```markdown
| Name | Role | Preferred channel | Context |
|------|------|-------------------|---------|
| Dana Ruiz | Salesforce admin, Acme | dana@acme.example | Owns the Connected App and the integration user's permission set |
```

Scale cut: one table while there are ≤15 people; past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index. When someone stops being involved, delete the row and note the date in `memory.md`. Never a phone number or an address the user did not ask you to keep, and never a credential.

**`~/Clawic/data/projects/<project>.md`** — identity is the project name, which is the file name. One file per project from the first. Hold objective, status, milestones and decisions; the Salesforce detail (mapping, design) stays in `artifacts/` and is referenced by name.

**`~/Clawic/data/finances/subscriptions.md`** — identity is the subscription name. One row: `| Salesforce | Enterprise Edition, 40 licenses | 6,000 USD/mo | annual, renews 2027-02 |`, adapting to whatever columns the file already has. Only what the user stated — never a number scraped from an org — and never an account number or payment credential.

**Cross-reference rule**: when a row here names an entity that belongs to another box, write the entity in its box and keep only its name here. An org owned by a client references the client by name; duplicating the client record is how two skills end up contradicting each other.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`orgs.md` — from the second org onward, one row per org including sandboxes:

```markdown
# Salesforce Orgs

| Alias | Type | Org id | Instance URL | API version | Auth flow | Credential | Notes |
|-------|------|--------|--------------|-------------|-----------|------------|-------|
| prod | production | 00D5g0000... | https://acme.my.salesforce.com | v62.0 | jwt-bearer | file:~/.certs/sf-jwt.key | Enterprise, ~40 licenses |
| uat | full sandbox | 00D2v0000... | https://acme--uat.sandbox.my.salesforce.com | v62.0 | jwt-bearer | file:~/.certs/sf-jwt-uat.key | refreshes every 29 days; username = prod username + `.uat` |
```

The instance URL is what the last token response returned, not what someone typed. When an org is decommissioned or a sandbox is deleted, delete the row and note the date — a list of orgs that only grows sends the next load to a dead one.

`queries.md` — `## Saved Queries`, once past ~15. Keep the `Purpose / Kind / Query or id / Notes` columns; `Notes` carries whether the filter is selective and what it cost.

`gotchas.md` — `## Gotchas`, once past ~15. Same three columns. This is the highest-value file in the box: every row is an afternoon somebody already lost to the org's own customizations.
