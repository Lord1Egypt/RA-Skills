## Description:

A WeChat Official Account publishing and administration skill for drafting, publishing, formatting, asset management, analytics, and comment moderation using the WeChat publishing APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to manage WeChat Official Account article workflows, including draft creation, publication, uploaded media, reader statistics, and comment moderation. It is suited for agents that need to prepare commands, configuration, or operational guidance for a live WeChat account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish and delete live WeChat account content and comments without built-in confirmation safeguards.

Mitigation: Review every publish, delete, and moderation command before execution, and require an external approval step for destructive or public-facing actions.

Risk: The skill requires WeChat application credentials for account operations.

Mitigation: Use restricted credentials where possible and install the skill only for agents intended to operate a live WeChat official account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/wechat-article-publisher-pro)
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/subscription/api/)
- [Publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, JSON examples, and Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that operate on a live WeChat Official Account when credentials are configured.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
