# Parent Child Patterns

Use this file when business scope, ownership, or review context must be determined through a related parent object.

## When to Traverse

Traverse to a parent object when any of these are true:
- the current object has no `OwnerId`
- the current object has no sales team or sales group fields suitable for filtering
- the business rule is explicitly defined on a parent object

## Opportunity-Driven Scope

Many approval or review objects derive business scope from `Opportunity`.

Pattern:

```sql
SELECT
  CRM_Opportunity__c,
  CRM_Opportunity__r.Name,
  CRM_Opportunity__r.Owner.Name,
  CRM_Opportunity__r.Owner.CRM_Sales_Team__c,
  CRM_Opportunity__r.Owner.CRM_Sales_Group__c,
  ...
FROM Child_Object__c
WHERE CRM_Opportunity__c IN (
  SELECT Id
  FROM Opportunity
  WHERE Owner.CRM_Sales_Team__c = 'Europe'
)
```

Use parent owner fields in `SELECT` when business reviewers need to see why the record was included.

## Relationship Limits

Do not assume SOQL can traverse arbitrarily in `WHERE`.

Known pitfalls:
- some child objects reject multi-level relationship operands in `WHERE`
- nested semi-joins are not supported

If a direct relationship filter fails:
- fall back to parent id collection first
- or switch to a two-step approach

## Review-Oriented Exports

When exporting for business review, include both:
- the child object's business fields
- the parent context fields that explain inclusion

Typical parent context fields:
- parent name
- parent owner name
- parent owner sales team
- parent owner sales group
