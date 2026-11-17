## Description:

用于 Instagram 数据助手、内容搜索、帖子详情、评论分析、创作者资料和创作者帖子列表。覆盖 Instagram content and creator research，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can research Instagram content and creators, including post details, comments, profile information, and creator post lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatically installed CLI is unpinned and could change, potentially exposing credentials or accessing the execution environment.

Mitigation: Use a reviewed, pinned CLI version and install it through a controlled, integrity-checked process.

Risk: Search terms or identifiers may be sent to SocialDataX.

Mitigation: Avoid sending sensitive search terms or identifiers through the skill.

Risk: The security scan was partial because some local references could not be resolved.

Mitigation: Resolve and review the unavailable references, then repeat the security review before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-instagram)
- [SocialDataX](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Instagram data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search and retrieval results for Instagram content and creator information.]

## Skill Version(s):

0.1.6 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
