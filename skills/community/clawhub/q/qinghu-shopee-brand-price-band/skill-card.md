## Description:

查询 Shopee 品牌商品在各价格区间的商品数、店铺数、近 30 天销量及占比。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to assess a brand's price bands and compare product counts, store coverage, and recent sales across those bands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup may install or update Node and qhkit and configure an API token.

Mitigation: Review installation and token setup before use; prefer a preinstalled, pinned qhkit version.

Risk: Queries may consume paid Qinghu credits.

Mitigation: Check the current credit estimate and get the user's approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-price-band)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown analysis with an optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies site, reporting period, and credits used for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
