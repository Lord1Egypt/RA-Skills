## Description:

用于快手达人数据、快手达人信息、账号资料、创作者画像、主页信息和粉丝规模查询。覆盖 Kuaishou / Kwai creator profiles，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can discover Kuaishou creators by keyword and look up creator profile details such as account basics and audience size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI uses an automatically installed, unpinned latest package, creating supply-chain risk, especially when login instructions provide it with an API key.

Mitigation: Review the package and pin a version before installation; avoid providing an API key until the package has been reviewed.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-creator-profile)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON profile data with concise textual or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile fields depend on the data available for each creator.]

## Skill Version(s):

0.1.24 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
