## Description:

小红书公开数据只读技能，可按关键词搜索笔记，并查看笔记详情、评论与博主作品和互动数据，输出结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and analysts use this skill to research public Xiaohongshu posts, review note details and comments, and inspect creator activity for topic research, competitor monitoring, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence; some components were only partly inspected, and requests may expose keywords or link tokens to the named third-party service.

Mitigation: Review the scan coverage before installation and send only keywords and links you are comfortable sharing; remove sensitive terms or link tokens where possible.

## Reference(s):

- [Guaikei service](https://www.guaikei.com)
- [ClawHub skill listing](https://clawhub.ai/um-why/skills/xiaohongshu-data-insight)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One JSON envelope per command; the agent should report key fields rather than echo the full response.]

## Skill Version(s):

1.2.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
