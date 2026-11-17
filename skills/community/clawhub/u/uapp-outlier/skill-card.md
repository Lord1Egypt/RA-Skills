## Description:

Queries UApp (友盟+) application outlier reports, yesterday anomaly status, and intelligent inspection summaries for application monitoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operations teams use this skill to query UApp application anomalies, retrieve detailed outlier report links, and summarize intelligent inspection data such as event tracking health and error codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to UApp monitoring credentials and application analytics data.

Mitigation: Provide credentials through protected configuration or environment variables, avoid command-line secrets, keep umeng-config.json out of version control, and restrict file permissions.

Risk: Default usage reporting can send appkey and date usage events through umeng-cli.

Mitigation: Set UMENG_ENABLE_STATS=false unless usage reporting is explicitly acceptable for the deployment.

Risk: The documented global umeng-cli installation may rely on an unpinned external dependency.

Mitigation: Prefer a pinned local dependency or reviewed installation source for umeng-cli.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/squall0925/skills/uapp-outlier)
- [UApp getOutlierPoints endpoint](https://mobile.umeng.com/ht/api/v3/ai/getOutlierPoints)
- [UApp getYesterdayOutliers endpoint](https://mobile.umeng.com/ht/api/v3/ai/getYesterdayOutliers)
- [UApp aiEventSummary endpoint](https://mobile.umeng.com/ht/api/v3/claw/meta/aiEventSummary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries with inline values, report links, translated error-code descriptions, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UApp shareUrl links, anomaly status, platform metrics, and credential configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
