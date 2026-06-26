# Web Search Rules Examples

## Search and stage

User asks: search for articles about AI agents and save useful items.

Agent flow:

1. Load config and rules.
2. Search the web.
3. Normalize and deduplicate URLs.
4. Apply rules.
5. Stage whitelisted and pending results.
6. Ask the user to choose whitelist, blacklist, save, or ignore.
7. Write confirmed changes and append audit logs.

Report template:

```text
Search Completion Report
Keywords: ai agents
Platform: obsidian
Total results: 18
Deduplicated: 14
Auto-approved: 3
Blacklisted: 2
Pending confirmation: 9
Saved: 5
New whitelist rules: 2
New blacklist rules: 1
Audit log: ~/.skill-config/web-search-rules/audit.log.jsonl
```

## Batch rule suggestion

When multiple results share a trusted domain, propose but do not apply automatically:

```text
Rule suggestion
Domain: example.com
Reason: 6 previously saved items from this domain
Proposed action: whitelist domain
Options: apply for this run only, create persistent rule, keep reviewing one by one
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
