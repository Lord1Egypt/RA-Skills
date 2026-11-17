## Description:

Queries up to 720 days of Shopee brand trends by month, quarter, or year across multiple sites using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and market analysts use this skill to compare long-term Shopee brand performance across supported sites and reporting periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or updates of qhkit and Node may alter the local runtime and PATH.

Mitigation: Review setup steps before execution; prefer a preinstalled, pinned qhkit version.

Risk: Configuring the Qinghu API token may store credentials locally.

Mitigation: Use a scoped secret-management mechanism when possible and avoid exposing tokens in shared environments.

Risk: Trend queries consume paid credits, and server failures may still incur charges.

Mitigation: Estimate charges and obtain user approval before paid calls; avoid repeated retries after a server failure.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise trend summary with supporting figures and optional table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Figures identify site and period; paid calls report credits used.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
