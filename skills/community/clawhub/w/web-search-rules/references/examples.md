# Web Search Rules Examples

## Search and stage

User asks: search for articles about AI agents and save useful items.

Agent flow:

1. Load config and rules.
2. Search the web.
3. Normalize and deduplicate URLs.
4. Apply rules.
5. Open relevant sources and classify claim evidence.
6. Stage trusted/allowed and review results without treating domain trust as claim truth.
7. Ask the user to approve rule changes, archive targets, or cloud writes.
8. Write confirmed changes and append audit logs only after operations succeed.

Report template:

```text
Search Completion Report
Keywords: ai agents
Platform: obsidian
Total results: 18
Deduplicated: 14
Opened: 10
Supported claims: 6
Conflicted or cannot-confirm claims: 2
Blocked: 2
Pending review: 4
Archived: Not Executed
Proposed trusted/blocked rules: 2 / 1
Audit log: ~/.skill-config/web-search-rules/audit.log.jsonl
```

## Batch rule suggestion

When multiple useful results share a domain, propose but do not apply a persistent rule automatically. The proposal concerns future source handling, not truth of every claim:

```text
Rule suggestion
Domain: example.com
Reason: 6 previously reviewed items from this domain
Proposed action: mark domain allowed for this topic
Options: apply for this run only, create a scoped persistent rule, keep reviewing one by one
```

## Cleanup dry-run

```text
Dry Run Report
Operation: delete staged content
Platform: obsidian
Items: 12
Target: unorganized-search-content/2026-04
Backup/version history: local files, user backup recommended
Confirmation required: confirm delete 12 staged items
```

## Platform switch

Switching from Obsidian to Feishu Wiki:

1. Read source counts.
2. Produce migration dry-run.
3. Confirm target wiki space and node.
4. Copy data to Feishu.
5. Validate imported counts.
6. Leave Obsidian source unchanged unless the user asks for a separate cleanup.
