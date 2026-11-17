## Description:

查询 Ozon 三级类目的市场销售详情，帮助用户了解指定类目的销售表现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and market analysts use this skill to request category-level sales details for a specified third-level category and reporting period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or update qhkit or Node and change the host environment.

Mitigation: Review and approve setup steps before allowing changes on the machine.

Risk: Using the paid integration requires a service token and may incur charges for queries.

Mitigation: Configure the token only when intended, check the estimated credits, and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-category-sales)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written summary; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on available Ozon category data and the selected reporting period.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
