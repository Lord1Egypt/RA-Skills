## Description:

用于快手数据分析、快手作品详情、作品数据、互动指标、内容调研和内容分析。覆盖 Kuaishou / Kwai work details，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要查看快手作品详情的用户，用于获取作品内容、作者、发布时间和互动指标，以支持内容调研与分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags repeated use of an automatically installed, unpinned @latest CLI, and the available scan was partial.

Mitigation: Review the package version before installation or execution, especially before providing an API key, and inspect unresolved references before relying on the skill.

Risk: Data calls use an API key, so careless handling could expose credentials.

Mitigation: Use the documented environment variable or private CLI credential storage; do not put the key in command arguments, logs, or chat.

## Reference(s):

- [SocialDataX official page](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-detail)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data, optionally summarized in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include title or description, content, author, publish time, interaction counts, images, and media summary when available.]

## Skill Version(s):

0.1.24 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
