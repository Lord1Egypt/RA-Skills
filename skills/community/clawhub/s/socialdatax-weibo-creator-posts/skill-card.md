## Description:

用于微博创作者数据、微博创作者内容列表、近期发布、内容调研和创作者内容分析。覆盖 Weibo creator posts，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Social media analysts and account managers use this skill to retrieve Weibo creator posts for recent publishing reviews, content research, style analysis, benchmarking, and account tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI package is installed without a pinned version and could access the configured API key; the scan was partial, so the reviewed evidence is incomplete.

Mitigation: Review the CLI package and use a pinned version before installing it or providing an API key.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and JSON creator-post data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post IDs, content, media, publish times, interaction counts, and author facts when present; opaque pagination tokens are reused unchanged.]

## Skill Version(s):

0.1.25 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
