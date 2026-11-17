## Description:

Looks up details for up to 10 Ozon shops by shop ID using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and market analysts use this skill to retrieve shop details for specified shop IDs, including competitor shops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing qhkit from an untrusted source could introduce unsafe software.

Mitigation: Install from a trusted npm source and review the package before use.

Risk: The skill requires a Qinghu API token and paid shop-detail calls can consume credits.

Mitigation: Protect the token, check the cost estimate, and obtain user approval before paid queries.

Risk: Shop-detail results do not cover a full competitor analysis.

Mitigation: Use this skill only when shop IDs and shop-detail data address the request.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-shop-detail)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Shop-detail data, Shell commands, Configuration guidance]

**Output Format:** [JSON tool results summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries accept up to 10 comma-separated shop IDs; results report consumed Qinghu credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
