# Object Mapping Guide

Patterns for translating common reporting questions into Salesforce object/field combinations.

## Standard Report Type Selection

| If the question is about... | Start with this object | Common joins |
|---|---|---|
| People / members / contacts | Contact | Account (lookup), Case (child) |
| Companies / organizations | Account | Contact (child), Opportunity (child) |
| Open deals / pipeline | Opportunity | Account (lookup), Contact (junction) |
| Support tickets / cases | Case | Contact (lookup), Account (lookup) |
| Tasks / activity | Activity (Task/Event) | Contact, Lead, Opportunity (polymorphic WhoId/WhatId) |
| Custom objects | Your custom object | Related lookups |

## Common Reporting Patterns

### "Show me X where Y is missing"
- Use a filter: `[Field] equals (blank)` or `[Field] = null`
- If the field doesn't exist yet → flag as a gap, suggest creating a checkbox or formula field

### "Count X by Y"
- Group by Y (summary field)
- Summary type: Record Count or Sum
- Report type: Tabular or Summary

### "Show timeline / history of X"
- Use the Field History report type for the relevant object (if field tracking is enabled)
- Or query `[Object]History` via SOQL: `SELECT Field, OldValue, NewValue, CreatedDate FROM ContactHistory`

### "Compare X across groups"
- Report type: Matrix
- Group rows by one dimension, columns by another
- Good for: period-over-period, team vs team, status breakdowns

## AYSO-Specific Object Notes

For the AYSO org (`ayso-api` alias):

- **Region accounts**: `Account` with `RecordTypeId = 0123j000001LcX0AAK`
- **Executive Members**: `Contact` with `Executive_Member__c` lookup (direct Contact lookup, not AccountContactRelation)
- **SAR code formula**: `S_A_R__c` = Section + "/" + Area + "/" + Region (formula, read-only)
- **Certification tracking**: check for custom objects; describe the org to confirm current schema

## Relationship Traversal in SOQL

```sql
-- Parent lookup (Contact → Account)
SELECT Name, Account.Name, Account.BillingCity FROM Contact

-- Child relationship (Account → Contacts)
SELECT Name, (SELECT LastName FROM Contacts) FROM Account

-- Custom relationship name (check sf sobject describe for relationshipName)
SELECT Name, Region__r.Name FROM Contact WHERE Region__r.SAR__c = '5/10/100'
```

## Gaps to Flag

Always call out these common issues before producing a blueprint:

1. **Field not in any report type** — some fields are in object schema but excluded from Report Builder. Test by checking `reportable: true` in the describe output.
2. **Custom report type needed** — if the join path doesn't exist in standard report types, a custom report type is required. Note this explicitly.
3. **Data not populated** — if the field exists but is historically empty (pre-dates the field creation), the report will show blanks. Recommend a data audit.
4. **Permission gap** — if the API user can see the field but the report-running user can't, the report will silently exclude it. Check FLS on the target profile.
