# Query Strategy

Use this file when the export task requires deciding how to translate a natural-language request into executable SOQL.

## Decision Order

1. Confirm the target object list.
2. Confirm whether the object exposes `OwnerId`.
3. Inspect `OwnerId.referenceTo` in `describe` output.
4. Decide whether scope is determined on the current object or on a parent object.
5. Decide whether one query is sufficient or whether a two-step export is required.

## Direct Owner Pattern

Use this pattern when `OwnerId.referenceTo` is only `User`.

Example filter:

```sql
WHERE LastModifiedDate < 2026-03-22T16:00:00Z
AND (
  Owner.CRM_Sales_Team__c = 'Europe'
  OR Owner.CRM_Sales_Team__c = NULL
)
```

Expose owner context directly in `SELECT`.

## Polymorphic Owner Pattern

Use this pattern when `OwnerId.referenceTo` includes both `User` and `Group`.

Filter:

```sql
WHERE OwnerId IN (
  SELECT Id
  FROM User
  WHERE CRM_Sales_Team__c = 'Europe'
)
```

Display owner context:

```sql
SELECT
  OwnerId,
  TYPEOF Owner
    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c
    WHEN Group THEN Name
  END,
  ...
```

Do not rely on `Owner.Custom_Field__c` in `WHERE` for these objects.

## Parent Traversal Pattern

Use this pattern when the current object does not expose owner or scope fields directly, but a parent object does.

Typical example:

```sql
FROM CRM_Technical_Review__c
WHERE CRM_Opportunity__c IN (
  SELECT Id
  FROM Opportunity
  WHERE Owner.CRM_Sales_Team__c = 'Europe'
)
```

## Two-Step Detail Pattern

Use this pattern when SOQL relationship filtering is too limited for a single query.

Step 1:
- query parent records and collect ids

Step 2:
- split parent ids into chunks
- query child/detail object with `IN (...)`
- merge rows into one output file

Use this for detail-heavy objects such as order details.
