## Description:

按关键词搜索 1688 货源，并按销量、价格区间和 48 小时揽收率等条件筛选与排序。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

采购人员和电商运营人员使用此技能搜索 1688 货源，按价格、销量及揽收率筛选候选商品。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update local qhkit tooling and configure an API token.

Mitigation: Review installation and credential setup first; prefer a managed or sandboxed install and avoid persistent PATH changes unless intended.

Risk: Product searches can consume Qinghu credits.

Mitigation: Check the estimated credit cost and get user approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-1688-keyword-search)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown results with an optional tabular export file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes search results, cites sample size and reports credits spent on paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
