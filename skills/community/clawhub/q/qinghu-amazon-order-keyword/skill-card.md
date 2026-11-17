## Description:

反查一个或多个亚马逊 ASIN 在指定周期内带来曝光与转化的关键词，并分析转化结构变化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

亚马逊卖家和广告投放人员可按 ASIN、站点和周期识别带来转化、转化流失或无效曝光的关键词，辅助广告与 Listing 优化。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation or upgrades can change local Node tooling and PATH or execute an unreviewed package version.

Mitigation: Review and pin qhkit before installation; avoid runtime npx or @latest execution and approve any PATH changes.

Risk: The skill needs a Qinghu API token for its data queries.

Mitigation: Keep the token private, use the intended Qinghu site and review credential configuration before use.

Risk: Keyword lookups consume paid Qinghu credits, and larger results may cost more.

Mitigation: Check the current estimate and obtain user approval before paid calls or large batches.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-order-keyword)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎AI API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Concise Chinese-language summary with optional table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Labels the Amazon marketplace, period, sample size and credits spent.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
