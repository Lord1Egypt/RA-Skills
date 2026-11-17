## Description:

Guides an agent through preparing copy and images, uploading assets to WeChat's material library, and creating WeChat Official Account article drafts for publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and account operators use this skill to assemble illustrated WeChat Official Account articles, generate or prepare images, upload required assets to WeChat, create drafts, and choose API or manual publication based on account capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles WeChat app credentials and short-lived access tokens.

Mitigation: Use test or least-privilege credentials, avoid pasting real secrets into shell commands, and rotate tokens or credentials if exposed.

Risk: The workflow can upload media, create article drafts, and proposes an API publication path for eligible accounts.

Mitigation: Require human review and explicit approval before upload or publication steps, especially when using production accounts.

Risk: Generated images and article HTML may contain errors, broken assets, or unsuitable content.

Mitigation: Review generated images, HTML, and WeChat material URLs before draft creation or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/skills/wechat-publish)
- [Publisher profile](https://clawhub.ai/user/zhuchenggong19851114-design)
- [WeChat Official Account platform](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, HTML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WeChat API request payloads, article HTML, image-generation prompts, and operational checklists for a single article workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
