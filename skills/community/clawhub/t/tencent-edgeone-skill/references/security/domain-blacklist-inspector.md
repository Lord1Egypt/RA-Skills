# domain-blacklist-inspector

Query the security policies associated with a specified EdgeOne domain, parse IP group references in rules with `action=block`, and output a blocklist IP group mapping report.

> **Purpose**: This skill is a **prerequisite diagnostic step** for write operations (such as `eo-ip-threat-blacklist`). Before writing entries to a blocklist IP group, use this skill to identify the correct target blocklist group ID to avoid operating on the wrong IP group.

## APIs Involved

| Action | Description |
|---|---|
| `DescribeSecurityPolicy` | Query the security policy configuration associated with a domain |
| `DescribeSecurityIPGroup` | Query all IP groups under the zone |
| `DescribeSecurityIPGroupContent` | Query detailed entries of a specified IP group |

> **Command usage**: This document only lists API names and process guidelines.
> Before execution, consult the API documentation via `../api/api-discovery.md` to confirm the complete parameters and response descriptions.

## Prerequisites

1. All Tencent Cloud API calls are executed via `tccli` — confirm login authentication is complete before execution.

2. You need to obtain the ZoneId first — see `../api/zone-discovery.md`.
3. The user must explicitly provide the target domain (e.g., `example.com`); if the user says "this domain" without specifying, ask for clarification first.

## Execution Flow

**Trigger**: User says "check which IP group in example.com's security policy is a blocklist", "which IP group blocks traffic for this domain", "help me check example.com's IP ban list", "I want to add IPs to the blocklist — first help me identify the blocklist group".

Call the following APIs in order to build the blocklist IP group mapping report:

### Step 1: Get the Security Policy Associated with the Domain

Call the `DescribeSecurityPolicy` API, extract all rules from the result, identify rules with **blocking or banning semantics** (e.g., `action=block`, `Action.Name=Deny`, etc. — determine based on the actual meaning of field values), and record the IP group IDs referenced by these rules.

### Step 2: Get All IP Groups Under the Zone

Call the `DescribeSecurityIPGroup` API, cross-reference the IP group IDs identified in Step 1 with this list to fill in metadata like IP group names.

### Step 3: Query Detailed Entries of Blocklist IP Groups

For each blocklist IP group identified in Step 1, call the `DescribeSecurityIPGroupContent` API to query its detailed contents.

### Blocklist IP Group Identification Rules

**Use rule action as the primary criterion**:

- **Confirmed as blocklist group**: IP groups directly referenced by `action=block` rules in security policies
- **Auxiliary reference**: IP group names containing semantic keywords like `blacklist`, `blocklist`, `deny`, or localized equivalents can serve as supplementary evidence, but should not be the sole criterion

> ⚠️ **Note**:
> - Do not judge solely by IP group name — must verify against rule actions in security policies.
> - If multiple IP groups are referenced by `action=block` rules, list them all and explain the rule context for each.
> - If determination is unclear, state this honestly and list all IP groups referenced by blocking rules for the user to manually confirm.

## Output Format

> **Language note**: Adapt the report language to match the user's language. The template below is an example — output should be in the same language the user is using.

```markdown
## Blocklist IP Group Query Results

**Domain**: example.com (ZoneId: zone-xxx)
**Query Date**: YYYY-MM-DD
**Data Sources**: `DescribeSecurityPolicy` / `DescribeSecurityIPGroup` / `DescribeSecurityIPGroupContent`

### Blocklist IP Groups (Referenced by action=block Rules)

> The following IP groups are directly referenced by blocking rules in the security policy — they are the blocklist IP groups for this domain:

| IP Group Name | **IP Group ID** | Entry Count | Associated Rule ID | Rule Action |
|---|---|---|---|---|
| blacklist-prod | **ipg-xxxxxxxx** | 42 | rule-001 | Block |

> To write entries to the above IP group, use IP Group ID: `ipg-xxxxxxxx`

### IP Group Detailed Entries

**blacklist-prod** (ipg-xxxxxxxx)

| # | IP / CIDR | Notes |
|---|---|---|
| 1 | 1.2.3.4 | ... |
| 2 | 5.6.7.8/24 | ... |

> If there are more than 20 entries, show the first 20 and note "N total entries, showing first 20".

### Security Policy Associated Rules Summary

| Rule ID | Rule Name | Action | Referenced IP Group | Notes |
|---|---|---|---|---|
| rule-001 | Blocklist Block | Block | blacklist-prod | ... |

### Additional Notes (if any)

- Anomalous entry notes (e.g., empty IP group, overly broad CIDR like `0.0.0.0/0`, etc.)
- Other noteworthy blocking rules
```

> **Read-only disclaimer**: This skill only performs query operations and does not modify any IP groups or policy configurations. To modify blocklists, use the console or call the appropriate write APIs — confirm the impact scope before operating.
