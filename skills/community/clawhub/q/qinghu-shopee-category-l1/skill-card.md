## Description:

按站点和语言查询 Shopee 一级类目的 ID 与名称，供后续类目和榜单查询使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers, analysts, and developers use this skill to find site- and language-specific top-level category IDs and names before making related category or ranking queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an external CLI and using an external data service introduces supply-chain and credential-handling exposure.

Mitigation: Confirm trust in the qhkit package and 青虎AI service before installation; prefer a managed Node/npm environment and protect the API token.

Risk: The external API can charge credits for queries.

Mitigation: Review the estimated credits and obtain user consent before paid calls; disclose actual credits spent.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-l1)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎AI API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Concise text or Markdown; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports category IDs and names for the requested site and language; discloses credits spent after paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
