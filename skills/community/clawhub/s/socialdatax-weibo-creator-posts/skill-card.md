## Description:

用于查找微博创作者近期发布内容，并支持内容调研、风格分析、创作者对标和账号跟踪。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

开发者、研究人员和运营分析人员可查询微博创作者的近期内容，用于内容调研、风格分析、创作者对标和账号跟踪。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious because its instructions invoke an unpinned CLI package with automatic approval; the assessment was partial because some referenced paths could not be matched to bundled artifacts.

Mitigation: Review the CLI package and its referenced behavior, and pin it to a reviewed version before installation.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON creator-post data with concise text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post text, media links, publish times, interaction counts, author details, and pagination data when provided by the source.]

## Skill Version(s):

0.1.24 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
