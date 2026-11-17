## Description:

用于小红书博主数据、小红书博主笔记、账号内容列表、近期发布、内容调研和创作者内容分析。覆盖 Xiaohongshu / XHS / RedNote creator notes，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can retrieve Xiaohongshu creator note lists to review recent publishing, research content, analyze creator styles, compare creators, and track accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill repeatedly runs an unpinned CLI that could change between uses; the scan was partial and does not establish malicious intent.

Mitigation: Review the package and its credential-handling approach before installing, and prefer a reviewed, pinned release where possible.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-creator-notes)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown, Guidance]

**Output Format:** [Creator-note data in JSON, with text or Markdown summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include titles or descriptions, summaries, publish times, interaction counts, media links, content types, and pagination metadata when present.]

## Skill Version(s):

0.1.23 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
