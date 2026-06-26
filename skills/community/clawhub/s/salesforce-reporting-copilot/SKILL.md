---
name: salesforce-reporting-copilot
description: Generate a Salesforce report blueprint from real org metadata. Use this skill when someone asks to build a report in Salesforce, understand how to query their org's data, map objects to a reporting question, or get started with SFDC CLI metadata pulls. Triggers on phrases like "build a Salesforce report", "how do I report on X in Salesforce", "pull Salesforce metadata", "what objects do I need for this report", "SFDC CLI setup", "understand my org schema", or "create a report blueprint".
version: 1.0.0
metadata:
  clawdbot:
    emoji: "📊"
    homepage: https://github.com/breynol01/salesforce-reporting-copilot
    requires:
      bins:
        - sf
    files:
      - references/*
---

# Salesforce Reporting Copilot

Generate a **Report Blueprint** from real Salesforce org metadata. Given an org and a reporting question, map the right objects, fields, and relationships — then produce a blueprint you can build in Salesforce Report Builder immediately.

## Workflow

### Step 1 — Authenticate and pull org metadata

```bash
# Verify CLI auth
sf org list

# Pull object list
sf sobject list --target-org <alias>

# Describe a specific object (fields, relationships, picklists)
sf sobject describe --sobject <ObjectName> --target-org <alias>

# Pull report types available in the org
sf data query --query "SELECT Id, Name, BaseObject FROM ReportType LIMIT 200" --target-org <alias>
```

See `references/cli-reference.md` for full command patterns, flags, and troubleshooting.

### Step 2 — Map the reporting question to objects

Given the user's question (e.g. "I want to see which volunteers are missing certifications"):

1. Identify the **primary object** (the thing being counted or filtered)
2. Identify **related objects** needed via lookup/master-detail joins
3. Note any **formula fields** or **rollup summaries** that pre-aggregate the data
4. Flag any missing fields or relationships that would require a new custom field

See `references/object-mapping.md` for common Salesforce object patterns and report type selection guidance.

### Step 3 — Produce the Report Blueprint

Output a structured blueprint:

```
## Report Blueprint: [Question]

**Report Type:** [Standard or custom report type name]
**Primary Object:** [e.g. Contact]
**Related Objects:** [e.g. Account (lookup), Certification__c (child)]

### Columns
| Field Label | API Name | Object | Notes |
|---|---|---|---|
| Full Name | Name | Contact | |
| Certification Status | Certification_Status__c | Certification__c | May need custom field |

### Filters
- [Field]: [Operator] [Value]

### Grouping / Summary
- Group by: [Field]
- Summary: [Count/Sum/etc.]

### Gaps / Blockers
- [Any missing fields, permissions, or relationships]
```

## Constraints

- Run `sf sobject describe` before making field claims — never assume field API names
- If the user's question can't be answered with existing fields, say so clearly and suggest what needs to be built
- Do not fabricate object or field names; always pull from live org metadata
- If the user has no SF CLI auth configured, walk them through `sf org login web` first (see `references/cli-reference.md`)
