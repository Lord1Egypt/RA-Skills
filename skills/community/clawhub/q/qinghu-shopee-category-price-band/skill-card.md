## Description:

Queries Shopee category sales, revenue, and product counts by price band to identify the leading price ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market analysts use this skill to compare sales, revenue, and product counts across price bands within second- or third-level categories and identify prevailing prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires local Node/qhkit installation and a Qinghu API token for the domestic service.

Mitigation: Confirm the intended Qinghu service before installing, keep the API token private, and consider pinning qhkit versions.

Risk: Paid data queries can consume Qinghu credits.

Mitigation: Check estimated credits and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-price-band)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Concise Markdown summary with supporting figures; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the Shopee site and reporting period; paid queries consume Qinghu credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
