## Description:

Sends text messages and local files to specified WeChat contacts or groups through OpenClaw's WeChat integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lianghaoxun](https://clawhub.ai/user/lianghaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to query WeChat account/session context and send user-approved text messages or selected local files to WeChat contacts, groups, or bot accounts through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use stored WeChat credentials and account state to send selected messages or files.

Mitigation: Install and invoke it only when that access is intended, and review the recipient, message content, and file path before execution.

Risk: The security evidence reports no clear confirmation gate before message or file sending.

Mitigation: Require explicit user confirmation for the target account, recipient, and payload in the calling workflow before running the send scripts.

Risk: Tokens, upload parameters, or key material can be exposed in execution logs.

Mitigation: Avoid running it where logs are shared, persisted, or visible to others, and redact sensitive values before sharing logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lianghaoxun/skills/wechat-account-send)
- [Publisher profile](https://clawhub.ai/user/lianghaoxun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples and console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Python scripts that read local OpenClaw WeChat account state and send messages or files through WeChat APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
