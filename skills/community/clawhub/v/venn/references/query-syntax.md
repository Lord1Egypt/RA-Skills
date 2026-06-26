# Platform Query Syntax

Quick reference for platform-specific query languages when searching via Venn tools.

## Jira (JQL)

```
status = 'In Progress' AND assignee = currentUser()
project = PROJ AND created >= -7d
labels IN (bug, critical) ORDER BY priority DESC
sprint in openSprints() AND assignee = currentUser()
```

## Salesforce (SOQL-style)

Query accounts, leads, contacts, opportunities with WHERE clauses:
```
Name LIKE '%Acme%'
CreatedDate >= LAST_N_DAYS:30
Status = 'Open' AND Amount > 10000
```

## Gmail

```
from:boss@company.com
to:me subject:urgent
is:unread after:2024/01/01
has:attachment filename:pdf
```

## Slack

Free text search across messages and channels. No special syntax required — just describe what you're looking for.

## Google Drive

Full-text and metadata search:
```
name contains 'quarterly'
mimeType = 'application/pdf'
modifiedTime > '2024-01-01'
'user@example.com' in owners
```

## GitHub

Code, issue, and PR search with filters:
```
repo:org/repo is:pr is:open
language:python filename:setup.py
is:issue label:bug assignee:@me
org:myorg type:code "function_name"
```

