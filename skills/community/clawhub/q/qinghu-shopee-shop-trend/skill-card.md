## Description:

查询 Shopee 店铺最长 720 天的月度、季度或年度趋势，可按类目等条件筛选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market analysts use this skill to review a shop's longer-term sales trends across supported sites before making commercial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrades can change the local Node/qhkit setup and PATH.

Mitigation: Review or preinstall qhkit yourself; avoid unpinned npx and @latest upgrades where possible.

Risk: Configuring qhkit stores a Qinghu API token for authenticated access.

Mitigation: Review credential setup and provide the token only through the intended configuration or environment variable.

Risk: Shopee data calls consume Qinghu credits, including possible follow-up lookups.

Mitigation: Require the agent to list planned tools and expected credits and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Trend summaries, Markdown, Tabular files, Shell commands, Configuration guidance]

**Output Format:** [Concise Markdown summary; table file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monthly, quarterly or yearly data; up to 720 days; usage credits reported after paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
