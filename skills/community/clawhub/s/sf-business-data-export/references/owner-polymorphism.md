# Owner Polymorphism

Use this file when Salesforce accepts `Owner.Name` but rejects custom owner fields such as `Owner.CRM_Sales_Team__c`.

## Symptom

Typical error:

```text
No such column 'CRM_Sales_Team__c' on entity 'Name'
```

This means the relationship is being treated as the polymorphic `Name` type rather than a guaranteed `User`.

## How to Confirm

Check the `OwnerId` field in `describe` output.

If `referenceTo` looks like this:

```json
["Group", "User"]
```

handle the object as polymorphic.

If it looks like this:

```json
["User"]
```

owner custom fields are safe to query directly.

## Safe Pattern

For polymorphic owner objects:

1. Filter with `OwnerId IN (SELECT Id FROM User WHERE ...)`
2. Display owner context with `TYPEOF Owner`

Example:

```sql
SELECT
  OwnerId,
  TYPEOF Owner
    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c
    WHEN Group THEN Name
  END,
  Id,
  Name
FROM Quote
WHERE OwnerId IN (
  SELECT Id
  FROM User
  WHERE CRM_Sales_Team__c = 'Europe'
)
```

## Common Objects That Need This

Validate with `describe`, but common examples include:
- `Lead`
- `Quote`
- custom objects whose owner can be queue or user

Do not generalize from one object to another without checking `describe`.
