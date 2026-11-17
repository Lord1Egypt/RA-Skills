## Description:

用于 YouTube 数据助手、视频搜索、视频详情、评论分析、频道资料以及频道视频和 Shorts 列表。覆盖 YouTube video and channel research，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

People doing YouTube research use this skill to search videos, inspect video details and comments, review channel profiles, and list a channel's videos or Shorts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, YouTube URLs, and request parameters are sent to SocialDataX; broad requests such as --all may consume API credits.

Mitigation: Avoid confidential inputs and monitor API credit use, especially with --all.

Risk: The supplied skill review does not cover the downloaded CLI or hosted service, and CLI data calls use an API key.

Mitigation: Keep the API key in secret storage and review and pin the CLI version before use.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-youtube)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [JSON research results and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only YouTube research; no account changes.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
