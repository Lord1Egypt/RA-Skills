## Description:

Analyzes Amazon category demand trends using page views, product counts, return rates, and search-to-purchase ratios from Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and market researchers use this skill to assess demand changes for a marketplace category and compare page views, product counts, return rates, and search-to-purchase ratios over time.

### Deployment Geography for Use:

Global (supported Amazon marketplaces)

## Known Risks and Mitigations:

Risk: Setup can install or update Node and qhkit tooling on the host.

Mitigation: Prefer a sandbox or a preinstalled, pinned qhkit version; review installation steps before running them.

Risk: Qinghu API credentials can be stored locally for later use.

Mitigation: Use a narrowly scoped token and limit shell and account access to what the query needs.

Risk: Data queries may consume paid Qinghu credits, especially for larger result sets.

Mitigation: Check the estimate and obtain user approval before paid calls or large batches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-amazon-demand-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise narrative analysis with optional tabular export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies marketplace and period, reports supporting metrics and any charged Qinghu credits.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
