## Description:

Queries daily Shopee category sales and revenue trends by category ID for up to 720 days using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to review daily Shopee category sales and revenue trends for supported marketplaces and date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating qhkit and Node tooling changes software on the host.

Mitigation: Review the installation first and prefer a preinstalled, version-pinned qhkit setup.

Risk: Persisting a Qinghu API token on the host may expose credentials.

Mitigation: Use a controlled secret mechanism rather than persistent configuration when possible.

Risk: Paid queries consume Qinghu credits, and failed server calls may still incur charges.

Mitigation: Disclose estimated charges and obtain user authorization before paid calls; report actual credits afterward.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-daily-trend)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary with an optional tabular data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the marketplace, date range, and credits used; larger results may be delivered as a table file.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
