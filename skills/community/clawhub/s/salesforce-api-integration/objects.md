# Standard Objects — The Data Model and Its Quirks

**Before mapping anything to an object**, read `## Schema Map` in `~/Clawic/data/salesforce-api-integration/memory.md`: this org's custom fields, external ids and trigger behaviour on these objects are recorded there, and they override every general statement below.

Field lists here are the ones that matter to an integration, not the full schema — that comes from `metadata.md` and lands in `schema/<object>.md`.

**Contents:** [Which Object Holds What](#which-object-holds-what) · [Account](#account) · [Contact](#contact) · [Opportunity](#opportunity) · [Lead](#lead) · [Case](#case) · [Activities](#activities-task-and-event) · [Campaigns](#campaigns) · [Products and Pricing](#products-and-pricing) · [User](#user) · [Files](#files) · [Relationship Types](#relationship-types) · [Custom Objects](#custom-objects) · [Niche Objects](#niche-objects-you-will-eventually-meet)

## Which Object Holds What

| The user says | Object | Note |
|---|---|---|
| "customer", "company", "client" | `Account` | Person accounts merge this with Contact |
| "person at a company" | `Contact` | Can exist with no Account |
| "deal", "pipeline", "forecast" | `Opportunity` | Amount becomes read-only once products are attached |
| "prospect", "unqualified" | `Lead` | Converts into Account + Contact + Opportunity |
| "ticket", "support issue" | `Case` | `CaseNumber` is auto-generated, not settable |
| "call", "meeting", "to-do", "activity history" | `Task`, `Event` | Polymorphic parents; old ones get archived |
| "marketing campaign", "list member" | `Campaign`, `CampaignMember` | Junction to Contact **or** Lead, never both |
| "product", "price" | `Product2`, `PricebookEntry` | A product has no price until it is in a price book |
| "quote", "order", "contract", "asset" | `Quote`, `Order`, `Contract`, `Asset` | Enabled per org; check before mapping |
| "file", "attachment", "document" | `ContentVersion` / `ContentDocumentLink` | `Attachment` is the legacy object (`files.md`) |
| "user", "rep", "owner" | `User` | Cannot be deleted, only deactivated |
| Anything ending in `__c` | A custom object | Its behaviour is whatever the admin built |

## Account

Required: `Name` (unless the org uses person accounts, where `LastName` takes over).

| Field | Note |
|---|---|
| `ParentId` | Self-lookup hierarchy — needs a two-pass load (`migration.md`) |
| `BillingAddress` / `ShippingAddress` | **Compound**: not queryable in Bulk, and written as `BillingStreet`, `BillingCity`, `BillingState`, `BillingPostalCode`, `BillingCountry` |
| `Type`, `Industry`, `Rating` | Picklists — API values, not labels |
| `OwnerId` | Drives sharing; changing it in bulk triggers sharing recalculation |
| `IsPersonAccount` | Read-only; true means the record is also a Contact |

Person accounts, where enabled, are the biggest structural surprise in the model: Contact fields live on the Account, `Name` is read-only and derived, and a `RecordTypeId` for a person-account record type is required on insert. Check `IsPersonAccount` support before writing any Account mapping.

## Contact

Required: `LastName`.

- `AccountId` is optional. Orphan contacts are legal and common, and a report that joins through Account silently drops them.
- `Email` is **not unique** by default. Deduplicating on it is a decision, not a constraint.
- `MailingAddress` and `OtherAddress` are compound, same rules as Account's.
- `ReportsToId` is a self-lookup, same two-pass problem as `ParentId`.
- Contacts can relate to several accounts through `AccountContactRelation` where the org enabled it — the direct `AccountId` is only the primary one.

## Opportunity

Required: `Name`, `StageName`, `CloseDate`.

- **`Amount` stops being writable once the opportunity has line items** — it becomes the rollup of `OpportunityLineItem` totals. A load that sets `Amount` on an opportunity with products either fails or is silently overwritten.
- `StageName` drives `Probability`, `IsClosed` and `IsWon` through the stage configuration; setting the derived fields directly is not how it works.
- `ForecastCategoryName` follows the stage unless explicitly overridden.
- `Pricebook2Id` must be set before any line item can be attached (`migration.md`).
- `AccountId` is required in practice for most reporting even though the schema tolerates its absence.

## Lead

Required: `LastName`, `Company`.

- Converted leads are effectively read-only: `IsConverted`, `ConvertedAccountId`, `ConvertedContactId`, `ConvertedOpportunityId` are set by the conversion and cannot be reconstructed by hand.
- Convert through the standard action, not by creating the three records yourself (`records.md`) — otherwise every "conversion rate" report is wrong.
- Assignment rules fire on insert unless `Sforce-Auto-Assign: FALSE` is sent.
- Lead has its own address and company fields that do **not** map one-to-one onto Account/Contact; the conversion mapping is configurable per org.

## Case

Required: `Status`, `Origin` in most orgs (configurable).

- `CaseNumber` is auto-generated and cannot be set, which matters when migrating tickets whose numbers customers know. Keep the source number in a custom external id field.
- `ContactId` and `AccountId` are independent lookups; setting the contact does not always populate the account.
- Assignment rules and escalation rules fire on insert and update.
- `CaseComment` and `EmailMessage` are separate objects holding the conversation — migrating cases without them migrates the shell.

## Activities (Task and Event)

- `WhoId` points at a Contact or Lead; `WhatId` points at almost anything else (Account, Opportunity, Case, custom objects). Both are polymorphic, so a mapping must know the target object per row (`soql.md` `TYPEOF`).
- `Task.Status`/`IsClosed` and `Event.StartDateTime`/`EndDateTime` are the fields reporting actually uses.
- Recurring events are stored as a series with child occurrences; treating them as ordinary rows produces duplicates.
- Old activities are archived and stop appearing in normal queries — a "missing activity history" that is not a bug (`soql.md`).

## Campaigns

`CampaignMember` is a junction with an exclusive rule: it carries **either** `ContactId` **or** `LeadId`, never both, and never neither. `Status` values come from the campaign's own member-status set, so a value valid for one campaign is rejected by another.

## Products and Pricing

Four objects in a fixed chain: `Product2` (the thing) → `PricebookEntry` (the thing's price in a given price book) → `OpportunityLineItem` (the priced thing on a deal), with `Pricebook2` holding the price books. Every org has a **standard price book**, and a product needs an entry there before it can be entered in any other price book. Skipping that step is why a line-item load fails with a cross-reference error on a product that plainly exists.

## User

- Users are never deleted, only deactivated. Any integration that expects a delete has to handle `IsActive = false` instead.
- Assigning records to an inactive user requires a specific permission.
- `Profile`, `UserRole` and permission set assignments decide what your integration can see when you authenticate as that user (`auth.md`).
- `UserLicense` consumption is what drives the org's API allocation (`limits.md`).

## Files

`ContentVersion` holds the bytes and the metadata; `ContentDocument` is the logical file; `ContentDocumentLink` attaches it to records — one file can be linked to many. The legacy `Attachment` and `Document` objects still exist in older orgs and behave differently. Details in `files.md`.

## Relationship Types

| | Lookup | Master-detail |
|---|---|---|
| Child can exist alone | Yes | No |
| Parent delete | Clears the lookup (or is blocked) | **Cascades** — children are deleted |
| Sharing and ownership | Child has its own owner | Child inherits the parent's |
| Rollup summaries on the parent | No | Yes |
| Reparenting | Free | Only if the admin allowed it |
| Required on insert | Optional | Effectively required |

This table decides more migration outcomes than any field list: a master-detail child cannot be loaded before its parent, cannot be reparented later, and disappears when the parent does.

## Custom Objects

- API name ends in `__c`; the relationship name in a SOQL traversal ends in `__r`; a managed-package object also carries a namespace prefix (`acme__Shipment__c`), which `Sforce-Call-Options: defaultNamespace` lets you omit (`records.md`).
- A **junction object** is a custom object with two master-detail relationships — the many-to-many pattern. The first master-detail defined controls ownership and sharing, which is a decision the admin already made and you inherit.
- Custom settings and custom metadata types (`__mdt`) look like objects but are configuration: queryable, rarely writable through the data API, and deployed rather than loaded.
- Big objects and external objects (`__x`, Salesforce Connect) support only a subset of SOQL and no ordinary DML — confirm the object type before designing against it.

## Niche Objects You Will Eventually Meet

`Quote` and `QuoteLineItem` (enabled per org, with their own sync-to-opportunity behaviour) · `Order` and `OrderItem` · `Contract` · `Asset` and `AssetRelationship` · `Entitlement`, `ServiceContract`, `Milestone` (Service Cloud) · `WorkOrder` (Field Service) · `Territory2` (enterprise territory management) · `Individual` and `ConsentEvent` (privacy) · `Knowledge__kav` (Knowledge articles, versioned and requiring their own publish workflow) · `EmailMessage` and `CaseComment` (the actual content of a support history) · `<Object>History` and `<Object>Share` (read-only history and explicit sharing rows).

Each is enabled per org. `SELECT QualifiedApiName FROM EntityDefinition` answers "does this org even have it" in one call (`metadata.md`).

**When an object turns out to behave unlike this page** — a required custom field, an external id, a trigger that rewrites values, a picklist restricted by record type, a master-detail you cannot reparent — add or update its row in `## Schema Map` in `memory.md`. If you had to derive the whole field list, it goes to `schema/<object-api-name>.md` with its `## Boxes` line in the same turn.
