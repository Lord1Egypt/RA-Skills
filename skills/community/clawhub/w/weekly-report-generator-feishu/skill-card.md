## Description:

Generates AI-assisted weekly reports from local Git activity, user-provided work context, and screenshots, then can send the resulting report to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prayone](https://clawhub.ai/user/prayone)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and team leads use this skill to summarize weekly engineering work from local repositories and optional screenshots into a business-facing Markdown report. It can also help configure a Feishu workflow for sending the report after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may scan local Git repositories and include private commit messages, project names, screenshots, or work details in a weekly report.

Mitigation: Run it only against an explicit project allowlist and preview the generated Markdown before sharing it.

Risk: The skill can send report contents to Feishu automatically after report generation.

Mitigation: Require a clear user opt-in before sending and keep scheduled sending disabled until the workflow has an uninstall path.

Risk: Feishu credentials are configured in the sending script.

Mitigation: Keep credentials out of checked-in scripts and prefer environment variables or a local secret store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prayone/skills/weekly-report-generator-feishu)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu messages API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with shell command snippets and Feishu send status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local weekly-report-YYYYMMDD.md file and send report text to Feishu when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
