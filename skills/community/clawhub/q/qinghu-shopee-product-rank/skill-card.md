## Description:

按站点和类目查询 Shopee 商品热销榜与飙升榜，支持日、周、月榜及跨境、本土等筛选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee 商家和选品分析人员可查询指定站点、类目和时间周期的热销或飙升商品榜单，以辅助商品趋势分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade Node and qhkit and change the local environment.

Mitigation: Require approval before installation or upgrades; prefer a disposable environment or preinstalled, pinned qhkit version.

Risk: Using the paid external service requires a qhkit API token and may incur charges.

Mitigation: Require explicit approval before token setup and paid calls; check estimated credits first.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-product-rank)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise summary with key results; tabular file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the Shopee site and time period; paid calls report Qinghu credits consumed.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
