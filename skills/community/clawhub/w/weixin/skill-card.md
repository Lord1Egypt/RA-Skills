## Description:

Weixin provides a zero-dependency CLI and practical guidance for WeChat Official Account and Mini Program API workflows, including token checks, media upload, draft creation, publishing, OAuth, JSSDK, and payment development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate and troubleshoot WeChat Official Account publishing flows and to reference implementation notes for Official Account, Mini Program, OAuth, JSSDK, and WeChat Pay V3 development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cache a powerful WeChat access token in a predictable temporary file.

Mitigation: Use a private cache directory or disable disk caching, protect WX_SECRET, and avoid shared machines for production credentials.

Risk: The generic API caller and publishing commands can perform broad posting, template-message, or group-message actions.

Mitigation: Require explicit user approval before publishing content or sending template or group messages.

Risk: Concurrent token refreshes can invalidate tokens used by production services.

Mitigation: Use a centralized production token cache and avoid parallel refreshes from local scripts.

## Reference(s):

- [ClawHub Weixin skill page](https://clawhub.ai/zhangifonly/skills/weixin)
- [WeChat Official Account API endpoint](https://api.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python CLI usage, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call WeChat APIs when the user provides credentials and explicitly approves publishing or message-sending actions.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
