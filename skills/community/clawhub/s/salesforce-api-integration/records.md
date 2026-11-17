# Records — Single-Record CRUD That Survives a Retry

**Before writing to an object for the first time**, read `## Schema Map` in `~/Clawic/data/salesforce-api-integration/memory.md` (and `schema/<object>.md` if `## Boxes` names one): required custom fields, external id fields, and triggers that rewrite what you sent are all recorded there.

Everything here is the one-record path. Two or more records at a time belongs in `composite.md` (200 per call); thousands belongs in `bulk.md`.

**Contents:** [Read](#read) · [Create](#create) · [Update](#update) · [Nulling a Field](#nulling-a-field) · [Upsert](#upsert-the-idempotent-write) · [Delete](#delete) · [Id Prefixes](#id-prefixes) · [Headers That Change Behaviour](#headers-that-change-behaviour) · [Operations With No REST Verb](#operations-with-no-rest-verb) · [Record Traps](#record-traps)

## Read

```bash
# Whole record, every field the user can see
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/001xx000003DGbYAAW" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# Named fields only — smaller, faster, and it fails loudly on a field you cannot read
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/001xx000003DGbYAAW?fields=Id,Name,Industry" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# By external id, when you do not hold the Salesforce id
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/ERP_Id__c/EXT-4471" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

Fetching by external id is what lets an external system talk to Salesforce without storing Salesforce ids at all. One record → 200; no match → 404; more than one match → **300 Multiple Choices** with the candidate ids in the body, which means the field is not actually unique.

Null fields are omitted from the response, and so are fields the user lacks FLS read on — the two are indistinguishable in the JSON (`SKILL.md` Rule 7).

## Create

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Name":"Acme Corporation","Industry":"Technology","Website":"https://acme.example"}'
```

`201` with `{"id":"001...","success":true,"errors":[]}`. Store that id or the external id you sent; a create whose id you discarded is a record you will find again by name, badly.

- Relationships are set by id (`"AccountId":"001..."`) or, better, by external id through a nested reference: `"Account":{"ERP_Id__c":"EXT-4471"}`. The second form does not require a lookup round trip and cannot go stale.
- The API does not apply UI defaults. A field the page layout fills in automatically is simply empty when the record arrives through the API, and a required field with a layout default fails with `REQUIRED_FIELD_MISSING`.
- Read-only and system fields (`Id`, `CreatedDate`, `LastModifiedDate`, `SystemModstamp`, formula and rollup fields) are rejected if present in the body. Strip them before re-posting a record you read back.
- `CreatedDate` and `OwnerId` can be set explicitly only when the org has the corresponding "set audit fields" permission enabled — the standard tool for a migration (`migration.md`).

## Update

```bash
curl -X PATCH "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/001xx000003DGbYAAW" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Industry":"Finance"}'
```

`204 No Content` on success — no body, so nothing to parse and nothing to confirm from. If the org's automation rewrote a value (a trigger recalculating `Amount`, a flow stamping an owner), the record now differs from what you sent and you will not know unless you re-read it. Record that behaviour in `## Schema Map` the first time you see it.

PATCH is a partial update: fields absent from the body keep their values. There is no PUT.

## Nulling a Field

Explicit `null` in JSON clears the field:

```json
{"Industry": null, "Website": null}
```

An empty string does **not** clear a field in every case, and in Bulk CSV an empty cell means "leave unchanged" while `#N/A` means "set to null" (`bulk.md`). These are three different conventions across the same platform; use the explicit one for the API you are in and never assume they match.

## Upsert (the idempotent write)

```bash
curl -X PATCH "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/ERP_Id__c/EXT-4471" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Name":"Acme Corporation","Industry":"Technology"}'
```

- `201` with the id when it inserted, `204` when it updated. Branch on the status if you need to know which happened.
- The field must be marked **External Id** and should be **Unique**; without uniqueness, a value matching two records returns `300 Multiple Choices` and writes nothing.
- Do not repeat the external id field inside the body with a different value — that is a `DUPLICATE_EXTERNAL_ID`-class error, not a merge.
- A null or missing external id value in the URL cannot match anything, so it always inserts. Filter blank keys out of the source before the loop, or every blank row becomes a new record.
- This is the whole answer to "the request timed out, do I retry?" — with upsert, yes, always, with no reconciliation afterwards (`SKILL.md` Rule 4).

## Delete

```bash
curl -X DELETE "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/001xx000003DGbYAAW" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

`204` on success. The record goes to the recycle bin, where it is still visible to `queryAll` and still occupies storage until the retention window passes.

- Deleting a parent **cascades to master-detail children** and, for some standard pairs, to related records. State the child count before deleting anything with children.
- A lookup child is not deleted; the lookup is cleared, or the delete is blocked if the relationship was defined as "don't allow deletion".
- Hard delete (bypassing the recycle bin) is not a REST verb: it is a Bulk API operation gated by the "Bulk API Hard Delete" permission (`bulk.md`). It is irreversible, so it stays behind an explicit confirmation and `safety_posture.hard_delete` in `config.yaml`.
- `Sforce-Call-Options` cannot soften a delete. Nothing can. Confirm the count first.

## Id Prefixes

The first three characters of any id name the object. This is the fastest way to catch a lookup pointed at the wrong thing, and it works offline.

| Prefix | Object | Prefix | Object |
|---|---|---|---|
| `001` | Account | `00T` | Task |
| `003` | Contact | `00U` | Event |
| `005` | User | `012` | RecordType |
| `006` | Opportunity | `701` | Campaign |
| `00Q` | Lead | `750` | Bulk job |
| `500` | Case | `00O` | Report |
| `068` | ContentVersion | `069` | ContentDocument |

Custom objects get their own prefix, visible in `describe` under `keyPrefix`. Record the prefixes of the org's custom objects in `## Schema Map` — an `INVALID_CROSS_REFERENCE_KEY` is usually a prefix mismatch you can spot by eye.

Ids come in a 15-character case-sensitive form and an 18-character case-insensitive form; the API returns 18. Normalize to 18 everywhere (`SKILL.md` Rule 6).

## Headers That Change Behaviour

| Header | Effect | Use when |
|---|---|---|
| `Sforce-Auto-Assign: FALSE` | Skips Lead/Case assignment rules | A load should not reassign every record to the round-robin queue |
| `Sforce-Duplicate-Rule-Header: allowSave=true` | Saves through a duplicate rule | A deliberate decision, recorded with its reason in `## Gotchas` — otherwise the rule is doing its job |
| `Sforce-Call-Options: defaultNamespace=acme` | Lets you drop the managed-package prefix from field names | Working inside a managed package's objects |
| `If-Modified-Since: <http-date>` | `304 Not Modified` instead of a payload | Caching describes (`metadata.md`) |
| `Sforce-Query-Options: batchSize=200` | Smaller query pages | Wide records that time out at 2,000 per page (`soql.md`) |

Every header that bypasses org behaviour is a decision worth a line in `## Gotchas` — the next person will wonder why the assignment rules did not fire.

## Operations With No REST Verb

- **Undelete** — restore from the recycle bin is Apex DML or the UI, not a REST call. Wrap it in an Apex REST endpoint if a job needs it (`apex.md`).
- **Merge** — merging duplicate Accounts, Contacts or Leads is Apex or SOAP; there is no plain REST merge.
- **Lead conversion** — use the standard invocable action `POST /services/data/vXX.0/actions/standard/convertLead`, which creates the Account, Contact and (optionally) Opportunity in one transaction and returns their ids (`apex.md`). Building conversion by hand out of three creates produces records that fail every "converted lead" report.
- **Field history** — read-only, queryable through the `<Object>History` objects, and only for fields the admin enabled history tracking on before the change happened.

## Record Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Re-posting a record you just read | Read-only and system fields are rejected | Strip `Id`, audit fields, formulas and rollups before writing |
| Retrying an insert after a timeout | The first one probably succeeded; now there are two | Upsert on an external id, or query before retrying |
| Empty string to clear a field | Convention differs per API and per field type | Explicit `null` in JSON, `#N/A` in Bulk CSV |
| Trusting the values you sent after a PATCH | 204 has no body, and triggers rewrite fields | Re-read the record when a downstream step depends on the stored value |
| Setting a lookup by name | Lookups take ids | Nested external id reference, or resolve once and cache the id |
| Deleting a parent to "clean up" | Master-detail children go with it, silently | Count children first, state the number, then confirm |
| Treating a 404 on external id as "not found" | It can also be a wrong field API name in the URL | A wrong field name gives a different error body — read it |

**Before the session ends**: an object's required fields, a trigger that rewrites a value, an external id field you discovered, a custom object's key prefix → `## Schema Map` in `memory.md`. An error whose real cause took work to find → `## Gotchas`. A bypass header you used and why → `## Gotchas`, so the behaviour is explainable later.
