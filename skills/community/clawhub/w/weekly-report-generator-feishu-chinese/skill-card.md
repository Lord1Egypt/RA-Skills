## Description:

Use this skill to generate weekly reports from git commit logs, analyze git history, categorize work, format a professional weekly report, and send it to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prayone](https://clawhub.ai/user/prayone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project leads, product managers, and technical managers use this skill to turn Git activity and supplied work context into a structured weekly report for workplace status updates. It can also prepare shell-driven Feishu delivery, which should be reviewed before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic Feishu sending can disclose sensitive project data or draft weekly-report content before the user reviews it.

Mitigation: Require a preview and explicit approval before sending; keep reports local by default.

Risk: Broad PROJECT_ROOT scanning can include unintended repositories in the report.

Mitigation: Restrict PROJECT_ROOT to only the repositories intended for weekly reporting.

Risk: Feishu credentials stored in executable scripts can expose secrets.

Mitigation: Store Feishu secrets outside executable scripts, such as in environment variables or a secret manager.

Risk: Scheduled execution can send reports unattended if enabled before review.

Mitigation: Avoid enabling the LaunchAgent until the exact plist file and schedule are present and audited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prayone/skills/weekly-report-generator-feishu-chinese)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)
- [Feishu current user API](https://open.feishu.cn/open-apis/contact/v3/users/me)
- [Feature overview document](artifact/周报生成器功能介绍.md)
- [Installation and configuration guide](artifact/安装和配置指南.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with supporting shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include Git commit summaries, code change counts, categorized work items, highlights, and Feishu delivery status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
