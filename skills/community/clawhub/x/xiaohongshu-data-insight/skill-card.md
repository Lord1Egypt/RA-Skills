## Description:

小红书公开数据只读技能：关键词搜笔记、爆款选题、笔记详情、评论舆情、博主作品、粉丝获赞与收藏，输出 JSON，不登录不发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and analysts use the skill to retrieve public Xiaohongshu notes, comments, and creator statistics for topic research, competitor monitoring, KOL screening, and public-opinion analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and note or profile links are sent to the third-party Guaikei service.

Mitigation: Use only public queries and avoid including private or sensitive information in keywords or URLs.

Risk: ClawScan reports a benign verdict with medium confidence, but code analysis was partial and tool-misuse analysis was degraded.

Mitigation: Review the code and its network behavior before installation; the benign verdict does not resolve the portions that were not fully inspected.

## Reference(s):

- [ClawHub release](https://clawhub.ai/um-why/skills/xiaohongshu-data-insight)
- [Service homepage](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)
- [FAQ and setup](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON envelope containing public note, comment, and creator data, or a structured empty/error result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only data retrieval; interaction counts may be strings.]

## Skill Version(s):

1.2.4 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
