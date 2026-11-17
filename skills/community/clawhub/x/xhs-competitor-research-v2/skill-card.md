## Description:

当用户需要做小红书竞品研究、小红书竞品分析、同赛道观察、内容角度对比、内容策略对比或品牌内容调研时使用。面向品牌、MCN、内容运营和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

品牌、MCN、内容运营人员和创作者可按关键词研究小红书同赛道内容，比较相关标题、账号和内容角度，并整理后续研究方向。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a mutable @latest CLI dependency that may change between runs and can handle credentials.

Mitigation: Consider the supply-chain risk before installing or running it, and follow the documented credential handling guidance without exposing API keys.

Risk: Research keywords may be sent to SocialDataX, and the security scan had incomplete coverage because it could not resolve three local references.

Mitigation: Avoid sending sensitive keywords and review the skill and its dependencies before use.

## Reference(s):

- [SocialDataX skill and API key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/xhs-competitor-research-v2)
- [Publisher profile](https://clawhub.ai/user/devinchen2014)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown research summaries with content titles, creator or account names, links or IDs, and follow-up angles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited by the requested keyword, filters, and page range; they do not represent complete platform coverage.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
