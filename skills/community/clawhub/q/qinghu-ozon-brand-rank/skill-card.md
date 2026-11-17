## Description:

按类目、品牌和账期查询 Ozon 品牌销量、销售额及价格排行，帮助用户比较头部品牌。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and market analysts use this skill to identify leading brands by category or name, compare sales rankings for a reporting period, and assess product opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package execution and host-wide tooling changes may introduce unreviewed software.

Mitigation: Review the installation steps and use trusted, pinned package versions where possible before changing the host environment.

Risk: The service requires an API token that could be exposed if entered or stored insecurely.

Mitigation: Provide the token only through a secret or environment mechanism under your control.

Risk: Brand-ranking requests may incur usage-based charges.

Mitigation: Check the current estimate and obtain user approval before making paid calls or retrieving large result sets.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-brand-rank)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown findings with optional tabular export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports platform, site, period, sample size and credits spent when applicable.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
