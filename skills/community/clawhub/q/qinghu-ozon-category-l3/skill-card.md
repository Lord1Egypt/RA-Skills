## Description:

按 Ozon 二级类目 ID 查询公共三级类目及其类目类型 ID（typeId）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商卖家和分析人员可按 Ozon 二级类目 ID 查找三级类目和 typeId，用于后续精准类目查询。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt installation of Node and qhkit, including a global package install.

Mitigation: Review the setup steps first, prefer a preinstalled pinned qhkit version, and confirm before any global install.

Risk: Configuring qhkit may expose a long-lived API token or overwrite the selected service site.

Mitigation: Confirm the site before changing configuration and avoid pasting long-lived tokens directly into shell commands when possible.

Risk: Category lookups can incur Qinghu credit charges.

Mitigation: Check the estimate and obtain user consent before paid calls; report the credits actually charged.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-category-l3)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise category results with typeId; table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries require a second-level category ID and language; optional category-name filter. Paid calls consume Qinghu credits.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
