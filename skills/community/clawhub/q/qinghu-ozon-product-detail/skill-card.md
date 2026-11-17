## Description:

按商品 ID 批量查询最多 10 个 Ozon 商品的基本信息与销售数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要查询 Ozon 商品表现的商家和分析人员，按商品 ID 获取基础信息与销售数据，辅助商品研究。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid product lookups consume Qinghu credits, and charges can vary with result size.

Mitigation: Check the current estimate, disclose expected costs and obtain user approval before paid calls; report actual credits charged.

Risk: Using qhkit requires third-party software installation and a Qinghu access token.

Mitigation: Review Node/npm setup before installation, prefer a preinstalled or pinned qhkit version, and configure the token only with the user's consent.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-product-detail)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎 API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise findings in text or Markdown; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Ozon site, period, sample size and Qinghu credits consumed after paid calls.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
