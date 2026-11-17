## Description:

按 Ozon 商品 ID 查询自然流量词、主题标签和广告流量词，辅助分析商品引流与竞品广告词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to inspect product traffic keywords, topic tags, and advertising keywords by product ID and summarize the results for competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or reconfigure local Node and qhkit tooling without sufficient user control.

Mitigation: Review and approve environment changes before installation; prefer a preinstalled, pinned qhkit version.

Risk: Configuring qhkit may expose or persist a Qinghu account token.

Mitigation: Do not share or store a token unless you trust the package and account configuration flow.

Risk: Keyword queries can consume paid Qinghu credits, with charges varying by result size.

Mitigation: Check the estimated credits and obtain explicit user approval before paid calls or large batches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-product-keywords)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written analysis; spreadsheet file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the platform, time period, sample size, and credits charged for paid queries.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
