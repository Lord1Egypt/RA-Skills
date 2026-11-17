## Description:

查询 Ozon 中国专区商品销售排行，并按类目、周期、销量、销售额或价格筛选结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border sellers and product analysts use this skill to compare Ozon China-zone products by category, sales, revenue and price over a selected period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or update local Node.js and qhkit tooling beyond the current query.

Mitigation: Install reviewed, pinned tool versions yourself before running the skill.

Risk: API configuration may be stored or changed on the machine.

Mitigation: Provide credentials through your usual secret-management flow and review existing qhkit configuration before changing it.

Risk: Paid product-data calls can incur variable credits, including on some failures.

Mitigation: Check the current estimate and get user approval before paid calls or large result sets.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown findings; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform, period, sample size and credits spent when applicable.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
