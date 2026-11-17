## Description:

按 Shopee 店铺 ID 查询热销商品的价格区间分布，支持日、周、月榜及销量或销售额排序。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market analysts use the skill to assess a shop's best-selling price bands and compare competitor pricing across supported sites and reporting periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can install or update Node and an unpinned qhkit package.

Mitigation: Review installation steps before execution and prefer a preinstalled, pinned qhkit version.

Risk: Account configuration can store or use an API token for the wrong qhkit site or account.

Mitigation: Confirm the intended site and account before providing a token or changing configuration.

Risk: Tool calls consume Qinghu credits, including some failed server calls.

Mitigation: Check the estimated charge and obtain user approval before paid calls; report actual credits consumed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-price-band)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Concise Markdown findings; table file for results with at least 10 records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Shopee site, period, sample size and credits charged; supports tw, my, id, th, ph, sg, vn and br sites.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
