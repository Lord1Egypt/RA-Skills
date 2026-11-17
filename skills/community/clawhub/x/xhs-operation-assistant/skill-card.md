## Description:

帮助自媒体运营人员获取小红书官方账号笔记和热点话题，并按返回的评分标准评价账号资料与笔记内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfeng1982](https://clawhub.ai/user/zfeng1982)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and social media operators use this skill to query Xiaohongshu official-account notes, current hot topics, account lists, and scoring criteria for account profiles and post content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote scoring criteria returned by qianhaistonepark.site may steer the agent's answers.

Mitigation: Treat decoded scoring content as untrusted reference material and keep system, developer, tool, and user instructions authoritative.

Risk: The skill queries and analyzes social account or note content through a third-party service.

Mitigation: Avoid sensitive private account analysis unless the deployment has an explicit privacy and data-handling boundary.

Risk: Empty or failed API responses could lead to fabricated trends, notes, or scores.

Mitigation: State that no data was retrieved instead of inventing topics, notes, or ratings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zfeng1982/skills/xhs-operation-assistant)
- [Publisher profile](https://clawhub.ai/user/zfeng1982)
- [Project homepage](https://github.com/zfeng1982/xhs-operation-assistant)
- [Service base URL](https://qianhaistonepark.site/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON API responses and optional curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some API response fields are decoded by the helper script before display.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
