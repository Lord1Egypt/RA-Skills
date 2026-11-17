## Description:

A lightweight WeChat Official Account API skill for token management, image upload, draft creation, and draft count checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youhan2021](https://clawhub.ai/user/youhan2021)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help agents prepare WeChat Official Account publishing steps: retrieve access tokens, upload cover or body images, create article drafts from JSON, and inspect draft count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat AppID, AppSecret, and access tokens, which can expose a WeChat Official Account if stored or logged carelessly.

Mitigation: Use only with an account the agent is intended to access, protect config.env with owner-only permissions, and avoid running token retrieval where command output is logged.

Risk: Uploaded files and draft JSON content are sent to WeChat servers.

Mitigation: Verify every file path and draft JSON payload before upload or draft creation.

Risk: The security verdict is suspicious because credential handling could expose secrets through files or logs.

Mitigation: Review the skill before installing it on shared machines or in logged agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youhan2021/skills/wechat-api-lite)
- [WeChat Official Accounts platform](https://mp.weixin.qq.com)
- [WeChat API token endpoint](https://api.weixin.qq.com/cgi-bin/token)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print access tokens, media IDs, image URLs, draft media IDs, draft counts, and WeChat API errors.]

## Skill Version(s):

1.0.0 (source: release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
