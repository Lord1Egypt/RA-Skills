## Description:

用于 YouTube 数据助手、视频搜索、视频详情、评论分析、频道资料以及频道视频和 Shorts 列表。覆盖 YouTube video and channel research，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Users and analysts use this skill to search public YouTube videos, inspect video details and comments, review channel profiles, and list a channel’s videos and Shorts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, video or channel URLs and IDs, and pagination or reply tokens are sent to SocialDataX for lookups.

Mitigation: Send only the inputs needed for the lookup and keep secrets and private information out of research inputs.

Risk: Referenced CLI files were unavailable during the security review, so their setup was not fully assessed.

Mitigation: Review the CLI and its setup before installing it or providing credentials.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [SocialDataX YouTube skill on ClawHub](https://clawhub.ai/devinchen2014/skills/socialdatax-youtube)
- [Publisher profile: devinchen2014](https://clawhub.ai/user/devinchen2014)

## Skill Output:

**Output Type(s):** [JSON data, Analysis]

**Output Format:** [Structured YouTube data with optional natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public YouTube research results; output depends on the selected lookup and available data.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
