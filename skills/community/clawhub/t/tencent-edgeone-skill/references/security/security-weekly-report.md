# security-weekly-report

Manage the security protection status of EdgeOne zones: generate configuration snapshots, detect abnormal policy changes, and produce security reports.

## APIs Involved

| Action | Description |
|---|---|
| `DescribeSecurityPolicy` | Query the zone's security policy configuration |
| `DescribeWebSecurityTemplates` | Query all security policy templates under the zone |
| `DescribeSecurityIPGroup` | Query the security IP group list |

> **Command usage**: This document only lists API names and process guidelines.
> Before execution, consult the API documentation via `../api/api-discovery.md` to confirm the complete parameters and response descriptions.

## Prerequisites

1. All Tencent Cloud API calls are executed via `tccli`. If no valid credentials are configured in the environment, you must first guide the user to complete login:

```sh
tccli auth login
```

> After execution, the terminal will print an authorization link and block until the user completes browser authorization — the command ends automatically upon success.
> Never ask the user for `SecretId` / `SecretKey`, and do not execute commands that might expose credential contents.

2. You need to obtain the ZoneId first — see `../api/zone-discovery.md`.

## Scenario A: Generate Current Security Configuration Snapshot

**Trigger**: User says "check the current security configuration", "help me compile a security policy snapshot for this zone".

For the same `ZoneId`, call the following 3 APIs in sequence: `DescribeSecurityPolicy`, `DescribeWebSecurityTemplates`, `DescribeSecurityIPGroup`.

**Output suggestion**: Respond with "current snapshot + risk alerts", appending a concise JSON snapshot at the end (see appendix format) for future report comparisons.

## Scenario B: Generate Security Protection Report

**Trigger**: User says "generate a security status report for this week", "check if there have been any security policy changes recently".

### Process

1. Confirm the time range (default "this week"), and explicitly state the start and end time in the report
2. Call the 3 APIs from Scenario A in sequence to collect the current configuration
3. If the user provides a historical baseline (last week's report, old snapshot, or historical results from the conversation), perform a diff comparison:

| Comparison Dimension | Description |
|---|---|
| Additions | Policies, templates, IP groups added this week |
| Deletions | Configurations deleted or unbound this week |
| Modifications | Configuration items changed this week |
| Risk escalation | Protection capabilities disabled, policies downgraded from block to observe, etc. |
| Risk de-escalation | Protection capabilities restored, policies tightened, etc. |

4. If **no historical snapshot is available**, explicitly state "only a configuration snapshot can be generated at this time — cannot determine whether changes are abnormal", and output the current result as the new baseline snapshot

**Output suggestion**: Structure the output as "Report scope → Current configuration summary → This week's changes & risks → Recommended actions → Appendix snapshot" (see output format).

## Scenario C: Risk Inspection

**Trigger**: User says "help me check if there are security configuration issues", "are there any high-risk configurations".

After completing the data collection from Scenario A, highlight the following anomalies:

- Critical protection capabilities disabled
- Policies downgraded from block to observe or off
- Overly broad allow configurations
- Security templates unbound or in abnormal status
- IP groups empty, containing overly broad CIDR ranges, or test groups active long-term

> ⚠️ **Note**: Do not declare "abnormal changes" without evidence — you must provide evidence from the current configuration or historical snapshot.

## Output Format

> **Language note**: Adapt the report language to match the user's language. The template below is an example — output should be in the same language the user is using.

```markdown
## Security Protection Report

**Zone**: example.com (ZoneId: zone-xxx)
**Time Range**: 2026-03-13 – 2026-03-19
**Data Sources**: `DescribeSecurityPolicy` / `DescribeWebSecurityTemplates` / `DescribeSecurityIPGroup`

### Current Configuration Summary
- Core protection capability status: ...
- Template binding summary: ...
- IP group summary: ...

### This Week's Changes & Risks
- Configuration changes found this week: ...
- Suspected abnormal changes: ...
- Items requiring manual confirmation: ...

### Recommended Actions
- Immediate action: ...
- Action within this week: ...
- Continue monitoring: ...
```

### Appendix: Concise JSON Snapshot

Append the following format snapshot at the end of the report, for future report comparisons:

```json
{
  "zoneId": "",
  "generatedAt": "",
  "timeRange": { "start": "", "end": "" },
  "securityPolicy": {},
  "webSecurityTemplates": [],
  "securityIPGroups": []
}
```
