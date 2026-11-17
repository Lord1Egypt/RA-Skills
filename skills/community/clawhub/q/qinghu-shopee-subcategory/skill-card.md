## Description:

Retrieves Shopee subcategory data for a selected category, site, and date to support category drill-down.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to retrieve child categories for a known category and drill down through a site's category hierarchy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or upgrade Node and qhkit, change PATH setup, or configure an API token on the host.

Mitigation: Prefer a preinstalled, pinned qhkit version and obtain explicit approval before installation or credential changes.

Risk: Qinghu data queries may consume paid credits.

Mitigation: Check the estimated charge and obtain user approval before paid API calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-subcategory)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written summary with category data; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the Shopee site, date, and sample size; paid calls report credits used.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
