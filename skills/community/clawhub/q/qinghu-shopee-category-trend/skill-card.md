## Description:

Queries monthly, quarterly, or yearly Shopee category trends across multiple sites, with product type and location filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to compare long-term Shopee category trends across sites and assess category growth by period, product type, and product location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qhkit or Node can change the local environment.

Mitigation: Prefer a preinstalled or pinned qhkit version and review npm or Node installation before allowing it.

Risk: Using the integration requires a Qinghu API token.

Mitigation: Provide the token only through the intended configuration or environment variable and avoid exposing it in shared output.

Risk: Trend queries can consume Qinghu credits.

Mitigation: Check the estimate and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise trend analysis with optional tabular export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies sites, periods, and sample sizes; reports credits consumed when paid queries run.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
