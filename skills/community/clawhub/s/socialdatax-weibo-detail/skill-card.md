## Description:

用于微博数据分析、微博帖子详情、帖子数据、互动指标、内容调研和内容分析。覆盖 Weibo post details，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要分析微博帖子的用户与内容研究人员；用于查询单条微博的正文、作者、发布时间、互动指标和媒体信息，并整理成结构化结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions invoke an unpinned latest CLI, which could change without review; the security scan was partial because two local references were unresolved.

Mitigation: Use a reviewed, pinned CLI release from a trusted package source, and review the unresolved referenced files before deployment.

Risk: CLI use involves API credentials and local runtime resources.

Mitigation: Run it in a trusted environment, keep credentials in private environment or credential storage, and avoid exposing keys in prompts, logs, or generated files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-detail)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured post-detail JSON with concise factual text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post fields such as content, author, media, interaction counts, publish time, and URL are included when available.]

## Skill Version(s):

0.1.23 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
