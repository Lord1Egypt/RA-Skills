# Migration — First Load, CRM Moves, and Backfills

**Before starting**, read `loads/<year>.md` and any `artifacts/mapping-*.md` the `## Boxes` index names: a previous attempt's row counts, failure list and field mapping are the cheapest planning input that exists. Read `## Gotchas` for the org's known rejections.

**Contents:** [The Order That Works](#the-order-that-works) · [External IDs Before Anything](#external-ids-before-anything) · [Quiet the Org](#quiet-the-org) · [Audit Fields and Owners](#audit-fields-and-owners) · [Hierarchies and Self-References](#hierarchies-and-self-references) · [Object-Specific Blockers](#object-specific-blockers) · [Deduplication](#deduplication) · [Rehearsal and Cutover](#rehearsal-and-cutover) · [There Is No Rollback](#there-is-no-rollback) · [Migration Traps](#migration-traps)

## The Order That Works

Dependencies decide the order; every "invalid cross reference" at scale is an ordering mistake.

| Phase | Load | Depends on |
|---|---|---|
| 1 | Users (or map to existing users) | — |
| 2 | Record types, picklist values, custom settings | Metadata deployed (`metadata.md`) |
| 3 | Accounts | Users for ownership |
| 4 | Account hierarchy (`ParentId` update pass) | Accounts existing |
| 5 | Contacts | Accounts |
| 6 | Products and price book entries | — |
| 7 | Opportunities | Accounts, price book |
| 8 | Opportunity line items | Opportunities + price book entries |
| 9 | Cases | Accounts, Contacts |
| 10 | Tasks, Events | Whatever their `WhoId`/`WhatId` points at |
| 11 | Files and attachments | Their parent records (`files.md`) |
| 12 | Anything else | Its parents |

Each phase is its own Bulk job, run to completion and verified before the next. One job per object is also the shape that minimizes lock contention (`bulk.md`).

## External IDs Before Anything

Create a text field on every migrated object, marked **External Id** and **Unique**, holding the source system's primary key. Do it as a metadata deploy before the first row loads.

This single decision gives you:

- **Idempotent loads.** Upsert instead of insert; a failed job is re-run rather than reconciled.
- **Relationships without a lookup pass.** A child CSV references its parent by external id (`Account.ERP_Id__c` column) instead of a Salesforce id you would have to query back (`bulk.md`).
- **A survivable id map.** Salesforce ids differ between sandbox and production, so a mapping keyed on them is worthless the moment you move orgs. External ids are the same everywhere.
- **A reconciliation key** for counting both sides afterwards.

Retrofitting external ids after a load means matching on names, which means a manual merge exercise measured in days.

## Quiet the Org

A migration loads historical data that current business rules were never written for. Decide each of these deliberately, write what was disabled into the migration plan in `artifacts/<kebab-name>.md`, and re-enable it in the same session:

| What | Why it bites | Typical decision |
|---|---|---|
| Validation rules | Historical records fail rules written for new ones | Deactivate the specific rules, never all of them |
| Record-triggered flows and triggers | Fire on every loaded row: notifications, rollups, callouts | Deactivate for the window, with the owner's agreement |
| Workflow rules and process automation | Same, plus field updates that overwrite loaded values | Deactivate |
| Duplicate rules | Block legitimate historical duplicates | Deactivate or send the bypass header |
| Assignment rules (Lead, Case) | Reassign everything to a round-robin queue | `Sforce-Auto-Assign: FALSE` |
| Email deliverability | The org emails thousands of real people | Set to system-only *before* the load, in sandbox and production |
| Sharing recalculation | Ownership changes cascade and lock the org | Ask the admin to defer sharing calculation for the window |

"Deactivate everything" is not the answer: data that cannot pass any rule is data the org will reject forever. The frontier is historical vs ongoing — a migration of closed records may bypass, an ongoing integration may not (`SKILL.md`, Where Experts Disagree).

Every item disabled goes on the re-enable list in that same migration plan. A validation rule left off after a migration is discovered months later by a data-quality problem nobody can explain.

## Audit Fields and Owners

- Setting `CreatedDate`, `CreatedById`, `LastModifiedDate` and `LastModifiedById` requires the org to enable audit-field creation and the load user to hold the permission. It works **on insert only** — once a record exists, its created date is permanent. Getting this wrong means every migrated record looks like it was created on cutover day, and every "deals created last quarter" report is wrong forever.
- `OwnerId` can be set on insert. Assigning records to a user who is already deactivated needs the corresponding permission; otherwise deactivate the source users *after* the load, not before.
- Loading as one integration user and reassigning later is a second full pass plus a sharing recalculation. Set the owner in the same job.

## Hierarchies and Self-References

`Account.ParentId` points at another Account, so a single-pass load cannot resolve rows whose parent has not loaded yet. Two passes:

1. Insert every record with the self-lookup empty.
2. Update, setting `ParentId` by external id reference now that all parents exist.

The same applies to any custom self-lookup and to manager chains on User. Sorting the file by hierarchy depth also works and is more fragile — one mis-sorted row fails silently.

## Object-Specific Blockers

- **Opportunity line items** require a `PricebookEntryId`, and the parent Opportunity needs a `Pricebook2Id` set first. Load products, then price book entries, then set the price book on the opportunities, then the line items. This is the single most common place a CRM migration stalls.
- **Person accounts**, where enabled, merge Account and Contact into one record. `LastName` and `RecordTypeId` go on the Account object, `Name` is read-only, and Contact-shaped source data must be reshaped entirely. Confirm whether the org uses them before mapping anything.
- **Tasks and Events** need `WhoId` (Contact or Lead) and `WhatId` (Account, Opportunity, Case) — polymorphic, so the mapping must know the target object per row.
- **Multi-currency orgs** require `CurrencyIsoCode` on every record with an amount. Omitting it silently applies the corporate currency and every converted total is wrong.
- **Converted Leads** cannot be recreated as converted through ordinary inserts; load them as the resulting Account/Contact/Opportunity, or convert through the standard action (`records.md`).
- **Case, Task and Opportunity histories** are read-only. Migrated records start with empty history — say so before anyone plans a report on it.

## Deduplication

Dedupe in the source, before loading. Cleaning duplicates inside Salesforce means merges, which are Apex or manual, and which lose field values by precedence rules nobody remembers.

- The external id is a unique constraint: two source rows with the same key fail the second row with `DUPLICATE_VALUE` rather than creating a duplicate. That is the safety net, not the strategy.
- For records with no reliable key, normalize the match field (lowercase, trim, strip punctuation) and decide the survivor rule *before* the load, writing it into the migration plan in `artifacts/<kebab-name>.md`.
- Duplicate rules in the org catch cross-system duplicates that your source-side dedupe cannot see. Read what they flagged rather than switching them off permanently.

## Rehearsal and Cutover

1. **Rehearse in a full sandbox** with production-shaped volume. Ten rows prove nothing: governor limits and lock contention only appear past a 200-record chunk (`bulk.md`).
2. **Append the rehearsal's numbers to `loads/<year>.md`** — rows in, succeeded, failed, elapsed time per phase, one row per phase. The cutover plan's timings come from there, not from an estimate.
3. **Fix the mapping, not the data**, when a whole column fails. Repeated manual patches on a rehearsal are the sign of a mapping bug.
4. **Cutover freeze**: the source system stops accepting writes, or the delta after the freeze is a documented second load.
5. **Reconcile**: record counts per object, sum of key currency fields, spot-check twenty records field by field. Do it before anyone declares success.
6. **Re-enable** everything from the quiet-the-org list, and verify one live record end to end.

## There Is No Rollback

Salesforce has no transaction spanning a migration. The recovery plan is what you kept:

- The **id map** — source key to Salesforce id — exported from `successfulResults` of every job.
- The **exact files** loaded, retained until sign-off.
- A **delete plan**: hard delete requires a permission and is irreversible; recycle-bin delete is reversible but bounded by the retention window and still occupies storage.
- On a fresh org, the cheapest rollback is often to refresh the sandbox or restart from an empty org — cheaper than untangling a half-load.

## Migration Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| No external ids | Nothing is idempotent, and relationships need a lookup pass | Deploy them before the first load |
| Loading children before parents | Every row fails on the cross-reference | Follow the phase order |
| Forgetting audit fields on insert | Created dates are permanent; every historical report is wrong | Enable the permission and set them in the same job |
| Leaving email deliverability on | Thousands of notifications to real customers | Set to system-only before the first row |
| Deactivating all validation rules | Rules stay off; the org's data quality decays for months | Deactivate the specific ones, with the re-enable list in the migration plan |
| Line items before the price book | `PricebookEntryId` cannot resolve | Products → price book entries → opportunity price book → line items |
| Rehearsing with a sample | Chunk-boundary failures never appear | Production-shaped volume in a full sandbox |
| Reassigning owners in a second pass | Doubles the load and triggers sharing recalculation twice | Set `OwnerId` in the original job |
| Declaring success on `JobComplete` | It means finished, not correct | Reconcile counts and sums per object |

**Write as you go**: the field mapping is `artifacts/mapping-<source>.md`, born as its own file with its `## Boxes` line, because it will be read at every rehearsal and again at cutover. The migration plan is a second artifact (`artifacts/<kebab-name>.md`) and it is where the deactivation/re-enable list and the dedupe survivor rule live — both are read again at cutover, and both are lost if they stay in the conversation. Every job appends its row to `loads/<year>.md`. The cutover plan and its results belong in the shared `~/Clawic/data/projects/<project>.md` if the user tracks the migration as a project, with the detail staying here and referenced by name. Everything the org rejected and why → `## Gotchas`.
