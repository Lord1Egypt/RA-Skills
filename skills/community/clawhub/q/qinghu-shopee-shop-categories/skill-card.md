## Description:

查询 Shopee 店铺热销商品的类目分布与销量占比。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to identify a shop's leading product categories and compare their shares of sales for a selected site and date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to install Node and qhkit from the network.

Mitigation: Preinstall a vetted qhkit version and avoid unpinned npx or ad hoc Node downloads during normal use.

Risk: The skill requires a service token to access Qinghu/Shopee analytics data.

Mitigation: Provide the token only through an approved configuration method and review the access granted before use.

Risk: Analytics queries can incur Qinghu credit charges.

Mitigation: Estimate charges and obtain user approval before paid calls; report actual credits used.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-categories)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise analysis with an optional table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports site, date, sample size, and credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
