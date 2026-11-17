## Description:

密码管理器 - 安全存储、随机生成、自动填充

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage passwords by generating, storing, retrieving, checking strength, and using auto-fill workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles passwords and does not provide enough detail about password storage, encryption implementation, network breach checks, auto-fill safety, or package verification.

Mitigation: Install only after verifying the publisher and exact package version; confirm storage, encryption, network, breach-check, and auto-fill behavior before using real secrets.

Risk: The documented installer uses a mutable latest install command.

Mitigation: Prefer a pinned installer version and verify the release hash before installation.

Risk: Password display and auto-fill workflows can expose secrets in untrusted terminals, browsers, or applications.

Mitigation: Avoid displaying or auto-filling secrets in untrusted environments and require user confirmation before filling credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaising-openclaw1/skills/xiaoming-password-manager)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
