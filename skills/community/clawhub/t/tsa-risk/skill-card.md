## Description:

Tencent Cloud Smart Advisor architecture risk inspection skill that retrieves cloud architecture details, architecture lists, directory data, risk assessment items, and latest architecture evaluation results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1ncludesteven](https://clawhub.ai/user/1ncludesteven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud architects, and operations teams use this skill to query Tencent Cloud Smart Advisor data, inspect cloud architecture diagrams, review risk assessment items, and summarize recent Well-Architected evaluation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud API credentials and may encourage durable AK/SK configuration.

Mitigation: Use a least-privilege sub-account, prefer short-lived credentials, and avoid storing long-lived AK/SK values in shell startup files.

Risk: The skill can create, attach policies to, assume, and delete Tencent Cloud CAM roles through separate scripts.

Mitigation: Review the role-creation and cleanup scripts before use, require explicit approval for write operations, and remove unused roles promptly.

Risk: Generated console-login links can grant temporary access to Tencent Cloud console pages.

Mitigation: Do not share generated login links, keep STS durations short, and regenerate links only when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1ncludesteven/skills/tsa-risk)
- [Tencent Cloud portal](https://cloud.tencent.com)
- [Tencent Cloud API credentials console](https://console.cloud.tencent.com/cam/capi)
- [DescribeArch reference](references/DescribeArch.md)
- [DescribeArchList reference](references/DescribeArchList.md)
- [DescribeLastEvaluation reference](references/DescribeLastEvaluation.md)
- [DescribeStrategies reference](references/DescribeStrategies.md)
- [ListDirectoryV2 reference](references/ListDirectoryV2.md)
- [ListUnorganizedDirectory reference](references/ListUnorganizedDirectory.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, API Calls, Configuration guidance]

**Output Format:** [Markdown responses with inline shell commands, JSON API results, summaries, and console links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate short-lived Tencent Cloud console-login links and should avoid exposing full sensitive URLs except as intended Markdown hyperlinks.]

## Skill Version(s):

1.5.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
