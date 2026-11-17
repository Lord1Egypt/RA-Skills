## Description:

Looks up Ozon products associated with keyword IDs, with optional price, product-type, and reporting-period filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to review products associated with search keywords and compare competitors using Qinghu data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may change the local environment through unpinned Node/npm/qhkit installations or shell startup changes.

Mitigation: Prefer a reviewed, pinned qhkit installation; approve local setup and shell changes before applying them.

Risk: Configuring Qinghu access requires a service token.

Mitigation: Provide the token only through trusted Qinghu configuration or environment variables; avoid exposing it in shared output.

Risk: Product queries use paid Qinghu credits, with charges that can grow with result volume.

Mitigation: Check the current estimate and obtain user consent before paid calls or larger batches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-keyword-products)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise findings with an optional table file and brief preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Qinghu credits consumed for paid queries.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
