## Description:

用于微博数据分析、微博帖子详情、帖子数据、互动指标、内容调研和内容分析。覆盖 Weibo post details，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve and present details for a Weibo post, including its content, author, publish time, media, and available interaction counts, for content research and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI package is invoked at its latest version, so its behavior could change after review and it could access credentials available to it.

Mitigation: Consider waiting until the CLI version is pinned to a reviewed release; review the concern before installing.

Risk: The security scan was partial and cannot establish that all behavior is safe.

Mitigation: Review the skill and scan findings before installation, and account for the scan's limited coverage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-detail)
- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [SocialDataX billing](https://socialdatax.com/dashboard/billing)

## Skill Output:

**Output Type(s):** [JSON, Text, Files]

**Output Format:** [Structured JSON containing Weibo post details, with concise factual text summaries; optional media files can be saved locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only post detail retrieval; optional media saving writes to a user-selected local path.]

## Skill Version(s):

0.1.24 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
