## Description:

Analyzes a brand's last 30 days of Shopee sales volume, revenue, and share across sites without requiring a site selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to compare a brand's Shopee sales and revenue shares across country sites for a selected reporting date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running an unpinned third-party CLI can change the local environment.

Mitigation: Review the installation before proceeding and prefer a preinstalled, pinned qhkit version.

Risk: Configuring an API token exposes credentials to a third-party tool.

Mitigation: Use a scoped token and review local credential setup before configuring it.

Risk: Paid data requests may incur unexpected charges.

Mitigation: Check the current estimate and obtain user consent before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-sites)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Concise narrative with site-level sales and revenue comparisons; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover the available sites for a requested brand and reporting date; paid calls require prior consent.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
