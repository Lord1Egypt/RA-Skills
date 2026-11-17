## Description:

水滴保险经纪综合服务助手（sdbao）。支持查看精选保险产品推荐、登记用户购险线索给经纪人、产品咨询、理赔协助和保单管理。当用户询问水滴保险产品、想了解精选险种、需要经纪人联系、或需要水滴系保险服务时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiwenbing](https://clawhub.ai/user/jiwenbing)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to explore selected ShuiDi insurance products, ask basic product or claims questions, and prepare a broker follow-up request. The skill guides collection of lead details such as name, phone number, interested product, age, budget, health notes, and other needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests sensitive lead details, including phone number and health information, without defining a secure submission path.

Mitigation: Collect only details the user explicitly agrees to provide, mask sensitive values in confirmations, and move collection to an approved secure channel before broker follow-up.

Risk: Insurance product, claims, or pricing guidance may become inaccurate if product availability or terms change.

Mitigation: Present product details as informational, direct users to official ShuiDi channels for binding terms, and avoid promising eligibility, price, coverage, or claim outcomes.

Risk: Lead registration may proceed without clear consent or retention expectations.

Mitigation: State the purpose of collection, callback use, and retention terms before recording lead information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiwenbing/skills/sdbao)
- [Publisher profile](https://clawhub.ai/user/jiwenbing)
- [products.md](artifact/products.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and structured text lead cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects and summarizes user-provided insurance lead information when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
