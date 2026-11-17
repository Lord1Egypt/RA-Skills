## Description:

按品牌名称查询 Shopee 各站点售卖该品牌的热销店铺列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee 商家和市场分析人员可按品牌、站点和榜单周期查找热销店铺，辅助了解品牌的销售渠道。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Qinghu data calls consume credits.

Mitigation: Estimate credit use and obtain user consent before making paid calls.

Risk: Installing qhkit or Node and configuring a Qinghu token can change the user's environment or expose credentials if mishandled.

Mitigation: Review and trust the npm package and Qinghu account workflow before setup; keep tokens private and confirm local installation steps.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-shops)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary with a tabular file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the Shopee site, reporting period and sample size; paid calls report credits used.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
