## Description:

Looks up Shopee keyword sales, revenue, search index, and category data for up to 10 keywords per request using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use the skill to compare Shopee search terms by sales, revenue, search interest, and category across supported marketplaces and billing periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword queries and a Qinghu API token are used with an external service.

Mitigation: Install qhkit only if comfortable using Qinghu, and provide the token only through its documented configuration.

Risk: Paid lookups may use credits or target an unintended marketplace or period.

Mitigation: Confirm the Shopee site, billing period, keywords, and estimated credit cost, then obtain consent before paid calls.

Risk: A generic request for keyword details may be unrelated to Shopee.

Mitigation: Clarify the platform before initiating a paid Shopee lookup.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-keyword-detail)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key setup](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary and, for larger results, a table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the Shopee site, period, sample size, and credits used; each lookup accepts up to 10 keywords.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
