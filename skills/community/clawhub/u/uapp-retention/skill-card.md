## Description:

This skill helps agents query Umeng U-App retention data through umeng-cli, covering new-user and active-user retention windows plus version or channel comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics operators use this skill to retrieve Umeng U-App retention metrics for a known appkey, date range, retention type, version, or channel. It guides agents in forming read-only umeng-cli calls and interpreting the returned retentionRate array.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's security evidence reports telemetry behavior that can send the Appkey in a separate trace command before the retention query.

Mitigation: Use this skill only when that telemetry behavior is acceptable for the appkey being queried, and avoid supplying sensitive appkeys in contexts where telemetry is not approved.

Risk: The security evidence reports an unsafe remote installer command.

Mitigation: Prefer the documented npm install path and avoid running the curl | sh installer.

Risk: Retention windows near the current date can return null or zero values before the window has matured.

Mitigation: Check whether each retention window has elapsed before summarizing null or zero values as actual retention performance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-retention)
- [umeng-cli project homepage](https://github.com/umeng/umeng-cli)
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi)
- [Umeng website](https://www.umeng.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retention lookup guidance; response interpretation requires selecting the correct retentionRate array index.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
