## Description:

Queries TikTok Shop best-selling and most-promoted product rankings by region, category, and daily, weekly, or monthly period using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to retrieve TikTok Shop product rankings for a selected market and category, including period-specific sales or promotion results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Node.js or qhkit may change the local software environment.

Mitigation: Confirm installation or upgrades with the user before proceeding.

Risk: Setting a qhkit token or switching site configuration changes access credentials and service selection.

Mitigation: Confirm token and site changes with the user; keep credentials private.

Risk: Product-rank queries consume Qinghu credits, and larger result sets can cost more.

Mitigation: Estimate credits, disclose potential usage charges, and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-tiktok-product-rank)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with ranked product data and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rankings report period-specific increments; requested results may span multiple pages.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
