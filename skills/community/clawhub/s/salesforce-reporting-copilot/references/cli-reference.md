# SFDC CLI Reference

Quick reference for the `sf` CLI (Salesforce CLI v2). All commands use the `sf` binary.

## Authentication

```bash
# Web-based login (interactive, opens browser)
sf org login web --alias my-org

# List all authenticated orgs
sf org list

# Check who you're connected as
sf org display --target-org <alias>
```

## Metadata Exploration

```bash
# List all objects in the org
sf sobject list --target-org <alias>

# Describe a single object (fields, field types, relationships, picklist values)
sf sobject describe --sobject Contact --target-org <alias>

# Describe and save to file (useful for large objects)
sf sobject describe --sobject Contact --target-org <alias> > contact-schema.json
```

## SOQL Queries

```bash
# Basic query
sf data query --query "SELECT Id, Name FROM Contact LIMIT 10" --target-org <alias>

# Query with relationship traversal
sf data query --query "SELECT Id, Name, Account.Name FROM Contact LIMIT 10" --target-org <alias>

# Count records
sf data query --query "SELECT COUNT() FROM Contact" --target-org <alias>

# Output as CSV
sf data query --query "SELECT Id, Name FROM Contact" --target-org <alias> --result-format csv
```

## Report Types

```bash
# List available report types
sf data query --query "SELECT Id, Name, BaseObject FROM ReportType LIMIT 200" --target-org <alias>

# Find report types for a specific base object
sf data query --query "SELECT Id, Name FROM ReportType WHERE BaseObject = 'Contact'" --target-org <alias>
```

## Field Discovery Patterns

When the user's question involves an object you're unfamiliar with:

1. `sf sobject list` — confirm the object exists and get the API name
2. `sf sobject describe --sobject <name>` — get all fields
3. Look for:
   - `referenceTo` arrays → lookup/master-detail relationships (join targets)
   - `relationshipName` → how to traverse in SOQL
   - `calculated: true` → formula fields (read-only, can filter/display but not group by in all report types)
   - `type: "Picklist"` → valid values are in `picklistValues`

## Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `No orgs found` | Not authenticated | `sf org login web --alias my-org` |
| `Entity type not found` | Wrong object API name | Check with `sf sobject list` |
| `Field not found` | Wrong field API name | Check with `sf sobject describe` |
| `INVALID_TYPE` in SOQL | Object not queryable via API | Use Metadata API or Reports API instead |
| `sf: command not found` | CLI not installed | `npm install -g @salesforce/cli` |
