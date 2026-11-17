## Description:

Helps agents retrieve Shopee category keyword rankings for best-selling and fast-rising searches across daily, weekly, or monthly periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and analysts use this skill to compare popular or fast-growing search terms within a Shopee category, site, and reporting period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install or upgrade qhkit and configure an access token automatically.

Mitigation: Review and approve dependency installation and token setup first; prefer a pinned, preinstalled package and managed secrets.

Risk: Ranking lookups and related category queries can consume paid Qinghu credits, including when some calls fail.

Mitigation: Check current estimates and obtain user approval for the planned paid calls before executing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-keyword-rank)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Concise findings with a data table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the Shopee site, ranking period, and sample size alongside findings.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
