## Description:

Retrieves Shopee category-level sales, revenue, and product-count summaries for a selected site and date through Qinghu's paid data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts compare category size across supported Shopee sites and category levels for a selected date, using sales, revenue, and product counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Node.js and qhkit introduces third-party software into the environment.

Mitigation: Confirm the disclosed download and package sources before installation; prefer a preinstalled or pinned qhkit version.

Risk: The connector requires a Qinghu API token, and a mismatched site configuration can cause authentication failures.

Mitigation: Use a Qinghu-issued token and verify the configured site before calling the service; avoid exposing the token in responses.

Risk: Category-data calls consume Qinghu credits, including potentially unsuccessful server requests.

Mitigation: Confirm site, date, category level, and estimated charges with the user before paid calls; avoid repeated speculative retries and report actual credits used.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-list)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary with a table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify site, date, and sample size; paid-call replies report Qinghu credits consumed.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
