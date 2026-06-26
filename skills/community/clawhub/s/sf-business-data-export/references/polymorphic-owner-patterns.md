# Polymorphic Owner Patterns

Use these patterns when `OwnerId.referenceTo` includes more than one sObject type, commonly `User` and `Group`.

## Why This Matters

When `OwnerId` is polymorphic, filters such as `Owner.Custom_Field__c = '...'` are not reliable in `WHERE`.
Salesforce may reject the query because the `Owner` relationship does not always resolve to `User`.

## Safe Pattern

Use a semi-join for filtering and `TYPEOF` for owner context in the result set.

```sql
SELECT
  Id,
  Name,
  OwnerId,
  TYPEOF Owner
    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c
    WHEN Group THEN Name
  END
FROM Case
WHERE OwnerId IN (
  SELECT Id
  FROM User
  WHERE CRM_Sales_Team__c = 'Europe'
)
```

## When To Use

- `OwnerId.referenceTo` contains both `User` and `Group`
- the export needs owner context in the output
- the filter scope depends on user fields such as sales team or sales group

## When Not To Use

- `OwnerId.referenceTo` is only `User`
- the object does not use owner-based scope at all

## Recommended Handling

1. Inspect `OwnerId.referenceTo` from `describe`.
2. If only `User`, use direct owner fields.
3. If polymorphic, filter with `OwnerId IN (SELECT Id FROM User ...)`.
4. Use `TYPEOF Owner` in `SELECT` when owner attributes must be shown in the export.
5. Record in the manifest that the object used the polymorphic owner strategy.

## Common Failure Mode

If a query fails with an error similar to `No such column ... on entity 'Name'`, re-check whether `OwnerId` is polymorphic and convert the query to the safe pattern above.
