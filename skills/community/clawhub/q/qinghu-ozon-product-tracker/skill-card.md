## Description:

Tracks Ozon product price, review count, ratings, competing sellers, and variants by product ID over a selected period of up to 90 days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to check a product's recent price changes, review growth, ratings, competing sellers, and variants before making merchandising decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qhkit or Node adds third-party software to the environment.

Mitigation: Install only if you trust the Qinghu package; prefer a preinstalled or pinned version in managed environments and avoid changing shell startup files unless explicitly desired.

Risk: The integration requires an API token and paid calls can spend Qinghu credits, potentially more for larger results.

Mitigation: Keep the token private, estimate credits before calling, and obtain the user's approval before paid requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-product-tracker)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written analysis with an optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports product, period, sample size, and Qinghu credits spent when applicable.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
