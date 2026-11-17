## Description:

按 Shopee 商品 ID 查询近 30 天的引流关键词，或推荐同类目热词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to identify search terms driving traffic to specified products and discover popular terms in the same category. Queries require product IDs, a supported Shopee site, a billing date, and a keyword-list type.

### Deployment Geography for Use:

Global; queries cover Shopee sites in Taiwan, Malaysia, Indonesia, Thailand, the Philippines, Singapore, Vietnam, and Brazil.

## Known Risks and Mitigations:

Risk: The skill may install or upgrade Node.js and the Qinghu qhkit package on the local machine.

Mitigation: Prefer an approved, existing installation and obtain explicit user approval before installing or updating software.

Risk: Configuring qhkit may store or replace a Qinghu API token.

Mitigation: Get explicit approval before changing credentials, and avoid exposing the token in shared output.

Risk: Keyword queries consume Qinghu credits, and failed calls may still incur charges.

Mitigation: Show the estimated credit cost and obtain approval before paid calls; avoid unnecessary retries and report actual usage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-item-keywords)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise keyword analysis in Markdown; tabular file for results with at least 10 records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [States Shopee site, query period, sample size, and credits spent; paid API responses may require reading a local results file.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
