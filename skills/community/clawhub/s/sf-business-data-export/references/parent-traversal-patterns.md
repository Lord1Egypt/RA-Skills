# Parent Traversal Patterns

Use these patterns when the current object does not directly carry the fields needed for scoping or review context, but a parent object does.

## Why This Matters

Many detail or extension objects do not expose owner, sales team, or business scope fields directly.
In those cases, scope must be resolved from a parent object before exporting the child rows.

## Common Pattern

```sql
SELECT
  Id,
  Name,
  CRM_Opportunity__c,
  CRM_Opportunity__r.Name
FROM Order_Detail__c
WHERE CRM_Opportunity__c IN (
  SELECT Id
  FROM Opportunity
  WHERE OwnerId IN (
    SELECT Id
    FROM User
    WHERE CRM_Sales_Team__c = 'Japan'
  )
)
```

## When To Use

- the current object lacks owner or scope fields
- the current object has a lookup or master-detail link to a parent object that defines scope
- the export must include both child rows and parent review context

## Recommended Handling

1. Identify which parent object defines scope.
2. Validate the parent relationship path in `describe`.
3. Try a parent-based semi-join first if SOQL supports it cleanly.
4. If one-query traversal is not reliable, switch to the documented two-step detail query flow.
5. Add parent review fields to the final export when they help business review.

## Notes

- Parent traversal can combine with polymorphic owner handling.
- Do not silently replace parent-based scope with a narrower child-only scope.
- Record the resolved parent scope path in the manifest or object notes.
