# Metadata and Schema — What the Org Actually Looks Like

**Before describing anything**, check `## Schema Map` in `~/Clawic/data/salesforce-api-integration/memory.md` and open `schema/<object>.md` if the `## Boxes` index names one. A full describe of a mature Account object is a large payload and a slow call; the stored field map answers most questions without it.

**Contents:** [The Cheap Way to List Fields](#the-cheap-way-to-list-fields) · [Describe](#describe) · [Reading a Describe](#reading-a-describe) · [Caching Describes](#caching-describes) · [Find the Automation Before You Load](#find-the-automation-before-you-load) · [Record Types and Layouts](#record-types-and-layouts) · [Tooling API](#tooling-api) · [Deploying Metadata](#deploying-metadata) · [Schema Traps](#schema-traps)

## The Cheap Way to List Fields

`EntityDefinition` and `FieldDefinition` are queryable with ordinary SOQL and return a fraction of a describe's bytes. Use them for "what fields exist" and save describe for "what are this field's rules".

```bash
curl -G "$SF_INSTANCE_URL/services/data/v62.0/query/" \
  --data-urlencode "q=SELECT QualifiedApiName, Label, DataType, IsCompound
                      FROM FieldDefinition
                      WHERE EntityDefinition.QualifiedApiName = 'Account'" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

`FieldDefinition` requires a filter on `EntityDefinition` — an unfiltered query is rejected, not slow. To find the org's custom objects: `SELECT QualifiedApiName, Label, KeyPrefix FROM EntityDefinition WHERE IsCustomSetting = false AND QualifiedApiName LIKE '%__c'`.

## Describe

```bash
# Every object the user can see, with key prefixes and flags — one call, moderate size
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# One object, everything about it
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/describe" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

The describe reflects **the running user**. Fields hidden by field-level security are absent, picklist values restricted by record type are filtered, and objects the profile cannot see never appear. Two users describing the same object legitimately get two different answers — which is why a schema file records the org *and* the user context it came from.

## Reading a Describe

The fields worth extracting, and the question each answers:

| Attribute | Answers |
|---|---|
| `createable` / `updateable` | Can this be sent on insert / on update? Sending a false one is an error, not a no-op |
| `nillable: false` + `createable: true` + `defaultedOnCreate: false` | **The real required-field list.** The page layout's red bars are not it |
| `defaultedOnCreate` | Salesforce fills it if omitted — the API applies these, unlike layout defaults |
| `calculated` | A formula field: never writable, often not filterable, never indexed |
| `externalId`, `unique` | Whether it can be an upsert key (`records.md`) |
| `referenceTo`, `relationshipName` | What a lookup points at, and the name to use in SOQL — `Contacts` not `Contact` |
| `picklistValues[].value` + `.active` | The API values; the label is a different string, and inactive values still exist on old records |
| `controllerName` | A dependent picklist: its valid values depend on another field's value, and an invalid pair is rejected |
| `length`, `precision`, `scale` | Where `STRING_TOO_LONG` and rounding surprises come from |
| `childRelationships[]` | The subquery names for parent-to-child SOQL |
| `keyPrefix` (global describe) | The 3-char id prefix (`records.md`) |

## Caching Describes

Describe responses support conditional requests:

```bash
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/describe" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "If-Modified-Since: Wed, 15 Jul 2026 09:00:00 GMT"
```

`304 Not Modified` means your cached copy is still valid and the call cost you almost nothing. Cache aggressively — an admin changing a field is a rare event, and re-describing on every run is a habit that shows up in the daily allocation.

Invalidate on any of: `INVALID_FIELD` on a field that used to work, a new Salesforce release, a picklist value that is rejected, or the user telling you the admin changed something. Then overwrite `schema/<object>.md` and update its date line.

## Find the Automation Before You Load

Most "the API rejected my perfectly good record" incidents are the org's own configuration. Three queries turn a debugging session into a five-minute check, and they are worth running before any bulk load or migration:

```sql
-- Validation rules that can block your rows
SELECT ValidationName, Active, ErrorMessage, EntityDefinition.QualifiedApiName
FROM ValidationRule WHERE EntityDefinition.QualifiedApiName = 'Account'   -- Tooling API

-- Triggers whose governor limits your batch size has to respect
SELECT Name, TableEnumOrId, Status FROM ApexTrigger WHERE Status = 'Active'   -- Tooling API

-- Record-triggered flows, which behave like triggers you cannot read
SELECT ApiName, Label, ProcessType, TriggerType, IsActive FROM FlowDefinitionView WHERE IsActive = true
```

Every active trigger and record-triggered flow on the target object consumes part of the same per-transaction governor budget as your DML (`SKILL.md` Rule 5). Counting them is how you predict the batch size that will actually work.

Record what you find in `## Schema Map` under the object's notes. It does not change often and it explains a class of failure that is otherwise unexplainable from the outside.

## Record Types and Layouts

```bash
curl "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/describe/layouts" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

- `recordTypeInfos[]` in the object describe gives each record type's id, developer name and whether it is `available` to this user. `RecordTypeId` is required on insert whenever the object has more than one active record type and the user has access to several.
- Picklist values are filtered per record type: a value that is valid for "Direct" may be rejected for "Partner". The layout describe carries the per-record-type picklist subsets.
- Compact layouts drive what appears in mobile and hover cards. Rarely relevant to an integration, occasionally the reason a field "does not show up" for a user.

## Tooling API

Same URL shape with `/tooling/` inserted: `"$SF_INSTANCE_URL/services/data/v62.0/tooling/query/?q=..."`.

| Object | What it gives you |
|---|---|
| `ApexClass`, `ApexTrigger` | Source and status of the org's code |
| `ValidationRule` | The rules that will reject your data, with their error messages |
| `CustomField`, `CustomObject` | Field metadata not exposed through describe, including field-level definitions |
| `ApexLog`, `TraceFlag` | Debug logs and how to start collecting them |
| `ApexTestResult` | Test outcomes after a deploy |
| `Flow`, `FlowDefinition` | Flow versions and which one is active |

Tooling queries share the same daily API allocation and the same SOQL rules. They are a metadata window, not a back door around limits.

## Deploying Metadata

Metadata changes travel through the Metadata API (SOAP), the Tooling API's deploy resource, or the `sf` CLI, which wraps both and is what most teams use. Whatever the transport, the discipline is the same:

1. **Validate first.** A check-only deploy runs the tests without committing; a validated deploy then stays eligible for a fast "quick deploy" for a few days, which is how a release ships in minutes rather than re-running the whole test suite in the change window.
2. **Deletions are a separate package.** A component missing from the deploy is not removed — removal requires an explicit destructive-changes manifest, and it is the half of the deploy nobody rehearses.
3. **Sandbox before production**, always, while `sandbox_first` is true (`SKILL.md` Rule 8). Metadata deploys are the case where the rule has no escape hatch: there is no partial rollback.
4. **The API version of the package matters.** Deploying a package built against a newer version than the target org supports fails wholesale.
5. Field-level security is metadata too: a new field deploys invisible to every profile unless the permission set travels with it. This is the most common cause of "we deployed the field but the integration cannot see it" (`SKILL.md` Rule 7).

Append every deploy to `loads/<year>.md` under `## Metadata Deploys`: date, what, target org, result, and how it would be rolled back.

## Schema Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Using field labels | The API takes API names; labels are translatable and change | `FieldDefinition` or describe for the real name |
| Assuming the layout's required fields are the API's | Layout requiredness is UI-only; the API's list comes from `nillable`/`defaultedOnCreate` | Compute the real list from describe |
| Re-describing on every run | Large payload, real allocation cost | `If-Modified-Since`, plus `schema/<object>.md` |
| Trusting a cached picklist | Admins add and deactivate values; inactive values persist on old records | Re-read on the first rejected value |
| Ignoring dependent picklists | The pair must be valid, not just each value | Check `controllerName` before building a mapping |
| Deploying a field without its FLS | Invisible to every profile including the integration user | Ship the permission set in the same package |
| Expecting a deploy to delete what you removed | Absence is not deletion | Explicit destructive-changes manifest |

**Before the session ends**: a full field table you had to derive → `schema/<object-api-name>.md`, born as its own file, with its `## Boxes` line written in the same turn. A one-line fact about an object — external id field, key prefix, a trigger that rewrites values, an active validation rule that blocks loads → the object's row in `## Schema Map`. A metadata deploy → `loads/<year>.md`.
