## Description:

按一级类目 ID 查询指定 Shopee 站点的二级类目 ID 与名称。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to look up second-level category IDs and names for a selected site, language, and first-level category ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions allow the agent to install or update Node and qhkit on the host.

Mitigation: Prefer a preinstalled, pinned qhkit version and review any proposed host changes before execution.

Risk: Using the service requires configuring a Qinghu API token on the machine.

Mitigation: Provide a scoped, revocable token and review how credentials are stored before configuration.

Risk: Category lookup calls may consume paid Qinghu credits.

Mitigation: Check estimated costs and get the user's consent before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-l2)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise text or Markdown; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns category IDs and names for the requested site and language; reports Qinghu credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
