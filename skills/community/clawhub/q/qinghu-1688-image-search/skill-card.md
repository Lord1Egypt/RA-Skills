## Description:

Finds matching or similar 1688 suppliers and products from publicly accessible product image URLs, with prices and sales information when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sourcing teams and sellers use a public product image URL to find similar items and potential suppliers on 1688, then review pricing and sales data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid searches consume Qinghu credits.

Mitigation: Estimate charges and obtain user consent before the first paid call; report the credits charged.

Risk: Using the integration requires a Qinghu API token and sends public product image URLs to the Qinghu/1688 service.

Mitigation: Use only URLs and credentials the user is comfortable sharing with the service; do not submit local image paths.

Risk: Installing qhkit or Node may run third-party software.

Mitigation: Prefer an already-installed or pinned qhkit version and review npm or Node installation commands before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-1688-image-search)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise sourcing summary, with a table file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits charged for paid calls; search results depend on the provider's returned data.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
