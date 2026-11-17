## Description:

Helps agents retrieve Shopee site-level sales volume, revenue, active listing counts, and average order value through Qinghu analytics for periods up to 720 days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers, market analysts, and their agents use the skill to assess Shopee marketplace size and trends for a specified site and date range, including comparisons across supported sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or upgrade Node and qhkit on the host.

Mitigation: Confirm installation or upgrades before execution and prefer a pinned package version where possible.

Risk: Setup may store a Qinghu API token or use the wrong account region.

Mitigation: Confirm the intended domestic or international account and handle the token as a secret.

Risk: Analytics requests consume paid Qinghu credits.

Mitigation: Check the estimated credit cost and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-site-overview)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written analysis with figures and brief previews; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shopee site and date range are identified with reported figures; source data updates daily (T+1) and supports up to 720 days of history.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
