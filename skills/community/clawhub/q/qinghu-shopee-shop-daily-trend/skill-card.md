## Description:

Helps agents retrieve daily Shopee shop sales, revenue, product counts, and ratings by shop ID for up to 720 days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to inspect a shop's daily sales trends and related metrics across supported Shopee sites.

### Deployment Geography for Use:

Global; data coverage is limited to the supported Shopee sites in Taiwan, Malaysia, Indonesia, Thailand, the Philippines, Singapore, Vietnam, and Brazil.

## Known Risks and Mitigations:

Risk: Installing or updating qhkit through npm introduces dependency and supply-chain exposure.

Mitigation: Prefer a preinstalled or pinned qhkit version and review installation prompts before proceeding.

Risk: Using the data service requires a Qinghu API token and paid calls may consume credits.

Mitigation: Provide credentials only through the intended configuration flow and confirm estimated credit usage with the user before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-daily-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Concise trend summary with supporting metrics; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the Shopee site, date range, and sample size; paid calls report Qinghu credit usage.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
