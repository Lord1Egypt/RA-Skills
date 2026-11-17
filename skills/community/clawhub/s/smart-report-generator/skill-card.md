## Description:

Generates daily or weekly task reports and can send supported reports to configured Feishu or DingTalk webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers can turn task status data into daily or weekly Markdown reports for status sharing. Teams can optionally deliver reports through approved webhook destinations after reviewing data sensitivity and platform support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task and report data may include customer, employee, financial, roadmap, incident, or other confidential information.

Mitigation: Review data classification before use and confirm that OpenClaw AI and webhook destinations are approved for the data.

Risk: Advertised monthly, Slack, WeCom, scheduling, and custom template features are not fully supported by the provided artifact.

Mitigation: Use only the implemented daily and weekly report flows and supported webhook destinations unless the publisher updates the artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/smart-report-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown reports with YAML configuration and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly report generation may call the OpenClaw AI service; webhook delivery depends on configured and supported destinations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
