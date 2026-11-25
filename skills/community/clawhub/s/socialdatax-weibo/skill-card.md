## Description:

用于微博数据助手、微博热搜、微博内容研究、帖子详情、评论分析、评论回复观察、转赞互动、创作者资料和创作者内容列表。覆盖 Weibo post research，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

People working with Weibo content and creator data can use this skill to review trending topics, posts, comments, engagement, creator profiles, and creator post lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly runs an automatically installed, unpinned CLI package, creating supply-chain risk.

Mitigation: Review the package and its version before use; pin an audited version where the execution setup allows it.

Risk: Search terms and lookup details are sent to SocialDataX, and the CLI handles an API key.

Mitigation: Avoid submitting sensitive search terms or identifiers, review SocialDataX data handling terms, and keep the API key in the documented private credential store or environment.

Risk: The security scan was partial, so its evidence is incomplete.

Mitigation: Review the full skill and dependencies before deployment.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Structured JSON data with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned content depends on the selected Weibo lookup; list results may be paginated.]

## Skill Version(s):

0.1.25 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
